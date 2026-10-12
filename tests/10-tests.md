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

A proof that key `3` can only spend into the two change quote outputs of the [proof to two change quotes](#transaction-transcripts) transaction below (the 3-sat quote and the remainder quote). The `template` leaf's `hash` is `SHA256` over that transaction's output section, the two change quote containers concatenated; the internal key is the same NUMS offset as the [auditable lock](#worked-example-auditable-lock-with-disclosure) (`u = 7`), so no key path exists. The spend is the swap's 8-sat input (same amount, keyset id and `C`) under this secret.

```json
{
  "output_section": "23006b0100010302002103db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b0300403438663532383464643535643362616165346334336135633663663064656230656261306131633765303165373838663435336532346634386631303938313523006702002102ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae203004037646232313538366635626664383935383936316364396134616339373233326162333735366165666233396136613365306366613434616462656335326165",
  "hash": "d6fa4d10a713f7d1c013886788459ff83345ceb638e4b0fdfd992a2ec169d0e3",
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9080020d6fa4d10a713f7d1c013886788459ff83345ceb638e4b0fdfd992a2ec169d0e3",
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "merkle_root": "e8b3d2da939e517c32a000449190c5eee581f5fb8e4f1e9a685b77b92d99b99e",
  "tweak": "2750fe9a12d1f4e5d23daf1c7089209c7591af24d5bc7e414c97e2991d0388e7",
  "secret": "029d37b99583d93ee27f1a014b13dcacafa5ca43388c8f1837cbab2ff65dd88fe0",
  "transaction_digest": "93a4acb8b6038265bbcdbca8079fc8fed44e7ffecafdd10558a8b3180ffd9f7b",
  "input_id": "6b7099d18881a2d4999e438ef0c9e62108a2aea0d92ea6e2b566a64331f0aa26",
  "input_digest": "3d92c2c469274799e7fb2ff622f2413a2d947d39a26f960beff23efbeb37fd9e"
}
```

The template leaf, spelled out (`n = 1`, `keys = [key 3]`, then `hash`):

```
00 05 | 02 0001 01 | 04 0021 02f930...e036f9 | 08 0020 d6fa4d...69d0e3
```

Key `3`'s script-path witness over that `input_digest`:

```json
{
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9080020d6fa4d10a713f7d1c013886788459ff83345ceb638e4b0fdfd992a2ec169d0e3",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": []
  },
  "signatures": [
    "08ecbcf36edb872a7e06399b2fd0783679727671cda4f404da15bc00e524bfde5e1d8eb19b0a3d0d271db7ee17b0f01806b2c83564f2eeaf60f7f8d03c32e165"
  ]
}
```

The same proof spent with the fixed quote at 4 sat instead of 3 (one byte of the output section, `23006b01000104...`) hashes its outputs to `8c4f98f5a5980165f4c4ba037af62292b1d27a0bba17c9009e828e5fe5854aaa`, so the witness **MUST** be rejected whatever it signs.

## Worked example: an arbiter escrow

Three leaves under the NUMS offset `u = 7`, so no key path exists. The arbiter (key `4`) can only release to the seller (key `5`) or refund the buyer (key `3`), each through a `template` leaf over one remainder change quote; buyer and seller together can spend through a 2-of-2 `threshold` leaf. Each party picks its own `id_preimage` and hands over only the derived quote id: the seller's is `55` repeated 32 times, the buyer's `33` repeated 32 times.

```json
{
  "seller_quote_id": "4e38daacd11ae677f32db3b58473cb6e432aaaee1e0e4a170919aeae1343f5ef",
  "buyer_quote_id": "a6cf70fcbc9dac2a31742624ce1687a573a2d283a28a306186687ca3b4cd4199",
  "out_seller": "230067020021022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe403004034653338646161636431316165363737663332646233623538343733636236653433326161616565316530653461313730393139616561653133343366356566",
  "out_buyer": "23006702002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f903004061366366373066636263396461633261333137343236323463653136383761353733613264323833613238613330363138363638376361336234636434313939",
  "leaf_release": "00050200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd130800207147627e56300778e86e5567a3f7c9af7aa7cfe3d6c9be7c950fdc5aa4a305dd",
  "leaf_refund": "00050200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd130800204338fa95d9b5a5dc3e33e229f2f13598bfeed9e205360bf39c6de8d0a75782cd",
  "leaf_coop": "00010200010204004202f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "leaf_hash_release": "863d70e4e9c0f0ed257291b49c1121c1ecb95d73505c278518abcdcad5e35269",
  "leaf_hash_refund": "771d789a68984f231ea2d74436df5c9ec854ced7e35b4bd28e557bdc50e15c10",
  "leaf_hash_coop": "dfa245f0b825b4ea746ee82f6f41de614a7ceb00e54760327218e5e4487b5c4b",
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "merkle_root": "202a8d585a8ec5d6869e857916e0e09b12c6f53850d8ee337bbad7865aeeb17c",
  "tweak": "ab2a407c87726808a65a06254707753f8f2caf12058ab792d2a1f478d3833256",
  "secret": "02e063ebbd59ba61103a7c1fa68e8d4a7a5e691a8855a8f5af45d44663a7a397d3"
}
```

Sorted by leaf hash the order is refund, release, coop: refund and release pair and coop is promoted, so `merkle_root = branch(branch(leaf_hash_refund, leaf_hash_release), leaf_hash_coop)`. Releasing to the seller spends the swap's 8-sat input under this secret into `out_seller` alone, its request carrying the seller's `id_preimage` (`transaction_digest` `40211bd2b534aff2641c2d8135530034da8a8d263cebf31c63f71b3b22ce230f`, `input_id` `c195216b0f895ed4b1454943c70507bc7ed082217cbe80fe127e9badf24e32c8`, `input_digest` `c9a0670fb12f02a603ad2bc22b4f89baab157d7218cc13ca921c2711fd63423d`). The arbiter's witness reveals the release leaf with `path = [leaf_hash_refund, leaf_hash_coop]`:

```json
{
  "leaf": "00050200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd130800207147627e56300778e86e5567a3f7c9af7aa7cfe3d6c9be7c950fdc5aa4a305dd",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": [
      "771d789a68984f231ea2d74436df5c9ec854ced7e35b4bd28e557bdc50e15c10",
      "dfa245f0b825b4ea746ee82f6f41de614a7ceb00e54760327218e5e4487b5c4b"
    ]
  },
  "signatures": [
    "d96a84b591b3a0377f3c7432505355bd053405efffcf65d2f1df53a4d2791af8328378b1ded8d23a35d9d0637ab110de47bc1089d1c5560930cf03538057ae98"
  ]
}
```

A remainder quote to the arbiter's own key (`id_preimage` `44` repeated 32 times) hashes its output section to `938551302fe2f732a34d4d621ab2cf161947566a885b8aafdc207ba06fcbeba8`, which matches neither template.

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
  "transaction_digest": "87d639d6f07510a509d5f564206b97239e150a67edc5651a635b343addec156d",
  "input_id": "185bbd6a83656cce61890e8ba015be2629bc745c991dd7936cc2e61911bf0f19",
  "input_digest": "3b0ac0a9f71ce1fbd51f318e320c88595720cb2fefd2395d4c894e4ba5b216d3"
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
    "b45249e8b1ae085f56a3b7d773bd92fedc16c2ffa7ebaf22fe2963c64ba1b49aa4f8c247bee55d3ccdb66a75383a81bddc9019ad31f6b00dfaae51a018c837ed"
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

Keyset `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6` (v3). Proofs use [NUT-13 V3](13-tests.md) counter `0`, and `1` in the multi-input vector. `digest` is the transaction digest. A blinded output's container carries `SHA256(B_)`, so a request shows `B_` where its transcript shows the hash.

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
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "b5a50082d44bdb0d9f9e91896fbe0f8f9052baf0ca7c8930c8987790164f277c",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "eca67b680015d42ffb9339b8c0475a90d162d189bd36a15d8b6910de48927edd"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "5b4b2cbdb5ea75dd2a6451bf2f348e8b837438375dd5e78ba5cb2f3c549258df8ff274e8de9987e7dab88c221f0de820546e42907cec816e2b290af814030a94"
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
  "digest": "638facdb740dcd6909c5934208a421dafa1b3756aa5fc4a0e5d1bd341f28fbc6",
  "inputs": [
    {
      "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
      "input_digest": "d8fcb88ff0252fc13519cf28a23e7b65278db09a4d8c1e82b27f692ea53bb5a7",
      "signature": "11f5af9cf93204f816b4328f47de2b6368eaa26d584c4a5f0eca9268ed94aa39093faad5e6d4fce3674851e3c506cd0af35c0a58f913d7853e51b80e39976499"
    },
    {
      "input_id": "0182252f564bf76e42e45514955b50c6bd6381b6c4971c8027cd5a6a90817c4b",
      "input_digest": "28e4afd844e0fb8a3c3e71fdb82abdecf263d25b4de1cfd96d0d5c620c69c1d1",
      "signature": "35482c41545a8a1dd1343678952085390c2ac0a056f28bb36c1623ceadece35181d0526386bc8feb5ab15ba71a608a1a51f4f302ca1e11c903d1255e9d039d0a"
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
      "input_digest": "764a2f46843cdefb389d2cf45807b569d646e51780265e1c28e0ac42cdb067e6",
      "signature": "affda39eba371dc7fe506e50ea9e97bea55d24bca91039f399dcbbcc00528c648fb4ba1dcb257851c4bb28e3bb869f2da13232ba539cfc67336276113adad289"
    },
    {
      "Y": "029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae",
      "container": "1100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2",
      "input_id": "efbdd5d14874cb021fc962d93a9848553ca65ae101e9b57f6678aa37ffe1ebd9"
    }
  ],
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033271100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba221004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b0100010202002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "74e13e494841037a8578176a18a25e412ef5b86e35e2de6f0bff5f30f79405b4"
}
```

**Mint.** Mint quote `quote-mint-0001` (amount 8, none issued) with one 8-sat output, locked to the [NUT-13 quote lock key](13-tests.md#version-3-secret-derivation) of counter `0` (`0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812`):

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
  "transcript": "12003d0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000021004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "3f2ed71b538ba1cdb59b7d176dae4709c5db6b30d2c364fc231bfd2985d9f845",
  "input_id": "d294012dd54976b05eb3e36eb218b9a6d66b19d79ec122944a35b99b8ddd8839",
  "input_digest": "cd149490f31c836c3f4bab5e401242100a1522e7e5e0af2db4da4020bb894af1"
}
```

**Partial mint.** Issuing 4 against 8-sat mint quote `quote-mint-0004` with 3 already issued, with one 4-sat output:

```
12 003e | 01 0001 04 | 02 000f 71756f...303034 | 03 0021 029290...209812 | 04 0001 03
```

```json
{
  "transcript": "12003e0100010402000f71756f74652d6d696e742d303030340300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d2098120400010321004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "93379041ba7dd1166d7dc1b028305a22470c461f62907982565a2343148cb64b",
  "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
  "input_id": "c2e4168d079d7ccc6c9fc80c480e75a255282ec41e660afad42cf743c95f14e3",
  "input_digest": "3e22290842db64b0c8417b72e16bf0965d5ee304815978d3b8c2d53574a60ebb",
  "signature": "5055a075e7534502457e914c81768d29bae3d0be046d106a8a6529507c3bdc851cbecd9654454d22efe88658803d4a96d8c2ba53716b9846da08411fbabf71de"
}
```

The signature **MUST NOT** verify over a transcript that commits amount `8` or `issued` `0`.

**Batched mint.** A [NUT-29](../29.md) batch of `quote-mint-0002` and `quote-mint-0003` with `quote_amounts` of `[5, 3]` and the mint vector's 8-sat output:

```
12 003d | 01 0001 05 | 02 000f 71756f...303032 | 03 0021 029290...209812 | 04 0000
12 003d | 01 0001 03 | 02 000f 71756f...303033 | 03 0021 02b357...99615d | 04 0000
```

```json
{
  "transcript": "12003d0100010502000f71756f74652d6d696e742d303030320300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000012003d0100010302000f71756f74652d6d696e742d3030303303002102b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d04000021004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "bf866b675bf6730b94f556095a22f4ac094fb3fe5d65d777dd05a41ebfb6f4ed",
  "inputs": [
    {
      "quote_id": "quote-mint-0002",
      "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
      "input_id": "8c7f916779dfba1b7ea2e0d3e69d1ee7eed1895af2891406fe8bdb7fbe0f39aa",
      "input_digest": "dbc45733112ba2e7fad938d62de00c13c085309c9330d082cadee0c6dfeca85f",
      "signature": "e0520f39e881481c7f6f12f987d09483c14b4bb3fbeea8f35d238f53bf0448be53db93f3a61ab882e50c8a96d26a87f48ded963ff5a585e404834f8c13b00e20"
    },
    {
      "quote_id": "quote-mint-0003",
      "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
      "input_id": "f7a60306c44e910fd5dea355541c4a4bb251220690688279bf08e7d19b3e9e45",
      "input_digest": "f14225ec0ff74cae090865a5d852b9cd8b06827d3f459ad2d6a5ce4cc1e91dac",
      "signature": "e726ee0cef6b2431850f4f5f7b5745d8810ead54888db3aae12c30d151049810c72dbe9f3d07812719fd1e2c8d55df91cec1e9a81e8cfe557485cefcb4e6447f"
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
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee2200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "adac16b768b73d5137096faf62a1b3b035cb8fd27e2a22c3159d99d1f2415c60",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "c5692db35c58c47c70aa4dab49d2ede41adec95f00a231bf40cc8af5ddee030f"
}
```

**Mint quote to melt.** Paying melt quote `quote-melt-0001` straight from mint quote `quote-mint-0001` in one transaction ([NUT-XX](../XX.md)): no proofs and no change outputs, so the transcript is the mint vector's quote input container followed by the melt vector's melt quote container. The quote input's bytes are unchanged, so it keeps the mint vector's `input_id`; the new transcript gives it a new `input_digest`, which its lock key signs:

```json
{
  "transcript": "12003d0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d2098120400002200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "8c54caecbdd6fdc5ae77bea97ed63dbf94a6919d6bc5d71cd7145765b52e49f3",
  "input_id": "d294012dd54976b05eb3e36eb218b9a6d66b19d79ec122944a35b99b8ddd8839",
  "input_digest": "492728212791e2222a327b9c4fe6c17e2da0e9e7d1aebbe0062c3585909edb57"
}
```

**Melt with rotation quote.** The melt with change, backed by a [rotation quote](../XX.md#rotation-quote) locked to the [NUT-13](13-tests.md) type `0x06` key for `quote-melt-0001` (`030d037dacc95764fe0e07ba08031137aba13b659b98cb7c5d3ebec6f552834040`). Its mint quote output carries no amount and follows the melt quote, its quote id the rotation quote id as UTF-8:

```
23 0067 | 02 0021 030d03...834040 | 03 0040 utf8("044f92...1c7bcf")
```

```json
{
  "mint_quote_output_container": "230067020021030d037dacc95764fe0e07ba08031137aba13b659b98cb7c5d3ebec6f55283404003004030343466393238616665626364353439633132613638636631626564346639323563313264373134343831333164663261373636666230333839316337626366",
  "quote_id": "044f928afebcd549c12a68cf1bed4f925c12d71448131df2a766fb03891c7bcf",
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee2200160100010802000f71756f74652d6d656c742d30303031230067020021030d037dacc95764fe0e07ba08031137aba13b659b98cb7c5d3ebec6f55283404003004030343466393238616665626364353439633132613638636631626564346639323563313264373134343831333164663261373636666230333839316337626366",
  "digest": "bece17daa86a50004c43ee0a54f2081c811b688d351e869e5e666765e9cfb375",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "c42ad213ea794a86879e1cb2d8a11e6e80aa039d755b1cbe64a7210d643699d7"
}
```

## Transport strings

Each string is its prefix plus base64url (no padding) of the JSON shown. The JSON is not canonical, so decoders parse rather than compare.

**Signing package.** The [auditable lock](#worked-example-auditable-lock-with-disclosure) as the sole input of the [swap](#transaction-transcripts), with one spend awaiting signatures on input `0`:

```json
{
  "version": "nutspA",
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe704003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
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
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjExMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYWFiYTQ2YTQ2M2QzZDEwYjU5ZmExNTMyYTMyZDlhNWU4ZmE4ZTk5NjJhOGM2NTcxOTE3OTgxYTZmYTRkNWZhZmIwOGMyMWJiZmY5NDE4OWUyNGU1YzI1NmZjMGE3ZmU3MDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MjEwMDRiMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlMjEwMDRiMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIiwic3BlbmRzIjpbeyJpbnB1dCI6MCwic2VjcmV0IjoiMDJmYzExYmY0ZjkzOWYyYmZkNDdlNGNlZTc5OWM4MjU0ZmM0YWNjMjdhMTM0YzcyOWVkZmMzYzZhM2MxM2EwNTNiIiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOTBhMDAwMTAxIiwiY29udHJvbCI6eyJLIjoiMDI4ZWRmZWJkNmZkZWEzZTFkODkzNTlhZjIwODY4YTJlNzYzMTViMzZjZGIxYTc5ZGU0OTdhMTc1N2NhN2JkNDA3IiwicGF0aCI6W119LCJzaWduYXR1cmVzIjpbXX1dfQ
```

Signed by key `3` over input digest `4b7ffce0...`, it merges into the [script-path witness](#worked-example-auditable-lock-with-disclosure) shown there:

```
nutspAeyJ2ZXJzaW9uIjoibnV0c3BBIiwidHJhbnNjcmlwdCI6IjExMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYWFiYTQ2YTQ2M2QzZDEwYjU5ZmExNTMyYTMyZDlhNWU4ZmE4ZTk5NjJhOGM2NTcxOTE3OTgxYTZmYTRkNWZhZmIwOGMyMWJiZmY5NDE4OWUyNGU1YzI1NmZjMGE3ZmU3MDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MjEwMDRiMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlMjEwMDRiMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIiwic3BlbmRzIjpbeyJpbnB1dCI6MCwic2VjcmV0IjoiMDJmYzExYmY0ZjkzOWYyYmZkNDdlNGNlZTc5OWM4MjU0ZmM0YWNjMjdhMTM0YzcyOWVkZmMzYzZhM2MxM2EwNTNiIiwibGVhZiI6IjAwMDEwMjAwMDEwMTA0MDAyMTAyZjkzMDhhMDE5MjU4YzMxMDQ5MzQ0Zjg1Zjg5ZDUyMjliNTMxYzg0NTgzNmY5OWIwODYwMWYxMTNiY2UwMzZmOTBhMDAwMTAxIiwiY29udHJvbCI6eyJLIjoiMDI4ZWRmZWJkNmZkZWEzZTFkODkzNTlhZjIwODY4YTJlNzYzMTViMzZjZGIxYTc5ZGU0OTdhMTc1N2NhN2JkNDA3IiwicGF0aCI6W119LCJzaWduYXR1cmVzIjpbImI0NTI0OWU4YjFhZTA4NWY1NmEzYjdkNzczYmQ5MmZlZGMxNmMyZmZhN2ViYWYyMmZlMjk2M2M2NGJhMWI0OWFhNGY4YzI0N2JlZTU1ZDNjY2RiNjZhNzUzODNhODFiZGRjOTAxOWFkMzFmNmIwMGRmYWFlNTFhMDE4YzgzN2VkIl19XX0
```

**Spend receipt.** For the [swap](#transaction-transcripts)'s bearer input, with its [V4 token](#v4-tokens-with-spend-info). `Y`, `input_digest`, the witness and the commitment are the [NUT-07 vector](07-tests.md)'s:

```json
{
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmU2ZTdjZmE3YjgyZDRiM2I0NDlmYTY0NjZjODkzNDY5YTcyN2QwMjE0ZDQ4ZGI0OTU2YTYwNTRiODAyMmEyOWJhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFrWCBHGW3AgRUM4T_Q5Hi4txgxuCW-OJIRycVqgGKmGvcDRw",
  "receipts": [
    {
      "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
      "keysetId": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "inputDigest": "eca67b680015d42ffb9339b8c0475a90d162d189bd36a15d8b6910de48927edd",
      "witness": "{\"signatures\":[\"5b4b2cbdb5ea75dd2a6451bf2f348e8b837438375dd5e78ba5cb2f3c549258df8ff274e8de9987e7dab88c221f0de820546e42907cec816e2b290af814030a94\"]}",
      "commitment": "eb3dce8232201aa69f4344f89e07dbfa6690c10cfb26eff9ef48a8be6efbf522",
      "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee"
    }
  ]
}
```

```
nutrcAeyJ0b2tlbiI6ImNhc2h1Qm8yRnRjV2gwZEhCek9pOHZiV2x1ZEM1MFpYTjBZWFZqYzJGMFlYU0JvbUZwU0FLMzRIZlFJUHEtWVhDQnBHRmhDR0Z6ZUVJd01tVTJaVGRqWm1FM1lqZ3laRFJpTTJJME5EbG1ZVFkwTmpaak9Ea3pORFk1WVRjeU4yUXdNakUwWkRRNFpHSTBPVFUyWVRZd05UUmlPREF5TW1FeU9XSmhZMWd3aE5HM0tScmxjMzg4aFJxalBLX2c5Nl9yWE10Tm9JYkVncnVGdDFKZVlWUl9HMXB0R2dHeF90SDVZTkdwMERNblluTnBvV0ZyV0NCSEdXM0FnUlVNNFRfUTVIaTR0eGd4dUNXLU9KSVJ5Y1ZxZ0dLbUd2Y0RSdyIsInJlY2VpcHRzIjpbeyJZIjoiYTBhY2Y5MzlmMDMzZTNkMGFlOWI1Zjc4NDM0MWZhZGEzODM2N2VlYzE5MGVkZmIzNGUxZjBjY2U5MDUwYzgwNjcyZGJlZTc3YTc1MTJiNzI0MzU0NGM4NWFlMjkwYTczIiwia2V5c2V0SWQiOiIwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYiLCJpbnB1dERpZ2VzdCI6ImVjYTY3YjY4MDAxNWQ0MmZmYjkzMzliOGMwNDc1YTkwZDE2MmQxODliZDM2YTE1ZDhiNjkxMGRlNDg5MjdlZGQiLCJ3aXRuZXNzIjoie1wic2lnbmF0dXJlc1wiOltcIjViNGIyY2JkYjVlYTc1ZGQyYTY0NTFiZjJmMzQ4ZThiODM3NDM4Mzc1ZGQ1ZTc4YmE1Y2IyZjNjNTQ5MjU4ZGY4ZmYyNzRlOGRlOTk4N2U3ZGFiODhjMjIxZjBkZTgyMDU0NmU0MjkwN2NlYzgxNmUyYjI5MGFmODE0MDMwYTk0XCJdfSIsImNvbW1pdG1lbnQiOiJlYjNkY2U4MjMyMjAxYWE2OWY0MzQ0Zjg5ZTA3ZGJmYTY2OTBjMTBjZmIyNmVmZjllZjQ4YThiZTZlZmJmNTIyIiwidHJhbnNjcmlwdCI6IjExMDA4ZTAxMDAwMTA4MDIwMDIxMDJiN2UwNzdkMDIwZmFiZWQ0NTZhNmJlMTM4YThlMjBlOWVmNDBiNDRkODczZmExMmMwMDViNjU2ZWIwY2Y5OWY2MDMwMDMwYTBhY2Y5MzlmMDMzZTNkMGFlOWI1Zjc4NDM0MWZhZGEzODM2N2VlYzE5MGVkZmIzNGUxZjBjY2U5MDUwYzgwNjcyZGJlZTc3YTc1MTJiNzI0MzU0NGM4NWFlMjkwYTczMDQwMDMwODRkMWI3MjkxYWU1NzM3ZjNjODUxYWEzM2NhZmUwZjdhZmViNWNjYjRkYTA4NmM0ODJiYjg1Yjc1MjVlNjE1NDdmMWI1YTZkMWEwMWIxZmVkMWY5NjBkMWE5ZDAzMzI3MjEwMDRiMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlMjEwMDRiMDEwMDAxMDQwMjAwMjEwMmI3ZTA3N2QwMjBmYWJlZDQ1NmE2YmUxMzhhOGUyMGU5ZWY0MGI0NGQ4NzNmYTEyYzAwNWI2NTZlYjBjZjk5ZjYwMzAwMjA1NjdiNGJhOTgwZGQwYzUxYzgwOTE5NjMzYjM4NGMwNzY0YjMwZTUyNTBjNGE4YjhlMzk1N2M5ZjQyMDhjZGVlIn1dfQ
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
