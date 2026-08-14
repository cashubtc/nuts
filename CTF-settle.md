# NUT-CTF-settle: Multi-Party Atomic Settlement

`draft`

`optional`

depends on: NUT-CTF, NUT-CTF-split-merge, NUT-Exchange, NUT-Exchange-partial-fill, NUT-02, NUT-03, NUT-06, NUT-07, NUT-09, NUT-10, NUT-11, NUT-12

---

This NUT is an extension of both [NUT-Exchange][exchange] and [NUT-CTF-split-merge][CTF-split-merge]. The key observation: [NUT-Exchange][exchange] becomes more efficient when the mint is aware of CTF-specific characteristics (per-outcome conservation, conditional keysets, attestation cutoff), and [NUT-CTF-split-merge][CTF-split-merge] gains multi-party support by reusing [NUT-Exchange][exchange]'s `PAY_TO_UNLOCK` authorisation model. This NUT combines the two on a single endpoint. It also inherits [NUT-Exchange-partial-fill][partial-fill]'s pool-based **range orders**, so a participant may lock a fixed input and authorise a range of output bundles at a limit rate (see [Range orders](#range-orders-partial-fill)).

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
- `participants`: ≥ 2 records. Input conditions follow [NUT-Exchange][exchange]: each input is validated under its own spending condition. Every proof's keyset is either the regular collateral keyset of the condition's unit, or a conditional keyset registered under this `condition_id`.
- A participant record MAY additionally carry `pool_manifest` and `pool_selection` to authorise a **range order** (partial fill); see [Range orders](#range-orders-partial-fill). A single request MAY mix standard-mode and pool-mode participants; the mint validates each participant under its own mode's rules (standard participants follow base [NUT-Exchange][exchange] rules 6–7 and 12; pool participants follow rules 6p–9p from [NUT-Exchange-partial-fill][partial-fill]).

Response: `{signatures: [...]}` — one `BlindSignature` array per participant, same as [NUT-Exchange][exchange].

## Differences from NUT-Exchange

| Aspect               | NUT-Exchange                                           | This NUT                                                                                                                                                                                                              |
| -------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Conservation         | per-class (rule 10)                                    | per-outcome (from [CTF-split-merge]); **replaces** rule 10                                                                                                                                                            |
| Keyset constraint    | exactly two distinct keysets (rule 8)                  | collateral + conditional under one `condition_id`; **replaces** rule 8                                                                                                                                                |
| Condition tags       | `offer_keyset`, `expiry`, `refund` (3 tags)            | standard: identical (3 tags); pool (range order): + `rate_n`, `rate_d`, `min_receive`, `max_debit`                                                                                                                    |
| `H_recv` domain      | `Cashu/PAY_TO_UNLOCK/recv`                             | `Cashu/ctf/convert/recv` (standard mode)                                                                                                                                                                              |
| `request_digest`     | `Cashu/exchange/request` over participant records only | `Cashu/ctf/convert/request` over `condition_id` + `parent_collection_id` + participant records                                                                                                                        |
| Refund digest domain | `Cashu/PAY_TO_UNLOCK/refund`                           | identical (unified)                                                                                                                                                                                                   |
| Attestation cutoff   | n/a                                                    | MUST reject after attestation; serialise with commit                                                                                                                                                                  |
| Liability accounting | n/a                                                    | per-outcome `ΔL(o)` (see below)                                                                                                                                                                                       |
| Partial fill         | pool mode (rules 6p–10p)                               | rules 6p, 7p, 9p and the per-participant clauses of 8p **inherited**; the request-global two-keyset clause of 8p and 10p **replaced** by rule 8 and per-outcome rule 10; manifest domain `Cashu/ctf/convert/manifest` |

**Inherited from NUT-Exchange:** rules 1, 2, 4, and 9 apply to every input and record; rule 3 is inherited as amended (per-input condition validation, endpoint-compatible condition classes, and the locked/bare record predicate — replacing the former every-input `PAY_TO_UNLOCK` rule); rule 5 applies to `PAY_TO_UNLOCK` inputs; rules 6–7 and 12 apply to standard locked records only — pool records are validated by the pool rule set (6p–9p) instead; rule 11 takes its minimum over `PAY_TO_UNLOCK` inputs only and is skipped when there are none; `PAY_TO_UNLOCK` condition mechanism (3 required tags for standard participants; CTF does not use the base optional tags `alt_outputs`, `allow_change`, or `min_output_amount`; pool-mode range orders add `rate_n`, `rate_d`, `min_receive`, `max_debit` — see [Range orders](#range-orders-partial-fill)); `H_recv` computation (entry encoding identical, domain differs); recovery; refund mechanics (including witness-free preimage and unified refund domain); idempotency; coordinator-trust properties.

**Replaced:** rule 8 (keyset constraint) and rule 10 (conservation) for all participants; for pool-mode participants additionally the request-global two-keyset clause of rule 8p and rule 10p — see [Range orders](#range-orders-partial-fill).

## Differences from NUT-CTF-split-merge

| Aspect               | CTF-split-merge            | This NUT                                                                           |
| -------------------- | -------------------------- | ---------------------------------------------------------------------------------- |
| Participants         | 1 (single-party)           | ≥ 2 (multi-party)                                                                  |
| Input conditions     | not required               | inherited — each input validated under its own condition                           |
| `in(o)` / `out(o)`   | single owner's bundle      | summed across **all participants**                                                 |
| Keyset-active cutoff | all keysets MUST be active | **inherited** — takes precedence over NUT-Exchange's weaker "still-spendable" rule |

Conservation rule, fee model, coverage from keyset metadata, and canonical collection encoding are inherited unchanged.

## CTF-specific validation

Standard participants inherit rules 1–7, 9, 11–12 from [NUT-Exchange][exchange] and reject the optional `alt_outputs`, `allow_change`, and `min_output_amount` tags. Pool-mode (range-order) participants instead inherit rules 6p, 7p, 9p and the per-participant clauses of 8p from [NUT-Exchange-partial-fill][partial-fill] (see [Range orders](#range-orders-partial-fill)). For all participants, rules 8 and 10 are **replaced**:

- **Rule 8 (replaced):** Every input/output keyset MUST be active. Collateral keysets MUST be regular with unit equal to the condition's collateral unit. Conditional keysets MUST be registered under this `condition_id`. Either class is valid on either side of a convert.
- **Rule 10 (replaced):** Per-outcome conservation with `in(o)` / `out(o)` summed across all participants: `out(o) == in(o) − F` for every `o ∈ Ω` (error 13041). Since collateral covers every outcome, an uncovered outcome (no participant receives tokens covering it) would force `out(o) = 0 = in(o) − F`, making the fee absorb all collateral — a degenerate settlement. Multi-party convert therefore requires at least one output to cover each outcome. (Single-party convert inherits split-merge's rule, which permits `out(o) == 0` when the fee legitimately consumes one outcome's value.)

Additional multi-party rules:

1. `parent_collection_id` MUST be omitted or all-zero. Advertised limits (`max_participants`, `max_inputs`, `max_outputs`, `max_request_bytes`, `max_pool_entries`) MUST be respected.
2. **No attestation recorded** for `condition_id` (error 13042). This check MUST serialise atomically with the convert commit — see [Attestation atomicity](#attestation-atomicity).
3. Inputs carrying a canonical `PAY_TO_UNLOCK` condition follow the participant rules. **Standard participants** use the 3 required tags (`offer_keyset`, `expiry`, `refund`) and optionally the inherited `coordinator_pubkey`; all `PAY_TO_UNLOCK` inputs in one participant record share the same `H_recv`, `expiry`, `refund`, and `offer_keyset`, with unique per-proof nonces, and each standard locked record's complete `outputs` list hashes to that `H_recv`. **Pool-mode (range-order) participants** add the 4 pool tags (`rate_n`, `rate_d`, `min_receive`, `max_debit`) and set `data = H_manifest` over the domain `Cashu/ctf/convert/manifest`; `coordinator_pubkey` is also permitted. See [Range orders](#range-orders-partial-fill). In both modes the `offer_keyset` MUST match each `PAY_TO_UNLOCK` proof's actual keyset (`Proof.id`). A pool record contains only pool-authorized `PAY_TO_UNLOCK` inputs and applies 6p–9p; a non-`PAY_TO_UNLOCK` input follows the inherited endpoint-compatible rule-3 class and supplies no `H_recv`, `expiry`, `refund`, `offer_keyset`, or pool fields. Inputs without a spending condition are validated as ordinary proofs. A bare record (no `PAY_TO_UNLOCK` inputs) has no `H_recv` requirement; its outputs are constrained by CTF rule 8 and per-outcome conservation (rule 10). A bare record uses the plain JCS participant canonical form; `pool_manifest` and `pool_selection` are forbidden on it.
4. Reject if any involved keyset has `input_fee_ppk == 0` unless admission control is in force _(without `F`, anyone can submit unlimited convert requests at no cost — a free-DoS vector)_.
5. For each `PAY_TO_UNLOCK` input, **`expiry` MUST precede** the earliest `final_expiry` among all conditional keysets registered under this `condition_id`. If any keyset lacks `final_expiry`, the mint MUST use its advertised `max_expiry_seconds` as the effective bound. Without this, a proof whose `expiry` falls after all same-outcome keysets are deactivated cannot be refunded or redeemed — stranding value permanently. _Known limitation: `expiry` is inside the blinded `Proof.secret` ([NUT-10][10]) and invisible to the mint at [NUT-03][03] swap time; the mint enforces this check at settlement, not creation. Wallets MUST set `expiry` conservatively._

## `request_digest` (optional)

Optional feature inherited from [NUT-Exchange][exchange] (advertised via `idempotent_retries` in [NUT-06][06] info). Enables idempotent retries: if a client's request commits but the response is lost, the client retries the identical request and the mint returns the cached response. Without it, clients fall back to [NUT-09][09] recovery, same as [NUT-03][03] swap.

The CTF digest (when supported) commits to **all** semantic top-level fields:

```
req_canonical = bytes(condition_id, 32) || bytes(parent_collection_id, 32) || participant[0]_canonical || ... || participant[n-1]_canonical
request_digest = tagged_hash("Cashu/ctf/convert/request", req_canonical)
coordinator_digest = tagged_hash("Cashu/ctf/convert/coordinator", req_canonical)
```

`condition_id` and `parent_collection_id` are each exactly 64 lowercase hex chars decoded to 32 raw bytes; an omitted `parent_collection_id` is 32 zero bytes (v1's only permitted explicit value). `participant_canonical` is mode-dependent: standard participants use `JCS({"inputs": ..., "outputs": ...})`; pool-mode participants use `JCS({"inputs": ..., "outputs": ..., "pool_manifest": ...}) || hex_decode(pool_selection)` (as in [NUT-Exchange-partial-fill][partial-fill]). `coordinator_sig` is excluded from `req_canonical`.

**Coordinator authentication** is inherited from [NUT-Exchange][exchange]: if any canonical `PAY_TO_UNLOCK` input carries `coordinator_pubkey`, the request must carry `coordinator_sig` — a BIP-340 signature valid under the bound key over `coordinator_digest`. Version 1 permits one key per request; `coordinator_sig` must be absent otherwise and is verified before any idempotency-cache hit (error 15015 on failure). `coordinator_pubkey` is permitted in standard and pool mode.

## Range orders (partial fill)

CTF convert supports partial fills via the pool-based **range orders** defined in [NUT-Exchange-partial-fill][partial-fill]. A participant locks a fixed input set (all proofs sharing one `H_manifest`) and authorises a **range** of output bundles at a limit rate; the coordinator selects the subset that matches the agreed price, and the mint signs only the selected entries. This replaces the earlier micro-lot input-subset pattern.

A pool-mode participant carries the `pool_manifest` and `pool_selection` fields from [NUT-Exchange-partial-fill][partial-fill], and its inputs' `PAY_TO_UNLOCK` condition carries the pool tags `rate_n`, `rate_d`, `min_receive`, `max_debit` with `data = H_manifest`. The base optional tags `alt_outputs`, `allow_change`, and `min_output_amount` MUST be absent. A single `/v1/ctf/convert` MAY mix standard-mode and pool-mode participants; the mint validates each participant under its own mode's rules.

**Inherited from [NUT-Exchange-partial-fill][partial-fill]:** rule 6p (manifest hash), 7p (selection consistency), 9p (policy: the rate covenant `receive_total × rate_d ≥ debit_total × rate_n`, plus `min_receive` and `max_debit`, in face-value minor units), and the **per-participant** clauses of rule 8p (receive entries share one `id`, change entries use the `offer_keyset`, both roles present). The **request-global** exactly-two-keysets clause of rule 8p is **replaced** by this NUT's rule 8 (collateral plus one or more conditional keysets under one `condition_id`), because a complementary match legitimately unions {collateral, YES, NO}. Rule 10p (per-class conservation) is **replaced** by this NUT's per-outcome rule 10.

**Endpoint binding (CTF rule 6p):** the manifest is hashed under the CTF-specific domain `Cashu/ctf/convert/manifest`, not the base `Cashu/PAY_TO_UNLOCK/manifest` domain. This mirrors the `H_recv` domain override and prevents a pool authorization prepared for `/v1/exchange` from being replayed at `/v1/ctf/convert`, where a different conservation and fee model applies. The mint MUST reject a manifest committed under any other domain.

**Limit-price encoding:** the rule 9p covenant is inherited unchanged. The tags are unsigned integers, so a limit price MUST be expressed as a reduced fraction over face-value minor units. For a **buy** at price `p = a/b` collateral units per conditional unit (debit ÷ receive ≤ `a/b`), the encoding is `rate_n = b`, `rate_d = a`, yielding `receive_total × a ≥ debit_total × b`. A **sell** at the same price reverses to `rate_n = a`, `rate_d = b`. Fractional prices are therefore representable (e.g. `0.60 = 3/5` → buy `rate_n = 5, rate_d = 3`).

**Conservation:** the pool selection sets each participant's input and output contribution; per-outcome conservation `out(o) == in(o) − F` is then enforced across **all** participants as usual (rule 10). The rate covenant (9p) is a per-participant limit-price check and is independent of global conservation. Pool-mode change is conservation-safe for the same reason all change is: a collateral input `I` contributes `I` to `in(o)` for every outcome `o`, and a collateral change output `C` contributes `C` to `out(o)` for every `o`, so their net `−(I − C) = −debit_total` is uniform across outcomes and cannot inflate any single `out(o)`; the binding constraint is the per-outcome equality itself (`max_debit` and the rate covenant bound authorization and price, not conservation).

**Input consolidation:** pool mode locks a fixed input set and charges `input_fee_ppk` on every locked input proof. A wallet SHOULD consolidate the maximum order into a single (or minimal-count) input proof before authorising a range order, so that per-input fees do not dominate a small fill or push it below the owner's rate.

Recovery, refund, and the discard-safety rule (an owner MUST NOT discard any unselected entry's secret or blinding factor before a definitive settlement outcome) are inherited unchanged from [NUT-Exchange-partial-fill][partial-fill].

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

Same [NUT-06][06] setting as [NUT-CTF-split-merge][CTF-split-merge], extended with `max_participants` (≥ 2), `max_expiry_seconds` (same semantics as [NUT-Exchange][exchange]: bounds `PAY_TO_UNLOCK` condition lifetime at [NUT-03][03] swap time), and the pool-mode fields from [NUT-Exchange-partial-fill][partial-fill]: `partial_fill` (capability bool) and `max_pool_entries` (per-participant manifest-entry cap). `max_request_bytes` bounds the complete serialized request, including every pool-mode participant's `pool_manifest` and `pool_selection`.

## FAQ

**Why a separate NUT?**
Single-party convert ([CTF-split-merge]) does not need `PAY_TO_UNLOCK` or any [NUT-Exchange][exchange] concept. This NUT adds the multi-party layer for readers who already know both.

**Does the mint enforce fair pricing?**
The mint enforces each participant's own limit price (the rule 9p rate covenant for range orders) but does **not** enforce best execution or fair matching — price discovery and match selection are off-mint. Per-outcome conservation (rule 10) is the only structural constraint on the aggregate.

## References

- [NUT-CTF][CTF] · [NUT-CTF-split-merge][CTF-split-merge] · [NUT-Exchange][exchange] · [NUT-Exchange-partial-fill][partial-fill]
- [Polymarket CTF Exchange](https://github.com/Polymarket/ctf-exchange-v2)

[02]: 02.md
[03]: 03.md
[06]: 06.md
[CTF]: CTF.md
[CTF-split-merge]: CTF-split-merge.md
[exchange]: https://github.com/cashubtc/nuts/pull/410
[partial-fill]: https://github.com/cashubtc/nuts/pull/410
