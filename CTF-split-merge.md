# NUT-CTF-split-merge: Conditional Token Split and Merge

`optional`

`depends on: NUT-CTF`

---

This NUT defines split and merge operations for conditional tokens ([NUT-CTF][CTF]). Users can deposit collateral to receive complete sets of conditional tokens (split), or surrender complete sets to recover collateral (merge). Inspired by the [Gnosis Conditional Token Framework](https://docs.gnosis.io/conditionaltokens/).

Caution: Applications must verify that the mint supports both NUT-CTF and NUT-CTF-split-merge via the [info][06] endpoint.

## Overview

```
           Register            Split                    Trade                 Attest              Redeem
Wallet ────────────► Mint   User ──────────────► Conditional ◄────────────►  Oracle ────────►    Winner ──────────►
       cond. info    creates     100 sats        Tokens         NUT-03       Signs              redeem_outcome
                     keysets                      (YES+NO        Swap         Outcome            → Regular
                                                  keysets)                                       Keyset
```

1. **Register**: Condition + partition registered via [NUT-CTF][CTF] to create conditional keysets
2. **Split**: `Alice` deposits collateral, receives complete set of conditional tokens
3. **Trade**: Standard [NUT-03][03] swaps within same conditional keyset
4. **Attest**: Oracle signs winning outcome
5. **Redeem**: Winners use `POST /v1/redeem_outcome` ([NUT-CTF][CTF])

## Split Operation

Deposits collateral and returns a complete set of conditional tokens. For every unit deposited, `Alice` receives one token per outcome collection.

Conditions and partitions must be registered via [NUT-CTF][CTF] before splitting.

```http
POST https://mint.host:3338/v1/ctf/split
```

**Request** of `Alice`:

```json
{
  "condition_id": <hex_str>,
  "inputs": <Array[Proof]>,
  "outputs": {
    "<outcome_collection_1>": <Array[BlindedMessage]>,
    "<outcome_collection_2>": <Array[BlindedMessage]>,
    ...
  }
}
```

- `condition_id`: 64-char hex. Returns error 13021 if unknown.
- `inputs`: `Proof` objects as collateral. Regular keyset for root conditions; parent collection's conditional keyset for nested.
- `outputs`: Object mapping each outcome collection to `BlindedMessage` arrays. Each MUST use the outcome-collection-specific keyset ID from partition registration.

```bash
curl -X POST https://mint.host:3338/v1/ctf/split \
  -H "Content-Type: application/json" \
  -d '{"condition_id":"a1b2c3...","inputs":[...],"outputs":{"YES":[...],"NO":[...]}}'
```

### Output Requirements

1. Output keys MUST form a previously registered partition
2. Each outcome collection's total amount MUST be identical
3. Each `BlindedMessage` MUST use the correct keyset ID
4. `sum(each_outcome_collection_outputs) = sum(inputs) - fees(inputs)` per [NUT-02][02]

**Example** (binary market, 100 sats collateral):

- `inputs`: 100 sats (regular keyset `009a1f293253e41e`)
- `outputs["YES"]`: 100 sats (conditional keyset `00abc123def456`)
- `outputs["NO"]`: 100 sats (conditional keyset `00def789abc012`)

If error 13021 is returned, `Alice` SHOULD register the condition and partition first, then retry.

### Mint Behavior

`Bob`:

1. Looks up condition (error 13021 if not found)
2. Validates output keys form a valid partition (error 13037/13038)
3. Validates keysets exist for all outcome collections (error 12001 if unknown)
4. Validates correct keyset IDs and equal amounts across outcome collections
5. Signs blinded messages

**Response** of `Bob`:

```json
{
  "signatures": {
    "<outcome_collection_1>": <Array[BlindSignature]>,
    "<outcome_collection_2>": <Array[BlindSignature]>,
    ...
  }
}
```

## Merge Operation

Combines a complete set of conditional tokens back into collateral. Inverse of split.

```http
POST https://mint.host:3338/v1/ctf/merge
```

**Request** of `Alice`:

```json
{
  "condition_id": <hex_str>,
  "inputs": {
    "<outcome_collection_1>": <Array[Proof]>,
    "<outcome_collection_2>": <Array[Proof]>,
    ...
  },
  "outputs": <Array[BlindedMessage]>
}
```

- `condition_id`: 64-char hex (error 13021 if unknown)
- `inputs`: Object mapping each outcome collection to `Proof` arrays with correct keyset IDs
- `outputs`: `BlindedMessage` objects for collateral. Regular keyset for root; parent keyset for nested.

```bash
curl -X POST https://mint.host:3338/v1/ctf/merge \
  -H "Content-Type: application/json" \
  -d '{"condition_id":"a1b2c3...","inputs":{"YES":[...],"NO":[...]},"outputs":[...]}'
```

### Input Requirements

1. Input keys MUST form a valid partition
2. Each outcome collection's amount MUST be identical
3. Each `Proof` MUST use the correct keyset ID
4. `sum(outputs) = per_outcome_collection_amount - fees(all_inputs)` per [NUT-02][02]

**Response** of `Bob`:

```json
{
  "signatures": <Array[BlindSignature]>
}
```

### Merge Verification

`Bob` MUST verify: (1) valid conditional keysets for the condition, (2) complete partition, (3) equal amounts, (4) correct output amount. No oracle witness required — the complete set cancels all risk.

## Combinatorial Markets

Conditions can be nested hierarchically. A user could bet on "Party A wins AND BTC > $100k" by splitting Party A tokens into BTC price sub-conditions.

Outcome collection IDs use EC point addition ([NUT-CTF][CTF]), ensuring nesting order does not matter: `(Party_A) & (BTC_UP)` = `(BTC_UP) & (Party_A)`.

When `parent_collection_id` is non-zero:

- **Split inputs**: Parent collection's conditional keyset (not regular)
- **Merge outputs**: Parent collection's conditional keyset
- **Redemption**: Outputs go to parent keyset instead of regular

See [supplementary material](suppl/CTF-split-merge.md) for a full combinatorial market example.

## Security Considerations

- **Atomicity**: Split and merge MUST be atomic — all signatures or none
- **Amount Conservation**: Split always creates ALL outcome collections with equal amounts; merge requires equal amounts of all
- **Depth Limits**: Mints MAY impose maximum nesting depth via [Mint Info Setting](#mint-info-setting)

## Error Codes

| Code  | Description                      |
| ----- | -------------------------------- |
| 13021 | Condition not found              |
| 13022 | Split amount mismatch            |
| 13024 | Condition not active             |
| 13025 | Merge amount mismatch            |
| 13037 | Overlapping outcome collections  |
| 13038 | Incomplete partition             |
| 13040 | Maximum condition depth exceeded |

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

- `supported`: Boolean indicating support
- `max_depth` (optional): Maximum nesting depth. If unspecified, only root conditions (depth 1) are supported.

For a complete end-to-end example including registration, split, trading, and redemption, see the [supplementary material](suppl/CTF-split-merge.md).

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
