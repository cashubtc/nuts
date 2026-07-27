# NUT-Exchange-partial-fill: Partial-Fill Authorization

`draft`

`optional`

`depends on: NUT-Exchange, NUT-01, NUT-02, NUT-03, NUT-06, NUT-09, NUT-10, NUT-11, NUT-12`

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

- `rate_n` / `rate_d`: minimum receive rate in integer keyset minor units: at least `rate_n` receive-keyset units for every `rate_d` offer-keyset units debited. `rate_d` MUST be greater than zero. The mint enforces `receive_total × rate_d ≥ debit_total × rate_n` using checked `u128` cross-multiplication, with no division or rounding. Implementations MUST NOT convert either total to display units before this comparison. For a sat receive keyset and a USD offer keyset whose amount `1` is one cent, one sat per cent is encoded as `rate_n = 1, rate_d = 1`. The inequality admits every better price.
- `min_receive`: minimum total receive-keyset output amount. Prevents dust fills. MUST be positive.
- `max_debit`: maximum total debit (`input_total − change_total`). Caps spending and MUST be no greater than the participant's input total. The mint MUST reject a request whose selected `change_total` exceeds `input_total`; it MUST NOT perform a wrapping subtraction.

Every proof contributed by one participant MUST carry the same `data` and the same tags (`offer_keyset`, `expiry`, `refund`, `rate_n`, `rate_d`, `min_receive`, `max_debit`), while each proof MUST use a unique `nonce`, following the per-proof nonce rule in [NUT-Exchange][exchange].

## Output pools

The owner generates two pools of `BlindedMessage` entries:

- **Receive pool:** entries in the receive keyset, at powers-of-2 denominations.
- **Change pool:** entries in the offer keyset, at powers-of-2 denominations covering the possible change range.

Each entry has a `role` (`receive` or `change`), `amount`, `id` (keyset), and `B_` (blinded point). The owner retains every entry's secret and blinding factor.

For each participant, every `receive` entry MUST have the same `id`, called that participant's receive keyset. Every `change` entry MUST have `id` equal to the condition's `offer_keyset`. Both roles MUST be present, and the receive keyset MUST differ from `offer_keyset`; therefore each participant's complete manifest contains exactly those two keyset IDs. Across the complete exchange request, the union of every participant's `offer_keyset` and derived receive keyset MUST contain exactly two distinct keyset IDs.

Pool mode uses powers-of-two denominations (`1, 2, 4, 8, ..., 2^k`), but Cashu does not guarantee that a keyset publishes those denominations. A wallet MUST inspect the [NUT-01][01] key maps for the receive and offer keysets and MUST NOT create a pool unless each keyset is active for issuance and publishes a signing key for every amount placed in that keyset's pool. The mint MUST reject a manifest if any entry's `(id, amount)` does not identify a published signing key in an active keyset. Given that denomination coverage, `⌈log₂(R+1)⌉` receive entries can represent every integer from 0 through `R`, and `⌈log₂(C+1)⌉` change entries can represent every integer from 0 through `C`. Total entries remain `O(log R + log C)`.

## Manifest hash

The `data` field is `H_manifest`, computed over the complete ordered `pool_manifest`. `PoolEntry` is the only name for an entry in that array and has exactly these fields:

```json
{"index": <uint>, "role": "receive|change", "amount": <uint>, "id": "<keyset_id>", "B_": "<hex_str>"}
```

`amount` is an unsigned 64-bit integer in the minor unit of the entry's keyset ([NUT-01][01]). `pool_manifest` MUST contain all `receive` entries first and all `change` entries second. Each entry's `index` MUST equal its zero-based position in `pool_manifest`; indices are unique and contiguous from `0` through `len(pool_manifest) − 1`.

Each `PoolEntry` is encoded using the [RFC 8785][rfc8785] JCS defined by [NUT-Exchange][exchange]:

```
manifest_canonical = JCS(pool_manifest[0]) || JCS(pool_manifest[1]) || ... || JCS(pool_manifest[n-1])
H_manifest = tagged_hash("Cashu/PAY_TO_UNLOCK/manifest", manifest_canonical)
```

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
- `pool_manifest`: the complete ordered array of `PoolEntry` values defined in [Manifest hash](#manifest-hash). The mint computes `H_manifest` from this array and verifies it against the condition's `data` field. This authenticates every candidate entry as part of the owner-created pool.
- `pool_selection`: a hex-encoded bitmap selecting which manifest entries to sign. Bit `i` (0-indexed from the least-significant bit of the first byte) corresponds to `pool_manifest[i]`. Bit `1` = selected (include in `outputs`), bit `0` = skipped. Unused trailing bits MUST be zero. The selected entries, in index order, MUST exactly match the `outputs` array.

`pool_selection` tells the mint which authenticated candidate outputs to sign. An entry whose bit is zero is an unsigned candidate, not ecash: the mint MUST NOT sign or return it, and signing every manifest entry would violate the per-class conservation rule. The full-manifest form reveals to the mint that all listed `B_` values belong to one authorization, but an unselected value never becomes a proof. After successful settlement, refund, or expiry, the owner MUST discard every unselected entry's secret and blinding factor and MUST NOT reuse its `B_`; a later transaction requiring that denomination MUST generate a fresh secret, blinding factor, and `B_`.

Example: a five-entry manifest has receive entries at manifest indices 0, 1, and 2 and change entries at manifest indices 3 and 4. Selecting manifest entries 0, 2, and 4 produces the bitmap `0b00010101` = `0x15`; therefore `pool_selection = "15"`, and `outputs` contains `pool_manifest[0]`, `pool_manifest[2]`, and `pool_manifest[4]`, in that order.

Non-pool-mode participants omit `pool_manifest` and `pool_selection` (standard NUT-Exchange behavior).

Version 1 uses the full manifest. Pool size is logarithmic in the representable receive and change ranges, and every request remains subject to both `max_pool_entries` per participant and NUT-Exchange's `max_request_bytes` for the complete request. The mint MUST reject a request exceeding either limit, and a wallet MUST NOT create a pool-mode authorization that cannot fit both advertised limits. Merkle roots and inclusion proofs are not valid version-1 request forms. A future Merkle form MUST use a separately advertised version or mode that defines the leaf encoding, global index binding, tree construction and domain separation, proof encoding, and proof-size limits.

Response: same as NUT-Exchange — `{signatures: [...]}`, one `BlindSignature` array per participant. Pool-mode participants receive signatures for their selected entries only.

## Mint validation

Pool-mode participants require additional validation beyond [NUT-Exchange][exchange] rules 1–5, 9, 11:

6p. **Manifest hash:** hash `pool_manifest` canonically → MUST equal condition `data`. Otherwise reject (error 13041).

7p. **Selection consistency:** the entries indicated by `pool_selection` MUST exactly match the `outputs` array (same `B_`, `amount`, `id` values in the same order). Otherwise reject.

8p. **Role/keyset and two-class consistency:** validate the entire `pool_manifest`, not only selected entries. For each participant, all `receive` entries MUST share one `id`; all `change` entries MUST use the condition's `offer_keyset`; both roles MUST be present; and the derived receive keyset MUST differ from `offer_keyset`. No other keyset ID may occur in that manifest. Across all participants, exactly two distinct keyset IDs MUST occur among all conditions' `offer_keyset` values and all derived receive keysets. At least one `receive` entry MUST be selected for each participant. For every manifest entry, the mint MUST also verify that `id` is active for issuance and that the keyset publishes a signing key for `amount`.

9p. **Policy:** parse `rate_n`, `rate_d`, `min_receive`, and `max_debit` as unsigned `u128` values. Reject if parsing fails, if `rate_d = 0`, or if `min_receive = 0`. Using checked `u128` addition, compute `input_total` from the participant's inputs, `receive_total` from selected receive entries, and `change_total` from selected change entries. Reject if any conversion or sum overflows, if `max_debit > input_total`, or if `change_total > input_total`. Only after those checks, compute `debit_total = input_total − change_total` with checked subtraction. Compute both rate products with checked multiplication and reject if either product overflows. Then enforce:

- `receive_total × rate_d ≥ debit_total × rate_n` (rate covenant)
- `receive_total ≥ min_receive` (minimum fill)
- `debit_total ≤ max_debit` (spending cap)

10p. **Conservation:** standard per-class conservation from [NUT-Exchange][exchange] rule 10, applied with change entries in the offer keyset. The mint signs only `outputs`; `pool_manifest` entries are authentication material, not outputs to sign.

NUT-Exchange rule 7's per-participant single-keyset output constraint is replaced by rule 8p because selected pool outputs may use both that participant's receive keyset and offer keyset for change. NUT-Exchange rule 8's exactly-two-keysets invariant is not relaxed; rule 8p applies it to the keysets derived from every complete manifest and to the request as a whole.

## Example

Alice wants to swap **10000 cents (100 USD) for 1000 sats**. Here `input_total = 10000` cents is the value locked in the authorization; `max_debit = 1000` permits at most 1000 cents to be spent, so a complete 1000-sat fill at Alice's boundary rate returns 9000 cents as change.

### Preparation

**Receive pool** (sats keyset, 10 entries): amounts 1, 2, 4, 8, 16, 32, 64, 128, 256, 512. Any subset sums to 0–1023.

**Change pool** (USD keyset; amounts are cents, 14 entries): amounts 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192. These entries can represent every integer change amount from 0 through 16383 cents.

**Manifest:** 24 entries. `H_manifest` is computed from the canonical `PoolEntry` encodings defined above.

**Policy:** `rate_n = 1, rate_d = 1` (receive at least 1 sat per cent debited), `min_receive = 1` sat, `max_debit = 1000` cents.

**Lock:** one or more `PAY_TO_UNLOCK` proofs totaling 10000 cents, all carrying the same manifest and policy tags and unique per-proof nonces.

### Settlement — boundary fill of 500 sats

Counterparty offers 500 sats for 500 cents.

Coordinator selects:

- Receive: {256, 128, 64, 32, 16, 4} = 500 sats (6 entries)
- Change: {8192, 1024, 256, 16, 8, 4} = 9500 cents (6 entries)

Mint checks:

- `H_manifest` matches condition `data` ✓
- Selected entries exactly match the bitmap and `outputs` ✓
- `input_total = 10000`, `change_total = 9500`, so `debit_total = 10000 − 9500 = 500` cents ✓
- Rate boundary: `500 × 1 ≥ 500 × 1` → `500 ≥ 500` ✓
- `receive_total = 500 ≥ min_receive = 1` ✓
- `debit_total = 500 ≤ max_debit = 1000` ✓
- Conservation: 10000 cents in = 9500 cents change + 500 cents to the counterparty; 500 sats in = 500 sats out ✓

Equality is accepted: this is exactly Alice's limit of one sat per cent. If the counterparty instead offered 499 sats for the same 500-cent debit, the mint would evaluate `499 × 1 ≥ 500 × 1`, which is false, and MUST reject the request.

The mint signs Alice's 12 selected `BlindedMessage` values. Alice unblinds them to obtain 500 sats and 9500 cents of change.

### Settlement — better-price partial fill of 237 sats

Counterparty offers 237 sats for 200 cents (2.00 USD).

Coordinator selects:

- Receive: {128, 64, 32, 8, 4, 1} = 237 sats (6 entries)
- Change: {8192, 1024, 512, 64, 8} = 9800 cents (5 entries)

Mint checks:

- `input_total = 10000`, `change_total = 9800`, so `debit_total = 200` cents ✓
- Rate: `237 × 1 ≥ 200 × 1` → `237 ≥ 200` ✓
- `receive_total = 237 ≥ min_receive = 1` ✓
- `debit_total = 200 ≤ max_debit = 1000` ✓
- Conservation: 10000 cents in = 9800 cents change + 200 cents to the counterparty; 237 sats in = 237 sats out ✓

The strict inequality admits this better price: Alice pays `200 / 237` cents per sat, less than her maximum of one cent per sat. The mint signs Alice's 11 selected `BlindedMessage` values, and Alice unblinds them to obtain 237 sats and 9800 cents of change.

## Recovery and refund

Identical to [NUT-Exchange][exchange]. Pool-mode proofs carry the same `expiry` and `refund` tags. After `expiry`, the owner refunds via NUT-03 swap with a `refund` signature. Unused pool entries are simply discarded — they were never spent.

## Mint info

```json
{
  "exchange": {
    "supported": true,
    "version": 1,
    "max_participants": "<uint>",
    "max_inputs": "<uint>",
    "max_outputs": "<uint>",
    "max_request_bytes": "<uint>",
    "idempotent_retries": "<bool>",
    "max_expiry_seconds": "<uint>",
    "partial_fill": true,
    "max_pool_entries": "<uint>"
  }
}
```

`max_pool_entries` bounds the total number of manifest entries per participant, while `max_request_bytes` bounds the complete serialized request, including every participant's manifest. A wallet MUST satisfy both limits and a mint MUST enforce both limits before signing or mutating state.

## FAQ

**Why powers-of-2 denominations?**
`⌈log₂(N)⌉` entries cover every integer from 0 to `N−1` via subset sum. For a 1000-unit range: 10 entries. This keeps wallet cost logarithmic.

**Can the coordinator steal outputs?**
No. Every selected entry must be in Alice's authenticated manifest (verified by `H_manifest`). The coordinator can only select entries Alice pre-generated with her own blinding factors. It cannot inject its own `BlindedMessage` values.

**Does the mint enforce best execution?**
No. The rate covenant enforces the owner's limit price. Any subset satisfying the covenant is valid. The coordinator may select the least favorable valid pair. Best execution is an off-mint concern.

## References

- [NUT-01](01.md) · [NUT-02](02.md) · [NUT-03](03.md) · [NUT-06](06.md) ·
  [NUT-09](09.md) · [NUT-10](10.md) · [NUT-11](11.md) · [NUT-12](12.md) ·
  [NUT-Exchange][exchange]

[01]: 01.md
[02]: 02.md
[03]: 03.md
[06]: 06.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[exchange]: https://github.com/cashubtc/nuts/pull/410
[rfc8785]: https://www.rfc-editor.org/rfc/rfc8785.html
