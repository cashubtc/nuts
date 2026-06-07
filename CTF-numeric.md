# NUT-CTF-numeric: Numeric Outcome Conditions

`optional`

`depends on: NUT-CTF, NUT-CTF-split-merge`

---

This NUT defines numeric outcome conditions where the oracle attests to a numeric value (e.g., BTC/USD price) rather than an enumerated outcome. The condition has two outcome collections — **HI** and **LO** — representing the high and low ends of a range. Both HI and LO token holders receive **proportional** redemption based on the attested value's position within the range.

This follows the [Gnosis CTF scalar condition model](https://conditional-tokens.readthedocs.io/en/latest/) ([contracts](https://github.com/gnosis/conditional-tokens-contracts)) and uses [DLC digit-decomposition oracle attestation](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md) for interoperability.

## HI/LO Conditions

A numeric condition has exactly 2 outcome collections:

- **LO**: Represents the low end of the range. LO holders profit when the attested value is near or below `lo_bound`.
- **HI**: Represents the high end of the range. HI holders profit when the attested value is near or above `hi_bound`.

The outcome collection keysets are always `["HI", "LO"]` for numeric conditions.

## Payout Calculation

Given range `[lo_bound, hi_bound]` and attested value `V`:

```
clamped_V = clamp(V, lo_bound, hi_bound)
hi_payout_ratio = (clamped_V - lo_bound) / (hi_bound - lo_bound)
lo_payout_ratio = 1 - hi_payout_ratio
```

For a face value of `amount`:

- HI holder redeems: `floor(amount * hi_payout_ratio)`
- LO holder redeems: `amount - floor(amount * hi_payout_ratio)` (ensures no rounding loss)

**Edge cases**:

- `V <= lo_bound`: LO gets 100%, HI gets 0%
- `V >= hi_bound`: HI gets 100%, LO gets 0%

### Example

Range `[0, 100000]`, attested value `V = 20000`:

```
hi_payout_ratio = (20000 - 0) / (100000 - 0) = 0.2
lo_payout_ratio = 1 - 0.2 = 0.8
```

For 100 sats face value:

- HI: `floor(100 * 0.2)` = 20 sats
- LO: `100 - 20` = 80 sats

## Condition Registration

Numeric conditions are registered via the same `POST /v1/conditions` endpoint ([NUT-CTF][CTF]) with additional fields:

### Request Body

**Request** of `Alice`:

```http
POST https://mint.host:3338/v1/conditions
```

```json
{
  "threshold": 1,
  "tags": [["description", "BTC/USD price on 2025-07-01"]],
  "announcements": [
    "<hex-encoded TLV with digit_decomposition_event_descriptor>"
  ],
  "condition_type": "numeric",
  "lo_bound": 0,
  "hi_bound": 100000,
  "precision": 0,
  "collateral": "sat"
}
```

```bash
curl -X POST https://mint.host:3338/v1/conditions \
  -H "Content-Type: application/json" \
  -d '{"threshold":1,"tags":[["description","BTC/USD price"]],"announcements":["fdd824..."],"condition_type":"numeric","lo_bound":0,"hi_bound":100000,"precision":0,"collateral":"sat"}'
```

- `condition_type`: `"numeric"` (vs default `"enum"` for existing [NUT-CTF][CTF] conditions). When omitted, defaults to `"enum"`.
- `lo_bound`: Lower bound of the range (integer)
- `hi_bound`: Upper bound of the range (integer, MUST be > `lo_bound`)
- `precision`: Base-10 exponent for the oracle's digit decomposition (from the DLC event descriptor). A precision of `n` means the oracle's attested digits represent a value multiplied by `10^n`. For example, precision `0` means the digits represent the value directly, precision `-2` means the digits represent cents (divide by 100).

**Response** of `Bob`:

```json
{
  "condition_id": <hex_str>
}
```

The mint always creates the `HI` and `LO` keysets during numeric condition registration. If `default_keyset_creation` is `"none"`, a client MAY provide `outcome_collections` exactly as `["HI", "LO"]`; any other collection is invalid. If the mint advertises `"one-vs-rest"` or `"all"`, the client MUST omit `outcome_collections`. In all cases, `collateral` is required because numeric registration creates keysets.

## Condition ID for Numeric Conditions

Numeric conditions extend the [NUT-CTF][CTF] condition ID formula by appending market-specific parameters:

```
condition_id = tagged_hash("Cashu_condition_id",
  sorted_oracle_pubkeys || event_id || outcome_count
  || 0x01 || lo_bound_i64be || hi_bound_i64be || precision_i32be)
```

Where:

- The first three components are identical to [NUT-CTF][CTF]
- `0x01`: 1-byte market type indicator (`0x01` = numeric). Enum markets ([NUT-CTF][CTF]) do NOT append this byte, preserving backward compatibility.
- `lo_bound_i64be`: `lo_bound` encoded as 8-byte big-endian signed integer
- `hi_bound_i64be`: `hi_bound` encoded as 8-byte big-endian signed integer
- `precision_i32be`: `precision` encoded as 4-byte big-endian signed integer

`outcome_count` = 2 (always). The outcome collection keysets are always `["HI", "LO"]`.

## Oracle Witness for Digit Decomposition

The oracle signs individual digits per the [DLC specification](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md). The witness format extends [NUT-CTF][CTF]:

```json
{
  "oracle_sigs": [
    {
      "oracle_pubkey": <hex_str>,
      "digit_sigs": <Array[str]>
    }
  ]
}
```

- `digit_sigs`: Array of 64-byte Schnorr signatures (128-char hex strings), one per digit, in left-to-right order (most significant digit first). Each signature is on the digit's UTF-8 string representation (e.g., `"2"` for digit value 2) using the corresponding R-value (nonce point) from the oracle announcement.
- For signed numbers: the first element is a signature on `"+"` or `"-"`

The witness uses `digit_sigs` (array of per-digit signatures) instead of `oracle_sig` (single signature) used in [NUT-CTF][CTF] enum conditions. The mint identifies which format to expect based on the `condition_type` of the condition referenced by the input keyset.

### Verification

The mint:

1. Extracts the digit values from `digit_sigs` by verifying each signature against the corresponding R-value from the oracle announcement
2. Reconstructs the numeric value from the digit values (accounting for sign and `precision`)
3. Clamps the value to `[lo_bound, hi_bound]`
4. Computes the payout ratio

## Redemption

Both HI and LO holders can redeem at `POST /v1/redeem_outcome` ([NUT-CTF][CTF]). Unlike enum conditions where only the winning outcome collection can redeem, in numeric conditions **both outcomes can redeem** with proportional amounts.

### HI Holder Redemption

Given attested value `V = 20000`, range `[0, 100000]`:

- Input: 100 sats of HI tokens + digit witness
- Payout ratio: `(20000 - 0) / (100000 - 0)` = 0.2
- Output: `floor(100 * 0.2)` = 20 sats regular ecash
- Remaining 80 sats are not issued (HI holder's loss)

### LO Holder Redemption

Same attestation, same range:

- Input: 100 sats of LO tokens + digit witness
- Payout ratio: `1 - 0.2` = 0.8
- Output: `100 - floor(100 * 0.2)` = 80 sats regular ecash

### Conservation

The mint MUST ensure that for a given face `amount`, total HI redemption + total LO redemption = `amount` (minus fees). The `amount - floor(amount * hi_payout_ratio)` formula for LO guarantees this by avoiding independent rounding.

## Convert (Split and Merge)

The [NUT-CTF-split-merge][CTF-split-merge] `convert` operation applies to numeric conditions. For canonicalisation, a numeric condition's outcome-atom set is the fixed synthetic order `Ω = ["HI", "LO"]`, independent of the digit-decomposition oracle fields. The only outcome collections are the two single atoms `HI` and `LO`; the full set `HI|LO` is the collateral/forbidden full-set and is never a conditional keyset. Convert on a numeric condition therefore reduces to:

- **Split**: Deposit collateral, receive equal amounts of HI and LO tokens (`outputs {"HI": ..., "LO": ...}`)
- **Merge**: Surrender equal amounts of HI and LO tokens, receive collateral back (`outputs {"*": ...}`)

Exact-equality conservation preserves the HI/LO face vector, so the proportional redemption above is unaffected. No other special handling is needed.

## Combinatorial Markets

Numeric conditions can participate in root-level [NUT-CTF-split-merge][CTF-split-merge] convert operations. Nested/combinatorial construction is out of scope for this version.

## Error Codes

| Code  | Description                                  |
| ----- | -------------------------------------------- |
| 13030 | Invalid numeric range (lo_bound >= hi_bound) |
| 13031 | Digit signature verification failed          |
| 13032 | Attested value outside representable range   |
| 13033 | Payout calculation overflow                  |

## Mint Info Setting

The [NUT-06][06] `MintMethodSetting` indicates support for this feature:

```json
{
  "CTF-numeric": {
    "supported": true,
    "max_digits": <int>
  }
}
```

- `supported`: Boolean indicating NUT-CTF-numeric support
- `max_digits`: Maximum number of oracle digits the mint supports (e.g., 20). Mints SHOULD reject condition registrations where the oracle announcement specifies more digits than `max_digits`.

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
[CTF]: CTF.md
[CTF-split-merge]: CTF-split-merge.md
