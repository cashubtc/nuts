# Proof of Liabilities (PoL) Test Vectors

This document provides test vectors for verifying implementations of the Proof of Liabilities (PoL) specification (NUT-XX), including Merkle Mountain Range with Sums (sum-MMR) computations, right-to-left peak bagging, and epoch manifest BIP-340 Schnorr signing.

---

## 1. Node Hashing and Peak Bagging Formulations

Each node in the sum-MMR has the structure `(hash, sum)` where `hash` is 32 bytes and `sum` is an 8-byte big-endian unsigned integer (uint64).

### Parent Node Hashing

Given left child $L = (\text{hash}_L, \text{sum}_L)$ and right child $R = (\text{hash}_R, \text{sum}_R)$:
- $\text{sum}_P = \text{sum}_L + \text{sum}_R$
- $\text{hash}_P = \text{SHA256}(\text{hash}_L \mathbin{\Vert} \text{hash}_R \mathbin{\Vert} \text{bytes}_8(\text{sum}_L) \mathbin{\Vert} \text{bytes}_8(\text{sum}_R))$

### Peak Bagging Hashing (Right-to-Left)

For a list of MMR peaks $P_1, P_2, \dots, P_k$ of decreasing heights, they are recursively bagged from right to left:
- $B_k = P_k$
- $B_i = \text{Parent}(P_i, B_{i+1}) \quad \text{for } i \in [1, k-1]$
- The final bagged commitment root is $B_1$.

---

## 2. 2-Leaf MMR Tree Computation

This test vector uses two leaf nodes, representing a sum-MMR of size 2. These two leaves are merged at height 1 into a single peak root.

### Leaves

| Blinded Message B\_ (33-Byte Compressed Pubkey Hex)                  | Value | Hash (SHA256 of Raw Bytes)                                         | Leaf Index |
| :------------------------------------------------------------------- | :---- | :----------------------------------------------------------------- | :--------- |
| `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4` | 100   | `6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85` | 0          |
| `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a` | 250   | `aa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f` | 1          |

### Bagged Root

- **Hash:** `90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f`
- **Sum:** `350`

### Sibling Inclusion Proofs

#### Proof for `02b1a03e...` (Index 0)

- **Leaf Index:** 0
- **Sibling Path:**
  ```json
  [
    {
      "hash": "aa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f",
      "sum": 250,
      "is_left": false
    }
  ]
  ```
- **Peaks:**
  ```json
  [
    {
      "hash": "90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f",
      "sum": 350
    }
  ]
  ```

#### Proof for `02c3a506...` (Index 1)

- **Leaf Index:** 1
- **Sibling Path:**
  ```json
  [
    {
      "hash": "6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85",
      "sum": 100,
      "is_left": true
    }
  ]
  ```
- **Peaks:**
  ```json
  [
    {
      "hash": "90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f",
      "sum": 350
    }
  ]
  ```

---

## 3. 3-Leaf MMR Tree Computation

This test vector uses three leaf nodes, representing a sum-MMR of size 3.

### Leaves

| Blinded Message B\_ (33-Byte Compressed Pubkey Hex)                  | Value | Hash (SHA256 of Raw Bytes)                                         | Leaf Index |
| :------------------------------------------------------------------- | :---- | :----------------------------------------------------------------- | :--------- |
| `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4` | 100   | `6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85` | 0          |
| `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a` | 250   | `aa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f` | 1          |
| `03c0029b38423f03b6d203a55e2d6778035740e40dd3d888301b3b47aede737b6f` | 500   | `95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40` | 2          |

### Bagged Root

- **Hash:** `2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040`
- **Sum:** `850`

### Sibling Inclusion Proofs

#### Proof for `02b1a03e...` (Index 0)

- **Leaf Index:** 0
- **Sibling Path:**
  ```json
  [
    {
      "hash": "aa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f",
      "sum": 250,
      "is_left": false
    }
  ]
  ```
- **Peaks:**
  ```json
  [
    {
      "hash": "90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f",
      "sum": 350
    },
    {
      "hash": "95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40",
      "sum": 500
    }
  ]
  ```

#### Proof for `02c3a506...` (Index 1)

- **Leaf Index:** 1
- **Sibling Path:**
  ```json
  [
    {
      "hash": "6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85",
      "sum": 100,
      "is_left": true
    }
  ]
  ```
- **Peaks:**
  ```json
  [
    {
      "hash": "90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f",
      "sum": 350
    },
    {
      "hash": "95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40",
      "sum": 500
    }
  ]
  ```

#### Proof for `03c0029b...` (Index 2)

- **Leaf Index:** 2
- **Sibling Path:** `[]`
- **Peaks:**
  ```json
  [
    {
      "hash": "90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f",
      "sum": 350
    },
    {
      "hash": "95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40",
      "sum": 500
    }
  ]
  ```

---

## 4. Epoch Manifest Signatures

The mint periodically aggregates the roots for all keysets, creates a deterministic global digest, obtains an OpenTimestamps (OTS) receipt, and signs an epoch manifest.

### Keys and Metadata

- **Master Private Key (`seckey`):** `371b3102088ee8fa21744920b996fa717417631271730ad34269646465998245`
- **Master Public Key (`pubkey`):** `f3dd0e40dd3d888301b3b47aede737b6f9451ab451dfc05a1ae023ab4235b4dd`
- **Keyset ID:** `009a6154b71113b7`
- **Epoch Index:** `1`
- **Timestamp:** `2026-06-11T12:00:00Z`
- **Previous Global Digest:** `0000000000000000000000000000000000000000000000000000000000000000`
- **Issued MMR Size:** `3`
- **Issued MMR Root Hash:** `2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040`
- **Issued MMR Root Sum:** `850`
- **Spent MMR Size:** `0`
- **Spent MMR Root Hash:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty MMR hash)
- **Spent MMR Root Sum:** `0`
- **Outstanding Balance:** `850`
- **OpenTimestamps Receipt (Hex):** `00000000000000004d4f434b5f4f54535f524543454950545f464f525f484153485f676c6f62616c5f6469676573745f6865785f76616c7565`

### Serialized Manifest String

The colon-separated UTF-8 string to sign (which excludes the `ots_receipt` and includes the `previous_global_digest`):

```
009a6154b71113b7:1:2026-06-11T12:00:00Z:0000000000000000000000000000000000000000000000000000000000000000:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:850
```

### Signature Computation

- **Message SHA-256 Digest:** `faaafafdc99bf27b8ba4d9b52d7ed5cd29d61c4a19ff65f8d4aaf49f6b964480`
- **Auxiliary Random Data (`aux_rand`):** `b777e0270e6f6bd9302268a253ffda221ce9257a6e13349e198169745c45d72e`
- **BIP-340 Schnorr Signature (`mint_signature`):** `f2720ae3c1eb13600acee4ee5694df89f12a51c32c171b52d71543f75534c197b2e98246828c41d85c31ea89fbed842df4b9622a6557899fb357aa4057920322`

---

## 5. Signed Transactional PoL Receipts

This section provides test vectors for the cryptographically signed Proof of Liability (PoL) receipts returned during state-transitioning actions, demonstrating the domain separation prefixes.

### Keys and Metadata

- **Keyset-amount Private Key (`seckey`):** `0000000000000000000000000000000000000000000000000000000000000001`
- **Keyset-amount Public Key (`pubkey`):** `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798`
- **Target Epoch:** `12`
- **Output Blinded Message (`B'_hex`):** `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4`
- **Spent Input Secret Point (`Y_hex`):** `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a`
- **Auxiliary Random Data (`aux_rand`):** `0000000000000000000000000000000000000000000000000000000000000000`

### 5.1 Output (Issued/Active) Receipt

- **Payload String to Sign:** `Cashu_PoL_Receipt_Issued:02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4:12`
- **Message SHA-256 Digest:** `cf056d6968059292716f12b612bcea6184a7204909da7126491ec49832edc3cb`
- **secp256k1 BIP-340 Schnorr Signature:** `31ef4e45aec5da42a7622bfbc6a8d0f9e07b562aa69092b6a2b7ea3a9b8ec92f88f4d510d488f55b00c2ea1bed0bb1f499c55eda275ffee9e0df60bf941a71b2`

### 5.2 Spent Input Receipt

- **Payload String to Sign:** `Cashu_PoL_Receipt_Spent:02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a:12`
- **Message SHA-256 Digest:** `630865434d37eb31ee3b8d472468a7154b63a1e45d530e7bc4cf736e8b9a9a6c`
- **secp256k1 BIP-340 Schnorr Signature:** `28b635335642ac4693f4eefb068500b5360c89df907537ad4f1baa25b5de48e30fb7a00f2e6a12ea864f5fbe0c0e5a8fd2c15ada088938eba55c339e215904df`
