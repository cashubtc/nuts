# NUT Draft: Proof of Liabilities (Solvency Audits)

`optional`

---

## Abstract

This document specifies a synchronized, epoch-based, stateless Proof of Liabilities (PoL) auditing scheme using a 256-depth Sparse Merkle Sum Tree (MS-SMT) with compact bitmasked sibling proofs and automated OpenTimestamps commitments on-chain. This scheme allows wallets and external auditors to mathematically verify the solvency of a Cashu mint.

## Motivation

A Cashu mint acts as a custodian of backing assets. To prove that the mint is solvent, it must prove that its outstanding liabilities (total issued ecash minus total spent/redeemed ecash) are fully backed by its outstanding reserves, and that no individual users' balances are hidden or manipulated.

This is solved using two synchronized Sparse Merkle Sum Trees (MS-SMT):
1. **Issued Tree (Promises):** Tracks all blinded messages `B'` signed by the mint.
2. **Spent Tree (Proofs Used):** Tracks all spent proof secrets `Y` (where `Y = hash_to_curve(secret)`) that have been redeemed or swapped at the mint.

Using an MS-SMT of depth 256 ensures that:
- Every active or spent token has a unique, deterministic leaf index calculated directly from its public key/secret hash.
- This prevents the mint from omitting or "double-bookkeeping" liabilities without being cryptographically caught.
- Epoch-based synchronization with OpenTimestamps commits the state roots to the Bitcoin blockchain periodically (e.g., daily), creating an immutable history.

## Sparse Merkle Sum Tree (MS-SMT) Specifications

The MS-SMT has a fixed depth of 256 levels (from level 0 at the leaves to level 256 at the root).

### 1. Leaf Index and Keys

Leaf indices are calculated deterministically:

- **Issued Leaf Index (`I_issued`):**
  1. Compute `h_B` as the SHA256 hash of the UTF-8 encoded `b_` (blinded message `B'` hex string).
  2. Parse `h_B` as a big-endian integer to obtain the leaf index.
  3. The leaf node represents a signed promise with a sum value equal to the promise's face amount.

- **Spent Leaf Index (`I_spent`):**
  1. Compute `Y = hash_to_curve(secret)`.
  2. Compute `h_Y` as the SHA256 hash of the hexadecimal string representation of the compressed public key `Y`.
  3. Parse `h_Y` as a big-endian integer to obtain the leaf index.
  4. The leaf node represents a spent proof with a sum value equal to the proof's face amount.

### 2. Node Structure & Hashing

Each node in the sum tree is a pair `(hash, sum_value)` where:
- `hash` is a 32-byte binary digest.
- `sum_value` is an integer representing the aggregated satoshi amount.

#### Default Empty Nodes
To represent empty branches without storing 2^256 nodes, default empty node values are precomputed for each level `d` from 0 to 256:
- **At level 0 (leaf):**
  - `hash_0` is the SHA256 hash of empty bytes (`b""`).
  - `sum_0` is `0`.
- **At level d (for d >= 1):**
  - `sum_d` is `0` (the sum of both default child sums: `0 + 0`).
  - `hash_d` is the SHA256 hash of the concatenated bytes:
    `hash_{d-1} + hash_{d-1} + bytes_8(sum_{d-1}) + bytes_8(sum_{d-1})`
    where `bytes_8(x)` is the 8-byte big-endian representation of integer `x`.

#### Parent Node Computation
For any level `d` from 0 to 255, two neighboring sibling nodes `L = (hash_L, sum_L)` and `R = (hash_R, sum_R)` at level `d` are aggregated into parent node `P = (hash_P, sum_P)` at level `d+1`:
- `sum_P` is the integer sum: `sum_L + sum_R`
- `hash_P` is the SHA256 hash of the concatenated bytes:
  `hash_L + hash_R + bytes_8(sum_L) + bytes_8(sum_R)`

---

## Epoch Manifest Creation and On-Chain Commitments

To prevent the mint from rewriting historic trees or showing different root values to different users, roots are committed to epochs synchronized across the entire mint.

Every epoch interval (e.g., 24 hours), the mint builds the Issued and Spent trees for all unexpired keysets, publishes on-chain commitments, and signs the resulting manifests:

1. **Sort Keysets:** Retrieve all unexpired keyset IDs and sort them alphabetically.
2. **Construct Commitment Data:** Construct a single contiguous sequence of bytes by concatenating the data of each sorted keyset sequentially. For each keyset, append:
   - The UTF-8 encoded keyset ID string.
   - The 32-byte binary representation of the `root_issued_hash`.
   - The 32-byte binary representation of the `root_spent_hash`.
3. **Calculate Global Digest:** Compute the SHA256 hash of the complete concatenated commitment bytes.
4. **Submit to OTS:** Submit this single SHA256 global digest to OpenTimestamps (OTS) calendar servers to obtain a binary on-chain proof of existence (the OTS receipt).
5. **Construct Manifest Message:** For each keyset, construct a colon-separated UTF-8 message string binding the keyset's status and the on-chain OTS receipt. The format is:
   `"{keyset_id}:{epoch_index}:{timestamp}:{root_issued_hash}:{root_issued_sum}:{root_spent_hash}:{root_spent_sum}:{outstanding_balance}:{ots_receipt}"`
   where `ots_receipt` is the hex-encoded representation of the OTS receipt from step 4.
6. **Sign Manifest Message:** Sign the constructed UTF-8 message using the mint's master NUT-06 private key (the private key corresponding to the public `pubkey` advertised in the `/v1/info` response).
7. **Publish & Store Manifest:** Store and publish the signed manifest (including the signature, OTS receipt, roots, sums, and metadata). This allows wallets and external auditors to easily verify manifest signatures using the mint's publicly known master key.

---

## Compact Bitmasked Sibling Proofs

Rather than returning all 256 sibling nodes (which would require over 10 KB of data per proof), the mint returns a **Compact Sibling Proof** leveraging a bitmask:
1. If a sibling at level `d` is a default empty node, it is **omitted** from the returned list of siblings.
2. A 256-bit bitmask is returned. The `d`-th bit of the mask is set to `1` if the sibling at level `d` is non-empty (included in the response), and `0` if the sibling is empty (and should be substituted with the precomputed default empty node for level `d`).

---

## HTTP API Specifications

### 1. Get Keyset Manifest
`GET /v1/pol/{keyset_id}/manifest`

**Query Parameters:**
- `epoch_index` (optional, integer): Defaults to the latest epoch if omitted.

**Response:**
```json
{
  "keyset_id": "009a6154b71113b7",
  "epoch_index": 1,
  "timestamp": "2026-06-11T12:00:00Z",
  "signing_pubkey": "020...",
  "root_issued": {
    "hash": "8f3c...",
    "sum": 1000000
  },
  "root_spent": {
    "hash": "4d1a...",
    "sum": 450000
  },
  "outstanding_balance": 550000,
  "ots_receipt": "<hex_encoded_ots_file_content>",
  "mint_signature": "<hex_encoded_signature>"
}
```

### 2. Query Issued Tree Proofs
`POST /v1/pol/{keyset_id}/proofs/issued`

**Query Parameters:**
- `epoch_index` (optional, integer): Defaults to latest.

**Request Body:**
```json
{
  "blinded_messages": [
    "02b1a..."
  ]
}
```

**Response:**
```json
{
  "proofs": [
    {
      "item": "02b1a...",
      "index": "8a31...",
      "value": 1000,
      "compact_mask": "0x301a...",
      "siblings": [
        {
          "hash": "b4a1...",
          "sum": 500
        }
      ]
    }
  ]
}
```

### 3. Query Spent Tree Proofs
`POST /v1/pol/{keyset_id}/proofs/spent`

**Query Parameters:**
- `epoch_index` (optional, integer): Defaults to latest.

**Request Body:**
```json
{
  "ys": [
    "02b1a..."
  ]
}
```

**Response:** Same format as `/proofs/issued` where each returned item in the response contains the `Y` point hex string in the `item` field.

---

## Signed Transactional Proof of Liability Receipts

To prevent the mint from denying or delaying the inclusion of user actions in the publicized sum trees (e.g., claiming "I received your inputs/outputs but they are not included in this epoch yet, check the next one"), the mint **MUST** return a cryptographically signed **PoL Receipt** for every single individual input (ecash note) spent and every output (blind signature) returned during state-transitioning actions (`mint`, `melt`, and `swap`).

Signing individual inputs and outputs (rather than transaction-level batches) ensures modular validation and allows the user to hold the mint cryptographically accountable for each individual note.

### 1. Receipt JSON Schema

Every individual output (`BlindSignature`) and spent input includes a nested `pol_receipt` object:

```json
{
  "target_epoch": 12,
  "signature": "<hex_encoded_signature>"
}
```

### 2. Message Formats and Keys

Each receipt `signature` is a BIP340 Schnorr signature on the SHA-256 hash of the formatted message to sign. It is produced by the mint using the keyset-specific private key of the corresponding value (amount) for that input or output.

#### A. Outputs (Blinded Messages)
For each returned blind signature, the mint returns a nested `pol_receipt`.
- **Message format to sign:**
  `{B_hex}:{target_epoch}`
  where `{B_hex}` is the hex-encoded string of the output's BlindedMessage `B'`, and `{target_epoch}` is the target upcoming epoch index string.
- **Signing key:** The keyset private key corresponding to the output's specific amount (`keyset.private_keys[amount]`).
- **Verification:** Wallets verify the BIP340 Schnorr signature on the SHA-256 hash of the formatted message against the keyset public key corresponding to the output's amount (`keyset.public_keys[amount]`).

#### B. Spent Inputs (Ecash Proofs)
For each spent proof in a swap or melt, the mint returns a list of `spent_receipts` in the response.
- **Message format to sign:**
  `{Y_hex}:{target_epoch}`
  where `{Y_hex}` is the hex-encoded public key string of the spent proof's curve point `Y = hash_to_curve(secret)`, and `{target_epoch}` is the target upcoming epoch index string.
- **Signing key:** The keyset private key corresponding to the spent input's specific amount (`keyset.private_keys[amount]`).
- **Verification:** Wallets verify the BIP340 Schnorr signature on the SHA-256 hash of the formatted message against the keyset public key corresponding to the spent input's amount (`keyset.public_keys[amount]`).

### 3. Response Structure & Alignment

To maintain simplicity and zero overhead, returned receipts are **fully order-preserving** (matching 1:1 indexes of inputs and outputs of the request):

- **Mint responses (`POST /v1/mint/bolt11` and `POST /v1/mint/bolt11/batch`):** Each returned `BlindSignature` object inside the `signatures` array has its own nested `pol_receipt`.
- **Swap responses (`POST /v1/swap`):** 
  - Output receipts are nested inside each `BlindSignature` object in the `signatures` array.
  - Input spent receipts are returned as a top-level list of receipts `spent_receipts: List[PolReceipt]` where `spent_receipts[i]` maps to `inputs[i]` of the request.
- **Melt responses (`POST /v1/melt/bolt11`):** Spent receipts are returned as a top-level list `spent_receipts: List[PolReceipt]` where `spent_receipts[i]` maps to `inputs[i]` of the request.

---

## Verification Protocol

Wallets **SHOULD** periodically audit their held tokens using the following 5-step solvency verification protocol:

### Step 1: Verify Manifest Signature
Verify the `mint_signature` against `signing_pubkey` for the formatted epoch string. Ensure that the `signing_pubkey` matches the mint's master public key advertised in the NUT-06 `/v1/info` endpoint response.

### Step 2: Validate OpenTimestamps Attestation
Parse the binary `ots_receipt` to verify that the root hashes were committed to the Bitcoin blockchain. To verify anchoring programmatically without external library dependencies:
1. **Upgrade Proof (Optional):** Submit the binary `ots_receipt` to a public calendar server upgrade endpoint (e.g., `https://alice.btc.calendar.opentimestamps.org/upgrade`). If a mined block contains the commitment, the calendar returns an upgraded receipt containing the on-chain Merkle path.
2. **Scan for Block Attestation:** Scan the binary upgraded receipt for the Bitcoin Block Header attestation tag (`0x00` followed by `0x05` for `A_BLOCKHEADER`).
3. **Parse Block Height:** Parse the Bitcoin block height immediately following the tag (serialized as a standard variable-length VarInt).
4. **Verify Block Confirmation:** Query any independent public Bitcoin block explorer API (e.g. `https://mempool.space/api/blocks/tip/height`) to check that the parsed block height exists, matches the manifest timestamp, and has sufficient confirmations. If present, the attestation is fully confirmed. If the pending tag `0x00 0x06` is found instead, the receipt has been submitted to the calendar but is still awaiting blockchain anchoring.

### Step 3: Validate Issued Path Walks
For each active token held:
1. Reconstruct `B'` (if only holding `C` and `r`, compute `B' = Y + rG`).
2. Compute the leaf index by parsing the SHA256 hash of `B'` as a big-endian integer.
3. Reconstruct the root hash and sum by walking up the 256 levels:
   - For `d` from 0 to 255:
     - The `d`-th bit of the bitmask determines whether the current node is the left or right child.
     - If the `d`-th bit of the compact mask is `1`, pop the next sibling from the response `siblings` array.
     - If `0`, use the precomputed default empty node `(default_hash[d], 0)`.
     - Hash parent and sum to get the node at level `d+1`.
4. Ensure the computed root matches `root_issued`.

### Step 4: Validate Spent Path Walks
For all spent tokens (history):
1. Compute `Y = hash_to_curve(secret)`.
2. Compute the leaf index by parsing the SHA256 hash of `Y` as a big-endian integer.
3. Perform the same walk up to verify inclusion in the `root_spent` tree.

### Step 5: Verify Solvency Equation
Check that the outstanding balance reported matches:
`outstanding_balance == root_issued_sum - root_spent_sum`

---

## Cryptographic Fraud Challenge (JSON format)

If any verification path walk fails (e.g., the leaf is not present or has a sum value different from the token's face value, or the computed root doesn't match the signed root), the wallet generates a **Fraud Challenge**. This is an aggregated, self-contained JSON document that can be shared publicly to mathematically prove the mint committed perjury.

To prove that the ecash note (input or output) is genuinely from that mint and of the claimed keyset, a third party must be able to verify the mint's signature on it. Therefore, the fraud challenge contains the original blinded message and blind signature (for `issued` proofs), or the nullifier and unblinded signature (for `spent` proofs), as well as a DLEQ proof if the keyset version requires it:

1. **For keyset version <= v2 (BDHKE):**
   - Verification of the BDHKE signature requires a Discrete Logarithm Equality (DLEQ) proof to be verified by a third party.
   - For `issued` proofs: The challenge includes `B_hex`, the blind signature `C_prime_hex`, and the DLEQ proof `dleq` (consisting of `{e, s}`) returned by the mint in `BlindSignature` (NUT-12).
   - For `spent` proofs: The challenge includes the nullifier `Y_hex`, the unblinded signature `C_hex`, and the DLEQ proof `dleq` (consisting of `{e, s, r}`, where `r` is the secret's blinding factor) returned in `Proof` (NUT-12).

2. **For keyset version >= v3 (BLS):**
   - No DLEQ proof is necessary. A third party can directly verify the BLS signature (`C_prime_hex` or `C_hex`) against the public key of the keyset corresponding to the token's value.

### Challenge JSON Schema

```json
{
  "challenge_type": "pol_fraud_proof",
  "keyset_id": "009a6154b71113b7",
  "keyset_version": 2,
  "epoch_index": 1,
  "manifest": { ... },
  "pol_receipt": {
    "target_epoch": 1,
    "signature": "<hex_encoded_signature>"
  },
  "proof_type": "issued | spent",
  "leaf_data": {
    "B_hex": "02b1a...",             // Blinded message B' (required for proof_type "issued")
    "C_prime_hex": "038a1...",       // Blind signature C' (required for proof_type "issued")
    "Y_hex": "02b1a...",             // Nullifier Y = hash_to_curve(secret) (required for proof_type "spent")
    "C_hex": "038a1...",             // Unblinded signature C (required for proof_type "spent")
    "dleq": {                        // Required if keyset_version <= 2
      "e": "8a31...",
      "s": "4b2c...",
      "r": "9f1d..."                 // Blinding factor r (only required/included for proof_type "spent")
    }
  },
  "index": "8a31...",
  "claimed_value": 1000,
  "actual_value": 0,
  "compact_mask": "0x...",
  "siblings": [ ... ]
}
```

This format provides all mathematical inputs needed for any independent third party to verify the forgery without relying on trust. The inclusion of the `pol_receipt` (signed by the keyset-amount private key) serves as the indisputable proof that the mint previously promised to include this note in the specified epoch, while the verified signature on the leaf data proves that the note itself was legitimately issued/processed by that mint.
