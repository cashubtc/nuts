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
	"secret_0":	"7614f34ff4ab0e9faa2e8c0a9ef4d50be8516c38349f33f9ee6ddb0305cb5296",
	"secret_1":	"6da184e4f071826922a89f9212f685109484275d385576338225229f0358e538",
	"secret_2": "8ffe423197f49c3392605918267a31d1a604346b0c306ac18d90b7e6fdc098a5",
	"secret_3": "5adc787c2d58b5d3d66f96476b8fda2c692a34304d68f83702cd2a4a91d69896",
	"secret_4": "c6b5809f737da4a751a9cb0c72ab7e8227079078a11289661cfc30dbcb9e0aaa",
}
```

The corresponding blinding factors `r` are:
```json
{
  "r_0": "6814cff964b8eea6515c7cfc055801ee882a136c269fb6d68775da853625c278",
  "r_1": "44f95897b18ef106afa62b85c047c785eeddb7b66121f96c26addc47e9758e90",
  "r_2": "159142a3dcb9da743454ff5a13f9992375104e8d46b2359099683039930f3bc9",
  "r_3": "647e49ce7ea8894cc249307371bc64f202affbc5d2b1849da5ed8cd06ea5227e",
  "r_4": "a39f2a0d984260d4763335d02d4e2def02524f52701a67af596a80e3c61af713",
}
```