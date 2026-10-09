# NUT-10 Test Vectors

These vectors cover [nutroot secrets](../10.md#nutroot-secrets-v3-keysets) (v3 keysets). All signatures are BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes them reproducible; verifiers **MUST** accept any valid signature.

## Conventions

Tag hashes ([NUT-10](../10.md)); the NUMS point is `0250929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0`:

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

`threshold_1of1_key3_disclosure` appends the `disclosure` field (`0a000101`).

## The tree fold

A three-leaf tree (`threshold_1of1_key3`, `after_1of1_key4`, `hashlock_1of1_key3`, in transmitted order). Sorted by leaf hash the order is `h0, h2, h1`: `h0` and `h2` pair and `h1` is promoted, so the path for leaf 2 is `[h0, h1]`.

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

The commitment also verifies through `path_for_index_2` from leaf 2 alone.

Two copies of `threshold_1of1_key3` under internal key `6`: the root is `tagged_hash("Cashu_NutrootBranch", h || h)`, not the single-leaf `h`, and either copy spends with `path = [h]`:

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

`keypath_priv` is the key Carol signs with.

The witnesses below sign an **illustrative** input digest, `SHA256("illustrative transaction transcript")` = `e1d7170b89a2b6eedec90453e32b6c320dfadd590e6a6454bddec95a0e3834cd`. Carol's key-path witness:

```json
{
  "signatures": [
    "619e0726595b5adff06cc3e6ea1c409f10f7b064cf8888f0eed0efbac854eabf4632642930bdc7c4d7d983379301a4f263991dbd19d96e5ebcfab9e8583bd510"
  ]
}
```

Alice's script-path witness after the locktime:

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

## Worked example: a template covenant

A proof that can only be spent into the two change quote outputs of the [proof to two change quotes](#transaction-transcripts) transaction below (3 sat to key `5`, the remainder to key `6`), by key `3` until `1758240000`, then by key `3` freely. The `template` leaf's `hash` is `SHA256` over that transaction's output section, the two change quote containers concatenated; the internal key is the same NUMS offset as the [auditable lock](#worked-example-auditable-lock-with-disclosure) (`u = 7`), so no key path exists. The spend is the swap's 8-sat input (same amount, keyset id and `C`) under this secret.

```json
{
  "output_section": "23002801000103020021022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe423002402002103fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
  "hash": "1588c70281ee4113a1dc18656ad41d197be43c5b04228dfa3d1653d8a8259815",
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d000800201588c70281ee4113a1dc18656ad41d197be43c5b04228dfa3d1653d8a8259815",
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "merkle_root": "47b588a5570157a99045bb9c3d345aff2422693099b607e5f985202675beae49",
  "tweak": "9c69d71547bb11f186438aa5c4f18a61789c25c990304613d59c4a7d6e51e71f",
  "secret": "031e656e31f7dbc918d662dd91343f077a9d94aec46f754d9e2332775f08019576",
  "transaction_digest": "ef4af8ce6554f61e5ed2f2b8f1f6727c3cffeb67120d4e5b98c458752c626dc8",
  "input_id": "1fcda016464ddd2f58ac013f4d27a7eb87d0e06d44796c4a17fd819d756ba66b",
  "input_digest": "6a38d7bba2bc18d81abe2ac9b478e25cc46dd5264070412de9bebec18025ccc5"
}
```

The template leaf, spelled out (`n = 1`, `keys = [key 3]`, `time = 1758240000`, then `hash`):

```
00 05 | 02 0001 01 | 04 0021 02f930...e036f9 | 06 0004 68cc9d00 | 08 0020 1588c7...259815
```

Key `3`'s script-path witness over that `input_digest`:

```json
{
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d000800201588c70281ee4113a1dc18656ad41d197be43c5b04228dfa3d1653d8a8259815",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": []
  },
  "signatures": [
    "ce51e3afd1858bb511223e0a2718dde5e271584c874549aeec41b6313fd10829f320ad88edc9ae80baf9263b8a98fc98c7454d79cf9e4956bde9ce4b8d981ee5"
  ]
}
```

The same proof spent with the fixed quote at 4 sat instead of 3 (one byte of the output section, `23002801000104...`) hashes its outputs to `c859f4a83d97c153e11e5b8c59f485a8befcce05870a877467d876c64a2e6a7d`, so the witness **MUST** be rejected whatever it signs.

## Worked example: two leaves and a filled path

The template leaf above beside an `after` leaf (key `3`, time `1758240000`) under internal key `6`, the parent's key path: until the locktime key `3` can only spend into the template's outputs, after it key `3` spends freely through either leaf, and key `6` can always spend via the key path. The `after` leaf would normally name different keys; it is kept here for a filled path. Leaf 0 is the template, leaf 1 the `after` leaf.

```json
{
  "internal_key": "03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
  "leaf_0_template": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d000800201588c70281ee4113a1dc18656ad41d197be43c5b04228dfa3d1653d8a8259815",
  "leaf_1_after": "00020200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d00",
  "leaf_hash_0": "47b588a5570157a99045bb9c3d345aff2422693099b607e5f985202675beae49",
  "leaf_hash_1": "80468218b6e329d4d80682883617af0acd1d4a9d5b1658fbc448cc4781b4f254",
  "merkle_root": "2887131fc650d8315c7d25d9299ca153b7a4ebb11f8f54d8c1bbedfc11904855",
  "tweak": "85f5dae5f152e58829e0daa508d23a66c530984140bcfb561517764df13bc6dd",
  "secret": "02ec5b37085b359c928e372e0f29a54ca1e9d4d445444756bf17159782286eb673"
}
```

`merkle_root = tagged_hash("Cashu_NutrootBranch", leaf_hash_0 || leaf_hash_1)`: the pair is sorted, so `leaf_hash_0` comes first. Spending this proof into the template's outputs (the same transaction as above under this secret: `input_digest` `e7d0745e65fb1c2d0218004a15c3992f4ea816a8e9c22ab8be0613820b01c4b8`) reveals leaf 0 with `path = [leaf_hash_1]`:

```json
{
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468cc9d000800201588c70281ee4113a1dc18656ad41d197be43c5b04228dfa3d1653d8a8259815",
  "control": {
    "K": "03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
    "path": ["80468218b6e329d4d80682883617af0acd1d4a9d5b1658fbc448cc4781b4f254"]
  },
  "signatures": [
    "c2fa806522cfdc676b40ec9954192abdd37a40ed8cc36d9479bac50e3522767725783f05dc2bf44d6de59587cb386b50f7590d4c364b05ed7e8504f824f06e2a"
  ]
}
```

After the locktime, key `3` reveals leaf 1 instead, with `path = [leaf_hash_0]`.

## Worked example: a commit leaf

The auditable lock below plus a `commit` leaf whose `hash` is `SHA256("external data")` (same NUMS `K`, `u = 7`). `P` spends through the `threshold` leaf with `path = [leaf_hash_commit]`; a witness revealing `leaf_commit` **MUST** be rejected.

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

A `commit` leaf with any other field, or with `disclosure`, is malformed.

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
  "transaction_digest": "a892e0859fc0817fab1671b5515579611aed1666bc56938ad5dcc80120586213",
  "input_id": "185bbd6a83656cce61890e8ba015be2629bc745c991dd7936cc2e61911bf0f19",
  "input_digest": "4b7ffce02cb6ea76d04aaafaa40c0b0522cfcd35f01e3ba697b004b6953cead2"
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
    "e8dc3839d64485f75555d9b459ab0f0cab46d5a0420bb80f661b253e9431d0e42526f974f4118c52f95b12427f9cfd2ad24fa7d3c2c93560a08063f849026100"
  ]
}
```

The [NUT-07 vectors](07-tests.md) carry the matching commitment and opening.

## Rejection vectors

An unknown field rejects, and odd type numbers are reserved with none allocated, so this leaf (`threshold_1of1_key3` with a four-byte field `0x09` appended) is malformed. An unallocated leaf type is unsatisfiable: the same leaf's bytes under type `0xff` parse to nothing, so a tree containing it still commits (its hash is one more sibling) but a witness revealing it **MUST** be rejected regardless of its signature:

```json
{
  "leaf_unknown_field": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9090004deadbeef",
  "leaf_unknown_type": "00ff0200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9"
}
```

Appending `0a000100` (mode `0x00`), `0a0000` (empty) or `0a000102` (unallocated mode) to `threshold_1of1_key3` makes it malformed:

```json
{
  "leaf_disclosure_mode0": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000100",
  "leaf_disclosure_empty": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a0000",
  "leaf_disclosure_mode2": "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000102"
}
```

Listing Carol's key-path signature twice, or Alice's script-path signature twice (her leaf lists one key), makes each witness above invalid.

## Empty tweak

The empty tweak, `t = tagged_hash("Cashu_NutrootTweak", K)` with no merkle root, for `K` = public key of `3`:

```json
{
  "internal_key": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "tweak": "764c0e0da0d17acb5cc863fbe939211869e04e522c017171a0b71e91d5b69908",
  "secret": "03b2bb251c006ae42d9c19f3157d02b3c347b1fb6512885225a8699a06d9233aee",
  "keypath_priv": "764c0e0da0d17acb5cc863fbe939211869e04e522c017171a0b71e91d5b6990b"
}
```

## Transaction transcripts

Keyset `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6` (v3). Proofs use [NUT-13 V3](13-tests.md) counter `0`, and `1` in the multi-input vector. `digest` is the transaction digest.

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
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5521005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "b7dcf0abc714b1716211fa00a0b595475fb247031ce3f2868b23456200fdf630",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "cb464413d088ae738b9f78141a02d49f51c6ad85029b6e43cb3ac86ef327990e"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "45fa48240f7793b749aa5a5b7c4a9abaf836a81dfaa690df20a61d6916b812130febdb02e3806be59a1dd01a03bf8ee51252e42cff87a6e065aa1daa2c5e9c0a"
  ]
}
```

**Multiple proof inputs.** The swap above plus a second proof (the [NUT-13 V3](13-tests.md) counter `1` secret, same `C`), with outputs of `8` and `4`:

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
  "digest": "840af8e9a375ebba48372b12903b5a054c6b4fbd331e6bc945fb0699a810187b",
  "inputs": [
    {
      "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
      "input_digest": "9774434402282a1901d41f15b47d40c90d40ec614ec2d7978217e308e8d5a394",
      "signature": "16cd91fef9205b0ed1e23574a6f745393a0ec190360b36d6eee056b88eba91ef9284e7078e6168486ad0edc1c036ee240536bc554305daa80a13987965b45be4"
    },
    {
      "input_id": "0182252f564bf76e42e45514955b50c6bd6381b6c4971c8027cd5a6a90817c4b",
      "input_digest": "6cbb64956add1020e506ed8abe833f19f79bb4cec2b287b586cdad05abfd13c0",
      "signature": "918c176b99ee312384f6559da45e7ffc328e19e4be575a9d37b00d4fe946e796ee4b5ed1316a0f05a29628e01c961f6ca62272612ef1efc8d7c99831956bff3f"
    }
  ]
}
```

Each signature **MUST** verify only against its corresponding `input_digest`; neither signs the shared `digest`.

**Mixed keysets.** The swap's v3 input joined by a pre-v3 input on keyset `00456a94ab4e1c46` (a v0 id), paying two outputs of `8` and `2` on the v3 keyset:

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

Each input's `Y` and container record, then the transcript and digests. Only the v3 input signs an input digest; the pre-v3 input's `input_id` is listed only to check the container bytes:

```json
{
  "inputs": [
    {
      "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
      "container": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327",
      "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
      "input_digest": "a01808ebee8586577034824a151a2558910496144b5fa020dbfd431f3b421021",
      "signature": "e103fff937b80b45cd8d5a3a6fa739e7c26fc20d5067b94cfeaf506b3ecbfd1f5c693c5988fb8e8d7f53ce9e09092611c7ac9e4da26d36db5d120d968857d745"
    },
    {
      "Y": "029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae",
      "container": "1100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2",
      "input_id": "efbdd5d14874cb021fc962d93a9848553ca65ae101e9b57f6678aa37ffe1ebd9"
    }
  ],
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033271100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba221005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5521005b0100010202002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "f3eda61cef37e0ea952968fecf7a54fa2ee31fd5b9b62a3ec0e6cbcab5675f0e"
}
```

**Mint.** Mint quote `quote-mint-0001` (amount 8) with one 8-sat output, locked to the [NUT-13 quote lock key](13-tests.md#version-3-secret-derivation) of counter `0` (`0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812`):

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
  "transcript": "12003a0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981221005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "15322931ec8853ee9fee34cebefe0aba1ca04df7b14267d46a2d5d6361476b58",
  "input_id": "36683e426305851b0c5bee1a8b9d567a5a0a3feba6252c4144aefde0ec852ef1",
  "input_digest": "76fd9ab46843a003bff3b81e0875b30ddfe413b09d1e1cfad399972f498f106f"
}
```

**Partial mint.** Issuing 4 against 8-sat mint quote `quote-mint-0004`, with one 4-sat output:

```
12 003a | 01 0001 04 | 02 000f 71756f...303034 | 03 0021 029290...209812
```

```json
{
  "transcript": "12003a0100010402000f71756f74652d6d696e742d303030340300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981221005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "7db5f2b9b50d7a4883b80f96885d21675e3c841945d70994649d147e8744f2a2",
  "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
  "input_id": "b2b5f1be66f3ac7a12fec7f3f063d0399793a70fbcbee81d39a9a279a908d9bd",
  "input_digest": "7c8e461d87bdcb275810c2bc00a5b33f87c1d2789ffac120262f7a2b04177564",
  "signature": "37ce63cb54e3e6cb9fd075abb754c1e098305ccb73fcdedd4981262c4e03957561569b3604bf5932aaec54b911647756222fa1a88f951eed0ed9bdd6a6a05105"
}
```

The signature **MUST NOT** verify over the transcript that commits `8`.

**Batched mint.** A [NUT-29](../29.md) batch of `quote-mint-0002` and `quote-mint-0003` with `quote_amounts` of `[5, 3]` and the mint vector's 8-sat output:

```
12 003a | 01 0001 05 | 02 000f 71756f...303032 | 03 0021 029290...209812
12 003a | 01 0001 03 | 02 000f 71756f...303033 | 03 0021 02b357...99615d
```

```json
{
  "transcript": "12003a0100010502000f71756f74652d6d696e742d303030320300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981212003a0100010302000f71756f74652d6d696e742d3030303303002102b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d21005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "1fcc843aeb8a087e0c348c9b6b9fb2cef155039deb3bd7d4d2610c5c9447cdaf",
  "inputs": [
    {
      "quote_id": "quote-mint-0002",
      "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
      "input_id": "dd1472cce2ae89c5134d54a9fba5f99f26c212cda68cf6d0bba7f8f2e253f425",
      "input_digest": "344ae975bbecbb734a663e756cc0413bfa50a5bf4f1577fd5e86fac3064fc86c",
      "signature": "46bf2b2ac046694ef33037ca8d3e1ca5e8119fb837887d41ac631059059436a163a9a5f43594bef92e162e7b16f7d490293591789e69074fe5d4a5fcd5eccafb"
    },
    {
      "quote_id": "quote-mint-0003",
      "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
      "input_id": "78bd15ebfccf1774d313df80acf0ac276aaac32bb581c8555870d1f36a728248",
      "input_digest": "b6cc535347c07bea1cc167796a6f6febce4daaf60df9c2275229d5f52297ce7e",
      "signature": "2be4e6dbaaf205e433894c289496236079a537e37552a037437efe19430d3938c6630d71eced65cb60e9a52f730a25200403fdf3c4d738edc99b51004bebd838"
    }
  ]
}
```

**Melt.** Paying melt quote `quote-melt-0001` (amount 8, fee reserve 0, no change outputs) with the swap's 8-sat proof:

```json
{
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033272200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "1b9e4e88ad05d873bee5b00a3d621e9a6565bb611a27174dfc17d268dffd38c2",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "5319b114091bd127f42fd209b4b363d13a145da174c534fb8fa4c584a8405c0f"
}
```

The melt shares the swap's `input_id` but not its `input_digest`, so neither witness verifies in the other transaction.

**Melt with change.** The same melt with two [NUT-08](../08.md) blank outputs (amount 0) on the swap's keyset and `B_`. They precede the melt quote in the transcript, and each zero amount encodes as `010000`:

```json
{
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5521005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd552200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "48ab8b928ef9aa667d7a6144b07533c5ce0b902c624257646757301835bc6055",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "807572ffbc0582b8bf4cf9720a9ff4695e008cb41bdaa281cc06182e70ba4379"
}
```

**Mint quote to melt.** Paying melt quote `quote-melt-0001` straight from mint quote `quote-mint-0001` in one transaction ([NUT-XX](../XX.md)): no proofs and no change outputs, so the transcript is the mint vector's quote input container followed by the melt vector's melt quote container. The quote input's bytes are unchanged, so it keeps the mint vector's `input_id`; the new transcript gives it a new `input_digest`, which its lock key signs:

```json
{
  "transcript": "12003a0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d2098122200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "39478135ba23dba30de68edd11991b2c4d8edb8faeb680d8a7e3e415e8e9ab56",
  "input_id": "36683e426305851b0c5bee1a8b9d567a5a0a3feba6252c4144aefde0ec852ef1",
  "input_digest": "6e78356a9d2ea49dca461114c299256362ee76ed03a173729d0170daa13666a7"
}
```

**Proof to change quote.** Parking the swap's 8-sat proof in a remainder quote locked to key `5` ([NUT-XX](../XX.md)): the change quote output is the only output, and with no amount it binds the lock key alone.

The change quote container, spelled out:

```
23 0024 | 02 0021 022f8b...40efe4
```

The proof input keeps the swap's `input_id`; `quote_id` is the id the mint gives the change quote, derived from its lock key:

```json
{
  "change_container": "230024020021022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "quote_id": "a4a5abdbbd7fb43ff3891c5335c461b7be1032e954e9f7ba43785224f6e5c030",
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327230024020021022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "digest": "824bef448b38a40312f98bbb58b8d2dc8afa84e71647a4a1122e0bf62a4924e0",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "30a20a07c0ece5536a13257480fdf2636011f0b89b2f2033c32ca5009b6617aa"
}
```

**Proof to two change quotes.** Splitting the same proof between a 3-sat change quote locked to key `5` and a remainder quote locked to key `6`, in that request order: the fixed quote's container carries its amount first, the remainder quote's does not, and no keyset appears in the transcript.

```
23 0028 | 01 0001 03 | 02 0021 022f8b...40efe4
23 0024 | 02 0021 03fff9...297556
```

```json
{
  "change_containers": [
    "23002801000103020021022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "23002402002103fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556"
  ],
  "quote_ids": [
    "a4a5abdbbd7fb43ff3891c5335c461b7be1032e954e9f7ba43785224f6e5c030",
    "cbabdabc03877d03af1dc6882c60af1b79225c1cef9d2bde81749e0bd3ad740d"
  ],
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332723002801000103020021022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe423002402002103fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
  "digest": "3a778d64a738526124c1858d7b5def958a2e14736383650e49a9ea46e720ceda",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "c161aeecde16ff65ad29127d23a3c6dd47ac2bc52a0d2d7572c7dddb7dfdfc11"
}
```

## Transport strings

Each string is its prefix plus base64url (no padding) of the JSON shown. The JSON is not canonical, so decoders parse rather than compare.

**Signing package.** The [auditable lock](#worked-example-auditable-lock-with-disclosure) as the sole input of the [swap](#transaction-transcripts), with one spend awaiting signatures on input `0`:

```json
{
  "version": "nutspA",
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe704003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5521005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "spends": [
    {
      "input": 0,
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
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjExMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYWFiYTQ2YTQ2M2QzZDEwYjU5ZmExNTMyYTMyZDlhNWU4ZmE4ZTk5NjJhOGM2NTcxOTE3OTgxYTZmYTRkNWZhZmIwOGMyMWJiZmY5NDE4OWUyNGU1YzI1NmZjMGE3ZmU3MDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MjEwMDViMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMzBiNDJhMGJjYzM5NTk4ZGIxZGNhNjE3YWVlYTZiYzM2N2YyNTY2NjM2ODI2ZGM5NjFhNTRmYWFlMTViM2I4ZDEwYWZjMWNiMDIwNmU3MGFiM2IwZTEyYzJiOTQ3OGNkNTUyMTAwNWIwMTAwMDEwNDAyMDAyMTAyYjdlMDc3ZDAyMGZhYmVkNDU2YTZiZTEzOGE4ZTIwZTllZjQwYjQ0ZDg3M2ZhMTJjMDA1YjY1NmViMGNmOTlmNjAzMDAzMGI0MmEwYmNjMzk1OThkYjFkY2E2MTdhZWVhNmJjMzY3ZjI1NjY2MzY4MjZkYzk2MWE1NGZhYWUxNWIzYjhkMTBhZmMxY2IwMjA2ZTcwYWIzYjBlMTJjMmI5NDc4Y2Q1NSIsInNwZW5kcyI6W3siaW5wdXQiOjAsInNlY3JldCI6IjAyZmMxMWJmNGY5MzlmMmJmZDQ3ZTRjZWU3OTljODI1NGZjNGFjYzI3YTEzNGM3MjllZGZjM2M2YTNjMTNhMDUzYiIsImxlYWYiOiIwMDAxMDIwMDAxMDEwNDAwMjEwMmY5MzA4YTAxOTI1OGMzMTA0OTM0NGY4NWY4OWQ1MjI5YjUzMWM4NDU4MzZmOTliMDg2MDFmMTEzYmNlMDM2ZjkwYTAwMDEwMSIsImNvbnRyb2wiOnsiSyI6IjAyOGVkZmViZDZmZGVhM2UxZDg5MzU5YWYyMDg2OGEyZTc2MzE1YjM2Y2RiMWE3OWRlNDk3YTE3NTdjYTdiZDQwNyIsInBhdGgiOltdfSwic2lnbmF0dXJlcyI6W119XX0
```

Signed by key `3` over input digest `4b7ffce0...`, it merges into the [script-path witness](#worked-example-auditable-lock-with-disclosure) shown there:

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjExMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYWFiYTQ2YTQ2M2QzZDEwYjU5ZmExNTMyYTMyZDlhNWU4ZmE4ZTk5NjJhOGM2NTcxOTE3OTgxYTZmYTRkNWZhZmIwOGMyMWJiZmY5NDE4OWUyNGU1YzI1NmZjMGE3ZmU3MDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MjEwMDViMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMzBiNDJhMGJjYzM5NTk4ZGIxZGNhNjE3YWVlYTZiYzM2N2YyNTY2NjM2ODI2ZGM5NjFhNTRmYWFlMTViM2I4ZDEwYWZjMWNiMDIwNmU3MGFiM2IwZTEyYzJiOTQ3OGNkNTUyMTAwNWIwMTAwMDEwNDAyMDAyMTAyYjdlMDc3ZDAyMGZhYmVkNDU2YTZiZTEzOGE4ZTIwZTllZjQwYjQ0ZDg3M2ZhMTJjMDA1YjY1NmViMGNmOTlmNjAzMDAzMGI0MmEwYmNjMzk1OThkYjFkY2E2MTdhZWVhNmJjMzY3ZjI1NjY2MzY4MjZkYzk2MWE1NGZhYWUxNWIzYjhkMTBhZmMxY2IwMjA2ZTcwYWIzYjBlMTJjMmI5NDc4Y2Q1NSIsInNwZW5kcyI6W3siaW5wdXQiOjAsInNlY3JldCI6IjAyZmMxMWJmNGY5MzlmMmJmZDQ3ZTRjZWU3OTljODI1NGZjNGFjYzI3YTEzNGM3MjllZGZjM2M2YTNjMTNhMDUzYiIsImxlYWYiOiIwMDAxMDIwMDAxMDEwNDAwMjEwMmY5MzA4YTAxOTI1OGMzMTA0OTM0NGY4NWY4OWQ1MjI5YjUzMWM4NDU4MzZmOTliMDg2MDFmMTEzYmNlMDM2ZjkwYTAwMDEwMSIsImNvbnRyb2wiOnsiSyI6IjAyOGVkZmViZDZmZGVhM2UxZDg5MzU5YWYyMDg2OGEyZTc2MzE1YjM2Y2RiMWE3OWRlNDk3YTE3NTdjYTdiZDQwNyIsInBhdGgiOltdfSwic2lnbmF0dXJlcyI6WyJlOGRjMzgzOWQ2NDQ4NWY3NTU1NWQ5YjQ1OWFiMGYwY2FiNDZkNWEwNDIwYmI4MGY2NjFiMjUzZTk0MzFkMGU0MjUyNmY5NzRmNDExOGM1MmY5NWIxMjQyN2Y5Y2ZkMmFkMjRmYTdkM2MyYzkzNTYwYTA4MDYzZjg0OTAyNjEwMCJdfV19
```

**Spend receipt.** For the [swap](#transaction-transcripts)'s bearer input, with its [V4 token](#v4-tokens-with-spend-info). `Y`, `input_digest`, the witness and the commitment are the [NUT-07 vector](07-tests.md)'s:

```json
{
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmU2ZTdjZmE3YjgyZDRiM2I0NDlmYTY0NjZjODkzNDY5YTcyN2QwMjE0ZDQ4ZGI0OTU2YTYwNTRiODAyMmEyOWJhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFrWCBHGW3AgRUM4T_Q5Hi4txgxuCW-OJIRycVqgGKmGvcDRw",
  "receipts": [
    {
      "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
      "keysetId": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "inputDigest": "cb464413d088ae738b9f78141a02d49f51c6ad85029b6e43cb3ac86ef327990e",
      "witness": "{\"signatures\":[\"45fa48240f7793b749aa5a5b7c4a9abaf836a81dfaa690df20a61d6916b812130febdb02e3806be59a1dd01a03bf8ee51252e42cff87a6e065aa1daa2c5e9c0a\"]}",
      "commitment": "90d5e0bdfd9f893c666cb45e397a1e5821659e2cbbac7c9e5306670440f1e415",
      "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5521005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

```
nutrcAeyJ0b2tlbiI6ImNhc2h1Qm8yRnRjV2gwZEhCek9pOHZiV2x1ZEM1MFpYTjBZWFZqYzJGMFlYU0JvbUZwU0FLMzRIZlFJUHEtWVhDQnBHRmhDR0Z6ZUVJd01tVTJaVGRqWm1FM1lqZ3laRFJpTTJJME5EbG1ZVFkwTmpaak9Ea3pORFk1WVRjeU4yUXdNakUwWkRRNFpHSTBPVFUyWVRZd05UUmlPREF5TW1FeU9XSmhZMWd3aE5HM0tScmxjMzg4aFJxalBLX2c5Nl9yWE10Tm9JYkVncnVGdDFKZVlWUl9HMXB0R2dHeF90SDVZTkdwMERNblluTnBvV0ZyV0NCSEdXM0FnUlVNNFRfUTVIaTR0eGd4dUNXLU9KSVJ5Y1ZxZ0dLbUd2Y0RSdyIsInJlY2VpcHRzIjpbeyJZIjoiYTBhY2Y5MzlmMDMzZTNkMGFlOWI1Zjc4NDM0MWZhZGEzODM2N2VlYzE5MGVkZmIzNGUxZjBjY2U5MDUwYzgwNjcyZGJlZTc3YTc1MTJiNzI0MzU0NGM4NWFlMjkwYTczIiwia2V5c2V0SWQiOiIwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYiLCJpbnB1dERpZ2VzdCI6ImNiNDY0NDEzZDA4OGFlNzM4YjlmNzgxNDFhMDJkNDlmNTFjNmFkODUwMjliNmU0M2NiM2FjODZlZjMyNzk5MGUiLCJ3aXRuZXNzIjoie1wic2lnbmF0dXJlc1wiOltcIjQ1ZmE0ODI0MGY3NzkzYjc0OWFhNWE1YjdjNGE5YWJhZjgzNmE4MWRmYWE2OTBkZjIwYTYxZDY5MTZiODEyMTMwZmViZGIwMmUzODA2YmU1OWExZGQwMWEwM2JmOGVlNTEyNTJlNDJjZmY4N2E2ZTA2NWFhMWRhYTJjNWU5YzBhXCJdfSIsImNvbW1pdG1lbnQiOiI5MGQ1ZTBiZGZkOWY4OTNjNjY2Y2I0NWUzOTdhMWU1ODIxNjU5ZTJjYmJhYzdjOWU1MzA2NjcwNDQwZjFlNDE1IiwidHJhbnNjcmlwdCI6IjExMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYTBhY2Y5MzlmMDMzZTNkMGFlOWI1Zjc4NDM0MWZhZGEzODM2N2VlYzE5MGVkZmIzNGUxZjBjY2U5MDUwYzgwNjcyZGJlZTc3YTc1MTJiNzI0MzU0NGM4NWFlMjkwYTczMDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MjEwMDViMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMzBiNDJhMGJjYzM5NTk4ZGIxZGNhNjE3YWVlYTZiYzM2N2YyNTY2NjM2ODI2ZGM5NjFhNTRmYWFlMTViM2I4ZDEwYWZjMWNiMDIwNmU3MGFiM2IwZTEyYzJiOTQ3OGNkNTUyMTAwNWIwMTAwMDEwNDAyMDAyMTAyYjdlMDc3ZDAyMGZhYmVkNDU2YTZiZTEzOGE4ZTIwZTllZjQwYjQ0ZDg3M2ZhMTJjMDA1YjY1NmViMGNmOTlmNjAzMDAzMGI0MmEwYmNjMzk1OThkYjFkY2E2MTdhZWVhNmJjMzY3ZjI1NjY2MzY4MjZkYzk2MWE1NGZhYWUxNWIzYjhkMTBhZmMxY2IwMjA2ZTcwYWIzYjBlMTJjMmI5NDc4Y2Q1NSJ9XX0
```

## V4 tokens with spend info

One 8-sat proof per token, mint `https://mint.test`, unit `sat`, keyset id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6`, `C` = `84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327`.

Tokens use the short keyset id form. Each shape decodes to the stated `spend_info` fields and re-encodes to the same string.

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

Script-only (`si.i` + `si.u` + `si.t`). `u` is fixed for a stable vector; a real send uses a fresh one per proof.

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
