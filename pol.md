# NUT-XX: Proof of Liabilities

`optional`

---

## Abstract

This document specifies a synchronized, epoch-based, stateless Proof of Liabilities (PoL) auditing scheme using a 256-depth Sparse Merkle Sum Tree (MS-SMT) with compact bitmasked sibling proofs and automated OpenTimestamps (OTS) commitments on-chain. This scheme allows wallets and external auditors to mathematically verify the outstanding liabilities of a Cashu mint.

---

## Architecture Overview

A Cashu mint acts as a custodian of backing assets. Outstanding liabilities are proven using two synchronized 256-depth Sparse Merkle Sum Trees (MS-SMT):

1. **Issued Tree (Promises):** Tracks all signed blinded messages $B'$.
2. **Spent Tree (Proofs Used):** Tracks all spent proof secrets $Y = \text{hash\_to\_curve}(\text{secret})$.

This prevents the mint from omitting or manipulating liabilities. Epoch-based state roots are periodically committed to the Bitcoin blockchain via OpenTimestamps, establishing an immutable history.

---

## MS-SMT Specifications

The MS-SMT has a fixed depth of 256 levels (level 0 at leaves, 256 at root).

### 1. Leaf Index and Keys

- **Issued Leaf Index ($I_{\text{issued}}$):**
  - Index: $\text{SHA256}(\text{UTF8}(B'\_{\text{hex}}))$ parsed as a big-endian integer.
  - Value: Face amount of the signed promise.
- **Spent Leaf Index ($I_{\text{spent}}$):**
  - Index: $\text{SHA256}(\text{hex}(Y_{\text{compressed}}))$ parsed as a big-endian integer.
  - Value: Face amount of the spent proof.

### 2. Node Structure & Hashing

Each node is represented as $(hash, sum\_value)$ where $hash$ is 32 bytes and $sum\_value$ is an 8-byte big-endian integer.

#### Default Empty Nodes

Precomputed default empty nodes at level $d \in [0, 256]$:

- **Level 0 (leaf):**
  - $hash_0 = \text{SHA256}(b"")$
  - $sum_0 = 0$
- **Level $d \ge 1$:**
  - $sum_d = 0$
  - $hash_d = \text{SHA256}(hash_{d-1} \mathbin{\Vert} hash_{d-1} \mathbin{\Vert} \text{bytes}_8(0) \mathbin{\Vert} \text{bytes}_8(0))$

#### Parent Node Computation

For siblings $L = (hash_L, sum_L)$ and $R = (hash_R, sum_R)$ at level $d$:

- $sum_P = sum_L + sum_R$
- $hash_P = \text{SHA256}(hash_L \mathbin{\Vert} hash_R \mathbin{\Vert} \text{bytes}_8(sum_L) \mathbin{\Vert} \text{bytes}_8(sum_R))$

---

## Epoch Manifests & On-Chain Commitments

Every epoch interval (e.g., 24 hours), the mint constructs and signs an Epoch Manifest:

1. **Sort Keysets:** Sort all unexpired keyset IDs alphabetically.
2. **Commitment Data:** Concatenate the UTF-8 `keyset_id`, 32-byte `root_issued_hash`, and 32-byte `root_spent_hash` for each keyset sequentially.
3. **Global Digest:** Compute $\text{SHA256}(\text{commitment\_data})$.
4. **OTS Submission:** Submit this digest to OTS calendar servers to obtain a binary receipt.
5. **Manifest Message:** Construct a colon-separated UTF-8 string:
   `"{keyset_id}:{epoch_index}:{timestamp}:{root_issued_hash}:{root_issued_sum}:{root_spent_hash}:{root_spent_sum}:{outstanding_balance}:{ots_receipt}"`
   where `ots_receipt` is the hex-encoded OTS receipt.
6. **Signing:** Sign the message with a BIP-340 Schnorr signature using the mint's master NUT-06 private key signing the SHA256 digest of this serialized manifest string.
7. **Publish:** Store and publish the signed manifest, signatures, and OTS receipts.

---

## Compact Bitmasked Sibling Proofs

To minimize proof size, default empty sibling nodes are omitted. Instead, the mint returns a 256-bit bitmask where the $d$-th bit indicates if the sibling at level $d$ is non-empty ($1$) or empty ($0$, to be replaced by the precomputed default empty node).

For detailed examples and test vectors, see the [test vectors][tests].

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
  "signing_pubkey": "020...",
  "root_issued": { "hash": "8f3c...", "sum": 1000000 },
  "root_spent": { "hash": "4d1a...", "sum": 450000 },
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
      "index": "8a31...",
      "value": 1000,
      "compact_mask": "0x301a...",
      "siblings": [{ "hash": "b4a1...", "sum": 500 }]
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

- **Response:** Same format as `/proofs/issued` with the $Y$ point hex string in the `item` field.

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

- **Message to Sign:** `<point_hex>:<target_epoch_decimal_string>`
  - **Output:** `B'_hex:target_epoch`
  - **Spent Input:** `Y_hex:target_epoch`

| Version   | Curve     | Signature Details                                                                                                                                                                                                                                                              |
| :-------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00`/`01` | secp256k1 | BIP340 Schnorr over $\text{SHA256}(\text{message})$. Verified against `public_keys[amount]`.                                                                                                                                                                                   |
| `02`      | BLS12-381 | $\sigma = a \cdot H_{G1}(\text{message})$ (compressed G1). Verified via $e(\sigma, G2) == e(H_{G1}(\text{message}), K)$ where $K = \text{public\_keys}[amount]$ (G2). $H_{G1}$ is RFC 9380 `hash_to_curve_G1` under DST `"Cashu_PoL_Receipt_BLS12381G1_XMD:SHA-256_SSWU_RO_"`. |

### 3. Response Alignment

Returned receipts are fully order-preserving (1:1 index matching of request inputs/outputs):

- **Mint (`POST /v1/mint/bolt11` & `/v1/mint/bolt11/batch`):** Nested in `pol_receipt` of each `BlindSignature` inside `signatures`.
- **Swap (`POST /v1/swap`):**
  - Outputs: Nested in `pol_receipt` of each `BlindSignature` inside `signatures`.
  - Inputs: Top-level `spent_receipts: List[PolReceipt]` mapping to the request's `inputs`.
- **Melt (`POST /v1/melt/bolt11`):** Top-level `spent_receipts: List[PolReceipt]` mapping to the request's `inputs`.

---

## Verification Protocol

Wallets periodically audit their held and spent tokens:

### Step 1: Verify Manifest Signature

Verify the BIP-340 Schnorr signature `mint_signature` against the mint's master public key (`signing_pubkey` from `/v1/info`) over the SHA256 digest of the constructed epoch string.

### Step 2: Validate OpenTimestamps Attestation

1. **Upgrade Receipt:** Post `ots_receipt` to a calendar upgrade endpoint (e.g., `https://alice.btc.calendar.opentimestamps.org/upgrade`) to fetch the Merkle path.
2. **Scan for Block:** Find block header attestation tag `0x00 0x05` (`A_BLOCKHEADER`). If pending tag `0x00 0x06` is found, the receipt is still awaiting block confirmation.
3. **Parse Height:** Decode the Bitcoin block height (serialized as a VarInt) immediately following the tag.
4. **Confirm:** Check via an independent explorer (e.g., `https://mempool.space/api/...`) that the block height exists, matches the manifest timestamp, and has sufficient confirmations.

### Step 3: Validate Issued Path Walks

For each held active token:

1. Reconstruct $B'$ (BDHKE: $B' = Y + rG$; BLS: $B' = r \cdot Y$).
2. Leaf index $I = \text{SHA256}(B')$ parsed as a big-endian integer.
3. Walk up the 256 levels:
   - For $d \in [0, 255]$:
     - The $d$-th bit of the bitmask determines child position.
     - If the $d$-th bit is $1$, pop the next sibling from the proof's `siblings`.
     - If $0$, use default empty node $(default\_hash[d], 0)$.
     - Compute the parent node $(hash, sum)$ at level $d+1$.
4. Ensure the final root matches `root_issued`.

### Step 4: Validate Spent Path Walks

For spent tokens (history):

1. Compute $Y = \text{hash\_to\_curve}(\text{secret})$.
2. Leaf index $I = \text{SHA256}(Y)$ parsed as a big-endian integer.
3. Walk up the tree and verify matching `root_spent`.

### Step 5: Verify Liabilities Equation

Ensure:
$$\text{outstanding\_balance} == \text{root\_issued\_sum} - \text{root\_spent\_sum}$$

---

## Cryptographic Fraud Challenge

If verification fails, the wallet generates a **Fraud Challenge**—a self-contained JSON document proving perjury.

- **BDHKE (Keyset Version <= v2):** Includes the Discrete Logarithm Equality (DLEQ) proof `{e, s}` (issued) or `{e, s, r}` (spent) to allow third-party verification.
- **BLS (Keyset Version >= v3):** No DLEQ proof is required; the BLS signature ($C'$ or $C$) can be verified directly against the keyset-amount public key.

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
  "index": "8a31...",
  "claimed_value": 1000,
  "actual_value": 0,
  "compact_mask": "0x...",
  "siblings": [{ "hash": "...", "sum": 0 }]
}
```

The `pol_receipt` (signed by the keyset-amount private key) proves the mint promised inclusion in the specified epoch, while the verified signature on the leaf data proves the note was legitimately issued or spent.

[tests]: tests/pol-tests.md
