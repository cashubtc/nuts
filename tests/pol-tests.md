# Proof of Liabilities (PoL) Test Vectors

This document provides test vectors for verifying implementations of the Proof of Liabilities (PoL) specification (NUT-XX), including Sparse Merkle Sum Tree (MS-SMT) computations, compact bitmasked sibling proofs, and epoch manifest BIP-340 Schnorr signing.

---

## 1. MS-SMT Precomputed Default Empty Nodes

Precomputed default empty nodes at level $d \in [0, 256]$. Each empty node has a sum of `0` and a hash computed by hashing the concatenation of the left child's hash, right child's hash, and their respective 8-byte big-endian sum values.

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

This test vector uses two active leaf nodes.

### Leaves

| Item            | Value | Hash (SHA256)                                                      | Index Integer (Hex)                                                  |
| :-------------- | :---- | :----------------------------------------------------------------- | :------------------------------------------------------------------- |
| `blinded_msg_1` | 100   | `d6957170936084afd3512013e8c474b5a859ce6e788964eacd61ffd380cd5487` | `0xd6957170936084afd3512013e8c474b5a859ce6e788964eacd61ffd380cd5487` |
| `blinded_msg_2` | 250   | `6675428850697b62d86c14e6e91a3999b600cc44ae17d965f8d643d5892075e4` | `0x6675428850697b62d86c14e6e91a3999b600cc44ae17d965f8d643d5892075e4` |

### Tree Root

- **Hash:** `7c4314392d644e3bacd868701a4db93ec123020355ae7833283ad6640debd3ff`
- **Sum:** `350`

### Sibling Inclusion Proofs

#### Proof for `blinded_msg_1`

- **Compact Mask:** `0x8000000000000000000000000000000000000000000000000000000000000000` (Bit 255 is set, indicating only the level 255 sibling is non-empty)
- **Siblings:**
  ```json
  [
    {
      "hash": "1aecc383233a40792fdb7ddb76d377792acc854d1adab60bab8f5e81588a6d1e",
      "sum": 250
    }
  ]
  ```

#### Proof for `blinded_msg_2`

- **Compact Mask:** `0x8000000000000000000000000000000000000000000000000000000000000000`
- **Siblings:**
  ```json
  [
    {
      "hash": "530ca26a79023d36e9ac21a3000f1848be5c79ba19b9a7a19bb8637fcb96897f",
      "sum": 100
    }
  ]
  ```

---

## 3. 3-Leaf Tree Computation

This test vector uses three active leaf nodes. Note that `blinded_msg_1` and `blinded_msg_3` share a path at higher levels since they are both located in the right subtree of the root (index MSB = `1`).

### Leaves

| Item            | Value | Hash (SHA256)                                                      | Index Integer (Hex)                                                  |
| :-------------- | :---- | :----------------------------------------------------------------- | :------------------------------------------------------------------- |
| `blinded_msg_1` | 100   | `d6957170936084afd3512013e8c474b5a859ce6e788964eacd61ffd380cd5487` | `0xd6957170936084afd3512013e8c474b5a859ce6e788964eacd61ffd380cd5487` |
| `blinded_msg_2` | 250   | `6675428850697b62d86c14e6e91a3999b600cc44ae17d965f8d643d5892075e4` | `0x6675428850697b62d86c14e6e91a3999b600cc44ae17d965f8d643d5892075e4` |
| `blinded_msg_3` | 500   | `d3b82220e9b89c35bc8a9bcf4862ea534f299ef90062b528e279ad03c6e33a0c` | `0xd3b82220e9b89c35bc8a9bcf4862ea534f299ef90062b528e279ad03c6e33a0c` |

### Tree Root

- **Hash:** `40e8ca24d54cb722675fb14f06ca0eb615fa743230e9573ebc63ba33b1aa1e57`
- **Sum:** `850`

### Sibling Inclusion Proofs

#### Proof for `blinded_msg_1`

- **Compact Mask:** `0x8400000000000000000000000000000000000000000000000000000000000000` (Bits 255 and 250 are set)
- **Siblings:**
  ```json
  [
    {
      "hash": "52cb8c18abd3086eb6625da50c37c04aab32044866446b95c11c4d5ade04d8f1",
      "sum": 500
    },
    {
      "hash": "1aecc383233a40792fdb7ddb76d377792acc854d1adab60bab8f5e81588a6d1e",
      "sum": 250
    }
  ]
  ```

#### Proof for `blinded_msg_2`

- **Compact Mask:** `0x8000000000000000000000000000000000000000000000000000000000000000`
- **Siblings:**
  ```json
  [
    {
      "hash": "e273595bf29ad7e352b68c77c73cafa08cf70017283d3ac98a5230b785a5a6c8",
      "sum": 600
    }
  ]
  ```

#### Proof for `blinded_msg_3`

- **Compact Mask:** `0x8400000000000000000000000000000000000000000000000000000000000000` (Bits 255 and 250 are set)
- **Siblings:**
  ```json
  [
    {
      "hash": "11bf3654634b3b2bf66f31af348bce2572cba1ebeea2eca304d7a7d97b2ed80d",
      "sum": 100
    },
    {
      "hash": "1aecc383233a40792fdb7ddb76d377792acc854d1adab60bab8f5e81588a6d1e",
      "sum": 250
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
- **Root Issued Hash:** `7c4314392d644e3bacd868701a4db93ec123020355ae7833283ad6640debd3ff`
- **Root Issued Sum:** `350`
- **Root Spent Hash:** `2a7b5220250ca23ef34228a6a223035aaefdf08c715836c46be4fc941699f6ba` (default empty node at level 256)
- **Root Spent Sum:** `0`
- **Outstanding Balance:** `350`
- **OpenTimestamps Receipt (Hex):** `00000000000000004d4f434b5f4f54535f524543454950545f464f525f484153485f676c6f62616c5f6469676573745f6865785f76616c7565`

### Serialized Manifest String

The colon-separated UTF-8 string to sign:

```
009a6154b71113b7:1:2026-06-11T12:00:00Z:7c4314392d644e3bacd868701a4db93ec123020355ae7833283ad6640debd3ff:350:2a7b5220250ca23ef34228a6a223035aaefdf08c715836c46be4fc941699f6ba:0:350:00000000000000004d4f434b5f4f54535f524543454950545f464f525f484153485f676c6f62616c5f6469676573745f6865785f76616c7565
```

### Signature Computation

- **Message SHA-256 Digest:** `ff6034b0bed27ce2d842e63d6f1c2f8d9b526c0aac86eac93965d9c4454f7d87`
- **Auxiliary Random Data (`aux_rand`):** `b777e0270e6f6bd9302268a253ffda221ce9257a6e13349e198169745c45d72e`
- **BIP-340 Schnorr Signature (`mint_signature`):** `2cedaa542f50483d4555dca5723004f859f411579fd65cb83991c3b87acd96e01e8d947132b0a898b8fada873587287a4d391cded21ed45da07a08cd4492a44e`
