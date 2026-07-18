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

1. **Sort Keysets:** Normalize all unexpired `keyset_id` strings (both active and inactive) to lowercase hexadecimal representation, and then sort them alphabetically (lexicographically by their ASCII values).
2. **Commitment Data:** Prepend the 32-byte binary `previous_global_digest` of the previous epoch (for the first epoch, this MUST be 32 bytes of zeros `0x00...00`). Then concatenate the UTF-8 lowercase `keyset_id`, 8-byte big-endian `issued_mmr_size`, 32-byte binary `issued_mmr_root_hash`, 8-byte big-endian `issued_mmr_root_sum`, 8-byte big-endian `spent_mmr_size`, 32-byte binary `spent_mmr_root_hash`, and 8-byte big-endian `spent_mmr_root_sum` for each keyset sequentially.
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
7. **Publish:** Store and publish the signed manifests, signatures, OTS receipts, `global_digest`, and the ordered `epoch_keysets` array used to construct `commitment_data`. Each entry in `epoch_keysets` MUST contain the `keyset_id`, `issued_mmr_size`, `issued_mmr_root_hash`, `issued_mmr_root_sum`, `spent_mmr_size`, `spent_mmr_root_hash`, and `spent_mmr_root_sum`; the array MUST contain every unexpired keyset exactly once and match the corresponding signed manifests. This lets verifiers reconstruct the exact Global Digest preimage.

---

## sum-MMR Inclusion Proof Structure

To minimize verification overhead on clients, sum-MMR inclusion proofs provide the minimal sibling path and peak forest necessary to reconstruct the single bagged commitment:

1. **Leaf Index:** The sequential 0-based insertion index of the leaf.
2. **Sibling Path:** A list of `(hash, sum, is_left)` sibling nodes traversed from the leaf up to its local mountain peak.
3. **Peaks:** The list of all peak roots `(hash, sum)` of the MMR forest at that epoch (of size N).

The `leaf_index` is not trusted metadata. A verifier MUST derive it from the proof. Derive the ordered peak heights from the set bits of the MMR leaf count N (highest to lowest). If the sibling path has length h, it MUST terminate at the unique peak of height h. For each sibling at path level j, starting with j = 0 at the leaf, `is_left = true` means the current node is the right child and contributes 2^j to its local offset; `is_left = false` contributes 0. The sum of that local offset and the widths of all preceding peaks MUST equal `leaf_index`.

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
  "global_digest": "7c6d...",
  "epoch_keysets": [
    {
      "keyset_id": "009a6154b71113b7",
      "issued_mmr_size": 125000,
      "issued_mmr_root_hash": "8f3c...",
      "issued_mmr_root_sum": 1000000,
      "spent_mmr_size": 52000,
      "spent_mmr_root_hash": "4d1a...",
      "spent_mmr_root_sum": 450000
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

1. **Reconstruct the Global Digest:** Reconstruct `commitment_data` from `previous_global_digest` and the published, ordered `epoch_keysets` array exactly as specified in Epoch Manifests. Compute its SHA256 hash, require it to equal the published `global_digest`, and require each entry to match its corresponding signed keyset manifest.
2. **Verify or Upgrade Receipt:** Deserialize the `ots_receipt` and require its starting digest to equal the reconstructed Global Digest. If the receipt contains a pending attestation tag (`0x83dfe30d2ef90c8e`) and has remained unconfirmed/pending after a maximum timeout bound (MUST NOT be more than 24 hours from the manifest `timestamp`), the verifier MUST treat it as an **audit failure**, rather than waiting indefinitely.
3. **Upgrade Proof (if pending):** If the receipt is still pending but within the timeout window, the verifier can attempt to fetch the Merkle path by posting the `ots_receipt` to a calendar upgrade endpoint (e.g., `https://alice.btc.calendar.opentimestamps.org/upgrade`). Note, however, that a properly functioning mint carries the upgrade burden and should publish already upgraded, offline-verifiable receipts.
4. **Execute and Verify the Proof:** Using a conforming OpenTimestamps implementation, execute every append, prepend, and hashing operation from the starting digest to a Bitcoin block-header attestation (`0x0588960d73d71901`). Decode its block height, obtain that block from an independently validated Bitcoin node, and require the operation result to match the block's committed Merkle root. Merely finding an attestation tag and a real block at the claimed height is insufficient.
5. **Confirm Block Timestamp:** Require the independently validated block to have sufficient confirmations. Furthermore, verify that the Bitcoin block's timestamp is within a reasonable tolerance window (e.g., within 4 hours) of the manifest `timestamp`, rather than requiring an exact match.

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
5. Derive the leaf position from the peak heights and `is_left` bits as specified in the sum-MMR Inclusion Proof Structure, and require it to equal `leaf_index`.
6. Perform Peak Bagging on `peaks` from right to left:
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

## Cryptographic Fraud Challenges & Mint Responses

When a client or auditor detects a verification failure, they can generate a **Fraud Challenge**—a self-contained cryptographic proof of mint perjury. To prevent malicious clients from publishing false challenges to slander an honest mint, every challenge must be falsifiable. The mint can refute any false challenge by publishing a corresponding cryptographic **Defense/Response**.

### Note on Spent-Side Inflation & Keyset Rotations

A naive threat model might suggest that a malicious mint could fabricate fake spent leaves (by appending random curve points `Y` to the Spent MMR) to artificially deflate its proven outstanding liabilities. However, because the mint owns the private signing keys for its keysets, a malicious mint can always generate valid ecash signatures (`C'`) for themselves, and then "validly" spend this self-signed fake ecash. Because the mint holds the preimages/secrets for these spends, a preimage/spend verification challenge is futile and cannot prevent this behavior.

Instead, spent-side inflation is caught naturally by the **append-only nature of the MMR** and **keyset rotations/deactivations**:

1. **Append-Only Immutability:** Once a leaf is appended to either MMR, it is permanent and cannot be deleted. If the mint fabricates a spend, that spent leaf is locked into history forever.
2. **Keyset Rotation:** Eventually, keysets are deactivated and later expire. Once deactivated, no new ecash can be issued under that keyset, but existing ecash can still be spent until expiry. Once expired, no ecash can be issued or spent under that keyset.
3. **Redemption Wind-Down:** As genuine users redeem their remaining ecash, the outstanding balance must mathematically wind down to 0. If the mint inflated the Spent MMR (claiming more ecash was spent than was actually issued to real users), the genuine outstanding tokens remaining in circulation will eventually exceed the _claimed_ remaining liabilities (or the claimed liabilities will become negative/insufficient to cover the real ecash redemptions). Because the mint cannot retroactively delete or rewrite their historical MMR leaves, they will be caught when they cannot honor valid redemptions or when their outstanding balance equation breaks.

As a result, there are four recognized categories of Fraud Challenges, detailed below.

---

### 1. Leaf Omission or Value Mismatch (`leaf_omission_or_mismatch`)

- **Description:** A client holds a valid, signed transactional PoL receipt promising inclusion of a leaf in epoch `E` (or earlier), but the leaf is either missing from the public MMR for epoch `E` (or later), or is present with an incorrect value (sum).
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

  - `pol_receipt.signature` must be a valid signature under the keyset-amount public key corresponding to `leaf_data.value` (denomination) over the domain-separated receipt message (`"Cashu_PoL_Receipt_Issued:..."` or `"Cashu_PoL_Receipt_Spent:..."` for the specified `target_epoch`).

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
      "sibling_path": [{ "hash": "b4a1df...", "sum": 500, "is_left": true }],
      "peaks": [{ "hash": "f29a2c...", "sum": 20000 }]
    }
  }
  ```
- **Mint's Defense / Response & Verification:**
  - **If the mint is NOT in the wrong:** The mint must publish the above response containing the valid sum-MMR inclusion proof for the challenged `item` at `epoch_index` with the correct `value`.
  - **Verification:** Third parties verify that the inclusion proof walk computes up to one of the mountain peaks, and that the peaks recursively peak-bagged from right-to-left match the manifest's `issued_mmr_root_hash` / `spent_mmr_root_hash` and sum. If it verifies, the challenge is refuted.

---

### 2. History Rewriting or Append-Only Violation (`append_only_violation`)

- **Description:** The mint has modified, deleted, or reordered past leaves. This changes the internal hashes/sums of the tree, violating the strict append-only prefix preservation property.
- **Challenge Schema:**
  The challenger presents two signed epoch manifests along with two valid inclusion proofs whose proof-derived positions are the exact same `leaf_index`, showing a mismatch.

  ```json
  {
    "challenge_type": "append_only_violation",
    "keyset_id": "009a6154b71113b7",
    "epoch_index_1": 11,
    "epoch_index_2": 12,
    "leaf_index": 45012,
    "proof_1": {
      "item": "02b1a...",
      "value": 1000,
      "sibling_path": [{ "hash": "b4a1...", "sum": 500, "is_left": true }],
      "peaks": [{ "hash": "f29a...", "sum": 20000 }]
    },
    "proof_2": {
      "item": "02b1a...",
      "value": 500,
      "sibling_path": [{ "hash": "9c1a...", "sum": 100, "is_left": true }],
      "peaks": [{ "hash": "3d2a...", "sum": 25000 }]
    }
  }
  ```

  - Before comparing the proofs, the verifier MUST independently derive each leaf position from its sibling path and peak layout as specified in the sum-MMR Inclusion Proof Structure and reject the challenge unless both derived positions equal the claimed `leaf_index`. Here, `proof_1` is valid for the manifest at `epoch_index_1`, and `proof_2` is valid for the manifest at `epoch_index_2`. However, either the leaf value changed (e.g., from `1000` to `500`), the item changed, or the sibling paths do not satisfy prefix preservation.

- **Mint's Defense / Response:**
  - There is **no valid response** if the challenger's manifests are signed by the mint and both inclusion proofs verify against those manifests. The mint is proven fraudulent.
  - **If the mint is NOT in the wrong:** The mint can only refute the challenge by demonstrating that one of the presented inclusion proofs is mathematically invalid (i.e., it does not correctly hash up to the peaks of that epoch's signed manifest) or that the manifest signatures are forged.

---

### 3. Manifest Equivocation (`manifest_equivocation`)

- **Description:** The mint has published two different, conflicting versions of the epoch manifest for the same keyset and epoch index (e.g., to hide liabilities from one group of users while showing them to another).
- **Challenge Schema:**
  The challenger presents two complete, distinct, validly signed epoch manifests with the same `keyset_id` and `epoch_index` but any difference in their signed content. Each manifest MUST include every field in the serialized manifest message so that third parties can reconstruct its signed digest.
  ```json
  {
    "challenge_type": "manifest_equivocation",
    "manifest_a": {
      "keyset_id": "009a6154b71113b7",
      "epoch_index": 12,
      "timestamp": "2026-06-11T12:00:00Z",
      "previous_global_digest": "4b8e...",
      "issued_mmr_size": 45013,
      "issued_mmr_root_hash": "8f3c...",
      "issued_mmr_root_sum": 25000,
      "spent_mmr_size": 12001,
      "spent_mmr_root_hash": "7d4e...",
      "spent_mmr_root_sum": 9000,
      "outstanding_balance": 16000,
      "mint_signature": "<signature_a>"
    },
    "manifest_b": {
      "keyset_id": "009a6154b71113b7",
      "epoch_index": 12,
      "timestamp": "2026-06-11T12:00:00Z",
      "previous_global_digest": "4b8e...",
      "issued_mmr_size": 45013,
      "issued_mmr_root_hash": "9a2b...",
      "issued_mmr_root_sum": 24000,
      "spent_mmr_size": 12001,
      "spent_mmr_root_hash": "7d4e...",
      "spent_mmr_root_sum": 9000,
      "outstanding_balance": 15000,
      "mint_signature": "<signature_b>"
    }
  }
  ```
- **Mint's Defense / Response:**
  - Third parties serialize each manifest as specified in Epoch Manifests, compute each SHA256 digest, and verify both BIP-340 signatures against the mint's master NUT-06 public key. They then confirm that the manifests have the same `keyset_id` and `epoch_index` but differ in at least one signed field.
  - There is **no valid response** or defense when both signatures verify. Any signed equivocation is definitive proof of malicious behavior.

---

### 4. sum-MMR Consistency Violation (`sum_mmr_consistency_violation`)

- **Description:** An auditor challenges the mint to prove that the sum-MMR tree at epoch `E_2` is a valid append-only extension of the tree at `E_1` (`E_2 > E_1`). Unlike Challenge 2 (`append_only_violation`), this is an interactive, zero-knowledge challenge that enables third-party watchtowers to audit the tree's historical integrity without holding or revealing private client tokens.
- **Challenge Schema:**
  The challenger presents the two validly signed epoch manifests for `E_1` and `E_2`. The burden of proving consistency is placed entirely on the mint.
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
      "old_size": 125000,
      "new_size": 126500,
      "proof_hashes": [{ "hash": "8f3c...", "sum": 1000000, "height": 3 }]
    }
  }
  ```
- **Mint's Defense / Response & Verification:**
  - **If the mint is NOT in the wrong:** The mint must respond to the challenge by publishing the **correct, valid MMR consistency proof** specified in the response schema (consisting of the list of sibling/peak proof hashes, sums, and heights) that mathematically merges the peaks of epoch `E_1` and the new elements to produce the peaks of epoch `E_2`.
  - **Verification:** Third parties verify the mint's published consistency proof against the root hashes and sums in the two signed manifests. If the proof successfully validates the deterministic transition, the challenge is refuted and proven false. Challenge discovery, notification, and response deadlines are coordination-policy concerns outside this NUT. Silence alone is not cryptographic proof of fraud; each third-party auditor decides whether a non-response is actionable under its published policy and only after the mint has acknowledged or otherwise verifiably received the challenge.

[tests]: tests/pol-tests.md
