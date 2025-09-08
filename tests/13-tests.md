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

Using [NUT-13](13.md) derivation procedure for V2 with keyset ID `012e23479a0029432eaad0d2040c09be53bab592d5cbf1d55e0dd26c9495951b30`, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The secrets derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "secret_0": "ba250bf927b1df5dd0a07c543be783a4349a7f99904acd3406548402d3484118",
  "secret_1": "3a6423fe56abd5e74ec9d22a91ee110cd2ce45a7039901439d62e5534d3438c1",
  "secret_2": "843484a75b78850096fac5b513e62854f11d57491cf775a6fd2edf4e583ae8c0",
  "secret_3": "3600608d5cf8197374f060cfbcff134d2cd1fb57eea68cbcf2fa6917c58911b6",
  "secret_4": "717fce9cc6f9ea060d20dd4e0230af4d63f3894cc49dd062fd99d033ea1ac1dd"
}
```

The corresponding blinding factors `r` are:

```json
{
  "r_0": "4f8b32a54aed811b692a665ed296b4c1fc2f37a8be4006379e95063a76693745",
  "r_1": "c4b8412ee644067007423480c9e556385b71ffdff0f340bc16a95c0534fe0e01",
  "r_2": "ceff40983441c40acaf77d2a8ddffd5c1c84391fb9fd0dc4607c186daab1c829",
  "r_3": "41ad26b840fb62d29b2318a82f1d9cd40dc0f1e58183cc57562f360a32fdfad6",
  "r_4": "fb986a9c76758593b0e2d1a5172ade977c858d87111a220e16c292a9347abf81"
}
```
