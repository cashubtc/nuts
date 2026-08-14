# NUT-10 Test Vectors

These vectors cover [taproot secrets](../10.md#taproot-secrets-v3-keysets) (v3 keysets). All signatures are BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes them reproducible; verifiers **MUST** accept any valid signature.

## Conventions

Tagged hashes use the tags `Cashu_TapLeaf`, `Cashu_TapBranch` and `Cashu_TapTweak`; receiver-keyed blinding uses `Cashu_P2BK_v1` ([NUT-28](../28.md)); the transaction domain tag is `Cashu_Transaction_v1`; the NUMS point is `0250929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0`. These are the normative constants of [NUT-10](../10.md), restated here so the vectors read standalone.

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
  "after_1of1_key4": "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
}
```

## The tree fold

A three-leaf tree (`threshold_1of1_key3`, `after_1of1_key4`, `hashlock_1of1_key3`, in transmitted order) exercises the odd-count fold: leaves 0 and 1 pair, leaf 2 is promoted unchanged, and the two hashes at the next level pair. The merkle path for leaf 2 is therefore a single sibling, `branch(h0, h1)`.

```json
{
  "three_leaf_tree": [
    "00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
    "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80",
    "00030200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9080020a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"
  ],
  "root": "c4fb3d4ccca2ddff6d756e1fdab834d459b0449f706233a3e82bad2409380513",
  "path_for_index_2": [
    "1b5196405f3404af4c9eff23612852b37325c59ca0c254c8293b294b150113e7"
  ],
  "internal_key": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "secret": "033d319c858e0b102a922588d033aa9afda993b8c5a8559478b75fb01b7156b6ff"
}
```

`secret = internal_key + tagged_hash("Cashu_TapTweak", internal_key || root)*G`, and the commitment also verifies through `path_for_index_2` from leaf 2 alone.

## Worked example: receiver-keyed proof with a refund leaf

Alice pays Carol, refundable to Alice after `time`. Carol's static key is key `3`, Alice's refund key is key `4`, Alice's ephemeral is key `5`. The internal key is Carol's static key blinded at slot 0 ([NUT-28](../28.md#taproot-secrets-v3-keysets)); the tree is the single `after` leaf.

```json
{
  "carol_static": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "ephemeral_E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "slot0_r": "7dfb649b0edda814f7cf0feb889e5657eb2083a528aa60a3a943fe0cea066181",
  "internal_key": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "leaf": "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80",
  "merkle_root": "e59092b6ae00f7af3dfb2c5d3b4080a61b593ac9da75a8dd5769d5b2e72bce9b",
  "tweak": "5549241190e37631886b3122e53551ab86cb487337809bad749f93884f72d78d",
  "secret": "03c222ef6dec2bec02ab0d6508e4f8302948021875a267f14e0854325d819bf823",
  "keypath_priv": "d34488ac9fc11e46803a410e6dd3a80371ebcc18602afc511de3919539793911"
}
```

Here `merkle_root = tagged_hash("Cashu_TapLeaf", leaf)` (single leaf), and `keypath_priv = (3 + slot0_r + tweak) mod n`, the key Carol signs with.

The witnesses below sign an **illustrative** digest, `SHA256("illustrative transaction transcript")` = `e1d7170b89a2b6eedec90453e32b6c320dfadd590e6a6454bddec95a0e3834cd` (a real spend signs a transaction digest, see below). Carol's key-path witness:

```json
{
  "signatures": [
    "59428dc63ae76fc01c819bbe368e4c5582d5ad7da80dfdb585637459716d020ce92f4f5f74791c1d28f89e6692217a9ddad8a41929d19b2f0b8821d6fc17792c"
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
  "leaf_hash_0": "b2a5853a34fb233d543c15b4f1511f2e88e7b057b663dacc5bd4eff2914c06c7",
  "leaf_hash_1": "71fe4dfbac73f21b0c084febba39a1b1f5adc5afe8dadaeceaa35055cb21df03",
  "merkle_root": "a01a34e050b5f0146445dc537d3245d441d9dfe72a5057c60301c9e4984d47a1",
  "tweak": "afef4965d84f8ad2ecae202acad1c3b4292901b6c130abd6bcb1e5751436e4be",
  "secret": "0254c9b4c1281656f5bdacf5e6ffce7a3c3659f9fd4f46aa00af0d77cc93057424"
}
```

`merkle_root = tagged_hash("Cashu_TapBranch", leaf_hash_1 || leaf_hash_0)`: the pair is sorted, so `leaf_hash_1` comes first. A witness revealing `leaf_0_unknown_type` with `path = [leaf_hash_1]` reconstructs the secret but **MUST** be rejected as unsatisfiable (unknown leaf type).

## Empty tweak

An aggregated internal key commits to having no script path with the empty tweak: `t = tagged_hash("Cashu_TapTweak", K)`, no merkle root bytes. With `K` = public key of `3`:

```json
{
  "internal_key": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "tweak": "93ee8d8b880c6aa1d858f816e16ad46e53ae3ce0d08ea2b4454b69732f75de94",
  "secret": "0284f13903124432d5013cf5b7c1dd7353127bd70129b9495591bbd406eaceeaa6",
  "keypath_priv": "93ee8d8b880c6aa1d858f816e16ad46e53ae3ce0d08ea2b4454b69732f75de97"
}
```

## Transaction transcripts

`msg = "Cashu_Transaction_v1" (ASCII) || transcript`, `digest = SHA256(msg)`. The keyset is a v3 keyset with id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6` (contributing raw bytes); quote ids contribute UTF-8 bytes; amounts are minimal big-endian. The proof secret is [NUT-13 V3](13-tests.md) counter 0's, so its witnesses below are by that counter's secret key.

**Swap.** A `PostSwapRequest` ([NUT-03](../03.md)) spending one 8-sat proof into two 4-sat outputs:

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "secret": "0234df38671738d8e9ee205dc364fd4b45df8ed2ff91686e93d02ca1feb3b2f118",
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
  "transcript": "01007f0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f60300210234df38671738d8e9ee205dc364fd4b45df8ed2ff91686e93d02ca1feb3b2f11804003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "5603e6bd91eae45db2edc5b763057671b8a9667a06fe7c9317846b7981318572"
}
```

and the input's key-path witness over that digest is:

```json
{
  "signatures": [
    "2223919fc0cbd9e75ff3f7b1330e8644899721bb68fb4d26b08d8d5b2c495582782c93fb3f609cbe47d5521fe864bb2c5c4a58f0d4db013fa6f54658c44714d7"
  ]
}
```

**Mint.** Executing mint quote `quote-mint-0001` (amount 8, [NUT-04](../04.md#taproot-transactions-v3-keysets)) with one 8-sat output. The quote is the transaction's only input; its lock key signs this digest via the mint request's `signature` field:

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
  "digest": "096a9b2002cc0b8ebc9b79e0902159385a929f4e63f35eb9e1dee0119205efb6"
}
```

**Melt.** Paying melt quote `quote-melt-0001` (amount 8, no change outputs) with the swap's 8-sat proof as the only input; the melt quote is the only output, binding its quote id and amount:

```json
{
  "transcript": "01007f0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f60300210234df38671738d8e9ee205dc364fd4b45df8ed2ff91686e93d02ca1feb3b2f11804003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033270400160100010802000f71756f74652d6d656c742d30303031",
  "digest": "0eb9a8c9b8214437e36af259250c85afe22379126e7d17abbb7ee4eacdaa5cf3"
}
```

**Melt with change.** The same melt carrying two [NUT-08](../08.md) blank change outputs (amount 0, on the same keyset with the swap's `B_`). Containers group in ascending type order, so the blank outputs (type `0x03`) precede the melt quote (type `0x04`) in the transcript regardless of the request's field order; note each blank's zero amount encodes to a zero-length record (`010000`):

```json
{
  "transcript": "01007f0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f60300210234df38671738d8e9ee205dc364fd4b45df8ed2ff91686e93d02ca1feb3b2f11804003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332703005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd5503005a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd550400160100010802000f71756f74652d6d656c742d30303031",
  "digest": "98bd694b8b67668d27a82a37a59261aacac3baec47959cb7a45de63ab9c7bfe0"
}
```

## V4 tokens with spend info

One 8-sat proof per token, mint `https://mint.test`, unit `sat`, keyset id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6`, `C` = `84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327`.

Tokens use the short keyset id form; decoders **MUST** also accept the full-length id ([NUT-00][00]). Each shape decodes to the stated `spend_info` fields and re-encodes to the same string.

Bearer (`si.k`, secret is the bare key of `k`):

```json
{
  "secret": "0234df38671738d8e9ee205dc364fd4b45df8ed2ff91686e93d02ca1feb3b2f118",
  "spend_info": {
    "k": "7a7b3f7eb44f4a943041d936c0e0b2bf1dd0ac9a210bc8f8bc12b65cdbde9bd3"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMjM0ZGYzODY3MTczOGQ4ZTllZTIwNWRjMzY0ZmQ0YjQ1ZGY4ZWQyZmY5MTY4NmU5M2QwMmNhMWZlYjNiMmYxMThhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFrWCB6ez9-tE9KlDBB2TbA4LK_HdCsmiELyPi8ErZc296b0w"
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
  "secret": "03c222ef6dec2bec02ab0d6508e4f8302948021875a267f14e0854325d819bf823",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwM2MyMjJlZjZkZWMyYmVjMDJhYjBkNjUwOGU0ZjgzMDI5NDgwMjE4NzVhMjY3ZjE0ZTA4NTQzMjVkODE5YmY4MjNhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpomFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-RhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

A disclosed tree with an explicit internal key (`si.i` + `si.t`; no key handed over, the script-only and third-party-signer shape):

```json
{
  "secret": "03c222ef6dec2bec02ab0d6508e4f8302948021875a267f14e0854325d819bf823",
  "spend_info": {
    "K": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwM2MyMjJlZjZkZWMyYmVjMDJhYjBkNjUwOGU0ZjgzMDI5NDgwMjE4NzVhMjY3ZjE0ZTA4NTQzMjVkODE5YmY4MjNhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpomFpWCEDo-EswHflYF82RBBG9QwRT8yIOweaNAKL7WZzLjpBnlFhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

[00]: ../00.md
