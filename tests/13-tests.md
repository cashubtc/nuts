# NUT-13 Test vectors

## Version 3: Secret derivation

Using [NUT-13](../13.md#v3-message) derivation procedure for V3 with the following inputs:

```json
{
  "seed_utf8": "nut13 v3 test seed",
  "seed_hex": "6e7574313320763320746573742073656564",
  "keyset_id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6"
}
```

The values derived for counters `0` to `3` are:

```json
[
  {
    "counter": 0,
    "secret_key": "47196dc081150ce13fd0e478b8b71831b825be389211c9c56a8062a61af70347",
    "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
    "blinding_factor": "156857a0bce1b2788895f1885a21c56cf000df0de1e855608c7ccb6d9e2d7728",
    "nums_offset": "4af68649f3230c5589879f0cf33fd6d9f007cd3a54a2e6ed8699a576630fc025",
    "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73"
  },
  {
    "counter": 1,
    "secret_key": "659a545656334a47e08de62377e2f3128c72cd27e576908842e1ab359d395247",
    "secret": "03a882e17eb79f4f87313b299e208f9109734d0211a8df307b1570dbad2cdf74bf",
    "blinding_factor": "6de008e7a6c418b76a94e48c4b71a11078173de70abb3eaeb7cc1273a6dccede",
    "nums_offset": "d78b39a2ba263f92ea3ea2f721705c545d949349767e55bbdc41884cbb9a8b18"
  },
  {
    "counter": 2,
    "secret_key": "cee0df42cdaee25b228300b460edcbfab94be650ce2676abd77ef0697311e5e2",
    "secret": "02da107b7bfa3afedc0b49c62de58cb5429e1ad42b45c14a3e6da20156222ea41b",
    "blinding_factor": "35f56bb2016802a96a2846de8635712281d68182788410735b9826a211499fd4",
    "nums_offset": "d01054af49de60a8a62c592c4bea44f02782f7c6371136d985dfd9d690de5a15"
  },
  {
    "counter": 3,
    "secret_key": "46c2c20d79496e1ebe19805ba4df33535474800eefefc252140e1f20d0284ffe",
    "secret": "03189b6c67a0046084bbd2d810b5c6086c117082fe569cb56107d70f4acf8ddb5c",
    "blinding_factor": "65724fcdbc4ccfbb2a610b1bddd14238492b81d3761584b6492fcbadfeb9355f",
    "nums_offset": "54d0371fad402c83b0f3854fd9b7c876da857e7f276614d7e19dfb6680356f09"
  }
]
```

The rejection loops are not decoration: for counters `0` to `3` the `0x00` branch accepts at attempts `0, 0, 0, 0` and the `0x01` branch at attempts `7, 1, 2, 2` (earlier attempts produce `x >= BLS_FR_ORDER`). An implementation that omits the loop, skips the length framing, or reuses the V2 message computes different values and fails these vectors.

The **leaf keys** (type `0x03`) at counter `0`, with the index suffix `u32_BE(i)`:

```json
[
  {
    "counter": 0,
    "index": 0,
    "privkey": "8aac8b31fe4babb8097f416ef8f8508fdba63589087f4d10bf6f96bddba23788",
    "pubkey": "033c1828d880aebfd316781d3dffe1c45953087917e6f734032666c1ed80f0653c"
  },
  {
    "counter": 0,
    "index": 1,
    "privkey": "c77d6d9440bde035b140fe622e96dea2ffb2227179c3241df6e2994811984656",
    "pubkey": "0210b63f8016248a6f4c372366eb521784002ab182acbeba94e00ec4898f629d81"
  },
  {
    "counter": 0,
    "index": 2,
    "privkey": "ba7a8fc52b8c77b7412e5edaae211d92f2c79980788e3e3a480eb0dccac0b33e",
    "pubkey": "020e35e2edc190c2c34e46e586233a4f357e35fa428ae6f53636bb93f201792096"
  }
]
```

**NOTE**:`i` is not a leaf's position: recover by deriving candidates and matching the tree's keys by value.

Type `0x04` quote lock keys have their own vectors in [NUT-20](20-test.md#deterministic-quote-locking-key-derivation-v3-keysets).

Counter `0` also carries `Y = hash_to_curve_G1(secret_bytes)` over the **decoded 33 bytes** of the secret, pinning the binary-secret hashing rule ([NUT-00](../00.md#secret-bytes)).
