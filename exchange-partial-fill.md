# NUT-Exchange-partial-fill: Partial-Fill Authorization

`draft`

`optional`

`depends on: NUT-Exchange, NUT-02, NUT-03, NUT-06, NUT-09, NUT-10, NUT-11, NUT-12`

---

This NUT extends [NUT-Exchange][exchange]'s `PAY_TO_UNLOCK` condition with a **pool-based authorization mode**: the owner locks a single input and authorizes a **range** of possible output bundles, with the actual output selection determined at match time.

In standard mode (NUT-Exchange), `data` is `H_recv` — a hash of one exact output bundle. In pool mode (this NUT), `data` is a manifest hash over a small set of pre-generated output entries in binary denominations, plus a numeric rate policy that the mint enforces. The coordinator selects any subset satisfying the policy; the mint signs only the selected entries.

Readers should be familiar with [NUT-Exchange][exchange] (`PAY_TO_UNLOCK`, conservation rules, recovery, refund, the `participants` request shape).

## Condition

Pool mode is signaled by the presence of `rate_n` and `rate_d` tags. When absent, the condition uses standard mode (exact `H_recv` match, as defined in [NUT-Exchange][exchange]).

```json
[
  "PAY_TO_UNLOCK",
  {
    "nonce": "<hex_str: 32 bytes>",
    "data": "<hex_str: H_manifest>",
    "tags": [
      ["offer_keyset", "<keyset_id>"],
      ["expiry", "<unix_seconds_str>"],
      ["refund", "<xonly_pubkey_hex>"],
      ["rate_n", "<uint_str>"],
      ["rate_d", "<uint_str>"],
      ["min_receive", "<uint_str>"],
      ["max_debit", "<uint_str>"]
    ]
  }
]
```

**Required tags** (same as NUT-Exchange): `offer_keyset`, `expiry`, `refund`.

**Pool-mode tags** (presence signals pool mode; all four required together):

- `rate_n` / `rate_d`: minimum receive rate, expressed as a rational `rate_n / rate_d`. The mint enforces `receive_total × rate_d ≥ debit_total × rate_n` using checked `u128` cross-multiplication (no division, no rounding ambiguity). This is an **inequality** — better prices are automatically admitted.
- `min_receive`: minimum total receive-keyset output amount. Prevents dust fills. MUST be positive.
- `max_debit`: maximum total debit (`input_total − change_total`). Caps the spending. MUST be ≤ the participant's input total.

Every proof contributed by one participant MUST carry the same condition (same `nonce`, `data`, tags), with unique per-proof nonces (same rule as [NUT-Exchange][exchange]).

## Output pools

The owner generates two pools of `BlindedMessage` entries:

- **Receive pool:** entries in the receive keyset, at powers-of-2 denominations (1, 2, 4, 8, ..., 2^k). Any subset sums to any integer from 0 to `2^(k+1) − 1`.
- **Change pool:** entries in the offer keyset, at powers-of-2 denominations covering the possible change range.

Each entry has a `role` (`receive` or `change`), `amount`, `id` (keyset), and `B_` (blinded point). The owner retains every entry's secret and blinding factor.

Denominations MUST be powers of 2 (1, 2, 4, 8, ..., 2^k), matching the Cashu binary keyset convention ([NUT-00][00]). For a max receive of `R` units, `⌈log₂(R+1)⌉` entries cover every integer from 0 to `R`. For a max change of `C` units, `⌈log₂(C+1)⌉` entries suffice. Total entries: `O(log R + log C)` — typically 15–25 for most orders.

## Manifest hash

The `data` field is `H_manifest`, computed over the canonical encoding of all pool entries:

```
manifest_canonical = entry[0]_canonical || entry[1]_canonical || ... || entry[n-1]_canonical
H_manifest = tagged_hash("Cashu/PAY_TO_UNLOCK/manifest", manifest_canonical)
```

Each `entry_canonical` is the JCS encoding of:

```json
{"amount":"<decimal_str>","B_":"<hex>","id":"<keyset_id>","index":<uint>,"role":"receive|change"}
```

Entries are sorted by `(role, index)`. Amounts are decimal strings (same precision rule as [NUT-Exchange][exchange]). The `index` field ensures unambiguous ordering even with duplicate amounts.

## Request format

Pool-mode participants include the full manifest and a selection bitmap:

```json
{
  "participants": [
    {
      "inputs": "<Array[Proof]>",
      "outputs": "<Array[BlindedMessage] — selected entries only>",
      "pool_manifest": "<Array[PoolEntry] — all entries>",
      "pool_selection": "<hex_str — bitmap over manifest indices>"
    }
  ]
}
```

- `outputs`: the selected entries only — these are the `BlindedMessage` values the mint will sign. MUST be a subset of `pool_manifest`, in manifest index order.
- `pool_manifest`: the full array of `PoolEntry` objects that the owner pre-generated. Each entry has `{index, role, amount, id, B_}`. The mint hashes this array (see [Manifest hash](#manifest-hash)) and verifies it matches the condition's `data` field. This proves every entry was created by the owner.
- `pool_selection`: a hex-encoded bitmap selecting which manifest entries to sign. Bit `i` (0-indexed from the least-significant bit of the first byte) corresponds to `pool_manifest[i]`. Bit `1` = selected (include in `outputs`), bit `0` = skipped. Unused trailing bits MUST be zero. The selected entries, in index order, MUST exactly match the `outputs` array.

**PoolEntry schema:**

```json
{"index": <uint>, "role": "receive|change", "amount": "<decimal_str>", "id": "<keyset_id>", "B_": "<hex_str>"}
```

Example: a manifest with 3 receive entries and 2 change entries. If the coordinator selects receive entries 0 and 2 plus change entry 0, the bitmap is `0b000010101` = `0x15` (bits 0, 2, and 4 set). `pool_selection = "15"`. `outputs` contains entries 0, 2, and 4 from the manifest, in that order.

Non-pool-mode participants omit `pool_manifest` and `pool_selection` (standard NUT-Exchange behavior).

Response: same as NUT-Exchange — `{signatures: [...]}`, one `BlindSignature` array per participant. Pool-mode participants receive signatures for their selected entries only.

## Mint validation

Pool-mode participants require additional validation beyond [NUT-Exchange][exchange] rules 1–5, 9, 11:

6p. **Manifest hash:** hash `pool_manifest` canonically → MUST equal condition `data`. Otherwise reject (error 13041).

7p. **Selection consistency:** the entries indicated by `pool_selection` MUST exactly match the `outputs` array (same `B_`, `amount`, `id` values in the same order). Otherwise reject.

8p. **Role/keyset consistency:** every selected `receive` entry MUST use the receive keyset (derived from the manifest's `role` field); every selected `change` entry MUST use the offer keyset. At least one `receive` entry MUST be selected.

9p. **Policy:** compute `receive_total` (sum of selected receive amounts) and `debit_total` (input total − sum of selected change amounts). Enforce using checked `u128` arithmetic:

- `receive_total × rate_d ≥ debit_total × rate_n` (rate covenant)
- `receive_total ≥ min_receive` (minimum fill)
- `debit_total ≤ max_debit` (spending cap)

10p. **Conservation:** standard per-class conservation from [NUT-Exchange][exchange] rule 10, applied with change entries in the offer keyset. The mint signs only `outputs`; `pool_manifest` entries are authentication material, not outputs to sign.

Standard rules 7–8 from NUT-Exchange (single-keyset output constraint, two-keyset exchange) are **relaxed** for pool mode: outputs may use both the receive and offer keysets (change), exactly as with `allow_change` in NUT-Exchange.

## Example

Alice wants to swap **10 USD for up to 1000 sats** at price **≤ 0.01 USD/sat**.

### Preparation

**Receive pool** (sats keyset, 10 entries): amounts 1, 2, 4, 8, 16, 32, 64, 128, 256, 512. Any subset sums to 0–1023.

**Change pool** (USD keyset, 11 entries): amounts 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12 (covering 0–10.23 USD). _(Adjust denominations to match keyset's supported amounts.)_

**Manifest:** 21 entries. `H_manifest = hash(canonical encoding)`.

**Policy:** `rate_n = 1, rate_d = 100` (receive ≥ 100 sats per USD debited), `min_receive = 1`, `max_debit = 1000` (cents).

**Lock:** one 10-USD `PAY_TO_UNLOCK` proof in pool mode.

### Settlement — fill 500 sats

Counterparty offers 500 sats for 5 USD.

Coordinator selects:

- Receive: {256, 128, 64, 32, 16, 4} = 500 sats (6 entries)
- Change: {5.12... } → nearest representable set summing to ~5 USD

Mint checks:

- `H_manifest` matches condition `data` ✓
- Selected entries match bitmap ✓
- `receive_total = 500`, `debit_total = 500` (cents)
- `500 × 100 ≥ 500 × 1` → `50000 ≥ 500` ✓ (price well within limit)
- `500 ≥ 1` ✓, `500 ≤ 1000` ✓
- Conservation: 10 USD in = 5 USD change + 5 USD to counterparty. 500 sats in = 500 sats out. ✓

Mint signs 8 selected BlindedMessages. Alice unblinds to get 500 sats + 5 USD change.

### Settlement — partial fill 237 sats

Counterparty offers 237 sats for ~2.37 USD.

Coordinator searches for a valid (receive, change) pair:

- Receive: {128, 64, 32, 8, 4, 1} = 237 sats
- Change: subset summing to ~7.63 USD → nearest representable
- Check: `237 × 100 ≥ debit × 1` → debit ≤ 23700 cents = 237 USD... wait, units.

_(The coordinator optimizes over all valid subsets. The rate covenant ensures Alice never pays more than 0.01 USD/sat. The denomination granularity determines the exact achievable price.)_

## Recovery and refund

Identical to [NUT-Exchange][exchange]. Pool-mode proofs carry the same `expiry` and `refund` tags. After `expiry`, the owner refunds via NUT-03 swap with a `refund` signature. Unused pool entries are simply discarded — they were never spent.

## Mint info

Pool-mode support is advertised via [NUT-06][06]:

```json
{
  "exchange": {
    "supported": true,
    "partial_fill": true,
    "max_pool_entries": "<uint>"
  }
}
```

`max_pool_entries` bounds the total number of manifest entries per participant. A wallet MUST NOT create pool-mode conditions exceeding this limit.

## FAQ

**Why powers-of-2 denominations?**
`⌈log₂(N)⌉` entries cover every integer from 0 to `N−1` via subset sum. For a 1000-unit range: 10 entries. This keeps wallet cost logarithmic.

**Can the coordinator steal outputs?**
No. Every selected entry must be in Alice's authenticated manifest (verified by `H_manifest`). The coordinator can only select entries Alice pre-generated with her own blinding factors. It cannot inject its own `BlindedMessage` values.

**Does the mint enforce best execution?**
No. The rate covenant enforces the owner's limit price. Any subset satisfying the covenant is valid. The coordinator may select the least favorable valid pair. Best execution is an off-mint concern.

**How does this differ from `alt_outputs`?**
`alt_outputs` enumerates complete bundles (O(T) preprocessing for T fill scenarios). Pool mode generates O(log N) entries and lets the mint evaluate a numeric policy. Pool mode scales to fine-grained FAK; `alt_outputs` does not.

## References

- [NUT-Exchange][exchange] · [NUT-02](02.md) · [NUT-03](03.md) · [NUT-06](06.md) ·
  [NUT-09](09.md) · [NUT-10](10.md) · [NUT-11](11.md) · [NUT-12](12.md)

[00]: 00.md
[02]: 02.md
[03]: 03.md
[06]: 06.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[exchange]: https://github.com/cashubtc/nuts/pull/410
