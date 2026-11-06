# NUT-YY Test Vectors

These vectors cover the [template leaf](../YY.md). Keys, tags and signatures follow the [NUT-10 vectors](10-tests.md#conventions).

## A template covenant

A proof that key `3` can only spend into fixed txout quotes locked to the two lock keys of the [proof to two fixed txout quotes](00-tests.md#transaction-transcripts) transaction in the NUT-00 vectors. The `template` leaf lists them in `dests`; the internal key is the NUMS offset `u = 7`, as in the [NUT-18 vectors](18-tests.md), so no key path exists. The spend is the swap's 8-sat input (same amount, keyset id and `C`) under this secret, into that transaction's two fixed txout quotes.

```json
{
  "dests": [
    "03db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b",
    "02ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae2"
  ],
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90c004203db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b02ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae2",
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "merkle_root": "8d41634c46c8ee248a0b8bf65c2a4cd883ece04925e366205e6385cb3e41413d",
  "tweak": "41e5456a9808ef698ad6613fe86647c48d9b75ca0f8abe91a3d01debbbff0115",
  "secret": "03a07a07169b3dbad5ea5e6f7771acb326e788e42e38948d9d2d5f5d3f29b38cf1",
  "transaction_digest": "5eea592fbc0f3505589c7ce3f1ba30a3061b9c8dc37470302896da679345488c",
  "input_id": "b19a85ad10680b7391fef09ac08e6b49efe9a6207386e95c91ecc8aea5c352a9",
  "input_digest": "fb9b55ec1743839f617697ffe728f0540c434569ee86b092a0bc2d94a5dc0d8d"
}
```

The template leaf, spelled out (`n = 1`, `keys = [key 3]`, then `dests`):

```
00 05 | 02 0001 01 | 04 0021 02f930...e036f9 | 0c 0042 03db67...26d38b 02ccde...f18ae2
```

Key `3`'s script-path witness over that `input_digest`:

```json
{
  "leaf": "00050200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90c004203db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b02ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae2",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": []
  },
  "signatures": [
    "7224156d3b38b88dfb8887b9412b78744371b5659e20e4849f5e6dabcc67dc35908fed2ecb1142dd80ae5d266a3c08d1bc59a8bf19104bd3525e0c401a350a2a"
  ]
}
```

The same proof spent with its second fixed txout quote locked to key `4` (`02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13`) instead, which `dests` does not list, **MUST** be rejected whatever it signs.

## An arbiter escrow

Three leaves under the NUMS offset `u = 7`, so no key path exists. The arbiter (key `4`) can pay only the buyer (key `3`) and the seller (key `5`), in any split, through one `template` leaf; the buyer can take everything back alone from `1755561600` through an `after` leaf; buyer and seller together can spend through a 2-of-2 `threshold` leaf.

```json
{
  "leaf_arbiter": "00050200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd130c004202f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "leaf_refund": "00020200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f906000468a3be80",
  "leaf_coop": "00010200010204004202f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "leaf_hash_arbiter": "6a250690c3dacdbb0f3262ed8e7b6cf635cae6084f13213715cbb75c0019d9b0",
  "leaf_hash_refund": "c63d3a44d8775d6fbbe6c92137749831f2e4af57747defbc29ce0933cb77e1d3",
  "leaf_hash_coop": "dfa245f0b825b4ea746ee82f6f41de614a7ceb00e54760327218e5e4487b5c4b",
  "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
  "merkle_root": "5624fbc52d2041cf6bf0b72dc1712a6dc6499a228845718a52848eebb891d14b",
  "tweak": "1c2eff2c35b24cda8445026bfd459011ea82092fc13fbe9cf0db6b1af9ae5f5a",
  "secret": "022d32ec64d123475fac4593830f2e26d6ce1dc3768f6211d60f14d1eba6e06292"
}
```

The arbiter and refund leaves pair and coop is promoted, so `merkle_root = branch(branch(leaf_hash_arbiter, leaf_hash_refund), leaf_hash_coop)`. The seller builds a split and the arbiter signs it: the swap's 8-sat input under this secret into 5 sat to the seller and 3 sat to the buyer (`transaction_digest` `2f7871b27aeccb2f74965d3a49d1aba5346054f2c316544595a82b29f45051d3`, `input_id` `5fab28b6e901544d3e2881d1f0077b710922ed79d7a47e75f2f7791d6b0af502`, `input_digest` `f0f5737497bda769547aff5e60a0ea48222aa2139e4c25bd339afc8208069858`). The arbiter's witness reveals its leaf with `path = [leaf_hash_refund, leaf_hash_coop]`:

```json
{
  "leaf": "00050200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd130c004202f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
  "control": {
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "path": [
      "c63d3a44d8775d6fbbe6c92137749831f2e4af57747defbc29ce0933cb77e1d3",
      "dfa245f0b825b4ea746ee82f6f41de614a7ceb00e54760327218e5e4487b5c4b"
    ]
  },
  "signatures": [
    "5bacc9e6f8c2831c4f1d455d417e36ad8016e10df6febbbb73158ac8aab8f8d540505c8cbbb2dc2e7ed2021d8d1bf0ed6d343b2de5594b398cf13c052e6d5feb"
  ]
}
```

A txout quote to the arbiter's own key is outside `dests`, so no arbiter signature can satisfy the leaf with it.
