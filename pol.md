# NUT-XX: Proof of Liabilities

`optional`

---

## Abstract

This document specifies a synchronized, epoch-based, stateless Proof of Liabilities (PoL) auditing scheme using append-only Merkle Mountain Range with Sums (sum-MMR) trees and automated OpenTimestamps (OTS) commitments on-chain. This scheme allows wallets and external auditors to mathematically verify the outstanding liabilities of a Cashu mint while preventing historical manipulation or leaf deletion.

---

## Architecture Overview

A Cashu mint acts as a custodian of backing assets. Outstanding liabilities are proven using two synchronized append-only Merkle Mountain Range with Sums (sum-MMR) forests:

1. **Issued MMR (Blinded Messages):** Tracks all historically issued, active unspent blinded messages `B_`.
2. **Spent MMR (Proofs Used):** Tracks all historically spent proof secrets `Y = hash_to_curve(secret)`.

This prevents the mint from omitting or manipulating liabilities. Epoch-based MMR roots are periodically committed to the Bitcoin blockchain via OpenTimestamps. Because the MMR is strictly append-only, any historical leaf modification or deletion (such as fake spent leaves being removed) is mathematically impossible, establishing a fully immutable and audit-verifiable history.

---

## sum-MMR Specifications

A Merkle Mountain Range with Sums (sum-MMR) is an append-only collection of perfect binary Merkle-sum trees (mountains) of strictly decreasing heights.

### 1. Leaf Nodes

Each leaf node represents a distinct historical transaction (issuance or spend) in sequential order of occurrence (0-based leaf index).

- **Issued Leaf Node (`Leaf_issued`):**
  - Hash: `SHA256(bytes(B_))` (using the 33-byte compressed public key representation of `B_`).
  - Sum: Face amount of the token associated with the blinded message.
- **Spent Leaf Node (`Leaf_spent`):**
  - Hash: `SHA256(bytes(Y))` (using the 33-byte compressed public key representation of `Y`).
  - Sum: Face amount of the spent proof.

### 2. Node Structure & Hashing

Each node in the sum-MMR is represented as `(hash, sum)` where `hash` is 32 bytes and `sum` is an 8-byte big-endian unsigned integer (uint64).

If `sum_L + sum_R >= 2^64`, tree construction/append MUST fail due to overflow.

#### Parent Node Computation

For left child `L = (hash_L, sum_L)` and right child `R = (hash_R, sum_R)`:

- `sum_P = sum_L + sum_R`
- `hash_P = SHA256(hash_L || hash_R || bytes_8(sum_L) || bytes_8(sum_R))`

### 3. MMR Construction & Node Layout

Nodes are added to the MMR sequentially. The layout is determined by the post-order traversal of each perfect binary tree (mountain) formed as elements are appended. Below is an ASCII diagram of a sum-MMR with 7 leaves (resulting in 11 total nodes and 3 distinct mountain peaks):

```
Height 2:            (Node 7)
                    /        \
Height 1:       (Node 3)      (Node 6)             (Node 10)
                /      \      /      \             /       \
Height 0:    (Node 1) (Node 2) (Node 4) (Node 5) (Node 8) (Node 9)  (Node 11)
               [L0]     [L1]     [L2]     [L3]     [L4]     [L5]      [L6]
```

- **Peak 1 (Mountain of size 4 leaves):** Rooted at Node 7 (Height 2).
- **Peak 2 (Mountain of size 2 leaves):** Rooted at Node 10 (Height 1).
- **Peak 3 (Mountain of size 1 leaf):** Rooted at Node 11 (Height 0).

The number and sizes of individual mountains correspond exactly to the bits set to `1` in the binary representation of the leaf count. For example, 7 = 4 + 2 + 1, which is represented as binary `111` (2^2 + 2^1 + 2^0).

#### Parent and Peak Bagging with Sums

Because an MMR is a forest of multiple peak roots P_1, P_2, ..., P_k of strictly decreasing heights, a single unique root `(root_hash, root_sum)` must be derived for signing and on-chain commitments. This is done via **Right-to-Left Peak Bagging**:

1. Start with the rightmost peak as the initial accumulator: B_k = P_k.
2. For each peak P_i from right to left (i = k-1 down to 1):
   - Compute parent B_i = Parent(P_i, B_i+1):
     - `sum_B_i = sum(P_i) + sum(B_i+1)`
     - `hash_B_i = SHA256(hash(P_i) || hash(B_i+1) || bytes_8(sum(P_i)) || bytes_8(sum(B_i+1)))`
3. The final bagged root is B_1. If the MMR is empty (size 0), the root has `hash = SHA256(b"")` and `sum = 0`.

#### Stack-Based Construction Algorithm

An elegant and standard way to dynamically construct the MMR and track heights without complex index calculations is to use a stack of peak roots:

1. Maintain an empty list `peaks` acting as a stack of current peak nodes, where each element is represented as `(node, height)`.
2. When appending a new leaf with hash `H` and value `v`:
   - Create a new peak at height 0: `new_peak = (hash: H, sum: v)` and `height = 0`.
   - Push `(new_peak, height)` onto the `peaks` stack.
   - While `len(peaks) >= 2` and the `height` of the top element matches the `height` of the second element from the top (`peaks[-1].height == peaks[-2].height`):
     - Pop the right child: `(R_node, R_height) = peaks.pop()`
     - Pop the left child: `(L_node, L_height) = peaks.pop()`
     - Compute the parent node:
       - `sum_P = L_node.sum + R_node.sum`
       - `hash_P = SHA256(L_node.hash || R_node.hash || bytes_8(L_node.sum) || bytes_8(R_node.sum))`
     - Let `P_node = (hash: hash_P, sum: sum_P)` and `P_height = L_height + 1`.
     - Push `(P_node, P_height)` back onto the `peaks` stack.
3. After all leaves are appended, the remaining nodes in the `peaks` stack (ordered from left to right) represent the current forest of MMR peaks.

### 4. Append-Only Consistency Verification

To verify that MMR M (of size m) is a valid append-only extension of MMR N (of size n, where m > n), an auditor compares their peak lists. This append-only property can be verified in two ways:

1. **Standard MMR Consistency Proofs:** Cryptographically proving that the peaks of the old MMR N are deterministically preserved and folded into the peaks of the new MMR M.
2. **Distributed Sibling Path Prefix Checks:** Any client holding a valid inclusion proof (such as for active or spent ecash) can re-request a new proof in the following epoch and verify that the old sibling path is preserved as a direct prefix of the new sibling path. If the mint modified or removed any historical entries, the internal hashes would change, immediately violating prefix preservation.

---

## Epoch Manifests & On-Chain Commitments

Every epoch interval (e.g., 24 hours), the mint constructs and signs an Epoch Manifest:

1. **Sort Keysets:** Normalize all active unexpired `keyset_id` strings to lowercase hexadecimal representation, and then sort them alphabetically (lexicographically by their ASCII values).
2. **Commitment Data:** Prepend the 32-byte binary `previous_global_digest` of the previous epoch (for the first epoch, this MUST be 32 bytes of zeros `0x00...00`). Then concatenate the UTF-8 lowercase `keyset_id`, 8-byte big-endian `issued_mmr_size`, 32-byte binary `issued_mmr_root_hash`, 8-byte big-endian `spent_mmr_size`, and 32-byte binary `spent_mmr_root_hash` for each keyset sequentially.
3. **Global Digest:** Compute `SHA256(commitment_data)`.
4. **OTS Submission & Upgrading:**
   - Submit the **Global Digest** to OpenTimestamps (OTS) calendar servers to obtain an initial _pending_ (incomplete) receipt.
   - **Mint Upgrade Burden:** The mint MUST monitor the calendar server, upgrade the pending `.ots` receipt to an _anchored_ (completed) state once the transaction has been confirmed on the Bitcoin blockchain, and republish the fully upgraded, offline-verifiable `.ots` receipt alongside the manifest.
5. **Manifest Message:** Construct a colon-separated UTF-8 string:
   `"{keyset_id}:{epoch_index}:{timestamp}:{previous_global_digest}:{issued_mmr_size}:{issued_mmr_root_hash}:{issued_mmr_root_sum}:{spent_mmr_size}:{spent_mmr_root_hash}:{spent_mmr_root_sum}:{outstanding_balance}"`
   where:
   - `keyset_id` MUST be a lowercase hexadecimal string.
   - `timestamp` MUST be serialized as an RFC 3339 string with second precision, without fractional seconds, and strictly using uppercase `Z` for the UTC timezone (e.g., `2026-06-11T12:00:00Z`).
   - `previous_global_digest` MUST be serialized as a 64-character lowercase hexadecimal string.
   - `issued_mmr_root_hash` and `spent_mmr_root_hash` MUST be serialized as 64-character lowercase hexadecimal strings.
6. **Signing:** Sign the message with a BIP-340 Schnorr signature using the mint's master NUT-06 private key signing the SHA256 digest of this serialized manifest string. Note that this signature is over the manifest metadata only and **excludes** the `ots_receipt` to allow upgrading the receipt without changing the signature or causing equivocation false-positives.
7. **Publish:** Store and publish the signed manifest, signatures, and OTS receipts.

---

## sum-MMR Inclusion Proof Structure

To minimize verification overhead on clients, sum-MMR inclusion proofs provide the minimal sibling path and peak forest necessary to reconstruct the single bagged commitment:

1. **Leaf Index:** The sequential 0-based insertion index of the leaf.
2. **Sibling Path:** A list of `(hash, sum, is_left)` sibling nodes traversed from the leaf up to its local mountain peak.
3. **Peaks:** The list of all peak roots `(hash, sum)` of the MMR forest at that epoch (of size N).

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
  "issued_mmr_root_hash": "8f3c...",
  "issued_mmr_root_sum": 1000000,
  "spent_mmr_size": 52000,
  "spent_mmr_root_hash": "4d1a...",
  "spent_mmr_root_sum": 450000,
  "outstanding_balance": 550000,
  "ots_receipt": "<hex_encoded_ots_file_content>",
  "mint_signature": "<hex_encoded_signature>"
}
```

### 2. Query Issued Tree Proofs

`POST /v1/pol/{keyset_id}/proofs/issued`

- **Query Params:** `epoch_index` (optional, integer)
- **Request Body:**

```json
{ "blinded_messages": ["02b1a..."] }
```

- **Response:**

```json
{
  "proofs": [
    {
      "item": "02b1a...",
      "leaf_index": 45012,
      "value": 1000,
      "sibling_path": [{ "hash": "b4a1...", "sum": 500, "is_left": true }],
      "peaks": [{ "hash": "f29a...", "sum": 20000 }]
    }
  ]
}
```

### 3. Query Spent Tree Proofs

`POST /v1/pol/{keyset_id}/proofs/spent`

- **Query Params:** `epoch_index` (optional, integer)
- **Request Body:**

```json
{ "ys": ["02b1a..."] }
```

- **Response:** Same format as `/proofs/issued` with the `Y` point hex string in the `item` field.

---

## Signed Transactional Proof of Liability Receipts

The mint **MUST** return a cryptographically signed **PoL Receipt** nested inside each input spent and output returned during state-transitioning actions (`mint`, `melt`, and `swap`).

### 1. Receipt JSON Schema

```json
{
  "target_epoch": 12,
  "signature": "<hex_encoded_signature>"
}
```

### 2. Message Formats and Cryptography

Each receipt is signed under the keyset's per-amount private key (`private_keys[amount]`) corresponding to the note's denomination.

To prevent cross-protocol signature replay attacks and provide robust domain separation, a specific domain prefix MUST be prepended to the message to form the payload to be signed:

- **Message to Sign:**
  - **Output (Issued/Active):** `"Cashu_PoL_Receipt_Issued:" || B'_hex || ":" || target_epoch_decimal_string`
  - **Spent Input:** `"Cashu_PoL_Receipt_Spent:" || Y_hex || ":" || target_epoch_decimal_string`

Where `B'_hex` and `Y_hex` are the 33-byte compressed hexadecimal representations of `B'` and `Y` (lowercase), and `target_epoch_decimal_string` is the decimal representation of the target epoch (e.g., `"12"`).

| Version   | Curve     | Signature Details                                                                                                                                                                                                                            |
| :-------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00`/`01` | secp256k1 | BIP340 Schnorr over `SHA256(message)`. Verified against `public_keys[amount]`.                                                                                                                                                               |
| `02`      | BLS12-381 | `sigma = a * H_G1(message)` (compressed G1). Verified via `e(sigma, G2) == e(H_G1(message), K)` where `K = public_keys[amount]` (G2). `H_G1` is RFC 9380 `hash_to_curve_G1` under DST `"Cashu_PoL_Receipt_BLS12381G1_XMD:SHA-256_SSWU_RO_"`. |

### 3. Response Alignment

Returned receipts are fully order-preserving (1:1 index matching of request inputs/outputs):

- **Mint (`POST /v1/mint/{method}` & `/v1/mint/{method}/batch`):** Nested in `pol_receipt` of each `BlindSignature` inside `signatures`.
- **Swap (`POST /v1/swap`):**
  - Outputs: Nested in `pol_receipt` of each `BlindSignature` inside `signatures`.
  - Inputs: Top-level `spent_receipts: List[PolReceipt]` mapping to the request's `inputs`.
- **Melt (`POST /v1/melt/{method}`):** Top-level `spent_receipts: List[PolReceipt]` mapping to the request's `inputs`.

---

## Verification Protocol

Wallets periodically audit their held and spent tokens:

### Step 1: Verify Manifest Signature

Verify the BIP-340 Schnorr signature `mint_signature` against the mint's master public key (`signing_pubkey` from `/v1/info`) over the SHA256 digest of the constructed epoch string.

### Step 2: Validate OpenTimestamps Attestation

1. **Verify or Upgrade Receipt:** The verifier retrieves the `ots_receipt`. If the receipt contains a pending tag (`0x00 0x06`) and has remained unconfirmed/pending after a maximum timeout bound (MUST NOT be more than 24 hours from the manifest `timestamp`), the verifier MUST treat it as an **audit failure**, rather than waiting indefinitely.
2. **Upgrade Proof (if pending):** If the receipt is still pending but within the timeout window, the verifier can attempt to fetch the Merkle path by posting the `ots_receipt` to a calendar upgrade endpoint (e.g., `https://alice.btc.calendar.opentimestamps.org/upgrade`). Note, however, that a properly functioning mint carries the upgrade burden and should publish already upgraded, offline-verifiable receipts.
3. **Scan for Block:** Find block header attestation tag `0x00 0x05` (`A_BLOCKHEADER`).
4. **Parse Height:** Decode the Bitcoin block height (serialized as a VarInt) immediately following the tag.
5. **Confirm Block Timestamp:** Check via an independent explorer (e.g., `https://mempool.space/api/...`) that the block height exists and has sufficient confirmations. Furthermore, verify that the Bitcoin block's timestamp is within a reasonable tolerance window (e.g., within 4 hours) of the manifest `timestamp`, rather than requiring an exact match.

### Step 3: Validate MMR Append-Only Consistency

To ensure the mint does not modify or delete historical entries from an epoch to another:

1. Compare this epoch's `previous_global_digest` against the previous epoch's global digest (or against the digest cached by the wallet at its last audit). Treat a mismatch as an audit failure.
2. **Sibling Path Prefix Preservation Check:** Any client holding a valid inclusion proof (for issued ecash or spent history) in a previous epoch can verify consistency when refreshing or re-requesting their proof in the current epoch:
   - The sequential `leaf_index` and leaf node `(hash, sum)` MUST be identical across both proofs.
   - Let `k` be the length of the sibling path of the previous proof. The first `k` elements of the new proof's `sibling_path` MUST match the old proof's `sibling_path` exactly (in node hash, sum, and `is_left` positional boolean).
   - Any additional sibling nodes beyond index `k-1` in the new `sibling_path` represent subsequent peaks merged at higher mountain heights.
   - If this prefix match fails, the mint has modified, reordered, or deleted a past leaf (such as removing fabricated spent leaves), which constitutes an **audit failure**. Alternatively, external auditors can verify append-only extensions using standard MMR consistency proofs.

### Step 4: Validate Issued sum-MMR Sibling Walks

For each held active token:

1. Reconstruct the unsigned blinded message `B_` (BDHKE: `B_ = Y + rG`; BLS: `B_ = r * Y`).
2. Compute the leaf node:
   - `current_hash = SHA256(bytes(B_))`
   - `current_sum = token_value`
3. Walk up the sibling path:
   - For each sibling in `sibling_path`:
     - If `sibling.is_left == true`:
       - `current_hash = SHA256(sibling.hash || current_hash || bytes_8(sibling.sum) || bytes_8(current_sum))`
       - `current_sum = sibling.sum + current_sum`
     - If `sibling.is_left == false`:
       - `current_hash = SHA256(current_hash || sibling.hash || bytes_8(current_sum) || bytes_8(sibling.sum))`
       - `current_sum = current_sum + sibling.sum`
4. Ensure the resulting `(current_hash, current_sum)` is present as one of the peak roots in the `peaks` array of the proof.
5. Perform Peak Bagging on `peaks` from right to left:
   - Let the bagged accumulator B_k = P_k (the rightmost peak).
   - For each peak P_i from right to left (i = k-1 down to 1):
     - `sum_B_i = sum(P_i) + sum(B_i+1)`
     - `hash_B_i = SHA256(hash(P_i) || hash(B_i+1) || bytes_8(sum(P_i)) || bytes_8(sum(B_i+1)))`
   - Verify that the final bagged peak root B_1 matches the `issued_mmr_root_hash` and `issued_mmr_root_sum` in the Epoch Manifest.

### Step 5: Validate Spent sum-MMR Sibling Walks

For spent tokens (history):

1. Compute `Y = hash_to_curve(secret)`.
2. Compute the leaf node:
   - `current_hash = SHA256(bytes(Y))`
   - `current_sum = spent_value`
3. Walk up the sibling path, find the calculated peak in `peaks`, and perform Peak Bagging as specified in Step 4.
4. Verify that the final bagged peak root matches `spent_mmr_root_hash` and `spent_mmr_root_sum` in the Epoch Manifest.

### Step 6: Verify Liabilities Equation

Ensure:

```
outstanding_balance == issued_mmr_root_sum - spent_mmr_root_sum
```

---

## Cryptographic Fraud Challenge

If verification fails, the wallet generates a **Fraud Challenge**—a self-contained JSON document proving perjury.

- **BDHKE (Keyset Version <= v2):** Includes the Discrete Logarithm Equality (DLEQ) proof `{e, s}` (issued) or `{e, s, r}` (spent) to allow third-party verification.
- **BLS (Keyset Version >= v3):** No DLEQ proof is required; the BLS signature (`C'` or `C`) can be verified directly against the keyset-amount public key.

### Challenge JSON Schema

```json
{
  "challenge_type": "pol_fraud_proof",
  "keyset_id": "009a6154b71113b7",
  "keyset_version": 2,
  "epoch_index": 1,
  "manifest": { "...": "..." },
  "pol_receipt": {
    "target_epoch": 1,
    "signature": "<hex_encoded_signature>"
  },
  "proof_type": "issued | spent",
  "leaf_data": {
    "B_hex": "02b1a...", // Required for "issued"
    "C_prime_hex": "038a1...", // Required for "issued"
    "Y_hex": "02b1a...", // Required for "spent"
    "C_hex": "038a1...", // Required for "spent"
    "dleq": {
      // Required if keyset_version <= 2
      "e": "8a31...",
      "s": "4b2c...",
      "r": "9f1d..." // Only required for "spent"
    }
  },
  "leaf_index": 45012,
  "claimed_value": 1000,
  "actual_value": 0,
  "sibling_path": [{ "hash": "...", "sum": 0, "is_left": true }],
  "peaks": [{ "hash": "...", "sum": 0 }]
}
```

The `pol_receipt` (signed by the keyset-amount private key) proves the mint promised inclusion in the specified epoch, while the verified signature on the leaf data proves the note was legitimately issued or spent.

[tests]: tests/pol-tests.md
