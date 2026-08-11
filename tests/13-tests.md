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

V3 keysets derive a [secret key](../13.md#v3-secret-key) on the `0x00` branch (the secret is the compressed point `K = k*G`) and a [blinding factor](../13.md#v3-blinding-factor) by rejection sampling against `BLS_FR_ORDER` on the `0x01` branch. Both branches append a 4-byte big-endian `attempt` counter to the V2 HMAC message.

Using [NUT-13](../13.md) derivation procedure for V3 with the following inputs:

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
    "secret_key": "7a7b3f7eb44f4a943041d936c0e0b2bf1dd0ac9a210bc8f8bc12b65cdbde9bd3",
    "secret": "0234df38671738d8e9ee205dc364fd4b45df8ed2ff91686e93d02ca1feb3b2f118",
    "blinding_factor": "513d1a0f0f01a09fdad2f7cea1403143fb86a1be2d152969b46b45cdaabd21aa",
    "Y": "87d86a7c00ee5f3a18b93c793b8e36f49518de08c7c20fd5e4fe6d89c4a3a9adaf4af0e8f6e9e06e44d0f1d83a1235c7"
  },
  {
    "counter": 1,
    "secret_key": "46b6a7854d4007073151c09aa2091a763abd6492d1cbbc3a5abeb24fd1e1f075",
    "secret": "02f6231465a1f6d4a787a0ede94b39a070993a4d84c2076ac53e4aeb168b5ff75b",
    "blinding_factor": "48ec152dbe1ffff2f368d1623723009d9e8d6bdc8c138575eb15c34c6b56db7b"
  },
  {
    "counter": 2,
    "secret_key": "78ef719cc25d6ffa6bfec641dbe0c4fc2a4260c4595ca0d27688dd6eb73ebd92",
    "secret": "039a8259b6dcb41da0aff51ed9acd4b03b96d795d6825c4ff2c517dbbc31c73909",
    "blinding_factor": "5041c676498aad5b0ec9e1135aa877a0716dbb3f1a4ccb894688f16d6b1debf6"
  },
  {
    "counter": 3,
    "secret_key": "bc813beb35621f256e923bd9dd7cfb3460077c1b1b2ef07dbd479fe3fcc77f46",
    "secret": "02cc8d2b280ca8e46846159d8918409a0820d664a4223060024fc6f489140e8368",
    "blinding_factor": "3d625b8869fc030e126f0a6d8109fc6c48b00ab6a8bd50a68dbd100e3cbb40de"
  }
]
```

Every `secret_key` above is accepted at `attempt=0`. The blinding factors are accepted at attempts `3`, `4`, `1` and `1` for counters `0` to `3` (earlier attempts produce `x >= BLS_FR_ORDER`): implementations that omit the rejection loop compute a different `blinding_factor` and fail this vector.

Counter `0` also carries `Y = hash_to_curve_G1(secret_bytes)` over the **decoded 33 bytes** of the secret, pinning the binary-secret hashing rule ([NUT-00](../00.md#secret-bytes)).

## P2PK Derivation

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
