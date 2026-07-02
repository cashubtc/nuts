# Proof of Liabilities (PoL) Test Vectors

This document provides test vectors for verifying implementations of the Proof of Liabilities (PoL) specification (NUT-XX), including Sparse Merkle Sum Tree (MS-SMT) computations, compact bitmasked sibling proofs, and epoch manifest BIP-340 Schnorr signing.

---

## 1. MS-SMT Precomputed Default Empty Nodes

Precomputed default empty nodes at level `d in [0, 256]`. Each empty node has a sum of `0` and a hash computed by hashing the concatenation of the left child's hash, right child's hash, and their respective 8-byte big-endian sum values.

```json
[
  {
    "level": 0,
    "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "sum": 0
  },
  {
    "level": 1,
    "hash": "bc8ac1359d614e79e858cf990d2847126ed9b44defa2e0eeee501a9e979da658",
    "sum": 0
  },
  {
    "level": 2,
    "hash": "7ca0eae62b36334057b542a025a90d7e37beee71ed761e49483746142e1144a6",
    "sum": 0
  },
  {
    "level": 3,
    "hash": "6089c77949a1c945da0026b557dc9bf4f1dcd2c3e9b5c31ed5973e55df2a8458",
    "sum": 0
  },
  {
    "level": 4,
    "hash": "153c8aa8d18a34da8dc499bab40e9ae55564da0c533b0005bb0f410d6b6d51e8",
    "sum": 0
  },
  {
    "level": 10,
    "hash": "a4de2bac5474b673c8f220961b40d00329bc413c0d6f15ee1be3c181f813d07d",
    "sum": 0
  },
  {
    "level": 100,
    "hash": "079b58a5530a258ab4ff4c988e8024094aab07fe94a897d7f04c9c936034bf99",
    "sum": 0
  },
  {
    "level": 256,
    "hash": "2a7b5220250ca23ef34228a6a223035aaefdf08c715836c46be4fc941699f6ba",
    "sum": 0
  }
]
```

---

## 2. 2-Leaf Tree Computation

This test vector uses two active leaf nodes, derived by hashing the raw 33-byte compressed public key values of the blinded messages.

### Leaves

| Blinded Message B\_ (33-Byte Compressed Pubkey Hex)                  | Value | Hash (SHA256 of Raw Bytes)                                         | Index Integer (Hex)                                                  |
| :------------------------------------------------------------------- | :---- | :----------------------------------------------------------------- | :------------------------------------------------------------------- |
| `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4` | 100   | `6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85` | `0x6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85` |
| `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a` | 250   | `aa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f` | `0xaa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f` |

### Tree Root

- **Hash:** `fe8a4d26af66d5abffad49a553a483a466e81098c0006c32d8685b692dd0d755`
- **Sum:** `350`

### Sibling Inclusion Proofs

#### Proof for `02b1a03e...`

- **Compact Mask:** `0x8000000000000000000000000000000000000000000000000000000000000000` (Bit 255 is set, indicating only the level 255 sibling is non-empty)
- **Siblings:**
  ```json
  [
    {
      "hash": "57f827f76a295fbc65ca015eb80ece857ef5335beebbd3b39a53f1cbcd3ae97f",
      "sum": 250
    }
  ]
  ```

#### Proof for `02c3a506...`

- **Compact Mask:** `0x8000000000000000000000000000000000000000000000000000000000000000`
- **Siblings:**
  ```json
  [
    {
      "hash": "deae1aa655612bfe4b489ca03f706457d9b8ed9510645e6fdf0da492227ccd53",
      "sum": 100
    }
  ]
  ```

---

## 3. 3-Leaf Tree Computation

This test vector uses three active leaf nodes. Note that the second and third public keys share a path in the right subtree of the root (index MSB = `1`) and only diverge at bit index 253.

### Leaves

| Blinded Message B\_ (33-Byte Compressed Pubkey Hex)                  | Value | Hash (SHA256 of Raw Bytes)                                         | Index Integer (Hex)                                                  |
| :------------------------------------------------------------------- | :---- | :----------------------------------------------------------------- | :------------------------------------------------------------------- |
| `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4` | 100   | `6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85` | `0x6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85` |
| `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a` | 250   | `aa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f` | `0xaa80cd1d9ae985f212fd6c41cdf4c8747c92d787e9d8fd45e5d7e3f85941937f` |
| `03c0029b38423f03b6d203a55e2d6778035740e40dd3d888301b3b47aede737b6f` | 500   | `95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40` | `0x95b7ec67b1f85ca98781f08fc4613559820b99f178707b29c8ebb4577aca5f40` |

### Tree Root

- **Hash:** `cfe3bb0bf9c93e6d70912fedaaac0c9f858d18279305dcbd92f585b7e362adca`
- **Sum:** `850`

### Sibling Inclusion Proofs

#### Proof for `02b1a03e...`

- **Compact Mask:** `0x8000000000000000000000000000000000000000000000000000000000000000` (Bit 255 is set)
- **Siblings:**
  ```json
  [
    {
      "hash": "d12b7283fd13e96c22719e183c272857957feb457789d5eec820325cc70390dc",
      "sum": 750
    }
  ]
  ```

#### Proof for `02c3a506...`

- **Compact Mask:** `0xa000000000000000000000000000000000000000000000000000000000000000` (Bits 255 and 253 are set)
- **Siblings:**
  ```json
  [
    {
      "hash": "8d8ada84c6af46ca1b5da3dd9974b0c941746faa7bc3b08717028028813fefb0",
      "sum": 500
    },
    {
      "hash": "deae1aa655612bfe4b489ca03f706457d9b8ed9510645e6fdf0da492227ccd53",
      "sum": 100
    }
  ]
  ```

#### Proof for `03c0029b...`

- **Compact Mask:** `0xa000000000000000000000000000000000000000000000000000000000000000` (Bits 255 and 253 are set)
- **Siblings:**
  ```json
  [
    {
      "hash": "b44b631c9ffcbfbeef7a46e3e0ee6a84bd51e2981145766bfcfe715668d6c5b3",
      "sum": 250
    },
    {
      "hash": "deae1aa655612bfe4b489ca03f706457d9b8ed9510645e6fdf0da492227ccd53",
      "sum": 100
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
- **Root Issued Hash:** `fe8a4d26af66d5abffad49a553a483a466e81098c0006c32d8685b692dd0d755`
- **Root Issued Sum:** `350`
- **Root Spent Hash:** `2a7b5220250ca23ef34228a6a223035aaefdf08c715836c46be4fc941699f6ba` (default empty node at level 256)
- **Root Spent Sum:** `0`
- **Outstanding Balance:** `350`
- **OpenTimestamps Receipt (Hex):** `00000000000000004d4f434b5f4f54535f524543454950545f464f525f484153485f676c6f62616c5f6469676573745f6865785f76616c7565`

### Serialized Manifest String

The colon-separated UTF-8 string to sign (which excludes the `ots_receipt` and includes the `previous_global_digest`):

```
009a6154b71113b7:1:2026-06-11T12:00:00Z:0000000000000000000000000000000000000000000000000000000000000000:fe8a4d26af66d5abffad49a553a483a466e81098c0006c32d8685b692dd0d755:350:2a7b5220250ca23ef34228a6a223035aaefdf08c715836c46be4fc941699f6ba:0:350
```

### Signature Computation

- **Message SHA-256 Digest:** `045fde0709052b35c875488668bd78d5bc06d38a219c768a616c7fa9b88d064a`
- **Auxiliary Random Data (`aux_rand`):** `b777e0270e6f6bd9302268a253ffda221ce9257a6e13349e198169745c45d72e`
- **BIP-340 Schnorr Signature (`mint_signature`):** `71f4ab4d3279597095ee8c374e13374192e0cbf2016f7ea0fca35dca68df69c9c70a607ba361f7b18130ea899b9f28f487869a9b7ee69d75d74ed0a06b50bed6`

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
