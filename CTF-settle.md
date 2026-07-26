# NUT-CTF-settle: Multi-Party Atomic Settlement

`draft`

`optional`

`depends on: NUT-CTF, NUT-CTF-split-merge, NUT-02, NUT-03, NUT-06, NUT-07, NUT-09, NUT-10, NUT-11, NUT-12`

---

This NUT is an extension of both [NUT-Exchange][exchange] and [NUT-CTF-split-merge][CTF-split-merge]. The key observation: [NUT-Exchange][exchange] becomes more efficient when the mint is aware of CTF-specific characteristics (per-outcome conservation, conditional keysets, attestation cutoff), and [NUT-CTF-split-merge][CTF-split-merge] gains multi-party support by reusing [NUT-Exchange][exchange]'s `PAY_TO_UNLOCK` authorisation model. This NUT combines the two on a single endpoint.

Readers should be familiar with [NUT-Exchange][exchange] (`PAY_TO_UNLOCK`, `H_recv`, recovery, refund, the `participants` request shape, idempotency) and [NUT-CTF-split-merge][CTF-split-merge] (per-outcome conservation, coverage from keyset metadata, canonical collection encoding, fee model). This document specifies only the **differences**.

## Request

Same endpoint as [NUT-CTF-split-merge][CTF-split-merge]:

```http
POST https://mint.host:3338/v1/ctf/convert
```

Multi-party mode is detected by the `participants` key (same request/response shape as [NUT-Exchange][exchange]):

```json
{
  "condition_id": "<hex_str: 32 bytes>",
  "parent_collection_id": "<hex_str: 32 bytes, MUST be all-zero in v1>",
  "participants": [
    { "inputs": "<Array[Proof]>", "outputs": "<Array[BlindedMessage]>" },
    { "inputs": "<Array[Proof]>", "outputs": "<Array[BlindedMessage]>" }
  ]
}
```

- `condition_id`: shared across all participants; 64-char hex (error 13021 if unknown).
- `parent_collection_id`: reserved for nested conditions; MUST be omitted or all-zero in v1.
- `participants`: ≥ 2 records. Every input MUST carry a `PAY_TO_UNLOCK` condition. Every proof's keyset is either the regular collateral keyset of the condition's unit, or a conditional keyset registered under this `condition_id`.

Response: `{signatures: [...]}` — one `BlindSignature` array per participant, same as [NUT-Exchange][exchange].

## Differences from NUT-Exchange

| Aspect               | NUT-Exchange                                           | This NUT                                                                                                 |
| -------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Conservation         | per-class (rule 10)                                    | per-outcome (from [CTF-split-merge]); **replaces** rule 10                                               |
| Keyset constraint    | exactly two distinct keysets (rule 8)                  | collateral + conditional under one `condition_id`; **replaces** rule 8                                   |
| Condition tags       | `offer_keyset`, `expiry`, `refund` (3 tags)            | `expiry`, `refund` only (2 tags — CTF keysets have unique signing keys, so `offer_keyset` is not needed) |
| `H_recv` domain      | `Cashu/PAY_TO_UNLOCK/recv`                             | `Cashu/ctf/convert/recv`                                                                                 |
| `request_digest`     | `Cashu/exchange/request` over participant records only | `Cashu/ctf/convert/request` over `condition_id` + `parent_collection_id` + participant records           |
| Refund digest domain | `Cashu/PAY_TO_UNLOCK/refund`                           | `Cashu/ctf/convert/refund`                                                                               |
| Attestation cutoff   | n/a                                                    | MUST reject after attestation; serialise with commit                                                     |
| Liability accounting | n/a                                                    | per-outcome `ΔL(o)` (see below)                                                                          |

**Inherited from NUT-Exchange:** rules 1–7, 9, 11; `PAY_TO_UNLOCK` condition mechanism; `H_recv` computation (entry encoding identical, domain differs); recovery; refund mechanics; idempotency; coordinator-trust properties.

**Replaced:** rule 8 (keyset constraint) and rule 10 (conservation) — see CTF-specific validation below.

## Differences from NUT-CTF-split-merge

| Aspect               | CTF-split-merge            | This NUT                                                                           |
| -------------------- | -------------------------- | ---------------------------------------------------------------------------------- |
| Participants         | 1 (single-party)           | ≥ 2 (multi-party)                                                                  |
| Input conditions     | not required               | every input MUST carry `PAY_TO_UNLOCK`                                             |
| `in(o)` / `out(o)`   | single owner's bundle      | summed across **all participants**                                                 |
| Keyset-active cutoff | all keysets MUST be active | **inherited** — takes precedence over NUT-Exchange's weaker "still-spendable" rule |

Conservation rule, fee model, coverage from keyset metadata, and canonical collection encoding are inherited unchanged.

## CTF-specific validation

Rules 1–7, 9, 11 from [NUT-Exchange][exchange] are inherited. Rules 8 and 10 are **replaced**:

- **Rule 8 (replaced):** Every input/output keyset MUST be active. Collateral keysets MUST be regular with unit equal to the condition's collateral unit. Conditional keysets MUST be registered under this `condition_id`. Either class is valid on either side of a convert.
- **Rule 10 (replaced):** Per-outcome conservation with `in(o)` / `out(o)` summed across all participants: `out(o) == in(o) − F` for every `o ∈ Ω` (error 13041). Since collateral covers every outcome, an uncovered outcome (no participant receives tokens covering it) would force `out(o) = 0 = in(o) − F`, making the fee absorb all collateral — a degenerate settlement. Multi-party convert therefore requires at least one output to cover each outcome. (Single-party convert inherits split-merge's rule, which permits `out(o) == 0` when the fee legitimately consumes one outcome's value.)

Additional multi-party rules:

1. `parent_collection_id` MUST be omitted or all-zero. Advertised limits (`max_participants`, `max_inputs`, `max_outputs`, `max_request_bytes`) MUST be respected.
2. **No attestation recorded** for `condition_id` (error 13042). This check MUST serialise atomically with the convert commit — see [Attestation atomicity](#attestation-atomicity).
3. Every input carries a canonical `PAY_TO_UNLOCK` condition (2 tags). All inputs in one participant record share the same condition. Each participant's outputs hash to that `H_recv`.
4. Reject if any involved keyset has `input_fee_ppk == 0` unless admission control is in force _(without `F`, anyone can submit unlimited convert requests at no cost — a free-DoS vector)_.

## `request_digest` (optional)

Optional feature inherited from [NUT-Exchange][exchange] (advertised via `idempotent_retries` in [NUT-06][06] info). Enables idempotent retries: if a client's request commits but the response is lost, the client retries the identical request and the mint returns the cached response. Without it, clients fall back to [NUT-09][09] recovery, same as [NUT-03][03] swap.

The CTF digest (when supported) commits to **all** semantic top-level fields:

```
req_canonical = condition_id || parent_collection_id_canonical || participant[0]_canonical || ... || participant[n-1]_canonical
request_digest = tagged_hash("Cashu/ctf/convert/request", req_canonical)
```

where `parent_collection_id_canonical` is the all-zero 32-byte hex if the field is omitted.

## Attestation atomicity

_[Not in NUT-Exchange.]_ After the oracle attests the winning outcome, the condition is resolved. If a convert commits in the same instant — between the attestation write and keyset deactivation — the mint issues new conditional tokens for an already-resolved condition. Those tokens are worthless to holders but still backed by collateral, creating phantom liabilities.

To prevent this race, every `/v1/ctf/convert` commit (single-party and multi-party) MUST take the same row-level lock on the condition record as the [NUT-CTF][CTF] attestation write. Either the attestation records first (convert is rejected — condition resolved) or the convert commits first (attestation waits — condition still open). No race is possible.

## Liability accounting

_[Not in NUT-Exchange.]_

**In plain terms:** the mint doesn't gamble. It takes in collateral and hands out conditional tokens, but the books always balance — for any outcome the oracle might pick, the mint holds enough collateral to redeem every outstanding token. The fee it keeps is the same regardless of which outcome wins.

**Formally:** the reserve `R` (total collateral held) and per-outcome liability `L(o)` are defined by [NUT-CTF-split-merge][CTF-split-merge]'s Issuance Invariant. Every convert preserves `R ≥ L(o)` because:

- `ΔR = collateral_in − collateral_out` (net collateral locked by this convert).
- `ΔL(o) = out_conditional(o) − in_conditional(o)` (change in conditional liability on outcome `o`).
- Per-outcome conservation rearranges to `ΔL(o) = ΔR − F` for every `o`.
- Since `ΔR − ΔL(o) = F ≥ 0`, the solvency margin `R − L(o)` grows by `F` on every outcome.

## Polymarket match types

A single convert may mix `MINT` (buy + buy on complementary outcomes), `MERGE` (sell + sell), and `COMPLEMENTARY` (buy + sell same token) matches, provided per-outcome conservation holds. All three require atomic settlement via `/v1/ctf/convert`; [NUT-03][03] cannot mix regular and conditional keysets ([NUT-CTF][CTF]).

## Mint info

Same [NUT-06][06] setting as [NUT-CTF-split-merge][CTF-split-merge], extended with `max_participants` (≥ 2) and `max_expiry_seconds` (same semantics as [NUT-Exchange][exchange]: bounds `PAY_TO_UNLOCK` condition lifetime at [NUT-03][03] swap time).

## FAQ

**Why a separate NUT?**
Single-party convert ([CTF-split-merge]) does not need `PAY_TO_UNLOCK` or any [NUT-Exchange][exchange] concept. This NUT adds the multi-party layer for readers who already know both.

**Does the mint enforce fair pricing?**
No. Per-outcome conservation is the only structural constraint. Per-participant pricing is set off-mint.

## References

- [NUT-CTF][CTF] · [NUT-CTF-split-merge][CTF-split-merge] · [NUT-Exchange][exchange]
- [Polymarket CTF Exchange](https://github.com/Polymarket/ctf-exchange-v2)

[02]: 02.md
[03]: 03.md
[06]: 06.md
[CTF]: CTF.md
[CTF-split-merge]: CTF-split-merge.md
[exchange]: https://github.com/cashubtc/nuts/pull/410
