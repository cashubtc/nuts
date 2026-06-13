# NUT-CTF: Conditional Token Framework

`optional`

`depends on: NUT-02, NUT-06`

---

This NUT defines conditional tokens and conditional keysets for oracle-attested events.

A **conditional token** is a regular Cashu token ([NUT-00][00]) signed under a conditional keyset. It can be transferred and swapped like any other Cashu token, with one additional ability: it can be redeemed for regular ecash via `POST /v1/redeem_outcome` by providing a DLC oracle's attestation signature as a witness.

A **conditional keyset** is a per-outcome-collection signing keyset ([NUT-02][02]) that the mint creates during condition registration. Each outcome collection gets a unique keyset with different signing keys.

The oracle signature scheme is compatible with the [DLC specification](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md), allowing Cashu mints to leverage existing DLC oracle infrastructure.

Caution: Applications that rely on oracle resolution must verify that the oracle is trustworthy and check via the mint's [info][06] endpoint that NUT-CTF is supported.

**Related specifications:** [NUT-CTF-split-merge][CTF-split-merge] defines the `convert` operation — payoff-preserving rebalancing of conditional positions (split, merge, recombine, and conversion). [NUT-CTF-numeric][CTF-numeric] extends this framework with numeric outcome conditions.

## Terminology

- **Condition**: A question with defined outcomes, resolved by an oracle. Identified by a `condition_id`. Equivalent to "condition" in the [Gnosis Conditional Token Framework](https://conditional-tokens.readthedocs.io/en/latest/) ([contracts](https://github.com/gnosis/conditional-tokens-contracts)), which this spec adapts to Cashu. [Polymarket](https://github.com/Polymarket/ctf-exchange-v2) is a large-scale production deployment of the same model on Ethereum.
- **Outcome**: A single atomic result that an oracle attests to (e.g., `"YES"`, `"ALICE"`).
- **Outcome collection**: A non-empty, non-full subset of outcomes (e.g., `"YES"`, `"ALICE|BOB"`). Each requested collection gets its own conditional keyset. Redeemable if the oracle attests to ANY outcome it contains.
- **Condition ID** (`condition_id`): 32-byte tagged hash uniquely identifying a condition. Partition-independent. See [Condition ID](#condition-id).
- **Outcome collection ID** (`outcome_collection_id`): 32-byte x-only public key uniquely identifying an outcome collection within a condition. See [Outcome Collection ID](#outcome-collection-id).

## Outcome Collections

Outcome collections allow tokens to represent one or more outcomes. An outcome collection is either a single outcome or an OR-combination joined by `|` (e.g., `"ALICE|BOB"` = "Alice or Bob wins"). If an outcome name contains `|`, it MUST be escaped as `\|`; a literal `\` is escaped as `\\`. The token `"*"` is reserved (it denotes collateral in [NUT-CTF-split-merge][CTF-split-merge]) and is invalid as an outcome name and as an outcome collection string.

Outcome collection strings have a single canonical form so that, e.g., `ALICE|BOB` and `BOB|ALICE` derive the same keyset: outcome names are NFC-normalised and components are ordered by the outcome's index in the oracle announcement (for numeric conditions, the fixed order `["HI", "LO"]`). See [NUT-CTF-split-merge][CTF-split-merge] for the full encoding rules.

### Outcome Collection Keyset Rules

Condition registration MAY request any set of non-empty, non-full outcome collections:

1. Each requested outcome collection MUST be canonical.
2. Requested outcome collections MAY overlap.
3. Duplicate canonical outcome collections in one request MUST be rejected.
4. No single outcome collection may cover all outcomes (error 13043). The full-outcome-set payoff vector is represented only as collateral, never as a conditional keyset — this keeps the reserved collateral key `"*"` unambiguous in [NUT-CTF-split-merge][CTF-split-merge].

Valid requested keysets for outcomes `["A", "B", "C"]`:

- `["A", "B", "C"]` (individual outcomes)
- `["A", "B", "C", "A|B", "B|C", "A|C"]` (all non-full collections)

Invalid: `["A|B|C"]` (full-set), `["A", "A"]` (duplicate), `["A", "D"]` (unknown outcome).

## Conditional Keysets

Each requested outcome collection gets a unique keyset created during [condition registration](#register-condition). These use the same mechanism as regular keysets ([NUT-02][02]).

**Properties:**

- **Signing keys**: Unique keys derived by the mint from condition parameters
- **Unit**: Matches the collateral unit (e.g., `"sat"`)
- **Discovery**: Via `GET /v1/conditional_keysets` (see [Conditional Keyset Discovery](#conditional-keyset-discovery))
- **Active flag**: `true` during condition lifetime, `false` after resolution + vesting period
- **Expiry**: MAY use `final_expiry` corresponding to vesting period end

### Keyset ID Derivation

Conditional keyset IDs extend [NUT-02 V2 derivation][02] by appending condition-specific data:

```
<NUT-02 V2 base preimage> + "|condition_id:" + condition_id_hex + "|outcome_collection_id:" + outcome_collection_id_hex
```

The version byte remains `01`. In Python:

```python
keyset_id_bytes += f"|condition_id:{condition_id}".encode("utf-8")
keyset_id_bytes += f"|outcome_collection_id:{outcome_collection_id}".encode("utf-8")
```

Where `condition_id` and `outcome_collection_id` are 64-character hex strings. This binding allows wallets to independently verify a keyset's condition and outcome collection. See [supplementary material](suppl/CTF.md#keyset-id-derivation-rationale) for rationale.

## Token Lifecycle

```
Issuance:   Mint issues conditional tokens (via condition registration + keyset-specific minting)
Trading:    Conditional keyset -> same/rotated conditional keyset (NUT-03 swap, same outcome_collection_id, no witness)
Redemption: Conditional keyset -> regular keyset  (POST /v1/redeem_outcome + oracle witness)
```

- **Issuance**: The mint creates conditional keysets during [condition registration](#register-condition). Users obtain conditional tokens through [NUT-CTF-split-merge][CTF-split-merge] convert (split) operations or other minting mechanisms. Every conditional token, by any issuance path, MUST be backed by locked collateral at least equal to its face amount; sub-face or market-priced issuance into a conditional keyset is forbidden (see [NUT-CTF-split-merge][CTF-split-merge] Issuance Invariant).
- **Trading**: Standard [NUT-03][03] swap. All conditional keysets in a swap MUST share the same `outcome_collection_id`. No oracle witness required.
- **Redemption**: After oracle attestation, winners submit tokens to `POST /v1/redeem_outcome` with oracle signatures in `Proof.witness`.

## Condition ID

A condition is uniquely identified by a `condition_id` using a BIP-340 tagged hash:

```
condition_id = tagged_hash("Cashu_condition_id", sorted_oracle_pubkeys || event_id || outcome_count)
```

Where:

- `tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)` — [BIP-340 tagged hash](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki)
- `sorted_oracle_pubkeys`: 32-byte x-only public keys, sorted lexicographically, concatenated. Derived from `announcements[].oracle_public_key`.
- `event_id`: UTF-8 encoded event identifier. Derived from `announcements[0].oracle_event.event_id`. All announcements MUST share the same `event_id`.
- `outcome_count`: 1-byte unsigned integer. Derived from `len(announcements[0].oracle_event.event_descriptor.outcomes)`. All announcements MUST share the same ordered outcome list; that order (from `announcements[0]`) is the canonical outcome index used by outcome-collection encoding.

The `condition_id` is independent of requested keysets — the same oracle event always produces the same ID regardless of which outcome collections are requested.

> **Note:** [NUT-CTF-numeric][CTF-numeric] extends this formula with additional parameters for numeric conditions.

## Oracle Announcement Format

Oracle announcements MUST use the TLV format defined in the [DLC specification](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Messaging.md#the-oracle_announcement-type) (`oracle_announcement`, TLV type 55332). In API bodies, announcements are hex-encoded TLV byte strings.

## Oracle Communication

Oracle announcements and attestations use the [DLC specification](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md) format:

- **Signing algorithm**: BIP 340 Schnorr signatures with tagged hash `"DLC/oracle/attestation/v0"`
- **Announcement format**: [DLC oracle announcement](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Messaging.md#the-oracle_announcement-type) (TLV type 55332)
- **Event descriptors**: Enum event descriptors with UTF-8 NFC-normalized outcome strings

The transport for discovering oracle announcements from oracles is unspecified. [NIP-88](https://github.com/nostr-protocol/nips/pull/1681) is one option. See [supplementary material](suppl/CTF.md#oracle-communication-notes) for additional notes.

## Condition Registry

Conditions are registered via `POST /v1/conditions` before any operations on conditional tokens. Conditional keysets are created during condition registration.

### Condition Info

```json
{
  "condition_id": <hex_str>,
  "threshold": <int>,
  "tags": <Array[Array[str]]>,
  "announcements": <Array[hex_str]>,
  "collateral": <str>,
  "registered_at": <int>,
  "keysets": {
    "<outcome_collection>": <hex_str>,
    ...
  },
  "attestation": {
    "status": <str>,
    "winning_outcome": <str>,
    "attested_at": <int>
  }
}
```

- `condition_id`: 64-character hex string (see [Condition ID](#condition-id))
- `threshold`: Minimum oracles required for attestation (default: 1)
- `tags`: [NIP-88][NIP-88] tag array (e.g., `[["description", "..."], ["n", "BTC"]]`). Display-only metadata; does NOT affect `condition_id`.
- `announcements`: Hex-encoded oracle announcement TLV bytes
- `collateral` (optional): Condition's collateral currency unit, echoing the value accepted during registration. Clients use this to verify unit consistency before building markets on a condition.
- `registered_at`: Unix timestamp of registration
- `keysets`: Flat map of all root-level requested outcome collections to keyset IDs. Use `GET /v1/conditional_keysets` for full keyset metadata.
- `attestation` (optional, omitted if no attestation):
  - `status`: `"pending"` | `"attested"` | `"expired"` | `"violation"`
  - `winning_outcome`: Attested outcome string (`null` if pending)
  - `attested_at`: Unix timestamp (`null` if pending)

### Get Conditions

```http
GET https://mint.host:3338/v1/conditions
```

**Query parameters:**

- `since` (optional): Unix timestamp. Returns conditions with `registered_at >= since`. Wallets SHOULD first fetch all, then use `since` for incremental sync.
- `limit` (optional): Maximum conditions per response.
- `status` (optional, repeatable): Filter by `attestation.status`. E.g., `?status=pending&status=attested`. Conditions without `attestation` are treated as `pending`.

Mints MUST return results ordered by `registered_at` ascending. Clients paginate by setting `since` to the last `registered_at` received and MUST deduplicate by `condition_id`. See [supplementary material](suppl/CTF.md#qa-design-decisions) for pagination rationale.

**Response** of `Bob`:

```json
{
  "conditions": <Array[ConditionInfo]>
}
```

```bash
curl -X GET https://mint.host:3338/v1/conditions?status=pending&status=attested&limit=50
```

### Get Condition

```http
GET https://mint.host:3338/v1/conditions/{condition_id}
```

**Response** of `Bob`:

```json
{
  "condition": <ConditionInfo>
}
```

### Register Condition

```http
POST https://mint.host:3338/v1/conditions
```

Registers a new condition and creates requested conditional keysets.

**Request** of `Alice`:

```json
{
  "threshold": <int>,
  "tags": <Array[Array[str]]>,
  "announcements": <Array[hex_str]>,
  "collateral": <str>,
  "outcome_collections": <Array[str]>,
  "fee": <Array[Proof]>,
  "outputs": <Array[BlindedMessage]>
}
```

- `threshold`: Minimum oracles required (default: 1)
- `tags`: [NIP-88][NIP-88] tag array
- `announcements`: Hex-encoded oracle announcement TLV bytes
- `collateral`: Unit string for root conditions (e.g., `"sat"`). REQUIRED if `outcome_collections` is present or if the mint's default keyset creation rule creates keysets.
- `outcome_collections` (optional): Canonical outcome collections to create keysets for. If omitted, the mint applies its `default_keyset_creation` policy. If the mint advertises `default_keyset_creation` as `"one-vs-rest"` or `"all"`, clients MUST omit this field and the mint MUST reject client-defined collections.
- `fee` (optional): Anti-spam registration fee inputs paid as `Proof` objects. The proofs MUST be from a **regular** keyset ([NUT-02][02]) whose unit equals `collateral`; conditional-keyset proofs MUST be rejected (error 13017). REQUIRED when the mint advertises a non-zero registration fee (see [Mint Info Setting](#mint-info-setting)); MAY be omitted when the advertised fee is `0`. The mint retains exactly `required_fee` as revenue and returns any excess as regular ecash change using `outputs` / `change` as described in [Registration Fee](#registration-fee).
- `outputs` (optional): Blank `BlindedMessage` objects for returning excess fee input as regular ecash change, following the [NUT-08][08] blank-output model. The `amount` field in these messages is ignored by the mint and MAY be set to any valid placeholder amount by the client. Outputs MUST use a regular keyset whose unit equals `collateral`; conditional-keyset outputs MUST be rejected (error 13017). Clients SHOULD provide enough blank outputs to represent the maximum possible change from the selected `fee` proofs.

**Response** of `Bob`:

```json
{
  "condition_id": <hex_str>,
  "keysets": {
    "<outcome_collection_1>": <hex_str>,
    "<outcome_collection_2>": <hex_str>,
    ...
  },
  "change": <Array[BlindSignature]>
}
```

```bash
curl -X POST https://mint.host:3338/v1/conditions \
  -H "Content-Type: application/json" \
  -d '{"threshold":1,"tags":[["description","Will BTC reach $100k?"]],"announcements":["fdd824fd..."],"collateral":"sat","outcome_collections":["YES","NO"]}'
```

#### Mint Behavior

1. Parses and verifies announcement signatures (error 13011 if failed)
2. Computes `condition_id`
3. Determines requested keysets:
   - If `outcome_collections` is provided and `default_keyset_creation` is `"none"`: canonicalizes and validates the requested collections.
   - If `outcome_collections` is provided and `default_keyset_creation` is `"one-vs-rest"` or `"all"`: rejects the request.
   - If omitted: applies `default_keyset_creation`.
4. If condition exists with matching config and requested keyset set: returns existing `condition_id` and keysets (idempotent). The mint MUST NOT charge the registration fee on this path — see [Registration Fee](#registration-fee).
5. If condition exists with different config or requested keyset set: error 13028
6. If new: charges the registration fee (if any), stores the condition, creates keysets, and returns `condition_id`, `keysets`, and any fee `change` — all in a single atomic transaction (see [Registration Fee](#registration-fee))

The mint MUST make condition registration idempotent. Mints MAY charge a [registration fee](#registration-fee) and/or require [NUT-21][21] or [NUT-22][22] authentication for DoS prevention.

### Registration Fee

To bound condition-registration spam, a mint MAY charge a fee per new condition, advertised via [Mint Info Setting](#mint-info-setting). The required amount, denominated in the `collateral` unit, is:

```
required_fee = registration_fee_base + registration_fee_per_keyset * num_keysets
```

where `num_keysets` is the number of conditional keysets this registration creates (after step 3 above). When `registration_fee_base` and `registration_fee_per_keyset` are both `0`, registration is free and the `fee` field MAY be omitted.

The registration fee is mint-authoritative: the mint computes `num_keysets` after canonicalization, validation, default policy expansion, duplicate removal, and full-set exclusion. Clients MUST NOT rely on a locally computed keyset count as the payment authority.

No additional [NUT-02][02] `input_fee_ppk` is charged on `fee` proofs for condition registration; `required_fee` is the sole amount retained by the mint. When `required_fee == 0`, the mint MUST NOT consume any `fee` proofs and MUST NOT sign `outputs` as fee change.

When `required_fee > 0`, the mint MUST, for a **new** condition only:

1. Require the `fee` field. Each `Proof` MUST be valid, unspent, from a regular keyset whose unit equals `collateral` (error 13017 for a conditional/wrong-unit keyset), and the sum of `fee` proof amounts MUST be at least `required_fee` (error 13044 otherwise).
2. Compute `change_amount = sum(fee) - required_fee`.
3. If `change_amount > 0`, require `outputs` with enough blank messages to return the exact change amount as regular ecash. The mint decomposes `change_amount` into amounts supported by the output keyset, assigns those amounts to the blank outputs, signs them, and returns the resulting positive-value `BlindSignature`s in `change`. The returned `change` signatures MUST preserve the order of the blank outputs they correspond to and MUST omit zero-value outputs, matching [NUT-08][08]. If exact change cannot be returned from the provided outputs, the mint MUST reject the request (error 13047) and MUST NOT consume the fee proofs.
4. Atomically, in a single transaction: mark the `fee` proofs spent, store the condition, and create the keysets. If any step fails, none are applied — a failed registration MUST NOT consume the fee.

The response for a new paid registration MUST include `change` when `change_amount > 0`, and MAY omit `change` or return an empty array when `change_amount == 0`.

The mint MUST compute `required_fee` and verify the fee **after** the idempotency check (Mint Behavior step 4). A repeated registration that resolves to an existing condition MUST return the existing `condition_id` and `keysets` without charging again and without returning `change`; clients keep their unspent `fee` proofs and discard unused blank outputs. This prevents a client retry from double-charging or failing because retry proofs were already spent. The registration fee is mint revenue and is independent of condition collateral and the [NUT-CTF-split-merge][CTF-split-merge] solvency invariant. Fee change is regular ecash and is not condition collateral.

## Outcome Collection ID

Each outcome collection has a unique `outcome_collection_id` derived from the condition ID and outcome collection string. The result is a 32-byte x-only public key on secp256k1.

### Computation

```
outcome_collection_id(condition_id, outcome_collection_string):
  1. h = tagged_hash("Cashu_outcome_collection_id", condition_id || outcome_collection_string_bytes)
  2. P = hash_to_curve(h)
  3. Return x_only(P)
```

Where:

- `tagged_hash`: BIP-340 tagged hash
- `hash_to_curve`: Same approach as [NUT-00][00]'s `hash_to_curve` with domain separation via tagged hash input
- `x_only`: Per [BIP-340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki)

This version defines root-level outcome collections only. Combinatorial/nested condition construction is intentionally out of scope until the registration API includes an explicit way to create parent-scoped keysets.

## Conditional Keyset Discovery

Conditional keysets are served on a dedicated endpoint, separate from `GET /v1/keysets` ([NUT-02][02]). This ensures backward compatibility and prevents conditional keysets from inflating the regular listing.

```http
GET https://mint.host:3338/v1/conditional_keysets
```

**Query parameters:**

- `since` (optional): Unix timestamp. Returns keysets with `registered_at >= since`.
- `limit` (optional): Maximum keysets per response.
- `active` (optional): Boolean filter on `active` flag.

Mints MUST return results ordered by `registered_at` ascending. Same pagination approach as `GET /v1/conditions`.

**Response** of `Bob`:

Structurally identical to `GET /v1/keysets` ([NUT-02][02]) with four additional fields:

```json
{
  "keysets": [
    {
      "id": <hex_str>,
      "unit": <str>,
      "active": <bool>,
      "input_fee_ppk": <int>,
      "final_expiry": <int>,
      "condition_id": <hex_str>,
      "outcome_collection": <str>,
      "outcome_collection_id": <hex_str>,
      "registered_at": <int>
    }
  ]
}
```

```bash
curl -X GET https://mint.host:3338/v1/conditional_keysets?active=true
```

The standard `GET /v1/keys/{keyset_id}` ([NUT-02][02]) still works for fetching public keys of a specific conditional keyset.

## Redemption Witness

When redeeming via `POST /v1/redeem_outcome`, each input `Proof` MUST include a `witness` with oracle attestation:

```json
{
  "oracle_sigs": [
    {
      "oracle_pubkey": <hex_str>,
      "oracle_sig": <hex_str>
    }
  ]
}
```

- `oracle_sigs`: Array with at least `threshold` entries from distinct oracles
  - `oracle_pubkey`: 32-byte x-only key (64-char hex)
  - `oracle_sig`: 64-byte Schnorr signature (128-char hex) on the winning outcome

Always use the array format, even for single-oracle markets (threshold=1).

See [supplementary material](suppl/CTF.md#redemption-witness-comparison) for comparison with existing Cashu witness types.

## Redemption Endpoint

```http
POST https://mint.host:3338/v1/redeem_outcome
```

**Request** of `Alice`:

```json
{
  "inputs": <Array[Proof]>,
  "outputs": <Array[BlindedMessage]>
}
```

- `inputs`: `Proof` objects from a **single conditional keyset**, each with `witness` containing oracle attestation
- `outputs`: `BlindedMessage` objects (same unit). Outputs use a **regular keyset**.

`Alice` MAY omit `oracle_sigs` if `Bob` has already recorded a valid attestation for this outcome collection (check via `GET /v1/conditions/{condition_id}`).

**Response** of `Bob`:

```json
{
  "signatures": <Array[BlindSignature]>
}
```

```bash
curl -X POST https://mint.host:3338/v1/redeem_outcome \
  -H "Content-Type: application/json" \
  -d '{"inputs":[...],"outputs":[...]}'
```

### Consequence for NUT-03

Mints implementing NUT-CTF MUST enforce these rules on [NUT-03][03] swap:

- Swaps within the same conditional keyset: **allowed** (trading)
- Swaps within regular keysets (including cross-keyset): **allowed**
- Swaps where all inputs and outputs share the same `outcome_collection_id`: **allowed** (key rotation)
- Swaps spanning different `outcome_collection_id` values: **MUST reject**
- Swaps mixing conditional and regular keysets: **MUST reject**

All conditional-to-regular conversions go through `POST /v1/redeem_outcome`. Movement of value **across** outcome collections within a condition (regrouping, or crossing the collateral boundary) goes through the payoff-preserving `POST /v1/ctf/convert` operation ([NUT-CTF-split-merge][CTF-split-merge]), never a NUT-03 swap.

## Redemption Verification

When `Bob` receives a `POST /v1/redeem_outcome` request:

1. All inputs MUST use the same conditional keyset
2. All outputs MUST use a regular keyset with the same unit
3. If `Bob` already has a valid attestation for this outcome collection, MAY skip steps 4-5
4. Each input MUST include valid `witness` with `oracle_sigs`
5. Verify at least `threshold` signatures from distinct oracles using [DLC signing algorithm](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md#signing-algorithm) with tagged hash `"DLC/oracle/attestation/v0"` and UTF-8 NFC-normalized outcome string
6. Verify this outcome collection contains the attested atomic outcome

### Attestation Handling

The mint MUST persistently record the first valid attestation (atomic winning outcome + timestamp) for each condition. This record MUST survive restarts.

The mint MUST NOT process redemptions for non-winning keysets. If a valid signature for a different outcome is received (a DLC protocol violation), the mint MUST reject it and MUST log the conflict. Mints SHOULD expose violations via condition info.

## Vesting Period

The mint MAY deactivate conditional keysets after a vesting period following event maturity.

- Vesting period SHOULD be at least 30 days after `event_maturity_epoch`
- Mints MUST communicate vesting period via [Mint Info Setting](#mint-info-setting)
- After expiry: keyset `active` set to `false`; mint MAY refuse redemptions and delete event data
- Wallets SHOULD prominently display the deadline and alert users as it approaches

### Oracle Non-Attestation

If the oracle does not attest within expected time, the mint MAY refund conditional tokens to regular ecash at its discretion.

## Error Codes

| Code  | Description                                                 |
| ----- | ----------------------------------------------------------- |
| 13010 | Invalid oracle signature                                    |
| 13011 | Oracle announcement verification failed                     |
| 13014 | Conditional keyset requires oracle witness                  |
| 13015 | Oracle has not attested to this outcome collection          |
| 13016 | Conditional keyset swap spans different outcome collections |
| 13017 | Invalid keyset for collateral/output side                   |
| 13020 | Invalid condition ID                                        |
| 13021 | Condition not found                                         |
| 13027 | Oracle threshold not met                                    |
| 13028 | Condition already exists                                    |
| 13037 | Duplicate canonical outcome collection                      |
| 13038 | Unknown outcome in outcome collection                       |
| 13043 | Full-set or reserved outcome collection                     |
| 13044 | Missing or insufficient registration fee                    |
| 13045 | Hash to curve failed                                        |
| 13046 | EC point operation failed                                   |
| 13047 | Insufficient or invalid change outputs                      |

## Mint Info Setting

The [NUT-06][06] `MintMethodSetting` indicates support for this feature:

```json
{
  "CTF": {
    "supported": true,
    "dlc_version": <str>,
    "vesting_period": <int>,
    "default_keyset_creation": <str>,
    "registration_fee_base": <int>,
    "registration_fee_per_keyset": <int>
  }
}
```

- `supported`: Boolean indicating NUT-CTF support
- `vesting_period` (optional): Seconds after `event_maturity_epoch` for redemption. Default: 30 days (2592000). `0` = no expiry.
- `dlc_version`: DLC protocol version (currently `"0"`)
- `default_keyset_creation`: `"none"` (default), `"one-vs-rest"`, or `"all"`.
  - `"none"`: omitted `outcome_collections` creates no enum keysets; clients MAY request explicit non-full enum collections.
  - `"one-vs-rest"`: omitted `outcome_collections` creates each atomic outcome and its complement, deduplicated for binary conditions; clients MUST NOT request explicit collections.
  - `"all"`: omitted `outcome_collections` creates every non-empty, non-full collection subject to mint limits; clients MUST NOT request explicit collections.
  - Numeric conditions always create `HI` and `LO` keysets at registration, regardless of this policy.
- `registration_fee_base` (optional): Flat anti-spam fee charged per new condition, in the smallest unit of the condition's `collateral`. Default: `0` (free). See [Registration Fee](#registration-fee).
- `registration_fee_per_keyset` (optional): Additional fee charged per conditional keyset the registration creates, in the smallest unit of the condition's `collateral`. Default: `0`. The total required fee is `registration_fee_base + registration_fee_per_keyset * num_keysets`.

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
[CTF-split-merge]: CTF-split-merge.md
[CTF-numeric]: CTF-numeric.md
[NIP-88]: https://github.com/nostr-protocol/nips/pull/1681
