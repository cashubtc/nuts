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

Using [NUT-13](13.md) derivation procedure for V2 with keyset ID `0192e40e27cdb961670dfb011d920566d574a9e8b4cce8252247f0d812fbd6be37`, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The secrets derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "secret_0": "244d2c0ea9735ef0a400a5b29a1467d6794d5349bb47b587442bb0f12af8bea7",
  "secret_1": "de51fd389c2e3955fa4532de2eacea01376d86512c65ce16d8475e433962b218",
  "secret_2": "cec18f3e333a0310c090024529802610c00b189d38c71f0d53606bd66e82fffd",
  "secret_3": "82f233e1cd63d921eb2583f16914bb76d590cd8160f5fee4a4ec4ff72adb5dcd",
  "secret_4": "253b5e0960fa63519e0666e87577a05dfe447f379952e36640116bb47f9a6c15"
}
```

The corresponding blinding factors `r` are:

```json
{
  "r_0": "88df4711b6444b3e8ed3e9dd629d50f7ee6db7c65644526700eb7bcfc89c8ea1",
  "r_1": "b514140fa4396fcbff7c2b7fec48f113cfe6a3a595ee8c426d5c63299f40f6d0",
  "r_2": "68ab0ee49f8fe59d99f7b9da452354dd61b24575f17d6e9a7ce13a31e073c67e",
  "r_3": "f40e0f2dcc145d9c4fdc6a1758d387b1b6ee195ba919d52eada78ee8ff45d680",
  "r_4": "490b2174f8e232e0a9eeabc128f7e1fcd71538b7d41335927205aaf6bcf3ccc8"
}
```
