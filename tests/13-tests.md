# NUT-13 Test vectors

## Version 1: keyset ID integer representation

The integer representation of a keyset with an ID `009a1f293253e41e` and its corresponding derivation path for a counter of value `{counter}` are:

```json
{
  "keyset_id": "009a1f293253e41e",
  "keyest_id_int": 864559728,
  "derivation_path": "m/129372'/0'/864559728'/{counter}'"
}
```

## Version 1: Secret derivation

Using derivation `m/129372'/0'/864559728'/{counter}'`, we derive values starting from the following BIP39 mnemonic.

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The secrets derived for the first five counters from `counter=0` to `counter=4` are

```json
{
  "secret_0": "485875df74771877439ac06339e284c3acfcd9be7abf3bc20b516faeadfe77ae",
  "secret_1": "8f2b39e8e594a4056eb1e6dbb4b0c38ef13b1b2c751f64f810ec04ee35b77270",
  "secret_2": "bc628c79accd2364fd31511216a0fab62afd4a18ff77a20deded7b858c9860c8",
  "secret_3": "59284fd1650ea9fa17db2b3acf59ecd0f2d52ec3261dd4152785813ff27a33bf",
  "secret_4": "576c23393a8b31cc8da6688d9c9a96394ec74b40fdaf1f693a6bb84284334ea0"
}
```

The corresponding blinding factors `r` are

```json
{
  "r_0": "ad00d431add9c673e843d4c2bf9a778a5f402b985b8da2d5550bf39cda41d679",
  "r_1": "967d5232515e10b81ff226ecf5a9e2e2aff92d66ebc3edf0987eb56357fd6248",
  "r_2": "b20f47bb6ae083659f3aa986bfa0435c55c6d93f687d51a01f26862d9b9a4899",
  "r_3": "fb5fca398eb0b1deb955a2988b5ac77d32956155f1c002a373535211a2dfdc29",
  "r_4": "5f09bfbfe27c439a597719321e061e2e40aad4a36768bb2bcc3de547c9644bf9"
}
```

The corresponding derivation paths are

```json
{
  "derivation_path_0": "m/129372'/0'/864559728'/0'",
  "derivation_path_1": "m/129372'/0'/864559728'/1'",
  "derivation_path_2": "m/129372'/0'/864559728'/2'",
  "derivation_path_3": "m/129372'/0'/864559728'/3'",
  "derivation_path_4": "m/129372'/0'/864559728'/4'"
}
```

## Version 2: Secret derivation

Using [NUT-13](13.md) derivation procedure for V2 with keyset ID `015ba18a8adcd02e715a58358eb618da4a4b3791151a4bee5e968bb88406ccf76a`, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The secrets derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "secret_0": "db5561a07a6e6490f8dadeef5be4e92f7cebaecf2f245356b5b2a4ec40687298",
  "secret_1": "b70e7b10683da3bf1cdf0411206f8180c463faa16014663f39f2529b2fda922e",
  "secret_2": "78a7ac32ccecc6b83311c6081b89d84bb4128f5a0d0c5e1af081f301c7a513f5",
  "secret_3": "094a2b6c63bfa7970bc09cda0e1cfc9cd3d7c619b8e98fabcfc60aea9e4963e5",
  "secret_4": "5e89fc5d30d0bf307ddf0a3ac34aa7a8ee3702169dafa3d3fe1d0cae70ecd5ef"
}
```

The corresponding blinding factors `r` are:

```json
{
  "r_0": "6d26181a3695e32e9f88b80f039ba1ae2ab5a200ad4ce9dbc72c6d3769f2b035",
  "r_1": "bde4354cee75545bea1a2eee035a34f2d524cee2bb01613823636e998386952e",
  "r_2": "f40cc1218f085b395c8e1e5aaa25dccc851be3c6c7526a0f4e57108f12d6dac4",
  "r_3": "099ed70fc2f7ac769bc20b2a75cb662e80779827b7cc358981318643030577d0",
  "r_4": "5550337312d223ba62e3f75cfe2ab70477b046d98e3e71804eade3956c7b98cf"
}
```

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

## P2PK Derivation (pre-v3 keysets)

Using [NUT-13](13.md) derivation procedure for P2PK, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The public keys derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "m/129373'/10'/0'/0'/0": "021693d45f4fdf610ae641fedb0944fb460fbb8264f21c19d2626c3da755fcbbcb",
  "m/129373'/10'/0'/0'/1": "0395461ab678058c0ed6aa39f38dda490eaa163e9ad27070b23ec3d06b41e07535",
  "m/129373'/10'/0'/0'/2": "02a05e4e593a633e9b4405f01c9632c8afde24cb613017a1aee56fd76291ad26d1",
  "m/129373'/10'/0'/0'/3": "033addea25c3873b93d67d536c61c9d9c993f6efd8b9dfa657951b66b5001e51dd",
  "m/129373'/10'/0'/0'/4": "03c964bdf42fc82b6c574615746eeca37527a24f1fdfc1b34a732c53843b5744a5"
}
```
