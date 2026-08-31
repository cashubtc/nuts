# NUT-10 Test Vectors

These vectors cover [nutroot secrets](../10.md#nutroot-secrets-v3-keysets) (v3 keysets). All signatures are BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes them reproducible; verifiers **MUST** accept any valid signature.

## Conventions

Tagged hashes use the tags `Cashu_NutrootLeaf`, `Cashu_NutrootBranch` and `Cashu_NutrootTweak`; receiver-keyed blinding uses `Cashu_P2BK_v1` ([NUT-28](../28.md)); the transaction domain tag is `Cashu_Transaction_v1` and per-input signing messages use the tag `Cashu_TransactionInput`; the NUMS point is `0250929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0`. These are the normative constants of [NUT-10](../10.md), restated here so the vectors read standalone.

The keys throughout are the well-known small test keys, written `key N` for the private scalar `N`:

| Key | Compressed public key                                                |
| --- | -------------------------------------------------------------------- |
| `3` | `02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9` |
| `4` | `02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13` |
| `5` | `022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4` |
| `6` | `03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556` |
| `7` | `025cbdf0646e5db4eaa398f365f2ea7a0e3d419b7e0330e39ce92bddedcac4f9bc` |
| `9` | `03acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe` |

## Serialized leaves

The `after` leaf used throughout, spelled out (`n = 1`, `keys = [key 4]`, `time = 1755561600`):

```
00 02 | 02 0001 01 | 04 0021 02e493...c4cd13 | 06 0004 68a3be80
```

```json
{
  "threshold_1of1_key3": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "threshold_2of2_keys3_4": "00010200010204004202f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f902e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13",
  "hashlock_hash": "a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1",
  "hashlock_1of1_key3": "00030200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9080020a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1",
  "after_1of1_key4": "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80",
  "threshold_1of1_key3_disclosure": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101"
}
```

`threshold_1of1_key3_disclosure` appends the `disclosure` field (`0a000101`): satisfaction is unchanged, and a spend through it is published ([NUT-07 vectors](07-tests.md)).

## The tree fold

A three-leaf tree (`threshold_1of1_key3`, `after_1of1_key4`, `hashlock_1of1_key3`, in transmitted order) exercises the sorted odd-count fold: ascending by leaf hash the order is `h0, h2, h1`, so `h0` and `h2` pair, `h1` is promoted unchanged, and the two hashes at the next level pair. The merkle path for leaf 2 is therefore `[h0, h1]`.

```json
{
  "three_leaf_tree": [
    "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
    "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80",
    "00030200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9080020a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"
  ],
  "root": "3d4fbecf46f5c716d7cebd48863f3c4ab89e675e3beb4b3a28f3bd13b49d43ad",
  "path_for_index_2": [
    "23e8ff1693496ecad495b7ed3cdd7f8595c52a3adc0b92475835b0fb839116cb",
    "9ed9c0b8907f7af4fce51cbeac218907bbf80ba40f3342df2406bce30616589a"
  ],
  "internal_key": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "secret": "022d17fddb224e53e12b40c58ab3e8828d08931640105c52fc4eaf765ed51b9999"
}
```

`secret = internal_key + tagged_hash("Cashu_NutrootTweak", internal_key || root)*G`, and the commitment also verifies through `path_for_index_2` from leaf 2 alone.

Duplicate leaves fold without deduplication: two copies of `threshold_1of1_key3` under internal key `6` commit `root = tagged_hash("Cashu_NutrootBranch", h || h)`, distinct from the single-leaf root `h`, and either copy spends with `path = [h]`:

```json
{
  "leaves": [
    "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
    "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9"
  ],
  "leaf_hash": "23e8ff1693496ecad495b7ed3cdd7f8595c52a3adc0b92475835b0fb839116cb",
  "merkle_root": "1eaf291448e2f3c3a4fc00bfd591917bbb807e63af0fb905d054002bddd2cbc6",
  "internal_key": "03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
  "secret": "03dd2f11ab23b670222ada50325b5d49cd07e1d7a721d9b52fa2039df1f1b0dbfd"
}
```

## Worked example: receiver-keyed proof with a refund leaf

Alice pays Carol, refundable to Alice after `time`. Carol's static key is key `3`, Alice's refund key is key `4`, Alice's ephemeral is key `5`. The internal key is Carol's static key blinded at slot 0 ([NUT-28](../28.md#nutroot-secrets-v3-keysets)); the tree is the single `after` leaf.

```json
{
  "carol_static": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "ephemeral_E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "slot0_r": "7dfb649b0edda814f7cf0feb889e5657eb2083a528aa60a3a943fe0cea066181",
  "internal_key": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "leaf": "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80",
  "merkle_root": "9ed9c0b8907f7af4fce51cbeac218907bbf80ba40f3342df2406bce30616589a",
  "tweak": "b3b7846b14be0650bb03272d179931221637744d1997df80bf27d2df5effe8a4",
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "keypath_priv": "31b2e906239bae65b2d23718a037877b46a91b0b92f99fe8a899725f78d008e7"
}
```

Here `merkle_root = tagged_hash("Cashu_NutrootLeaf", leaf)` (single leaf), and `keypath_priv = (3 + slot0_r + tweak) mod n`, the key Carol signs with.

The witnesses below sign an **illustrative** input digest, `SHA256("illustrative transaction transcript")` = `e1d7170b89a2b6eedec90453e32b6c320dfadd590e6a6454bddec95a0e3834cd` (a real spend derives its input digest from the transaction transcript, see below). Carol's key-path witness:

```json
{
  "signatures": [
    "619e0726595b5adff06cc3e6ea1c409f10f7b064cf8888f0eed0efbac854eabf4632642930bdc7c4d7d983379301a4f263991dbd19d96e5ebcfab9e8583bd510"
  ]
}
```

Alice's script-path witness after the locktime (empty path, single-leaf tree; her signature verifies against key `4` listed in the leaf):

```json
{
  "leaf": "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80",
  "control": {
    "K": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
    "path": []
  },
  "signatures": [
    "0b2ea247bfca1264db86907aef4cb19935ed9a5b2043a757259dcdb5c599372c230602f2cfc0cd8b11aa98ff17fbed91f38f07db817263fcc7c50c846715873e"
  ]
}
```

For contrast, a bearer proof with no conditions: private key `7` travels as spend info `k`, and the secret is its bare public key `025cbdf0646e5db4eaa398f365f2ea7a0e3d419b7e0330e39ce92bddedcac4f9bc`.

## Worked example: two leaves and a filled path

A two-leaf tree under internal key `6`. Leaf 0 uses the **unallocated** type `0x04`, which makes this both a branch vector and a fail-closed vector: the commitment math below verifies, but a verifier **MUST** treat the `0x04` leaf as unsatisfiable, so a witness revealing it is rejected regardless of its (real) signature. Leaf 1 is an ordinary `after` leaf (key `3`, time `1758240000`) and is spendable once its locktime passes, with `path = [leaf_hash_0]`.

```json
{
  "internal_key": "03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
  "leaf_0_unknown_type": "00040200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a002103acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe",
  "leaf_1_after": "00020200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d00",
  "leaf_hash_0": "fdb9a975d2d191fbfbe2ac40d70f49ffe73836f4bbb0f2bb2405f63e2cc029b2",
  "leaf_hash_1": "80468218b6e329d4d80682883617af0acd1d4a9d5b1658fbc448cc4781b4f254",
  "merkle_root": "4b88a91c09bbbd87f7e0e27a9f2d26fbe15c0a09b57656f0b5b5fe997428d8cd",
  "tweak": "2c6aa2e8ebf952db486ab83a593eb7e93080b73afa363898fd2725ad1a9c2b43",
  "secret": "02e02bae49d0eac930bd2bd710f87810080f30c00540b49d7fa4d648ac4689c5dd"
}
```

`merkle_root = tagged_hash("Cashu_NutrootBranch", leaf_hash_1 || leaf_hash_0)`: the pair is sorted, so `leaf_hash_1` comes first. A witness revealing `leaf_0_unknown_type` with `path = [leaf_hash_1]` reconstructs the secret but **MUST** be rejected as unsatisfiable (unknown leaf type).

## Worked example: auditable lock with disclosure

The canonical [auditable lock](../10.md#auditable-locks) to `P` = key `3`: NUMS offset `u = 7` (the same offset as the [NUT-18 vectors](18-tests.md), so `K` matches), one `threshold` leaf `n = 1` carrying `disclosure` mode `0x01`.

```json
{
  "P": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "u": "0000000000000000000000000000000000000000000000000000000000000007",
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "leaf": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101",
  "merkle_root": "b957f8b50199184bb5b29cdd1e3e4b14c63f35501e843000a6fb30cd00793cd6",
  "tweak": "6c3a09b15dd0f8abd4e0e329f3038c6e726346d9bd5f7f40453cc8727689610b",
  "secret": "02fc11bf4f939f2bfd47e4cee799c8254fc4acc27a134c729edfc3c6a3c13a053b"
}
```

For the pinned spend transaction in the shared JSON vector:

```json
{
  "transaction_digest": "882b3bd6dba132160a3349fc64017214be68e3e150242f2a6f4ddfcb4aef49e6",
  "input_id": "71ab32aa7d1b611bb7ddfc63c34b67a9aacde5c027cebd4227e819afb8eaf6dd",
  "input_digest": "db64ca493b62de0a5d6e66d25a5f9544e0af97aebfb050059a731ea739d3675d"
}
```

`P`'s script-path witness over that `input_digest` is:

```json
{
  "leaf": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": []
  },
  "signatures": [
    "e0d832c9de4d75f3dec43205b55e814fef15b186e7309f275107e1aa566b5ab6b8422628e0b8e5ae303e8812f355c83953af8155d1b8310d78e2acb883f48861"
  ]
}
```

The `disclosure` field commits this spend to publication: the mint returns the exact witness string and its input digest through NUT-07, and the [NUT-07 vectors](07-tests.md) carry the matching commitment and opening.

## Rejection vectors

An unknown field rejects, and odd type numbers are reserved with none allocated, so this leaf (`threshold_1of1_key3` with a four-byte field `0x09` appended) is malformed:

```json
{
  "leaf_unknown_field": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9090004deadbeef"
}
```

`disclosure` fails closed on any value but mode `0x01`: appending `0a000100` (mode `0x00`), `0a0000` (empty), or `0a000102` (unallocated mode) to `threshold_1of1_key3` each make it malformed:

```json
{
  "leaf_disclosure_mode0": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000100",
  "leaf_disclosure_empty": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a0000",
  "leaf_disclosure_mode2": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000102"
}
```

`signatures` is bounded: exactly one entry on the key path, at most the leaf's key count on the script path. Listing Carol's key-path signature twice, or Alice's script-path signature twice (her leaf lists one key), makes each witness above invalid with no other change.

## Empty tweak

An aggregated internal key commits to having no script path with the empty tweak: `t = tagged_hash("Cashu_NutrootTweak", K)`, no merkle root bytes. With `K` = public key of `3`:

```json
{
  "internal_key": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "tweak": "764c0e0da0d17acb5cc863fbe939211869e04e522c017171a0b71e91d5b69908",
  "secret": "03b2bb251c006ae42d9c19f3157d02b3c347b1fb6512885225a8699a06d9233aee",
  "keypath_priv": "764c0e0da0d17acb5cc863fbe939211869e04e522c017171a0b71e91d5b6990b"
}
```

## Transaction transcripts

`transaction_digest = SHA256("Cashu_Transaction_v1" (ASCII) || transcript)`; each input signs `input_digest = tagged_hash("Cashu_TransactionInput", transaction_digest || input_id)`, where `input_id = SHA256(input container record)`. The single-input transactions below place that container first; the separate multi-input vector identifies both containers explicitly. The `digest` key in each vector is the transaction digest. The keyset is a v3 keyset with id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6` (contributing raw bytes); quote ids contribute UTF-8 bytes; amounts are minimal big-endian. Single-proof examples use [NUT-13 V3](13-tests.md) counter `0`; the multi-input example also uses counter `1`.

**Swap.** A `PostSwapRequest` ([NUT-03](../03.md)) spending one 8-sat proof into two 4-sat outputs:

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
      "C": "84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327"
    }
  ],
  "outputs": [
    {
      "amount": 4,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    },
    {
      "amount": 4,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

serializes to the following transcript and digest:

```json
{
  "transcript": "01007f0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f603002102e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b04003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "77d581ac1ea31d85ecc5c251a7115ef6777e5b2a8f297933fd3a1a7e441094bd",
  "input_id": "56db6f708b5b9ad59d160a6014321a76916bb41141b360d30c85c06d497cfd80",
  "input_digest": "0f9483a25c859d5156dccc3c141a26d987618ec365bfa12f8c107db0ebd02ae7"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "ff3be61493fba8bcb2eb8256a1976699f5d439f1ad9f1e82f724b1565091239fb4e0dcc5f99e83a995176fcb5a750dca017c76c4caac9862e416bfd86f3b8b71"
  ]
}
```

**Multiple proof inputs.** Appending the NUT-13 counter `1` proof (amount `4`) to the swap above and changing the two output amounts to `8` and `4` gives one shared transaction digest but a distinct signing digest for each proof:

```json
{
  "digest": "0b77a01a0df036026387107b89318714d1627a156cf28a1b82bdcf710d425c3f",
  "inputs": [
    {
      "input_id": "56db6f708b5b9ad59d160a6014321a76916bb41141b360d30c85c06d497cfd80",
      "input_digest": "50d55a5c4c176a526fc8c8f9ba554e6637a9d003317913498e1a9c9cb1131fab",
      "signature": "292e0418b7e58f71694f2d3faadaf368ca236711075b8530cb15184162e5cae18962671c61a369038eae3db26ac3ce982fdb6bbb269db1b23dd27ab341465872"
    },
    {
      "input_id": "3fe70f160a85a6fe4586b1643767099dbdb78b740d2a4ce281e8e435e6e83a54",
      "input_digest": "a2d8b55cad8f0123fdb25251750df39b43295942f1c76ae37d2bf72a1fcd20b2",
      "signature": "30d4dd3aa65aa2c74bfd05c9f3edc5d4097742e38554a5909f8bcbaf274728d491ddecc967bda42f222c0af57f96ff76e407bbada00d8ab09370d589760453f8"
    }
  ]
}
```

The complete transaction and transcript are pinned as `transcript.multi_input` in the shared JSON vector. Each signature **MUST** verify only against its corresponding `input_digest`; neither signs the shared `digest`.

**Mint.** Executing mint quote `quote-mint-0001` (amount 8, [NUT-04](../04.md#nutroot-transactions-v3-keysets)) with one 8-sat output. The quote is the transaction's only input; its lock key signs this digest via the mint request's `signature` field:

```json
{
  "outputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

```json
{
  "transcript": "0200160100010802000f71756f74652d6d696e742d3030303103005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "096a9b2002cc0b8ebc9b79e0902159385a929f4e63f35eb9e1dee0119205efb6",
  "input_id": "c7892510d9bd10a53d590f3454790546f0b5ae46d3ee2b6905b77592e4cb0346",
  "input_digest": "5564488281ed47fa6c335aa6b662e1529ca4ad2402bb2847750833dc35212060"
}
```

**Melt.** Paying melt quote `quote-melt-0001` (amount 8, no change outputs) with the swap's 8-sat proof as the only input; the melt quote is the only output, binding its quote id and amount:

```json
{
  "transcript": "01007f0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f603002102e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b04003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033270400160100010802000f71756f74652d6d656c742d30303031",
  "digest": "172e38f867afa4d096fe0c1caef1aad4a19a2da6ffea25a33660172df66474b3",
  "input_id": "56db6f708b5b9ad59d160a6014321a76916bb41141b360d30c85c06d497cfd80",
  "input_digest": "b9d84e5c5f2bf37da113fb12d9d5c0207b0109a322922eb0bfcb81f1523c479c"
}
```

The melt spends the swap's proof, so it shares the swap's `input_id`; the differing transcripts give it a different `input_digest`, so neither witness verifies in the other transaction.

**Melt with change.** The same melt carrying two [NUT-08](../08.md) blank change outputs (amount 0, on the same keyset with the swap's `B_`). Containers group in ascending type order, so the blank outputs (type `0x03`) precede the melt quote (type `0x04`) in the transcript regardless of the request's field order; note each blank's zero amount encodes to a zero-length record (`010000`):

```json
{
  "transcript": "01007f0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f603002102e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b04003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd550400160100010802000f71756f74652d6d656c742d30303031",
  "digest": "3b7a268b8c49e836d5235a4d4b89f1d5bfbe7bfa01d6427fa2a013f91b9d1a68",
  "input_id": "56db6f708b5b9ad59d160a6014321a76916bb41141b360d30c85c06d497cfd80",
  "input_digest": "98f8267de415b51d7e24eb8d9d6606e028c39b5d71e3de2135cfa65226dc9900"
}
```

## V4 tokens with spend info

One 8-sat proof per token, mint `https://mint.test`, unit `sat`, keyset id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6`, `C` = `84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327`.

Tokens use the short keyset id form; decoders **MUST** also accept the full-length id ([NUT-00][00]). Each shape decodes to the stated `spend_info` fields and re-encodes to the same string.

Bearer (`si.k`, secret is the bare key of `k`):

```json
{
  "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
  "spend_info": {
    "k": "47196dc081150ce13fd0e478b8b71831b825be389211c9c56a8062a61af70347"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmU2ZTdjZmE3YjgyZDRiM2I0NDlmYTY0NjZjODkzNDY5YTcyN2QwMjE0ZDQ4ZGI0OTU2YTYwNTRiODAyMmEyOWJhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFrWCBHGW3AgRUM4T_Q5Hi4txgxuCW-OJIRycVqgGKmGvcDRw"
}
```

Receiver-keyed, no conditions (`si.e` only):

```json
{
  "secret": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwM2EzZTEyY2MwNzdlNTYwNWYzNjQ0MTA0NmY1MGMxMTRmY2M4ODNiMDc5YTM0MDI4YmVkNjY3MzJlM2E0MTllNTFhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-Q"
}
```

Receiver-keyed with a disclosed tree (`si.e` + `si.t`; the receiver derives `K` from `E`):

```json
{
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmQzMTBhNGQ2NjFlMzE1OGU3ZDM2MDYxN2U3MzlkNmJhY2JmMDE1NDMxYjI0YTQzMTY4ZGIwYWI5OWVmOGY4MjhhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpomFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-RhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

A disclosed tree with an explicit internal key (`si.i` + `si.t`; no key handed over, the third-party-signer shape):

```json
{
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "spend_info": {
    "K": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmQzMTBhNGQ2NjFlMzE1OGU3ZDM2MDYxN2U3MzlkNmJhY2JmMDE1NDMxYjI0YTQzMTY4ZGIwYWI5OWVmOGY4MjhhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpomFpWCEDo-EswHflYF82RBBG9QwRT8yIOweaNAKL7WZzLjpBnlFhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

Script-only (`si.i` + `si.u` + `si.t`): `K = H + u*G`, so the holder checks `K - u*G == H` and knows no key path exists. `u` is fixed here for a stable vector; a real send uses a fresh one per proof.

```json
{
  "secret": "0251a4f35fa38c5edce83e16596de02be4e87ec6a91c5fd80ab577c22668fb6dd5",
  "spend_info": {
    "K": "0308ca9ef021bf7ec241dbef7fa31aec8e63b41be200eb7530cd3d67d2a2c7d096",
    "u": "4af68649f3230c5589879f0cf33fd6d9f007cd3a54a2e6ed8699a576630fc025",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMjUxYTRmMzVmYTM4YzVlZGNlODNlMTY1OTZkZTAyYmU0ZTg3ZWM2YTkxYzVmZDgwYWI1NzdjMjI2NjhmYjZkZDVhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpo2FpWCEDCMqe8CG_fsJB2-9_oxrsjmO0G-IA63UwzT1n0qLH0JZhdVggSvaGSfMjDFWJh58M8z_W2fAHzTpUoubthpmldmMPwCVhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

[00]: ../00.md
