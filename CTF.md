# NUT-CTF: Conditional Token Framework

`optional`

`depends on: NUT-02, NUT-06`

---

This NUT defines conditional tokens and conditional keysets for oracle-attested events.

A **conditional token** is a regular Cashu token ([NUT-00][00]) signed under a conditional keyset. It can be transferred and swapped like any other Cashu token, with one additional ability: it can be redeemed for regular ecash via `POST /v1/redeem_outcome` by providing a DLC oracle's attestation signature as a witness.

A **conditional keyset** is a per-outcome-collection signing keyset ([NUT-02][02]) that the mint creates during partition registration. Each outcome collection gets a unique keyset with different signing keys.

The oracle signature scheme is compatible with the [DLC specification](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md), allowing Cashu mints to leverage existing DLC oracle infrastructure.

Caution: Applications that rely on oracle resolution must verify that the oracle is trustworthy and check via the mint's [info][06] endpoint that NUT-CTF is supported.

**Related specifications:** [NUT-CTF-split-merge][CTF-split-merge] defines split/merge operations for creating and dissolving complete sets of conditional tokens. [NUT-CTF-numeric][CTF-numeric] extends this framework with numeric outcome conditions.

## Terminology

- **Condition**: A question with defined outcomes, resolved by an oracle. Identified by a `condition_id`. Equivalent to "condition" in the [Gnosis Conditional Token Framework](https://docs.gnosis.io/conditionaltokens/).
- **Outcome**: A single atomic result that an oracle attests to (e.g., `"YES"`, `"ALICE"`).
- **Outcome collection**: A subset of outcomes, defined by a partition element (e.g., `"YES"`, `"ALICE|BOB"`). Each gets its own conditional keyset. Redeemable if the oracle attests to ANY outcome it contains.
- **Partition**: A division of all outcomes into disjoint, complete outcome collections.
- **Condition ID** (`condition_id`): 32-byte tagged hash uniquely identifying a condition. Partition-independent. See [Condition ID](#condition-id).
- **Outcome collection ID** (`outcome_collection_id`): 32-byte x-only public key uniquely identifying an outcome collection within a condition. See [Outcome Collection ID](#outcome-collection-id).

## Outcome Collections

Outcome collections allow tokens to represent one or more outcomes. An outcome collection is either a single outcome or an OR-combination joined by `|` (e.g., `"ALICE|BOB"` = "Alice or Bob wins"). If an outcome name contains `|`, it MUST be escaped as `\|`.

### Partition Rules

Partition keys MUST form a valid partition of all outcomes:

1. **Disjoint**: No outcome appears in multiple outcome collections
2. **Complete**: Every outcome appears in exactly one outcome collection

Valid partitions for outcomes `["ALICE", "BOB", "CAROL"]`:

- `{"ALICE": [...], "BOB": [...], "CAROL": [...]}` (individual outcomes)
- `{"ALICE|BOB": [...], "CAROL": [...]}` (one collection + one individual)

Invalid: `{"ALICE|BOB": [...], "BOB|CAROL": [...]}` (overlapping), `{"ALICE|BOB": [...]}` (incomplete).

## Conditional Keysets

Each outcome collection gets a unique keyset created during [partition registration](#register-partition). These use the same mechanism as regular keysets ([NUT-02][02]).

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
Issuance:   Mint issues conditional tokens (via partition registration + keyset-specific minting)
Trading:    Conditional keyset -> same/rotated conditional keyset (NUT-03 swap, same outcome_collection_id, no witness)
Redemption: Conditional keyset -> regular keyset                  (POST /v1/redeem_outcome + oracle witness)
```

- **Issuance**: The mint creates conditional keysets during [partition registration](#register-partition). Users obtain conditional tokens through [NUT-CTF-split-merge][CTF-split-merge] split operations or other minting mechanisms.
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
- `outcome_count`: 1-byte unsigned integer. Derived from `len(announcements[0].oracle_event.event_descriptor.outcomes)`.

The `condition_id` is partition-independent — the same oracle event always produces the same ID regardless of partitioning.

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

Conditions are registered via `POST /v1/conditions` before any operations on conditional tokens. Conditional keysets are created during [partition registration](#register-partition).

### Condition Info

```json
{
  "condition_id": <hex_str>,
  "threshold": <int>,
  "tags": <Array[Array[str]]>,
  "announcements": <Array[hex_str]>,
  "registered_at": <int>,
  "keysets": {
    "<outcome_collection>": <hex_str>,
    ...
  },
  "partitions": [
    {
      "partition": <Array[str]>,
      "collateral": <str>,
      "parent_collection_id": <hex_str>,
      "registered_at": <int>
    }
  ],
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
- `registered_at`: Unix timestamp of registration
- `keysets`: Flat map of ALL outcome collections to keyset IDs across all root-level partitions. Shared outcome collections appear once. Nested keysets (non-zero `parent_collection_id`) are not included — use `GET /v1/conditional_keysets`.
- `partitions`: Array of registered partitions:
  - `partition`: Partition keys (e.g., `["YES", "NO"]`)
  - `collateral`: Unit string for root (e.g., `"sat"`), or `outcome_collection_id` hex for nested
  - `parent_collection_id`: 64-char hex; all zeros for root conditions
  - `registered_at`: Unix timestamp
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

Registers a new condition. Does not create keysets — keysets are created during [partition registration](#register-partition).

**Request** of `Alice`:

```json
{
  "threshold": <int>,
  "tags": <Array[Array[str]]>,
  "announcements": <Array[hex_str]>
}
```

- `threshold`: Minimum oracles required (default: 1)
- `tags`: [NIP-88][NIP-88] tag array
- `announcements`: Hex-encoded oracle announcement TLV bytes

**Response** of `Bob`:

```json
{
  "condition_id": <hex_str>
}
```

```bash
curl -X POST https://mint.host:3338/v1/conditions \
  -H "Content-Type: application/json" \
  -d '{"threshold":1,"tags":[["description","Will BTC reach $100k?"]],"announcements":["fdd824fd..."]}'
```

#### Mint Behavior

1. Parses and verifies announcement signatures (error 13011 if failed)
2. Computes `condition_id`
3. If condition exists with matching config: returns existing `condition_id` (idempotent)
4. If condition exists with different config: error 13028
5. If new: stores and returns `condition_id`

The mint MUST make condition registration idempotent. Mints MAY require [NUT-21][21] or [NUT-22][22] authentication for DoS prevention.

### Register Partition

```http
POST https://mint.host:3338/v1/conditions/{condition_id}/partitions
```

Registers a partition and creates conditional keysets.

**Request** of `Alice`:

```json
{
  "collateral": <str>,
  "partition": <Array[str]>,
  "parent_collection_id": <hex_str>
}
```

- `collateral`: Unit string for root (e.g., `"sat"`), or `outcome_collection_id` hex for nested
- `partition`: Partition keys (e.g., `["ALICE|BOB", "CAROL"]`). MUST satisfy [Partition Rules](#partition-rules).
- `parent_collection_id` (optional): 64-char hex. Defaults to all zeros for root conditions.

**Response** of `Bob`:

```json
{
  "keysets": {
    "<outcome_collection_1>": <hex_str>,
    "<outcome_collection_2>": <hex_str>,
    ...
  }
}
```

```bash
curl -X POST https://mint.host:3338/v1/conditions/a1b2c3d4.../partitions \
  -H "Content-Type: application/json" \
  -d '{"collateral":"sat","partition":["YES","NO"]}'
```

#### Mint Behavior

1. Looks up condition (error 13021 if not found)
2. Validates partition rules (error 13037 overlapping, error 13038 incomplete)
3. If `parent_collection_id` is non-zero: verifies the referenced collection exists (error 13021 if not)
4. For each outcome collection: computes `outcome_collection_id`, reuses existing keyset or creates new one
5. Returns keyset map

**Key property:** Keysets are per `outcome_collection_id`, not per partition. If two partitions include the same outcome collection (e.g., both include `"CAROL"`), they share the same keyset. This makes tokens fungible across partitions.

**Idempotency:** The mint MUST make partition registration idempotent.

**DoS prevention:** Mints MAY require [NUT-21][21] or [NUT-22][22] authentication.

## Outcome Collection ID

Each outcome collection has a unique `outcome_collection_id` derived from the condition ID, outcome collection string, and optional parent collection ID. The result is a 32-byte x-only public key on secp256k1.

### Computation

```
outcome_collection_id(parent_collection_id, condition_id, outcome_collection_string):
  1. h = tagged_hash("Cashu_outcome_collection_id", condition_id || outcome_collection_string_bytes)
  2. P = hash_to_curve(h)
  3. If parent_collection_id is the identity (32 zero bytes):
       Return x_only(P)
     Else:
       parent_point = lift_x(parent_collection_id)
       Return x_only(EC_add(parent_point, P))
```

Where:

- `tagged_hash`: BIP-340 tagged hash
- `hash_to_curve`: Same approach as [NUT-00][00]'s `hash_to_curve` with domain separation via tagged hash input
- `EC_add`: secp256k1 point addition
- `lift_x` / `x_only`: Per [BIP-340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki)

Because EC point addition is commutative, nesting order does not matter in combinatorial markets — `(Party_A) & (BTC_UP)` produces the same ID as `(BTC_UP) & (Party_A)`.

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
- `outputs`: `BlindedMessage` objects using a **regular keyset** (same unit)

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

All conditional-to-regular conversions go through `POST /v1/redeem_outcome`.

## Redemption Verification

When `Bob` receives a `POST /v1/redeem_outcome` request:

1. All inputs MUST use the same conditional keyset
2. All outputs MUST use a regular keyset (same unit)
3. If `Bob` already has a valid attestation for this outcome collection, MAY skip steps 4-5
4. Each input MUST include valid `witness` with `oracle_sigs`
5. Verify at least `threshold` signatures from distinct oracles using [DLC signing algorithm](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md#signing-algorithm) with tagged hash `"DLC/oracle/attestation/v0"` and UTF-8 NFC-normalized outcome string
6. Verify this outcome collection is the attested winner

### Attestation Handling

The mint MUST persistently record the first valid attestation (winning outcome + timestamp) for each condition. This record MUST survive restarts.

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
| 13017 | Outputs must use a regular keyset                           |
| 13020 | Invalid condition ID                                        |
| 13021 | Condition not found                                         |
| 13027 | Oracle threshold not met                                    |
| 13028 | Condition already exists                                    |
| 13037 | Overlapping outcome collections                             |
| 13038 | Incomplete partition                                        |

## Mint Info Setting

The [NUT-06][06] `MintMethodSetting` indicates support for this feature:

```json
{
  "CTF": {
    "supported": true,
    "dlc_version": <str>,
    "vesting_period": <int>
  }
}
```

- `supported`: Boolean indicating NUT-CTF support
- `vesting_period` (optional): Seconds after `event_maturity_epoch` for redemption. Default: 30 days (2592000). `0` = no expiry.
- `dlc_version`: DLC protocol version (currently `"0"`)

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
