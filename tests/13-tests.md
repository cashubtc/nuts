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
  "m/129372'/10'/0'/0'/0": "03381fbf0996b81d49c35bae17a70d71db9a9e802b1af5c2516fc90381f4741e06",
  "m/129372'/10'/0'/0'/1": "039bbb7a9cd234da13a113cdd8e037a25c66bbf3a77139d652786a1d7e9d73e600",
  "m/129372'/10'/0'/0'/2": "02ffd52ed54761750d75b67342544cc8da8a0994f84c46d546e0ab574dd3651a29",
  "m/129372'/10'/0'/0'/3": "02751ab780960ff177c2300e440fddc0850238a78782a1cab7b0ae03c41978d92d",
  "m/129372'/10'/0'/0'/4": "0391a9ba1c3caf39ca0536d44419a6ceeda922ee61aa651a72a60171499c02b423"
}
```
