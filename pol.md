# NUT-XX: Proof of Liabilities

`optional`

---

## Abstract

This document defines an epoch-based Proof of Liabilities (PoL) protocol using append-only Merkle Mountain Ranges with Sums (sum-MMRs) anchored to Bitcoin through OpenTimestamps (OTS). Wallets and auditors can verify a Cashu mint's outstanding liabilities and detect changes to its history.

---

## Architecture Overview

The mint maintains two synchronized, append-only sum-MMRs:

1. **Issued MMR (Blinded Messages):** Tracks all historically issued, active unspent blinded messages `B_`.
2. **Spent MMR (Proofs Used):** Tracks all historically spent proof secrets `Y = hash_to_curve(secret)`.

Each epoch's roots are timestamped through OTS. The append-only structure makes later modification or deletion detectable.

---

## sum-MMR Specifications

A sum-MMR is an append-only sequence of perfect binary Merkle-sum trees (mountains) with strictly decreasing heights.

### 1. Leaf Nodes

Leaves record issuances or spends in insertion order, starting at index 0.

- **Issued (`Leaf_issued`):** hash `SHA256(bytes(B_))`, using compressed 33-byte `B_`; sum is the token amount.
- **Spent (`Leaf_spent`):** hash `SHA256(bytes(Y))`, using compressed 33-byte `Y`; sum is the spent amount.

### 2. Node Structure & Hashing

Each node is `(hash, sum)`: a 32-byte hash and a uint64 sum serialized as eight-byte big-endian.

Construction or append MUST fail if `sum_L + sum_R >= 2^64`.

#### Parent Node Computation

For left child `L = (hash_L, sum_L)` and right child `R = (hash_R, sum_R)`:

- `sum_P = sum_L + sum_R`
- `hash_P = SHA256(hash_L || hash_R || bytes_8(sum_L) || bytes_8(sum_R))`

### 3. MMR Construction & Node Layout

Nodes use post-order layout. Seven leaves produce 11 nodes and three peaks:

```
Height 2:            (Node 7)
                    /        \
Height 1:       (Node 3)      (Node 6)             (Node 10)
                /      \      /      \             /       \
Height 0:    (Node 1) (Node 2) (Node 4) (Node 5) (Node 8) (Node 9)  (Node 11)
               [L0]     [L1]     [L2]     [L3]     [L4]     [L5]      [L6]
```

Peak sizes correspond to set bits in the leaf count. Here, `7 = 4 + 2 + 1` (`0b111`), so Nodes 7, 10, and 11 root peaks of heights 2, 1, and 0.

#### Parent and Peak Bagging with Sums

Derive one `(root_hash, root_sum)` by bagging peaks `P_1, ..., P_k` from right to left:

1. Start with the rightmost peak as the initial accumulator: B_k = P_k.
2. For `i = k-1` down to `1`, compute `B_i = Parent(P_i, B_i+1)` using the parent formula above.
3. The root is `B_1`. An empty MMR has `hash = SHA256(b"")` and `sum = 0`.

#### Stack-Based Construction Algorithm

Maintain a stack of `(node, height)` peaks:

1. Push a new leaf `(hash: H, sum: v)` at height 0.
2. While the top two peaks have equal heights, pop right then left, compute their parent, and push it at `left.height + 1`.
3. The remaining stack, left to right, is the peak forest.

### 4. Append-Only Consistency Verification

To verify that MMR `M` extends MMR `N`, where `m > n`, use either the consistency proof below or the sibling-path prefix check.

#### Consistency Proof

A consistency proof contains:

1. `old_size = n` and `new_size = m`.
2. `old_peaks`: every peak of `N`, from left to right, as `(hash, sum, height)`.
3. `appended_subtrees`: the roots of the deterministic decomposition of leaf range `[n, m)`, from left to right, as `(hash, sum, height)`.

The deterministic decomposition of `[n, m)` is computed as follows:

```text
cursor = n
while cursor < m:
    choose the largest h such that:
        2^h <= m - cursor
        and cursor mod 2^h == 0
    emit (cursor, h)
    cursor += 2^h
```

Each emitted `(cursor, h)` identifies a complete, aligned subtree covering leaves `[cursor, cursor + 2^h)`. The proof supplies only that subtree's root hash and sum. The number, order, and heights of the supplied roots are derived from `n` and `m` and MUST NOT be trusted from the proof.

Verify the proof as follows:

1. Require `old_size` and `new_size` to equal the applicable manifest MMR sizes and require `0 <= n < m < 2^63`.
2. Derive `N`'s expected peak heights from the set bits of `n`, highest first. Require `old_peaks` to contain exactly one node for each expected height, in that order, with no extra nodes.
3. Bag `old_peaks` right to left. Require the result to equal `N`'s manifest root hash and root sum. For `n = 0`, require an empty `old_peaks` list and the empty MMR root.
4. Derive the expected appended subtree heights with the decomposition algorithm above. Require `appended_subtrees` to have exactly those heights in exactly that order.
5. Initialize a stack with `old_peaks`. For each appended subtree, push `(node, height)`. While the top two stack entries have equal height, pop right then left, compute `Parent(left, right)`, and push it at height `h + 1`.
6. Derive `M`'s expected peak heights from the set bits of `m`, highest first. Require the final stack to have exactly those heights in that order.
7. Bag the final stack right to left and require the result to equal `M`'s manifest root hash and root sum.

This proves that every old peak is preserved unchanged and that only complete subtrees covering the appended suffix are folded into it. The appended subtree roots need no leaf-level proofs: consistency constrains preservation of the old prefix, while the later manifest commits to the contents of the appended suffix.

#### Sibling-Path Prefix Check

As a client-specific alternative, re-request an inclusion proof in a later epoch and require the old sibling path to prefix the new one as specified under Verification Protocol.

---

## Epoch Manifests & On-Chain Commitments

Each epoch, the mint constructs and signs a manifest:

1. **Sort keysets:** Lowercase and lexicographically sort all unexpired hexadecimal `keyset_id` values, active or inactive.
2. **Hash keyset leaves:** For each sorted keyset, compute:
   ```
   SHA256(
     utf8("Cashu_PoL_Keyset_Leaf_v1")
     || bytes_2(len(utf8(keyset_id))) || utf8(keyset_id)
     || bytes_8(issued_mmr_size) || issued_mmr_root_hash || bytes_8(issued_mmr_root_sum)
     || bytes_8(spent_mmr_size)  || spent_mmr_root_hash  || bytes_8(spent_mmr_root_sum)
     || bytes_1(active)
     || bytes_8(deactivation_epoch)
   )
   ```
   Length and integer encodings are big-endian; hashes are 32-byte binary values. `active` is `0x01` for true or `0x00` for false. `deactivation_epoch` is a mandatory uint64 epoch index.
3. **Build the keyset Merkle root:** Build a binary Merkle tree over the ordered leaf hashes. Compute each parent as:
   ```
   SHA256(utf8("Cashu_PoL_Keyset_Node_v1") || left_hash || right_hash)
   ```
   If a level contains an odd number of hashes, duplicate its final hash before computing the next level. A single leaf is its own root. The empty keyset root is `SHA256(utf8("Cashu_PoL_Keyset_Empty_v1"))`.
4. **Global digest:** Compute:
   ```
   SHA256(
     utf8("Cashu_PoL_Epoch_v1")
     || previous_global_digest
     || bytes_8(epoch_index)
     || bytes_2(keyset_count)
     || keyset_merkle_root
   )
   ```
   `previous_global_digest` is 32 zero bytes for the first epoch. `keyset_count` MUST fit in uint16.
5. **OTS receipt:** Submit the digest to OTS calendars. The mint MUST upgrade the pending receipt after Bitcoin confirmation and publish the offline-verifiable receipt with the manifest.
6. **Manifest message:** Construct this colon-separated UTF-8 string:
   `"{keyset_id}:{epoch_index}:{timestamp}:{previous_global_digest}:{issued_mmr_size}:{issued_mmr_root_hash}:{issued_mmr_root_sum}:{spent_mmr_size}:{spent_mmr_root_hash}:{spent_mmr_root_sum}:{outstanding_balance}:{active}:{deactivation_epoch}"`
   where:
   - `keyset_id` MUST be a lowercase hexadecimal string.
   - `timestamp` MUST use RFC 3339 UTC with second precision, no fraction, and uppercase `Z` (for example, `2026-06-11T12:00:00Z`).
   - `previous_global_digest` MUST be serialized as a 64-character lowercase hexadecimal string.
   - `issued_mmr_root_hash` and `spent_mmr_root_hash` MUST be serialized as 64-character lowercase hexadecimal strings.
   - `active` MUST be the literal lowercase string `true` or `false`, reflecting the NUT-02 state at epoch close.
   - `deactivation_epoch` MUST be the canonical unsigned decimal epoch index without leading zeros.
7. **Sign:** BIP-340 Schnorr-sign `SHA256(message)` with the mint's master NUT-06 key. The message excludes `ots_receipt`, allowing receipt upgrades without changing the signature.
8. **Publish:** Publish the manifests, signatures, OTS receipts, `global_digest`, `keyset_merkle_root`, and the ordered `epoch_keysets` used to build the Merkle tree. Each entry MUST contain `keyset_id`, `issued_mmr_size`, `issued_mmr_root_hash`, `issued_mmr_root_sum`, `spent_mmr_size`, `spent_mmr_root_hash`, `spent_mmr_root_sum`, `active`, and `deactivation_epoch`. The array MUST contain every unexpired keyset exactly once and match the signed manifests.

### Keyset Lifecycle Commitments

The redemption wind-down that exposes spent-side inflation begins only after a keyset stops issuing. Each keyset therefore commits to its lifecycle under these rules:

1. **Birth:** A keyset is born in the first epoch whose `epoch_keysets` contains it. A mint adopting this NUT mid-life treats its first committed epoch as the birth of every existing keyset.
2. **Single Declaration:** `deactivation_epoch` is REQUIRED, MUST be set in the keyset's first manifest, MUST be greater than the birth epoch, and MUST remain identical in every later manifest.
3. **Monotonic Status:** After any manifest contains `active: false`, every later manifest for that keyset MUST also contain `active: false`.
4. **Issued MMR Freeze:** The lock epoch is the first epoch containing `active: false`. From that epoch onward, `issued_mmr_size`, `issued_mmr_root_hash`, and `issued_mmr_root_sum` MUST remain unchanged. The lock-epoch manifest may include issuance performed earlier in that epoch before deactivation.
5. **Epoch Deadline:** A keyset MUST be `active: false` in every manifest whose `epoch_index` is greater than or equal to its `deactivation_epoch`.
6. **Early Deactivation:** `deactivation_epoch` is an upper bound. The mint MAY deactivate the keyset in an earlier epoch.

`active: false` closes the keyset for issuance only. Existing ecash remains redeemable until `final_expiry`; therefore the spent MMR MAY and ordinarily will continue growing after the lock epoch. Every such change remains subject to append-only consistency verification. The spent MMR freezes only when the keyset reaches `final_expiry` and redemptions are no longer accepted.

Wallets SHOULD treat an unacceptably distant `deactivation_epoch` as providing no useful committed rotation schedule. Verifiers SHOULD cross-check `/v1/keysets`: after a keyset first appears, it MUST occur in every epoch closed before its NUT-02 `final_expiry`. A newly offered keyset may be absent from the latest already-closed epoch, and an expired keyset may remain listed for historical compatibility.

---

## sum-MMR Inclusion Proof Structure

An inclusion proof contains:

1. **Leaf Index:** The sequential 0-based insertion index of the leaf.
2. **Sibling Path:** A list of `(hash, sum, is_left)` sibling nodes traversed from the leaf up to its local mountain peak.
3. **Peaks:** The list of all peak roots `(hash, sum)` of the MMR forest at that epoch (of size N).

The verifier MUST derive, not trust, `leaf_index`. Derive peak heights from the set bits of leaf count `N`, highest first. A path of length `h` MUST end at the unique height-`h` peak. At level `j`, `is_left = true` means the current node is the right child and adds `2^j` to its local offset; `false` adds 0. That offset plus the widths of preceding peaks MUST equal `leaf_index`.

---

## HTTP API Specifications

### 1. Get Keyset Manifest

`GET /v1/pol/{keyset_id}/manifest`

- **Query Params:** `epoch_index` (optional, integer)
- **Response:**

```json
{
  "keyset_id": "009a6154b71113b7",
  "epoch_index": 1,
  "timestamp": "2026-06-11T12:00:00Z",
  "previous_global_digest": "0000000000000000000000000000000000000000000000000000000000000000",
  "signing_pubkey": "f3dd0e40dd3d888301b3b47aede737b6f9451ab451dfc05a1ae023ab4235b4dd",
  "issued_mmr_size": 125000,
  "issued_mmr_root_hash": "8f3c45d51e9bb2a50c25a40b89f460ccd8b120de84929ee29502e7c99184f60f",
  "issued_mmr_root_sum": 1000000,
  "spent_mmr_size": 52000,
  "spent_mmr_root_hash": "4d1a7d72e8f498b52f751c69e1579f11ebba3f497c6a92fbb784eef0bd47fd44",
  "spent_mmr_root_sum": 450000,
  "outstanding_balance": 550000,
  "active": true,
  "deactivation_epoch": 12,
  "global_digest": "ec53f808f2885ff4fe74f0abebd2e216173cc784ec472213a81b2ae4723aa3b4",
  "keyset_merkle_root": "ddb1201da3139b338edf4be15104c48b34065d8d4a10e206df314870aea23256",
  "epoch_keysets": [
    {
      "keyset_id": "009a6154b71113b7",
      "issued_mmr_size": 125000,
      "issued_mmr_root_hash": "8f3c45d51e9bb2a50c25a40b89f460ccd8b120de84929ee29502e7c99184f60f",
      "issued_mmr_root_sum": 1000000,
      "spent_mmr_size": 52000,
      "spent_mmr_root_hash": "4d1a7d72e8f498b52f751c69e1579f11ebba3f497c6a92fbb784eef0bd47fd44",
      "spent_mmr_root_sum": 450000,
      "active": true,
      "deactivation_epoch": 12
    }
  ],
  "ots_receipt": "<hex_encoded_ots_file_content>",
  "mint_signature": "<hex_encoded_signature>"
}
```

### 2. Query Issued Tree Proofs

`POST /v1/pol/{keyset_id}/proofs/issued`

- **Query Params:** `epoch_index` (optional, integer)
- **Request Body:**

```json
{
  "blinded_messages": [
    "02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4"
  ]
}
```

- **Response:**

```json
{
  "proofs": [
    {
      "item": "02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4",
      "leaf_index": 45012,
      "value": 1000,
      "sibling_path": [
        {
          "hash": "b4a1df64d7d3cbfe8f0e59b2e41f47a90d5e8b26f04b3cf26d264eed55edf21b",
          "sum": 500,
          "is_left": true
        }
      ],
      "peaks": [
        {
          "hash": "f29a2cfeabdd677e8216c72e26f58007ac45e41b34db44d876ba7f7f25709125",
          "sum": 20000
        }
      ]
    }
  ]
}
```

### 3. Query Spent Tree Proofs

`POST /v1/pol/{keyset_id}/proofs/spent`

- **Query Params:** `epoch_index` (optional, integer)
- **Request Body:**

```json
{ "ys": ["02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4"] }
```

- **Response:** Same format as `/proofs/issued` with the `Y` point hex string in the `item` field.

---

## Signed Transactional Proof of Liability Receipts

For `mint`, `melt`, and `swap`, the mint **MUST** return a signed PoL receipt for every spent input and returned output.

### 1. Receipt JSON Schema

```json
{
  "target_epoch": 12,
  "signature": "<hex_encoded_signature>"
}
```

### 2. Message Formats and Cryptography

Sign each receipt with the keyset's per-amount key (`private_keys[amount]`). The applicable domain prefix MUST begin the message:

- **Output:** `"Cashu_PoL_Receipt_Issued:" || B'_hex || ":" || target_epoch_decimal_string`
- **Spent input:** `"Cashu_PoL_Receipt_Spent:" || Y_hex || ":" || target_epoch_decimal_string`

`B'_hex` and `Y_hex` are lowercase compressed 33-byte encodings. The epoch is decimal, for example `"12"`.

| Version   | Curve     | Signature Details                                                                                                                                                                                                                            |
| :-------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00`/`01` | secp256k1 | BIP340 Schnorr over `SHA256(message)`. Verified against `public_keys[amount]`.                                                                                                                                                               |
| `02`      | BLS12-381 | `sigma = a * H_G1(message)` (compressed G1). Verified via `e(sigma, G2) == e(H_G1(message), K)` where `K = public_keys[amount]` (G2). `H_G1` is RFC 9380 `hash_to_curve_G1` under DST `"Cashu_PoL_Receipt_BLS12381G1_XMD:SHA-256_SSWU_RO_"`. |

### 3. Response Alignment

Receipt order matches request input or output order:

- **Mint (`POST /v1/mint/{method}` & `/v1/mint/{method}/batch`):** Nested in `pol_receipt` of each `BlindSignature` inside `signatures`.
- **Swap (`POST /v1/swap`):**
  - Outputs: Nested in `pol_receipt` of each `BlindSignature` inside `signatures`.
  - Inputs: Top-level `spent_receipts: List[PolReceipt]` mapping to the request's `inputs`.
- **Melt (`POST /v1/melt/{method}`):** Top-level `spent_receipts: List[PolReceipt]` mapping to the request's `inputs`.

---

## Verification Protocol

Wallets audit held and spent tokens as follows.

### Step 1: Verify Manifest Signature

Verify `mint_signature` against the mint's master `signing_pubkey` from `/v1/info`, using BIP-340 over `SHA256(epoch_string)`.

### Step 2: Validate OpenTimestamps Attestation

1. Rebuild every keyset leaf and the ordered Merkle tree; require its root to equal `keyset_merkle_root`. Rebuild `global_digest` from the previous digest, epoch index, keyset count, and Merkle root. Require every `epoch_keysets` entry to match its signed manifest.
2. Deserialize `ots_receipt` and require its starting digest to equal `global_digest`. The pending-receipt timeout MUST NOT exceed 24 hours from the manifest `timestamp`; exceeding it MUST be an audit failure. The pending tag is `0x83dfe30d2ef90c8e`.
3. Within that window, a verifier can request an upgrade from an OTS calendar. The mint remains responsible for publishing an upgraded, offline-verifiable receipt.
4. With a conforming OTS implementation, execute every operation through the Bitcoin block-header attestation (`0x0588960d73d71901`). Using an independently validated node, require the result to match the block's committed Merkle root. An attestation tag and block height alone are insufficient.
5. Require sufficient confirmations and a block timestamp within a reasonable tolerance of the manifest timestamp, for example four hours.

### Step 3: Validate MMR Append-Only Consistency

1. Compare this epoch's `previous_global_digest` against the previous epoch's global digest (or against the digest cached by the wallet at its last audit). Treat a mismatch as an audit failure.
2. For a refreshed inclusion proof:
   - The sequential `leaf_index` and leaf node `(hash, sum)` MUST be identical across both proofs.
   - Let `k` be the length of the sibling path of the previous proof. The first `k` elements of the new proof's `sibling_path` MUST match the old proof's `sibling_path` exactly (in node hash, sum, and `is_left` positional boolean).
   - Later entries represent subsequent higher merges.
   - A prefix mismatch is an audit failure. Auditors can instead use standard MMR consistency proofs.
3. For each keyset's signed manifest history:
   - `deactivation_epoch` MUST remain identical to its first declaration.
   - `active` MUST never return to `true` after becoming `false`.
   - From the first `active: false` manifest, the issued MMR size, root hash, and root sum MUST remain unchanged.
   - A manifest at or after its `deactivation_epoch` MUST contain `active: false`.
   - Any violation is an audit failure and supplies evidence for `rotation_violation`.

### Step 4: Validate Issued sum-MMR Sibling Walks

For each held active token:

1. Reconstruct the unsigned blinded message `B_` (BDHKE: `B_ = Y + rG`; BLS: `B_ = r * Y`).
2. Compute the leaf node:
   - `current_hash = SHA256(bytes(B_))`
   - `current_sum = token_value`
3. For each sibling, set the current node to `Parent(sibling, current)` if `is_left` is true; otherwise use `Parent(current, sibling)`.
4. Require the result to appear in `peaks`.
5. Derive the position as specified under Inclusion Proof Structure and require it to equal `leaf_index`.
6. Bag `peaks` right to left and require the result to equal the manifest's `issued_mmr_root_hash` and `issued_mmr_root_sum`.

### Step 5: Validate Spent sum-MMR Sibling Walks

1. Compute `Y = hash_to_curve(secret)`.
2. Compute the leaf node:
   - `current_hash = SHA256(bytes(Y))`
   - `current_sum = spent_value`
3. Verify the path and bag the peaks as in Step 4.
4. Require the result to equal the manifest's `spent_mmr_root_hash` and `spent_mmr_root_sum`.

### Step 6: Verify Liabilities Equation

```
outstanding_balance == issued_mmr_root_sum - spent_mmr_root_sum
```

---

## Cryptographic Fraud Challenges & Mint Responses

Fraud challenges are self-contained and falsifiable. A mint refutes a false challenge with the specified cryptographic response.

### Note on Spent-Side Inflation & Keyset Rotations

A mint can issue ecash to itself and spend it with valid secrets, so preimage challenges cannot prevent spent-side inflation. Append-only history and keyset expiry expose it:

1. Fabricated spent leaves cannot be removed.
2. A deactivated keyset permits spends but no issuance; an expired keyset permits neither.
3. During wind-down, inflated spends make valid redemptions exceed claimed liabilities or break the balance equation.

The protocol defines five challenge types.

---

### 1. Leaf Omission or Value Mismatch (`leaf_omission_or_mismatch`)

- **Description:** A signed PoL receipt promises a leaf by epoch `E`, but the leaf is absent or has the wrong value in epoch `E` or later.
- **Challenge Schema:**

  ```json
  {
    "challenge_type": "leaf_omission_or_mismatch",
    "keyset_id": "009a6154b71113b7",
    "epoch_index": 12,
    "pol_receipt": {
      "target_epoch": 12,
      "signature": "<hex_encoded_signature>"
    },
    "leaf_type": "issued | spent",
    "leaf_data": {
      "item_hex": "02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4",
      "value": 1000
    }
  }
  ```

  `pol_receipt.signature` must verify under the keyset-amount public key for `leaf_data.value` and the applicable domain-separated receipt message.

- **Response Schema:**
  ```json
  {
    "response_type": "leaf_omission_or_mismatch_response",
    "keyset_id": "009a6154b71113b7",
    "epoch_index": 12,
    "leaf_type": "issued | spent",
    "proof": {
      "item": "02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4",
      "leaf_index": 45012,
      "value": 1000,
      "sibling_path": [
        {
          "hash": "b4a1df64d7d3cbfe8f0e59b2e41f47a90d5e8b26f04b3cf26d264eed55edf21b",
          "sum": 500,
          "is_left": true
        }
      ],
      "peaks": [
        {
          "hash": "f29a2cfeabdd677e8216c72e26f58007ac45e41b34db44d876ba7f7f25709125",
          "sum": 20000
        }
      ]
    }
  }
  ```
- **Response:** The mint refutes the challenge with a valid inclusion proof for the item, value, and epoch. The proof must resolve to the applicable manifest root and sum.

---

### 2. History Rewriting or Append-Only Violation (`append_only_violation`)

- **Description:** Two signed epochs contain conflicting histories for the same proof-derived leaf position.
- **Challenge schema:** Two signed manifests and valid inclusion proofs for the same `leaf_index`:

  ```json
  {
    "challenge_type": "append_only_violation",
    "keyset_id": "009a6154b71113b7",
    "epoch_index_1": 11,
    "epoch_index_2": 12,
    "leaf_index": 45012,
    "proof_1": {
      "item": "02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4",
      "value": 1000,
      "sibling_path": [
        {
          "hash": "b4a1df64d7d3cbfe8f0e59b2e41f47a90d5e8b26f04b3cf26d264eed55edf21b",
          "sum": 500,
          "is_left": true
        }
      ],
      "peaks": [
        {
          "hash": "f29a2cfeabdd677e8216c72e26f58007ac45e41b34db44d876ba7f7f25709125",
          "sum": 20000
        }
      ]
    },
    "proof_2": {
      "item": "02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4",
      "value": 500,
      "sibling_path": [
        {
          "hash": "9c1ae83721fa4035bd51f2aa0799d9b93f17603a5ea1a7d946446f295c6d3d0e",
          "sum": 100,
          "is_left": true
        }
      ],
      "peaks": [
        {
          "hash": "3d2a865c3b17894d0e429730880fe92d6445da54c694f05417f7c9de7f58ca3b",
          "sum": 25000
        }
      ]
    }
  }
  ```

  The verifier MUST derive both positions and reject the challenge unless each equals `leaf_index`. The proofs establish a violation if their item or value differs, or the later sibling path does not preserve the earlier prefix.

- **Response:** The mint can refute the challenge only by proving a manifest signature or inclusion proof invalid. If both verify, the challenge succeeds.

---

### 3. Manifest Equivocation (`manifest_equivocation`)

- **Description:** Two distinct signed manifests exist for the same keyset and epoch.
- **Challenge schema:** Both manifests MUST contain every signed field so verifiers can reconstruct their digests.
  ```json
  {
    "challenge_type": "manifest_equivocation",
    "manifest_a": {
      "keyset_id": "009a6154b71113b7",
      "epoch_index": 12,
      "timestamp": "2026-06-11T12:00:00Z",
      "previous_global_digest": "4b8e39cd3c008a6f5da0ea6c22946250086c7c53298f8d33b4f7a178e121ddd8",
      "issued_mmr_size": 45013,
      "issued_mmr_root_hash": "8f3c45d51e9bb2a50c25a40b89f460ccd8b120de84929ee29502e7c99184f60f",
      "issued_mmr_root_sum": 25000,
      "spent_mmr_size": 12001,
      "spent_mmr_root_hash": "7d4e277fc585b942a22314ff992cb9d4413da734183b7b5f669e5b38d5bd73bf",
      "spent_mmr_root_sum": 9000,
      "outstanding_balance": 16000,
      "active": true,
      "deactivation_epoch": 20,
      "mint_signature": "<signature_a>"
    },
    "manifest_b": {
      "keyset_id": "009a6154b71113b7",
      "epoch_index": 12,
      "timestamp": "2026-06-11T12:00:00Z",
      "previous_global_digest": "4b8e39cd3c008a6f5da0ea6c22946250086c7c53298f8d33b4f7a178e121ddd8",
      "issued_mmr_size": 45013,
      "issued_mmr_root_hash": "9a2b72d9d43fa53e05c27f4d9f296dc1912a819c33302fda106b40cfa4985f1e",
      "issued_mmr_root_sum": 24000,
      "spent_mmr_size": 12001,
      "spent_mmr_root_hash": "7d4e277fc585b942a22314ff992cb9d4413da734183b7b5f669e5b38d5bd73bf",
      "spent_mmr_root_sum": 9000,
      "outstanding_balance": 15000,
      "active": true,
      "deactivation_epoch": 20,
      "mint_signature": "<signature_b>"
    }
  }
  ```
- **Response:** Verify both serialized manifests against the mint's master NUT-06 key. If their keyset and epoch match, their signed fields differ, and both signatures verify, the challenge succeeds.

---

### 4. sum-MMR Consistency Violation (`sum_mmr_consistency_violation`)

- **Description:** The mint must prove that epoch `E_2` extends `E_1`, without relying on client tokens.
- **Challenge schema:** The challenger identifies two valid signed manifests where `E_2 > E_1`.
  ```json
  {
    "challenge_type": "sum_mmr_consistency_violation",
    "keyset_id": "009a6154b71113b7",
    "epoch_index_1": 11,
    "epoch_index_2": 12,
    "tree_type": "issued | spent"
  }
  ```
- **Response Schema:**
  ```json
  {
    "response_type": "sum_mmr_consistency_response",
    "keyset_id": "009a6154b71113b7",
    "epoch_index_1": 11,
    "epoch_index_2": 12,
    "tree_type": "issued | spent",
    "consistency_proof": {
      "old_size": 3,
      "new_size": 4,
      "old_peaks": [
        {
          "hash": "90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f",
          "sum": 350,
          "height": 1
        },
        {
          "hash": "95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40",
          "sum": 500,
          "height": 0
        }
      ],
      "appended_subtrees": [
        {
          "hash": "e1577700e127f1ce6e20a4efc2d96a986979c755d9ab559af6b1755eb3f3220e",
          "sum": 1000,
          "height": 0
        }
      ]
    }
  }
  ```
- **Response:** The mint refutes the challenge with a consistency proof that passes the algorithm under Append-Only Consistency Verification and resolves exactly to both manifests' sizes, roots, and sums. Discovery and response deadlines are outside this NUT; silence is not cryptographic proof of fraud.

---

### 5. Keyset Rotation Violation (`rotation_violation`)

- **Description:** The mint reactivated a locked keyset, issued after lock, remained active at or after its committed deactivation epoch, or changed its deactivation declaration. Each variant is proven entirely by signed manifests; challengers need not hold or reveal ecash.
- **Challenge Schema:**

  ```json
  {
    "challenge_type": "rotation_violation",
    "keyset_id": "009a6154b71113b7",
    "violation_kind": "reactivation | issuance_after_lock | deactivation_overrun | declaration_drift",
    "manifest_a": { "...": "all signed manifest fields" },
    "manifest_b": { "...": "all signed manifest fields, or omitted" }
  }
  ```

  Every supplied manifest MUST contain all fields of the serialized manifest message and a valid `mint_signature`. Evidence is defined per kind:
  - `reactivation`: `manifest_a.epoch_index < manifest_b.epoch_index`, `manifest_a.active` is false, and `manifest_b.active` is true.
  - `issuance_after_lock`: `manifest_a.active` is false and a later `manifest_b` differs in issued MMR size, root hash, or root sum.
  - `deactivation_overrun`: `manifest_a.active` is true and `manifest_a.epoch_index >= manifest_a.deactivation_epoch`. `manifest_b` is omitted.
  - `declaration_drift`: the manifests are for different epochs of the same keyset and contain different `deactivation_epoch` values. Conflicting declarations for the same epoch use `manifest_equivocation` instead.

- **Response:** Verify every supplied manifest under the mint's NUT-06 master key, then evaluate the selected predicate. If the signatures and predicate verify, the challenge succeeds and has no cryptographic refutation. The mint can refute it only by showing that a supplied signature or required predicate is invalid.

[tests]: tests/pol-tests.md
