# Proof of Liabilities (PoL) Test Vectors

This document provides test vectors for verifying implementations of the Proof of Liabilities (PoL) specification (NUT-XX), including Merkle Mountain Range with Sums (sum-MMR) computations, right-to-left peak bagging, and epoch manifest BIP-340 Schnorr signing.

---

## 1. Node Hashing and Peak Bagging Formulations

Each node in the sum-MMR has the structure `(hash, sum)` where `hash` is 32 bytes and `sum` is an 8-byte big-endian unsigned integer (uint64).

### Parent Node Hashing

Given left child L = (hash_L, sum_L) and right child R = (hash_R, sum_R):

- sum_P = sum_L + sum_R
- hash_P = SHA256(hash_L || hash_R || bytes_8(sum_L) || bytes_8(sum_R))

### Peak Bagging Hashing (Right-to-Left)

For a list of MMR peaks P_1, P_2, ..., P_k of decreasing heights, they are recursively bagged from right to left:

- B_k = P_k
- B_i = Parent(P_i, B_i+1) for i in [1, k-1]
- The final bagged commitment root is B_1.

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

#### Proof for `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4` (Index 0)

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

#### Proof for `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a` (Index 1)

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

#### Proof for `02b1a03e1b10a23429fa221087e53f19001b97ad89498a44b93b3f23a851121df4` (Index 0)

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

#### Proof for `02c3a50646bc1a1fef3da21973b064eb6897de58231c5f3e2730bf18361592394a` (Index 1)

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

#### Proof for `03c0029b38423f03b6d203a55e2d6778035740e40dd3d888301b3b47aede737b6f` (Index 2)

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

### Consistency Proof from 3 to 4 Leaves

Append this fourth leaf with value `1000`:

| Blinded Message B\_ (33-Byte Compressed Pubkey Hex)                  | Value | Hash                                                               | Leaf Index |
| :------------------------------------------------------------------- | :---- | :----------------------------------------------------------------- | :--------- |
| `021111111111111111111111111111111111111111111111111111111111111111` | 1000  | `e1577700e127f1ce6e20a4efc2d96a986979c755d9ab559af6b1755eb3f3220e` | 3          |

For `[n, m) = [3, 4)`, the deterministic appended-range decomposition contains one aligned height-0 subtree. The consistency proof is:

```json
{
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
```

Verification proceeds as follows:

1. Bagging the two old peaks reproduces the 3-leaf root `2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040` with sum `850`.
2. Push the appended height-0 node. It merges with the old height-0 peak to produce height-1 node `(197e3fd28f9b41840f7fa83cd78d0cd40436925fadeb6a87f0d89bf41a810f30, 1500)`.
3. That node merges with the old height-1 peak to produce the single height-2 peak.

The expected 4-leaf MMR is:

- **Root Hash:** `52bab3d1d98672c800ec1b86b360e18b738be260c1d1a2f4108998b336bc56d6`
- **Root Sum:** `1850`

Changing either old peak, the appended subtree, any sum, or any height MUST make the proof fail against at least one committed root or the deterministic height sequence.

---

## 4. Epoch Manifest Signatures

The mint periodically aggregates the roots for all keysets, creates a deterministic global digest, obtains an OpenTimestamps (OTS) receipt, and signs an epoch manifest.

### Keyset Merkle Commitment

For the single keyset in this vector, the canonical keyset leaf preimage is:

```text
utf8("Cashu_PoL_Keyset_Leaf_v1")
|| 0010
|| utf8("009a6154b71113b7")
|| 0000000000000003
|| 2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040
|| 0000000000000352
|| 0000000000000000
|| e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
|| 0000000000000000
|| 01
|| 01
|| 000000000000000c
```

- **Keyset Leaf Hash:** `cf3cebc4d9a6ee6b02a47ef4b651790fe01d227dd28fc9cf49b8dd89328b7e03`
- **Keyset Merkle Root:** `cf3cebc4d9a6ee6b02a47ef4b651790fe01d227dd28fc9cf49b8dd89328b7e03`
- **Empty Keyset Merkle Root:** `66b7de363bb498c9cf01f2997ec7f658b8734dd8bb5e959ea240c9ea9a951180`

The global digest preimage is:

```text
utf8("Cashu_PoL_Epoch_v1")
|| 0000000000000000000000000000000000000000000000000000000000000000
|| 0000000000000001
|| 0001
|| cf3cebc4d9a6ee6b02a47ef4b651790fe01d227dd28fc9cf49b8dd89328b7e03
```

- **Global Digest:** `b63c038a841f6700a1133703c1e2c6c4f36d749eb1d13722a8f96a11e70f4c32`

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
- **Active:** `true`
- **Deactivation Epoch:** `12`
- **OpenTimestamps Receipt (Hex):** `00000000000000004d4f434b5f4f54535f524543454950545f464f525f484153485f676c6f62616c5f6469676573745f6865785f76616c7565`

### Serialized Manifest String

The colon-separated UTF-8 string to sign (which excludes the `ots_receipt` and includes the `previous_global_digest`):

```
009a6154b71113b7:1:2026-06-11T12:00:00Z:0000000000000000000000000000000000000000000000000000000000000000:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:850:true:12
```

### Signature Computation

- **Message SHA-256 Digest:** `d8fff1452857ed54fc26a014a3db860dc82eb4d9046c34185a890484b6424b45`
- **Auxiliary Random Data (`aux_rand`):** `b777e0270e6f6bd9302268a253ffda221ce9257a6e13349e198169745c45d72e`
- **BIP-340 Schnorr Signature (`mint_signature`):** `085487e8f234bf3d11124c2d9459e6f863ebfbe424f855c7fa115e05b2786508120496d61d53bb89b545ec13e9a82070823d096012119c27eef8cc4185830398`

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

---

## 6. Keyset Lifecycle Vectors

These independent histories exercise every `rotation_violation` predicate. All signatures use the section 4 master key and 32 zero auxiliary bytes unless stated otherwise.

### 6.1 Clean Early Deactivation

Epoch 1 declares `deactivation_epoch: 12`. Epoch 2 deactivates early, freezes the issued MMR, and grows the spent MMR from size 0 to size 1 as existing ecash is redeemed. This is the expected post-deactivation behavior.

```text
009a6154b71113b7:2:2026-06-12T12:00:00Z:1111111111111111111111111111111111111111111111111111111111111111:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:1:6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85:100:750:false:12
```

- **Digest:** `c09ce798feaf4f6748902f076f9dd20a0f55cb8152a97f6b3f9b9b35738c9a8a`
- **Signature:** `0f73df30b2680ea0c65f98768bb8c58f3440f625e4b5c7c9dcdfe00c3a49f6f1eadfd6c1f513f99b5bc70b9cf37392e0452da8d3109be5e184ae24db07114dab`

This transition is valid.

### 6.2 Reactivation Violation

```text
00b2c4d6e8fa0c1e:3:2026-06-13T12:00:00Z:2222222222222222222222222222222222222222222222222222222222222222:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:1:6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85:100:750:false:null
```

- **Digest:** `6797dd542f4dde53121062effe58432fbb46b1cec7e2de5332d11ea44040980b`
- **Signature:** `7d41366b85d06f5a718fba60c1aac5b2a48a2bed4b37a821af90a84fbff60c368bea4caadac2bad385948a1d552ef28ce94b0b8ab96a780c192c8ef247e7e769`

```text
00b2c4d6e8fa0c1e:4:2026-06-14T12:00:00Z:3333333333333333333333333333333333333333333333333333333333333333:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:1:6711094bb65007f6313a7c2edc4833378ef715aaf8f62ce0f9478c591dba1e85:100:750:true:null
```

- **Digest:** `bb707de76fda62f65a35cd01746742d644f818306d168f6375b5a6344f749a44`
- **Signature:** `90d8d1a82962d19d4a956bc3abbb81065477f7b97959140c72260d116915922783e4db0d8e4413bc201869718bf3dec161fd50b3aee0f0face13387b053e6699`

The epoch-3 and epoch-4 manifests prove `reactivation`.

### 6.3 Issuance After Lock

```text
00c3d5e7f90b1d2f:5:2026-06-15T12:00:00Z:4444444444444444444444444444444444444444444444444444444444444444:2:90e8e647a08f35b5b24653ab52e5d27a2deddb05d1e54d5d21777ef02036b29f:350:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:350:false:null
```

- **Digest:** `b29bd4a8d95ffd4fda01cbeb8beda6bebf233abf1779444305084a7bb9b6e1fb`
- **Signature:** `ebbb6e5d096541c3d97e9e5331a88047abcae3dc53990bc0f3fe4ce3aa37b101c005e305e07f56f2b720a86c3224a5c5e25936675c91a6443c3927de867358ea`

```text
00c3d5e7f90b1d2f:6:2026-06-16T12:00:00Z:5555555555555555555555555555555555555555555555555555555555555555:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:850:false:null
```

- **Digest:** `497a7e810a7a5389e4bd14ae3ed3486f72c259f99f12c9e36087ec3139471331`
- **Signature:** `2355c5d251b976881d2dd29d018b74bed59d7edd3b383e4ed6c9bbfc7ec79f8e2b68cbee856f7af96d4e4df7a1a836f6ff78ad5f369a37a7c4b5a27ac2ecc697`

The issued MMR change after epoch 5 proves `issuance_after_lock`.

### 6.4 Declaration Drift

```text
00d4e6f80a1c2e30:7:2026-06-17T12:00:00Z:6666666666666666666666666666666666666666666666666666666666666666:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:850:true:12
```

- **Digest:** `a2811f0311f3c7bce7ff0f16b4df1ea16c0f995afd1b6ea2e49388c4c2dcfa70`
- **Signature:** `a18b662a5022cc694c3991393af9658157452c6724b38de0f3766b39a86d5b1a5be646bd43898f1b2a6ae3a552d558fc4faee1be02a18bbfc0fa03c66ed3da95`

```text
00d4e6f80a1c2e30:8:2026-06-18T12:00:00Z:7777777777777777777777777777777777777777777777777777777777777777:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:850:true:13
```

- **Digest:** `cb4fbf8ef6f2761d564b491fca41c6bdb84c34d9fd6dc9cff5d0c328d7c0b45a`
- **Signature:** `2e105e3808a01bb3d4b34ff1e4d00b5552f345404fbd0a03b22aaf7810744d923ee6b92920806c02ab47f51ae83d7af17a62f19410cec7b7fa2fd713b0f21e54`

The two declarations prove `declaration_drift`.

### 6.5 Deactivation Epoch Overrun

```text
00e5f7091b2d3f41:12:2026-06-22T12:00:00Z:8888888888888888888888888888888888888888888888888888888888888888:3:2518b42edfff24ecc53c8897d1860783d1d26c41d61c378fe612cddeed877040:850:0:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0:850:true:12
```

- **Digest:** `059159944686e29618dfbe6c1ce6ecda8be022681145e8a3e13b27f661341cda`
- **Signature:** `62f7106836bd9e002a78f594458ce9f063d8d0336126d17eea39534dcbbcf1adea13dc81f4c50d0b0afe709aaac4e7798ea9a2adf0c0dc350d153f86a7c7b944`

Because epoch 12 equals `deactivation_epoch` while `active` remains true, this manifest alone proves `deactivation_overrun`.
