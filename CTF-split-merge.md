# NUT-CTF-split-merge: Conditional Token Convert (Split, Merge, Recombine)

`optional`

`depends on: NUT-CTF`

---

This NUT defines a single **convert** operation for conditional tokens ([NUT-CTF][CTF]): any payoff-preserving rebalance of conditional positions within one condition at one nesting level. Convert subsumes four operations:

- **Split**: deposit collateral, receive a complete set of conditional tokens.
- **Merge**: surrender a complete set of conditional tokens, recover collateral.
- **Recombine**: regroup outcome collections (e.g. `A` + `B|C` → `A|B|C`) without touching collateral.
- **Conversion** (negative-risk style): cross the collateral boundary mid-bundle (e.g. `A|B|C` + `B|C|D` → collateral + `B|C`).

Inspired by the [Gnosis Conditional Token Framework](https://conditional-tokens.readthedocs.io/en/latest/) ([contracts](https://github.com/gnosis/conditional-tokens-contracts)), whose `splitPosition`/`mergePositions` operate on arbitrary partitions of any outcome collection. [Polymarket](https://github.com/Polymarket/ctf-exchange-v2)'s negative-risk position conversion is the special case where collateral appears mid-bundle; convert provides it natively with no separate adaptor.

Caution: Applications must verify that the mint supports both NUT-CTF and NUT-CTF-split-merge via the [info][06] endpoint.

## Overview

```
           Register            Convert (split)          Trade                Convert (merge)        Attest          Redeem
Wallet ────────────► Mint   User ──────────────► Conditional ◄───────────►  User ──────────►  ...  Oracle ──────►  Winner ─────►
       cond. info    creates    collateral        Tokens         NUT-03      complete set            Signs          redeem_outcome
                     keysets    + fee F            (per-OC                    → collateral           Outcome        → Regular
                                                   keysets)                   (− fee F)                              Keyset
```

1. **Register**: Condition + partition registered via [NUT-CTF][CTF] to create conditional keysets.
2. **Convert**: `Alice` submits an input bundle of proofs and an output bundle of blinded messages; the mint signs the outputs iff the operation is payoff-preserving after a flat fee (see [Conservation Rule](#conservation-rule)).
3. **Trade**: Standard [NUT-03][03] swaps within the same conditional keyset.
4. **Attest**: Oracle signs winning outcome.
5. **Redeem**: Winners use `POST /v1/redeem_outcome` ([NUT-CTF][CTF]).

## Payoff-Vector Model

For a condition with outcome-atom set **Ω** (for nested conditions, the child outcomes under the parent collection), a token for outcome collection `S` with amount `a` is the **payoff vector** that pays `a` on each outcome in `cover(S)` and `0` elsewhere. **Collateral** — plain ecash on a regular keyset (root), or the parent collection's conditional keyset (nested) — is the **all-ones** vector: it pays on every outcome in Ω.

A convert is valid iff the input and output payoff vectors are equal after deducting a flat fee on every outcome. This single condition generalises split, merge, recombine, and conversion.

## Convert Operation

```http
POST https://mint.host:3338/v1/ctf/convert
```

**Request** of `Alice`:

```json
{
  "condition_id": <hex_str>,
  "parent_collection_id": <hex_str>,
  "inputs": {
    "<outcome_collection_or_*>": <Array[Proof]>,
    ...
  },
  "outputs": {
    "<outcome_collection_or_*>": <Array[BlindedMessage]>,
    ...
  }
}
```

- `condition_id`: 64-char hex (error 13021 if unknown).
- `parent_collection_id` (optional): 64-char hex. Defaults to all zeros for root conditions.
- `inputs` / `outputs`: objects mapping each map key to an array of `Proof` / `BlindedMessage`. A map key is either a **canonical outcome collection string** (see [Canonical Collection Encoding](#canonical-collection-encoding)) or the reserved key `"*"` denoting **collateral**:
  - For root conditions (`parent_collection_id` all zeros), `"*"` uses the **regular keyset** of the collateral unit.
  - For nested conditions, `"*"` uses the **parent collection's conditional keyset** — the active keyset whose `outcome_collection_id` equals `parent_collection_id`.
- Duplicate JSON member names within `inputs` or `outputs` MUST be rejected.

**Response** of `Bob`:

```json
{
  "signatures": {
    "<outcome_collection_or_*>": <Array[BlindSignature]>,
    ...
  }
}
```

Each `signatures` array preserves the order of the corresponding `outputs` array.

```bash
curl -X POST https://mint.host:3338/v1/ctf/convert \
  -H "Content-Type: application/json" \
  -d '{"condition_id":"a1b2c3...","inputs":{"*":[...],"A":[...],"B|C":[...]},"outputs":{"A|B|C":[...]}}'
```

### Special Cases

| Operation | `inputs` | `outputs` |
| --------- | -------- | --------- |
| Split | `{"*": [...]}` | per-outcome-collection map (a partition) |
| Merge | per-outcome-collection map (a partition) | `{"*": [...]}` |
| Recombine | conditional collections only (no `"*"`) | conditional collections only (no `"*"`) |
| Conversion | conditional ± `"*"` | conditional ± `"*"` |

## Conservation Rule

Let:

- For each entry, let its **cover** be `Ω` if its keyset is the collateral keyset (the `"*"` entry), otherwise the outcome set of the canonical collection recorded in that keyset's **metadata** (see [Coverage From Keyset Metadata](#coverage-from-keyset-metadata)). The map key is validated to equal that canonical collection but is never itself used to compute coverage.
- `in(o)`  = the sum of input amounts whose entry covers `o`, for each `o ∈ Ω`.
- `out(o)` = the sum of output amounts whose entry covers `o`, for each `o ∈ Ω`.
- `F` = `ceil( Σ input_fee_ppk / 1000 )` over **all** input proofs (both `"*"` and conditional), per [NUT-02][02]. This flat fee is denominated in the collateral unit.

`Bob` MUST enforce, for **every** `o ∈ Ω`:

```
out(o) == in(o) − F
```

and MUST reject the request unless `in(o) ≥ F` for every `o ∈ Ω` (error 13041).

`in(o)` and `out(o)` are computed by expanding each token's **registered** canonical collection to its outcome set and summing overlaps **per outcome** (collections on the same side may overlap; e.g. outputs `A|B` and `B|C` both contribute to outcome `B`).

This rule:

- preserves the payoff vector exactly except for the flat fee `F`, which the mint retains on **every** outcome — so the fee is real collateral the mint keeps regardless of which outcome the oracle attests (non-contingent);
- requires the input bundle to cover the fee on every outcome. For a floor-0 recombine the user includes `F` of collateral under `"*"` to satisfy `in(o) ≥ F` everywhere;
- reduces to the classical split (`each outcome collection total == sum(inputs) − F`) and merge.

### Examples

**Split** (binary market, 100 sats collateral, `F = 0`):

- `inputs["*"]`: 100 sats (regular keyset `009a1f293253e41e`)
- `outputs["YES"]`: 100 sats (conditional keyset `00abc123def456`)
- `outputs["NO"]`: 100 sats (conditional keyset `00def789abc012`)
- `in(YES)=in(NO)=100`; `out(YES)=out(NO)=100`. ✓

**Recombine** (`Ω = {A,B,C,D}`, `F = 1`):

- `inputs`: `{"*": 1, "A": 1, "B|C": 1}` → `in = (A:2, B:2, C:2, D:1)`
- `outputs`: `{"A|B|C": 1}` → `out = (A:1, B:1, C:1, D:0)`
- `out(o) == in(o) − 1` for every `o`. ✓ The mint keeps 1 on every outcome.

**Conversion** (negative-risk style, `Ω = {A,B,C,D}`, `F = 1`):

- `inputs`: `{"A|B|C": 100, "B|C|D": 100}` → `in = (A:100, B:200, C:200, D:100)`
- `outputs`: `{"*": 99, "B|C": 100}` → `out = (A:99, B:199, C:199, D:99)`
- `out(o) == in(o) − 1` for every `o`. ✓ The holder withdraws 99 sats of spendable collateral (the bundle's guaranteed floor minus the fee) plus a `B|C` position, with no oracle witness.

## Coverage From Keyset Metadata

A map key is untrusted text and MUST NOT be used to compute coverage. For every non-`"*"` entry, `Bob` MUST resolve each `Proof`/`BlindedMessage` keyset `id` to its **stored keyset metadata** (error 12001 if unknown) and verify that the metadata matches this `condition_id`, `parent_collection_id`, unit, and a canonical outcome collection. The request map key MUST equal that canonical collection (error 13041 otherwise). `cover()` is derived from the metadata, never from the request string. Every `"*"` proof/message MUST use the collateral keyset defined above (error 13017 if a regular/conditional keyset is placed under the wrong key).

## Canonical Collection Encoding

Outcome collections have a single canonical string form, used both as map keys here and in [NUT-CTF][CTF] keyset-ID derivation, so that `A|B` and `B|A` denote one keyset:

- Outcome names are NFC-normalised.
- Components are ordered by **condition type**:
  - **enum** ([NUT-CTF][CTF]): by the outcome's index in `announcements[0].oracle_event.event_descriptor.outcomes` — the same announcement that defines `outcome_count` in the [condition ID][CTF]. All announcements for a condition MUST share the same ordered outcome list, so this index is unambiguous.
  - **numeric** ([NUT-CTF-numeric][CTF-numeric]): the fixed synthetic order `["HI", "LO"]`, independent of digit-oracle fields.
- Components are joined by `|`. A literal `|` in an outcome name is escaped `\|`; a literal `\` is escaped `\\`.

`Bob` MUST reject (error 13041): non-canonical ordering or encoding, duplicate outcomes, empty components, unknown outcomes, malformed escapes, the reserved token `"*"`, and any **full-set** cover.

## Mint Behavior

`Bob`:

1. Looks up the condition (error 13021 if not found). Rejects if an attestation has been recorded for the condition (error 13042), or if any involved keyset is inactive (error 12002). These two conditions are the only cutoffs: maturity is **not** a cutoff, and there is no separate status check — a `violation` status implies a recorded (conflicting) attestation, and an `expired` condition implies inactive keysets, so both are already covered. Convert is allowed until an attestation is recorded, provided the keysets are still active.
2. For each entry, resolves keyset metadata and validates `condition_id`, `parent_collection_id`, unit, canonical collection == map key, and `"*"` ↔ collateral keyset placement (see [Coverage From Keyset Metadata](#coverage-from-keyset-metadata)).
3. Rejects if any two input proofs across all entries share a secret (error 11007), or if any input or output amount is not positive, or if there is no input, or if `outputs` is empty.
4. Verifies all input proofs are valid and unspent (errors 10001 / 11001).
5. Computes `in(o)`, `out(o)`, and `F`, and enforces the [Conservation Rule](#conservation-rule) for every `o ∈ Ω` (error 13041).
6. Atomically marks all input proofs spent, signs all output blinded messages, and persists the signatures in a **single transaction**. No output is signed until every input is verified and reserved.

## Security Considerations

- **Atomicity**: Convert MUST be atomic — all signatures or none. Duplicate-detection, spent-marking, and signature persistence occur in one transaction.
- **Solvency**: Let `R` be the real collateral the mint holds and `L(o)` the outstanding conditional liability at outcome `o`. The conservation rule forces the per-outcome change `ΔL(o)` to equal the real collateral change `ΔR` minus the retained fee, for every `o`. Since `R ≥ L(o)` holds at inception (every conditional token is backed at face — see [Issuance Invariant](#issuance-invariant)), convert preserves `R ≥ L(o)` for all `o`. No oracle witness is required: a payoff-preserving conversion cancels all outcome risk.
- **Non-contingent fee / DoS**: Because `F` is retained on every outcome, each convert costs the requester real collateral regardless of the eventual outcome, bounding free operations. Keysets with `input_fee_ppk == 0` make convert free and MUST be rejected for convert (error 13041) unless separate admission control is in force. Mints MAY additionally require [NUT-21][21]/[NUT-22][22] authentication, rate limits, or per-request caps on output count / distinct collections / total amount as defense-in-depth.
- **Privacy**: As with any multi-input operation, the mint observes that all inputs and outputs of one convert are co-owned; a consolidating convert can link previously unlinked tokens.
- **Depth Limits**: Mints MAY impose a maximum nesting depth via [Mint Info Setting](#mint-info-setting).

### Issuance Invariant

Every conditional token, by any issuance path, MUST be backed by locked collateral at least equal to its face amount. `split`/`convert` satisfy this; a face-value [NUT-04][04] mint into a conditional keyset would too. Sub-face or market-priced issuance into a conditional keyset is forbidden — that is a trading operation, not minting, and would break solvency.

## Full-Set and Reserved Key Rules

To keep `"*"` unambiguous, the following [NUT-CTF][CTF] partition rules apply:

- A partition MUST contain at least two outcome collections, and no single outcome collection may cover all of Ω. The full-set payoff vector is represented only as collateral, never as a conditional keyset.
- `"*"` is reserved: it is invalid as an outcome name and as an outcome collection string.

## Combinatorial Markets

Conditions can be nested hierarchically (e.g. "Party A wins AND BTC > $100k") by splitting parent-collection tokens into sub-condition partitions. Outcome collection IDs use EC point addition ([NUT-CTF][CTF]), so nesting order does not matter: `(Party_A) & (BTC_UP)` = `(BTC_UP) & (Party_A)`.

When `parent_collection_id` is non-zero, the collateral side (`"*"`) is the parent collection's conditional keyset rather than a regular keyset, for both convert and [NUT-CTF][CTF] redemption. See [supplementary material](suppl/CTF-split-merge.md) for a full combinatorial example.

## Error Codes

| Code  | Description                                  |
| ----- | -------------------------------------------- |
| 11007 | Duplicate inputs provided                    |
| 12001 | Keyset is not known                          |
| 12002 | Keyset is inactive                           |
| 13021 | Condition not found                          |
| 13041 | Convert payoff/fee violation                 |
| 13042 | Convert not permitted for this condition     |
| 13043 | Full-set or single-element partition         |

## Mint Info Setting

The [NUT-06][06] `MintMethodSetting`:

```json
{
  "CTF-split-merge": {
    "supported": true,
    "max_depth": <int>
  }
}
```

- `supported`: Boolean indicating support for the convert operation.
- `max_depth` (optional): Maximum nesting depth. If unspecified, only root conditions (depth 1) are supported.

For a complete end-to-end example including registration, convert, trading, and redemption, see the [supplementary material](suppl/CTF-split-merge.md).

[00]: 00.md
[01]: 01.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[07]: 07.md
[08]: 08.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[14]: 14.md
[21]: 21.md
[22]: 22.md
[CTF]: CTF.md
[CTF-numeric]: CTF-numeric.md
