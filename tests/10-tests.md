# NUT-10 Test Vectors

These vectors cover [nutroot secrets](../10.md#nutroot-secrets-v3-keysets) (v3 keysets). All signatures are BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes them reproducible; verifiers **MUST** accept any valid signature.

## Conventions

Tagged hashes use the tags `Cashu_NutrootLeaf`, `Cashu_NutrootBranch` and `Cashu_NutrootTweak`; receiver-keyed blinding uses `Cashu_P2BK_v1` ([NUT-28](../28.md)); per-input signing messages use the tag `Cashu_TransactionInput`; the NUMS point is `0250929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0`. These are the normative constants of [NUT-10](../10.md), restated here so the vectors read standalone. Each tag hashes (SHA-256 of its UTF-8 bytes) to the `tag_hash` an implementation prefixes twice:

| Tag                      | `SHA256(tag)`                                                      |
| ------------------------ | ------------------------------------------------------------------ |
| `Cashu_NutrootLeaf`      | `e19ba80c5d6798399efd68b1d3b0e7ad57e79a2777310a9e6334934ee7a0b52b` |
| `Cashu_NutrootBranch`    | `f54194fd19dabbcca1474f329fe5ec065fc54d94063d14ae820788ba5bd8e55e` |
| `Cashu_NutrootTweak`     | `cc14d6872e6d0bc79a3dadb4c43f9362916bb6df512126dda139e65b812facd1` |
| `Cashu_TransactionInput` | `4996fee585f625e6a33865ce975efc32c42d2b1b95328385ce45f5209a16e9ec` |

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

A two-leaf tree under internal key `6`. Leaf 0 uses the **unallocated** type `0x05`, which makes this both a branch vector and a fail-closed vector: the commitment math below verifies, but a verifier **MUST** treat the `0x05` leaf as unsatisfiable, so a witness revealing it is rejected regardless of its (real) signature. Leaf 1 is an ordinary `after` leaf (key `3`, time `1758240000`) and is spendable once its locktime passes, with `path = [leaf_hash_0]`.

```json
{
  "internal_key": "03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
  "leaf_0_unknown_type": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a002103acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe",
  "leaf_1_after": "00020200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d00",
  "leaf_hash_0": "8714a51c3019861df9c4d0d6a1f30f0465ea1252e9c3b949802f73eda61cb101",
  "leaf_hash_1": "80468218b6e329d4d80682883617af0acd1d4a9d5b1658fbc448cc4781b4f254",
  "merkle_root": "9d8170c0f86d30de108834ff1ee334decac6ae094fb07652801d9c159c7b1bed",
  "tweak": "153e9c65e6bea3351f4e78145f328e5aae7e7a4722967bf347f057bcaa47bfba",
  "secret": "02f4ff2c2894698847760b62bce9d0d6c6c745d0d85c83577a00337d75437bccf0"
}
```

`merkle_root = tagged_hash("Cashu_NutrootBranch", leaf_hash_1 || leaf_hash_0)`: the pair is sorted, so `leaf_hash_1` comes first. A witness revealing `leaf_0_unknown_type` with `path = [leaf_hash_1]` reconstructs the secret but **MUST** be rejected as unsatisfiable (unknown leaf type).

## Worked example: a commit leaf

The auditable lock below with a `commit` leaf beside it: same NUMS `K` (`u = 7`), same `threshold` leaf, plus a `commit` leaf whose `hash` is `SHA256("external data")`. The commit leaf is never spendable; it only changes the root, so the proof is bound to whatever the digest covers. `P`'s only path is the `threshold` leaf, revealed with `path = [leaf_hash_commit]`: the mint sees the commitment as one sibling hash and nothing more. A witness revealing `leaf_commit` **MUST** be rejected.

```json
{
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "hash": "64451ff981aa92887b070762e97302df00a0ab97a853c323394b0a9cfaf46fae",
  "leaf_threshold": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101",
  "leaf_commit": "000408002064451ff981aa92887b070762e97302df00a0ab97a853c323394b0a9cfaf46fae",
  "leaf_hash_threshold": "b957f8b50199184bb5b29cdd1e3e4b14c63f35501e843000a6fb30cd00793cd6",
  "leaf_hash_commit": "20cccc22a45ddfdbec0647032487870dbeadb03471164eb6767b1234f9914f27",
  "merkle_root": "1414741279014d1a3f1dcd44dc6c512db584ea2824447eac2859c0fc12b01fad",
  "tweak": "2f2b4d5a1be62be21b2e7487f4f721ce7027fd17015d8e906a6de9c138253403",
  "secret": "0217b9074d62e061a85411367f73dbcda377fa8029650b75671b12cd4c6b9b3c28"
}
```

`merkle_root = tagged_hash("Cashu_NutrootBranch", leaf_hash_commit || leaf_hash_threshold)`: the pair is sorted, so the commit hash comes first. A `commit` leaf with any other field, or with `disclosure`, is malformed.

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

Spending this proof as the sole input of the [swap transaction](#transaction-transcripts) below, in place of its 8-sat input (same amount, keyset id and `C`; the two 4-sat outputs unchanged), gives:

```json
{
  "transaction_digest": "882b3bd6dba132160a3349fc64017214be68e3e150242f2a6f4ddfcb4aef49e6",
  "input_id": "1dda37bd259a04b176587b5804b192559f1b90608243ec5a3ba7b4d37b061f81",
  "input_digest": "1732e47d4ce0b6510a51c88ccc41cb7b5fe673987e635738d54d8ca9686336d1"
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
    "4cc8e5af02375b2497f5ad1c0241ea2de2b9ead33a6b5abd809bf27f8563967a13a0b484333e90e1d8622d5e884156ea40e1000587c25afe9904e1dbb85d0660"
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

`transaction_digest = SHA256(transcript)`; each input signs `input_digest = tagged_hash("Cashu_TransactionInput", transaction_digest || input_id)`, where `input_id = SHA256(input container record)`. The single-input transactions below place that container first; the separate multi-input vector identifies both containers explicitly. The `digest` key in each vector is the transaction digest. The keyset is a v3 keyset with id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6` (contributing raw bytes); a proof input's `03` is its `Y`, 48 bytes on a v3 keyset and 33 on a pre-v3 one (the mixed-keyset vector has both); quote ids contribute UTF-8 bytes; amounts are minimal big-endian. Single-proof examples use [NUT-13 V3](13-tests.md) counter `0`; the multi-input example also uses counter `1`.

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
  "transcript": "01008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "7d4783154ee7e697df3087d00206a26f74dab34fd469270f749ca14cc852d2aa",
  "input_id": "44002fef2fb9ce3168f3a4e88315290a890080c6c333c2fc47d5327f6c3616f3",
  "input_digest": "867091ad6dba3069bcff610e29300b5c1e2d89f0e5165f17d155000e77d18f9c"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "a46a08f9cf25bee38abe8e83a57dae316b64e826f3bd1a7261d3230cb97a70d910ffda84536464853b651cafeb3167affc13d1456d0647cdc685422ba56509a2"
  ]
}
```

**Multiple proof inputs.** Appending a second proof to the swap above, and changing the two output amounts to `8` and `4`, gives one shared transaction digest but a distinct signing digest for each proof. The appended input is the [NUT-13 V3](13-tests.md) counter `1` secret with the same `C`:

```json
{
  "amount": 4,
  "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
  "secret": "03a882e17eb79f4f87313b299e208f9109734d0211a8df307b1570dbad2cdf74bf",
  "C": "84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327"
}
```

The transaction and per-input digests, with each proof's key-path signature:

```json
{
  "digest": "9517f426f14d8dcf29aa4e44832f7cba5c44d754f2dde955fecdc0ad731610d6",
  "inputs": [
    {
      "input_id": "44002fef2fb9ce3168f3a4e88315290a890080c6c333c2fc47d5327f6c3616f3",
      "input_digest": "3c5ccb851c32f9822edc9f0851319a056e326a9020bc215c8409317e74a9aa1b",
      "signature": "51133bcfc80eb634ee6e746839d2abebd2741bd7b06cdef88356c8bc09555202b9a3b3666df73bc24a544d2010fde8fb3baec9feb4f4c30280dfc7a48c88280f"
    },
    {
      "input_id": "08960176e1785139ef04dc5ba5cd0484a285bd90907540a1b53e73767d6ffdaf",
      "input_digest": "720c3e060e4a01f7d064eec0ecde6cc6e65e60e6f527231b71c3112e32f68acf",
      "signature": "5069c493d313df6ab8728402cdf62e2998409c547ab4f22f121e07ff4af014bc0ce892b080c4ee3d188f709cc7bce4f288aa7f22862ad9ddc4569aa42d76135a"
    }
  ]
}
```

Each signature **MUST** verify only against its corresponding `input_digest`; neither signs the shared `digest`.

**Mixed keysets.** A transaction may spend pre-v3 and v3 inputs together (the migration path: old inputs, v3 outputs). Every proof input's `03` is its `Y` under its own keyset's version ([NUT-10](../10.md#nutroot-secrets-v3-keysets), [NUT-00](../00.md)). Here the swap's v3 input is joined by a pre-v3 input on keyset `00456a94ab4e1c46` (a v0 id, contributing its 8 raw bytes), paying two outputs of `8` and `2` on the v3 keyset:

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
      "C": "84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327"
    },
    {
      "amount": 2,
      "id": "00456a94ab4e1c46",
      "secret": "d341ee4871f1f889041e63cf0d3823c713eea6aff01e80f1719f08f9e5be98f6",
      "C": "02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2"
    }
  ],
  "outputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    },
    {
      "amount": 2,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

Each input's `Y` and container record, then the transcript and digests. Only the v3 input derives and signs an input digest; the pre-v3 input carries its own [NUT-11](../11.md) or bare witness as before, and its `input_id` is listed only to check the container bytes:

```json
{
  "inputs": [
    {
      "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
      "container": "01008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327",
      "input_id": "44002fef2fb9ce3168f3a4e88315290a890080c6c333c2fc47d5327f6c3616f3",
      "input_digest": "3f48aab72fb7ec0e29d1fa49e4e194f09110068fe94a95e8553f53755af55837",
      "signature": "4c4906b9093e30e404f29898d3905e14bc3ff85754cb210dc62f7da6b3e0bb612f3a09f5c33b0b504f389ba998d20f42f7dba80ceb22cd6cb0201b47e5e0dce7"
    },
    {
      "Y": "029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae",
      "container": "0100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2",
      "input_id": "22df4d688b7337f49aa47dd5d0dc6578506229c36908d79608c50d7814d1bd04"
    }
  ],
  "transcript": "01008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033270100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba203005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005b0100010202002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "e8eb75f3f209bbf592e7cc7ed727dcd33fe118add5ab7a992a3a2d7a9392d893"
}
```

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
  "digest": "271cb7d13b3de01fe693c8f1be0adcd7855ee2bed3532840778cdc9ff8a5b783",
  "input_id": "c7892510d9bd10a53d590f3454790546f0b5ae46d3ee2b6905b77592e4cb0346",
  "input_digest": "ca6970e6795f610be199bc1d4705dec7ef31f3939dcd08b8a1e2ea4960565f39"
}
```

**Partial mint.** Issuing 4 against 8-sat mint quote `quote-mint-0004`, with one 4-sat output. The quote input commits the 4 issued, not the quote's amount:

```
02 0016 | 01 0001 04 | 02 000f 71756f...303034
```

```json
{
  "transcript": "0200160100010402000f71756f74652d6d696e742d3030303403005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "e02e360bcd1f8350548ad44518f911eb026d4118aa068f1ec31935fa1ff83541",
  "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
  "input_id": "8a290719012a102a7de2957618a858a62075ef5651b84e3cb7287a5fc9959998",
  "input_digest": "7578e345637e38e71f68291a43d439d5284c3d16b02521660c8cd08dd3db2371",
  "signature": "1b6de2bf4674d6b6f8ea63ee221bd7c6d382166e8d6fb942d85133d31135402239b9bb3eb339476c76a192805aceaab59a3df3768d402d70639bb9cbec46c5cc"
}
```

The signature **MUST NOT** verify over the transcript that commits `8`.

**Batched mint.** A [NUT-29](../29.md) batch of two quotes, `quote-mint-0002` and `quote-mint-0003`, with `quote_amounts` of `[5, 3]` and the mint vector's 8-sat output. Each quote input commits its `quote_amounts` entry, and each lock key signs its own input digest:

```
02 0016 | 01 0001 05 | 02 000f 71756f...303032
02 0016 | 01 0001 03 | 02 000f 71756f...303033
```

```json
{
  "transcript": "0200160100010502000f71756f74652d6d696e742d303030320200160100010302000f71756f74652d6d696e742d3030303303005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "7309fef139318f9dc3faa7ec0b92208e6ff231ad007c6c3fcfc80343b4ad5bb7",
  "inputs": [
    {
      "quote_id": "quote-mint-0002",
      "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
      "input_id": "aaf0905f583d015ad1640e530c768797eab855034051e74fb7f725b5bdb96131",
      "input_digest": "04b6a1306d1a12640a91421b0117bbdf2880e6f186a0cbd2211db077e82019f0",
      "signature": "ee4e7131dad86f2d5c3f25f021e437cdeefe68ceff2bbe95e4a36974f4d78358b633ed7eb2cab2cac0d36f05669b1568c4b8b86cd4274cba0a596e5d87d63f6b"
    },
    {
      "quote_id": "quote-mint-0003",
      "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
      "input_id": "9976dbe45223a102e176fa2ede6973244157c5b82257d6e3e0f4977b32f0c706",
      "input_digest": "27aa267c0541b638c93b3d8c6324005654e9ac2663795c100c1d7dc8370dc2c5",
      "signature": "83a816f0bb9137e3523711e6136ce565229d0bd45ef2d0090a89b1c653046fc5fa067210310990ab3aed1ffabcb24a67f2db7d7700cc1243c5de20017b717728"
    }
  ]
}
```

**Melt.** Paying melt quote `quote-melt-0001` (quote amount 8 with a fee reserve of 0, so the output's amount is 8; no change outputs) with the swap's 8-sat proof as the only input; the melt quote is the only output, binding its quote id and that amount:

```json
{
  "transcript": "01008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033270400160100010802000f71756f74652d6d656c742d30303031",
  "digest": "1245d154ac77eaa2fa7107d236ca4f884b98babf0fd3812c660a364ded3618a0",
  "input_id": "44002fef2fb9ce3168f3a4e88315290a890080c6c333c2fc47d5327f6c3616f3",
  "input_digest": "269af868bed9f69ccb9de137ce2307a1d11f981fd936035debcfa0314d80a7e2"
}
```

The melt spends the swap's proof, so it shares the swap's `input_id`; the differing transcripts give it a different `input_digest`, so neither witness verifies in the other transaction.

**Melt with change.** The same melt carrying two [NUT-08](../08.md) blank change outputs (amount 0, on the same keyset with the swap's `B_`). Containers group in ascending type order, so the blank outputs (type `0x03`) precede the melt quote (type `0x04`) in the transcript regardless of the request's field order; note each blank's zero amount encodes to a zero-length record (`010000`):

```json
{
  "transcript": "01008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd550400160100010802000f71756f74652d6d656c742d30303031",
  "digest": "9443ab45dd96f0476d058c41f120c74838412eea361752bf45a2211e42aaffb4",
  "input_id": "44002fef2fb9ce3168f3a4e88315290a890080c6c333c2fc47d5327f6c3616f3",
  "input_digest": "1604341ea199ab31b9890f02bfb559ae7f767ac9eaf03b315e4aa274458a105d"
}
```

## Transport strings

Both strings are the prefix followed by base64url (no padding) of the JSON shown; the JSON is not canonical, so decoders parse rather than compare. Amounts are JSON integers.

**Signing package.** The [auditable lock](#worked-example-auditable-lock-with-disclosure) spent through its one leaf as the sole input of the [swap](#transaction-transcripts) (8 sat in, two 4-sat outputs). The package carries the transaction's inputs (by `Y`, as the transcript does; the spend entry names its proof's secret) and outputs, and one spend awaiting signatures; `path` is empty because the tree has one leaf, and there is no `E` or `slots` because the key is not blinded:

```json
{
  "version": "nutspA",
  "type": "swap",
  "inputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "Y": "aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe7",
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
  ],
  "spends": [
    {
      "secret": "02fc11bf4f939f2bfd47e4cee799c8254fc4acc27a134c729edfc3c6a3c13a053b",
      "leaf": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101",
      "control": {
        "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
        "path": []
      },
      "signatures": []
    }
  ]
}
```

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHlwZSI6InN3YXAiLCJpbnB1dHMiOlt7ImFtb3VudCI6OCwiaWQiOiIwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYiLCJZIjoiYWFiYTQ2YTQ2M2QzZDEwYjU5ZmExNTMyYTMyZDlhNWU4ZmE4ZTk5NjJhOGM2NTcxOTE3OTgxYTZmYTRkNWZhZmIwOGMyMWJiZmY5NDE4OWUyNGU1YzI1NmZjMGE3ZmU3IiwiQyI6Ijg0ZDFiNzI5MWFlNTczN2YzYzg1MWFhMzNjYWZlMGY3YWZlYjVjY2I0ZGEwODZjNDgyYmI4NWI3NTI1ZTYxNTQ3ZjFiNWE2ZDFhMDFiMWZlZDFmOTYwZDFhOWQwMzMyNyJ9XSwib3V0cHV0cyI6W3siYW1vdW50Ijo0LCJpZCI6IjAyYjdlMDc3ZDAyMGZhYmVkNDU2YTZiZTEzOGE4ZTIwZTllZjQwYjQ0ZDg3M2ZhMTJjMDA1YjY1NmViMGNmOTlmNiIsIkJfIjoiYjQyYTBiY2MzOTU5OGRiMWRjYTYxN2FlZWE2YmMzNjdmMjU2NjYzNjgyNmRjOTYxYTU0ZmFhZTE1YjNiOGQxMGFmYzFjYjAyMDZlNzBhYjNiMGUxMmMyYjk0NzhjZDU1In0seyJhbW91bnQiOjQsImlkIjoiMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2IiwiQl8iOiJiNDJhMGJjYzM5NTk4ZGIxZGNhNjE3YWVlYTZiYzM2N2YyNTY2NjM2ODI2ZGM5NjFhNTRmYWFlMTViM2I4ZDEwYWZjMWNiMDIwNmU3MGFiM2IwZTEyYzJiOTQ3OGNkNTUifV0sInNwZW5kcyI6W3sic2VjcmV0IjoiMDJmYzExYmY0ZjkzOWYyYmZkNDdlNGNlZTc5OWM4MjU0ZmM0YWNjMjdhMTM0YzcyOWVkZmMzYzZhM2MxM2EwNTNiIiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOTBhMDAwMTAxIiwiY29udHJvbCI6eyJLIjoiMDI4ZWRmZWJkNmZkZWEzZTFkODkzNTlhZjIwODY4YTJlNzYzMTViMzZjZGIxYTc5ZGU0OTdhMTc1N2NhN2JkNDA3IiwicGF0aCI6W119LCJzaWduYXR1cmVzIjpbXX1dfQ
```

Key `3` signs the spend's input digest (`1732e47d...`, see the worked example) and returns the package with `signatures` filled, which merges back into the transaction as the [script-path witness](#worked-example-auditable-lock-with-disclosure) shown there:

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHlwZSI6InN3YXAiLCJpbnB1dHMiOlt7ImFtb3VudCI6OCwiaWQiOiIwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYiLCJZIjoiYWFiYTQ2YTQ2M2QzZDEwYjU5ZmExNTMyYTMyZDlhNWU4ZmE4ZTk5NjJhOGM2NTcxOTE3OTgxYTZmYTRkNWZhZmIwOGMyMWJiZmY5NDE4OWUyNGU1YzI1NmZjMGE3ZmU3IiwiQyI6Ijg0ZDFiNzI5MWFlNTczN2YzYzg1MWFhMzNjYWZlMGY3YWZlYjVjY2I0ZGEwODZjNDgyYmI4NWI3NTI1ZTYxNTQ3ZjFiNWE2ZDFhMDFiMWZlZDFmOTYwZDFhOWQwMzMyNyJ9XSwib3V0cHV0cyI6W3siYW1vdW50Ijo0LCJpZCI6IjAyYjdlMDc3ZDAyMGZhYmVkNDU2YTZiZTEzOGE4ZTIwZTllZjQwYjQ0ZDg3M2ZhMTJjMDA1YjY1NmViMGNmOTlmNiIsIkJfIjoiYjQyYTBiY2MzOTU5OGRiMWRjYTYxN2FlZWE2YmMzNjdmMjU2NjYzNjgyNmRjOTYxYTU0ZmFhZTE1YjNiOGQxMGFmYzFjYjAyMDZlNzBhYjNiMGUxMmMyYjk0NzhjZDU1In0seyJhbW91bnQiOjQsImlkIjoiMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2IiwiQl8iOiJiNDJhMGJjYzM5NTk4ZGIxZGNhNjE3YWVlYTZiYzM2N2YyNTY2NjM2ODI2ZGM5NjFhNTRmYWFlMTViM2I4ZDEwYWZjMWNiMDIwNmU3MGFiM2IwZTEyYzJiOTQ3OGNkNTUifV0sInNwZW5kcyI6W3sic2VjcmV0IjoiMDJmYzExYmY0ZjkzOWYyYmZkNDdlNGNlZTc5OWM4MjU0ZmM0YWNjMjdhMTM0YzcyOWVkZmMzYzZhM2MxM2EwNTNiIiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOTBhMDAwMTAxIiwiY29udHJvbCI6eyJLIjoiMDI4ZWRmZWJkNmZkZWEzZTFkODkzNTlhZjIwODY4YTJlNzYzMTViMzZjZGIxYTc5ZGU0OTdhMTc1N2NhN2JkNDA3IiwicGF0aCI6W119LCJzaWduYXR1cmVzIjpbIjRjYzhlNWFmMDIzNzViMjQ5N2Y1YWQxYzAyNDFlYTJkZTJiOWVhZDMzYTZiNWFiZDgwOWJmMjdmODU2Mzk2N2ExM2EwYjQ4NDMzM2U5MGUxZDg2MjJkNWU4ODQxNTZlYTQwZTEwMDA1ODdjMjVhZmU5OTA0ZTFkYmI4NWQwNjYwIl19XX0
```

**Spend receipt.** The payer's receipt for the [swap](#transaction-transcripts)'s bearer input: its [V4 token](#v4-tokens-with-spend-info) (with `spend_info.k`, harmless once spent), and one receipt whose `transcript` is the swap's TLV transcript, so `SHA256(transcript)` is the transaction digest. `Y`, `input_digest`, the witness and the commitment are the [NUT-07 vector](07-tests.md)'s:

```json
{
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmU2ZTdjZmE3YjgyZDRiM2I0NDlmYTY0NjZjODkzNDY5YTcyN2QwMjE0ZDQ4ZGI0OTU2YTYwNTRiODAyMmEyOWJhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFrWCBHGW3AgRUM4T_Q5Hi4txgxuCW-OJIRycVqgGKmGvcDRw",
  "receipts": [
    {
      "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
      "keysetId": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "inputDigest": "867091ad6dba3069bcff610e29300b5c1e2d89f0e5165f17d155000e77d18f9c",
      "witness": "{\"signatures\":[\"a46a08f9cf25bee38abe8e83a57dae316b64e826f3bd1a7261d3230cb97a70d910ffda84536464853b651cafeb3167affc13d1456d0647cdc685422ba56509a2\"]}",
      "commitment": "80ef4c3484dd76f89eab82d2a24178f89259507cb6d1c5dfc3cb573fa9597f5b",
      "transcript": "01008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

```
nutrcAeyJ0b2tlbiI6ImNhc2h1Qm8yRnRjV2gwZEhCek9pOHZiV2x1ZEM1MFpYTjBZWFZqYzJGMFlYU0JvbUZwU0FLMzRIZlFJUHEtWVhDQnBHRmhDR0Z6ZUVJd01tVTJaVGRqWm1FM1lqZ3laRFJpTTJJME5EbG1ZVFkwTmpaak9Ea3pORFk1WVRjeU4yUXdNakUwWkRRNFpHSTBPVFUyWVRZd05UUmlPREF5TW1FeU9XSmhZMWd3aE5HM0tScmxjMzg4aFJxalBLX2c5Nl9yWE10Tm9JYkVncnVGdDFKZVlWUl9HMXB0R2dHeF90SDVZTkdwMERNblluTnBvV0ZyV0NCSEdXM0FnUlVNNFRfUTVIaTR0eGd4dUNXLU9KSVJ5Y1ZxZ0dLbUd2Y0RSdyIsInJlY2VpcHRzIjpbeyJZIjoiYTBhY2Y5MzlmMDMzZTNkMGFlOWI1Zjc4NDM0MWZhZGEzODM2N2VlYzE5MGVkZmIzNGUxZjBjY2U5MDUwYzgwNjcyZGJlZTc3YTc1MTJiNzI0MzU0NGM4NWFlMjkwYTczIiwia2V5c2V0SWQiOiIwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYiLCJpbnB1dERpZ2VzdCI6Ijg2NzA5MWFkNmRiYTMwNjliY2ZmNjEwZTI5MzAwYjVjMWUyZDg5ZjBlNTE2NWYxN2QxNTUwMDBlNzdkMThmOWMiLCJ3aXRuZXNzIjoie1wic2lnbmF0dXJlc1wiOltcImE0NmEwOGY5Y2YyNWJlZTM4YWJlOGU4M2E1N2RhZTMxNmI2NGU4MjZmM2JkMWE3MjYxZDMyMzBjYjk3YTcwZDkxMGZmZGE4NDUzNjQ2NDg1M2I2NTFjYWZlYjMxNjdhZmZjMTNkMTQ1NmQwNjQ3Y2RjNjg1NDIyYmE1NjUwOWEyXCJdfSIsImNvbW1pdG1lbnQiOiI4MGVmNGMzNDg0ZGQ3NmY4OWVhYjgyZDJhMjQxNzhmODkyNTk1MDdjYjZkMWM1ZGZjM2NiNTczZmE5NTk3ZjViIiwidHJhbnNjcmlwdCI6IjAxMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYTBhY2Y5MzlmMDMzZTNkMGFlOWI1Zjc4NDM0MWZhZGEzODM2N2VlYzE5MGVkZmIzNGUxZjBjY2U5MDUwYzgwNjcyZGJlZTc3YTc1MTJiNzI0MzU0NGM4NWFlMjkwYTczMDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MDMwMDViMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMzBiNDJhMGJjYzM5NTk4ZGIxZGNhNjE3YWVlYTZiYzM2N2YyNTY2NjM2ODI2ZGM5NjFhNTRmYWFlMTViM2I4ZDEwYWZjMWNiMDIwNmU3MGFiM2IwZTEyYzJiOTQ3OGNkNTUwMzAwNWIwMTAwMDEwNDAyMDAyMTAyYjdlMDc3ZDAyMGZhYmVkNDU2YTZiZTEzOGE4ZTIwZTllZjQwYjQ0ZDg3M2ZhMTJjMDA1YjY1NmViMGNmOTlmNjAzMDAzMGI0MmEwYmNjMzk1OThkYjFkY2E2MTdhZWVhNmJjMzY3ZjI1NjY2MzY4MjZkYzk2MWE1NGZhYWUxNWIzYjhkMTBhZmMxY2IwMjA2ZTcwYWIzYjBlMTJjMmI5NDc4Y2Q1NSJ9XX0
```

A verifier recomputes `input_digest` from `transcript` and the token's proof, the commitment from `Y`, `input_digest` and the witness, and checks the witness signature against the secret over `input_digest`; matching the commitment against the mint's for `Y` ties the receipt to the spend.

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
