# NUT-XX: Efficient Wallet Recovery

`optional`

`depends on: NUT-03, NUT-07, NUT-09, NUT-13`

---

This NUT defines an improved recovery algorithm for [NUT-13][13] wallets. It is motivated by the privacy and efficiency limitations of the current linear scan approach described in [nuts#301](https://github.com/cashubtc/nuts/issues/301).

The recovery procedure defined in [NUT-13][13] reveals the wallet's entire transaction history to the mint. During recovery, the wallet sends every `BlindedMessage` it has ever generated — including nonces for tokens that were never issued — to the mint in sequential batches. This has two consequences:

1. **Privacy**: The mint can correlate all of the user's past ecash activity retroactively, defeating the unlinkability guarantees of ecash.
2. **Efficiency**: Recovery requires O(T/b) network requests, where T is the total number of issued notes and b is the batch size.

This NUT reduces leakage to O(log N + g + d) `BlindedMessages`, where N is the nonce space (2^32), g is a gap-tolerance window, and d is a configurable depth parameter that bounds the unspent token region. This is achieved by combining a binary search to locate the last issued nonce index T, and maintaining a **Depth Invariant** that confines all unspent tokens to the last `d` nonce indices.

## Depth Invariant

This NUT introduces a protocol invariant that wallets **MUST** maintain during normal operation:

> **All unspent `Proofs` must have a nonce index greater than `T - d`.**

Where:

- **T** is the index of the nonce used for the last issued `BlindedMessage`. No issued note has a nonce index greater than T.
- **d** is a configurable positive integer defining the maximum depth of the unspent token window. Wallets **SHOULD** use d = 100 as the default.
- **g** is a configurable positive integer defining a gap-tolerance window scanned beyond the candidate T to handle failed operations. Wallets **SHOULD** use g = 50 as the default.
- **Nonce index** is the `counter_k` value used by [NUT-13][13] to derive the secret and blinding factor for a `Proof`.

Formally, for every unspent `Proof` with nonce index `i`: `i > T - d`

```
[0] |=============================[T-d]-----[T]>
     spent or reissued               unspent proofs (-), at most d of them
```

This invariant guarantees that all unspent tokens are confined to the nonce window `(T - d, T]`, whose size is bounded by `d`.

### Maintaining the invariant

To maintain the invariant, wallets that implement this NUT **MUST**:

1. **On receive (mint/swap-in)**: After receiving new tokens, T increases. If any existing unspent `Proof` now has a nonce index `i ≤ T - d`, the wallet **MUST** consolidate those proofs by re-issuing them via a [NUT-03][03] swap. The re-issued proofs receive new nonce indices near T, restoring the invariant.

2. **On send (swap-to-send)**: A send operation involves a [NUT-03][03] swap that creates new outputs (send proofs + change proofs), which increases T. If this increase causes any remaining unspent proofs (those not involved in the swap) to have index `i ≤ T - d`, the wallet **MUST** consolidate them. Note: a pure melt (paying a Lightning invoice without swap) does not increase T and therefore cannot violate the invariant.

3. **Coin selection**: Wallets **MAY** use arbitrary coin selection. After any operation that increases T, the wallet **MUST** check whether any unspent proof now has index `i ≤ T - d` and consolidate if so. This preserves free coin selection while enforcing the invariant.

> [!NOTE]
> The consolidation swap is a standard [NUT-03][03] swap — it does not reveal any additional information about the wallet's history beyond what is already implicit in the swap operation itself.

### Consolidation strategy

Since recovery can be triggered at any time by data loss, the invariant **MUST** hold at all times — not just "before recovery". Wallets **MUST** consolidate violating proofs immediately after any operation that increases T.

In practice, a simple strategy is:

- After each operation that increases T, check whether any unspent proof has index `i ≤ T - d`.
- If so, consolidate all such proofs in a single [NUT-03][03] swap before the operation is considered complete.

This ensures the invariant is never violated, even if the wallet crashes or loses data immediately after the operation.

## Recovery algorithm

### Locating T via binary search

The wallet uses binary search over the nonce space `[0, 2^32 - 1]` to find T with O(log N) queries to the mint's [NUT-09][09] restore endpoint.

At each step, the wallet queries the mint with a single `BlindedMessage` derived from the midpoint index `m`. If the mint returns a `BlindSignature` for it, `m ≤ T`; otherwise, `m > T`.

Where `query(keyset_id, index)` sends a single `BlindedMessage` (derived from `keyset_id` and `counter = index`) to the [NUT-09][09] endpoint and returns the mint's response.

Python:

```python
async def find_t(keyset_id: str) -> int:
    """Binary search to find T (last issued nonce index)."""
    lo = 0
    hi = 2**32 - 1

    # Edge case: nothing has been issued
    if not await query(keyset_id, 0):
        return -1

    while lo < hi:
        m = (lo + hi + 1) // 2
        if await query(keyset_id, m):
            lo = m       # T is at m or to the right
        else:
            hi = m - 1   # T is to the left of m

    return lo  # lo == hi == T_candidate
```

### Gap tolerance

Failed wallet operations (e.g., network interruptions after the counter was incremented but before the mint signed) may create gaps in the issued nonce space. A single gap at index `m` would cause the binary search to return a T less than the true value, potentially missing valid tokens.

To mitigate this, after `find_t` returns a candidate `T_candidate`, wallets **MUST** perform a forward linear scan of `[T_candidate + 1, T_candidate + g]` to verify that no issued nonces exist beyond `T_candidate`. If any are found, `T_candidate` is updated to the highest found index, and the scan window shifts forward from the new `T_candidate`.

Python:

```python
async def scan_gap(keyset_id: str, t_candidate: int, g: int = 50) -> int:
    """Forward scan to handle gaps in the nonce space."""
    t = t_candidate
    i = t + 1
    limit = t + g

    while i <= limit:
        if await query(keyset_id, i):
            t = i
            limit = i + g   # extend window from new T
        i += 1

    return t
```

This adds at most `g` queries per gap encountered. For wallets with no gaps (the common case), it adds exactly `g` queries total.

> [!NOTE]
> The gap scan can be implemented as a single [NUT-09][09] batch request containing `g` `BlindedMessages`, rather than `g` individual requests. If any signatures are returned, the wallet extends the window from the highest found index and sends another batch. This reduces total requests without affecting the number of nonces revealed.

### Recovering unspent proofs

With T known, all unspent tokens are in the nonce window `(T - d, T]` thanks to the Depth Invariant. The wallet sends a single batch request to the [NUT-09][09] endpoint with `BlindedMessages` for indices `T - d + 1` through `T`, then filters out spent `Proofs` using [NUT-07][07].

Python:

```python
async def recover(keyset_id: str, t: int, d: int = 100) -> list:
    """Recover unspent proofs from the bounded window."""
    start = max(0, t - d + 1)
    outputs = [blinded_message(keyset_id, i) for i in range(start, t + 1)]
    signatures = await restore(outputs)          # NUT-09
    proofs = unblind(signatures)
    unspent = await check_states(proofs)         # NUT-07
    return [p for p in unspent if p.state == "UNSPENT"]
```

This step requires exactly one [NUT-09][09] request (with at most `d` outputs) plus one [NUT-07][07] state check.

### Full recovery procedure

Wallets implementing this NUT **SHOULD** use the following procedure instead of the linear scan defined in [NUT-13][13]:

Python:

```python
async def recover_wallet(mnemonic: str, d: int = 100, g: int = 50):
    """Full wallet recovery using binary search."""
    init_from_mnemonic(mnemonic)
    for keyset_id in get_keysets():
        t_candidate = await find_t(keyset_id)
        if t_candidate == -1:
            continue

        t = await scan_gap(keyset_id, t_candidate, g)
        unspent = await recover(keyset_id, t, d)
        store(unspent)
        set_counter(keyset_id, t + 1)
```

## Privacy analysis

### Cost breakdown

With default parameters d = 100, g = 50:

| Component | Nonces revealed | Requests (individual) | Requests (batched) |
|---|---|---|---|
| Binary search | log₂(N) = 32 | 32 (sequential, cannot be batched) | 32 |
| Gap scan | g = 50 | 50 | 1–2 (single [NUT-09][09] batch) |
| Recovery | d = 100 | 1 ([NUT-09][09] batch) | 1 |
| State check | 0 | 1 ([NUT-07][07]) | 1 |
| **Total** | **182** | **84** | **~35** |

### Comparison with NUT-13

| Approach | Nonces revealed | Requests |
|---|---|---|
| [NUT-13][13] linear scan (batch=25) | T + 50 | T/25 + 2 |
| This NUT (d=100, g=50, batched) | 182 (constant) | ~35 |

Examples:

| Wallet size (T) | NUT-13 nonces | This NUT nonces | NUT-13 requests | This NUT requests |
|---|---|---|---|---|
| 100 | 150 | 182 | 6 | ~35 |
| 500 | 550 | 182 | 22 | ~35 |
| 1,000 | 1,050 | 182 | 42 | ~35 |
| 5,000 | 5,050 | 182 | 202 | ~35 |
| 100,000 | 100,050 | 182 | 4,002 | ~35 |

### Breakeven points

This NUT reveals **more** nonces than [NUT-13][13] for small wallets:

- **Privacy breakeven**: T ≈ 132. For wallets with T < 132, [NUT-13][13] reveals fewer nonces.
- **Efficiency breakeven**: T ≈ 825 (with batched gap scan). For wallets with T < 825, [NUT-13][13] makes fewer requests.

For wallets below these thresholds, the overhead of binary search (32 sequential round-trips) and the fixed recovery window (`d` nonces) exceeds the cost of a simple linear scan. Wallets **MAY** use a heuristic: if a previous recovery or local state suggests T < 200, fall back to the [NUT-13][13] linear scan.

### Privacy properties

The privacy gain for wallets above the breakeven comes from two properties:

1. **Bounded leakage**: The number of revealed nonces is constant (182) regardless of wallet history size. A wallet with T = 1,000 reveals the same number of nonces as one with T = 100,000.
2. **Non-sequential probes**: The 32 binary search probes are spread across the entire nonce space and are non-contiguous, making transaction history correlation significantly harder for the mint compared to the sequential batches of [NUT-13][13].

## Backwards compatibility

This NUT is fully backwards-compatible:

- **Mint**: No changes required. The wallet uses the existing [NUT-09][09] restore endpoint with single-element batches during binary search and a standard batch for the final recovery. No new endpoints or response fields are needed.
- **Wallet**: Implementing this NUT is optional. Wallets that do not implement it continue to use the [NUT-13][13] linear scan.
- **Interoperability**: Wallets that implement this NUT can recover funds from any [NUT-13][13] wallet. However, if the original wallet did NOT maintain the Depth Invariant, unspent tokens outside the `(T - d, T]` window will not be recovered. In this case, wallets **SHOULD** fall back to the [NUT-13][13] linear scan over `[0, T]` to ensure complete recovery.

### Migration

Existing wallets that adopt this NUT **SHOULD** perform a one-time consolidation at activation to bring all unspent proofs into the `(T - d, T]` window, establishing the Depth Invariant for future recoveries.

## Implementation notes

### Mints

No changes to the mint are required. The existing [NUT-09][09] restore endpoint is used as-is.

### Wallets

Wallets that implement this NUT **MUST**:
- Implement the consolidation logic to maintain the Depth Invariant after send and receive operations
- Store the nonce index (`counter_k`) for each `Proof` in their local database, so that violation checks can be performed efficiently

Wallets **SHOULD**:
- Use d = 100 as the default depth parameter
- Use g = 50 as the default gap-tolerance window
- Expose `d` as a user-configurable setting for advanced users who want to trade off recovery window size against consolidation frequency

## Test vectors

TBD — to be added before this NUT moves to final status.

[03]: 03.md
[07]: 07.md
[09]: 09.md
[13]: 13.md
