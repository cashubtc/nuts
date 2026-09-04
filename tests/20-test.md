# NUT-20 Test Vectors

## Deterministic quote locking key derivation (v3 keysets)

Using [NUT-20](../20.md#deterministic-quote-locking-key-derivation-v3-keysets) derivation on the [NUT-13 V3 message](../13.md#v3-message) with `derivation_type_byte` `0x04`. The message frames an **empty** keyset id, so these keys are the same whatever keyset the quote later mints onto:

```json
{
  "seed_utf8": "nut13 v3 test seed",
  "seed_hex": "6e7574313320763320746573742073656564"
}
```

```json
[
  {
    "counter": 0,
    "privkey": "1e84b00ac9a8f6831dcd0f4b8750efbfb2af22b19c07cf4cccbb8cdc33289b25",
    "pubkey": "039b390a9a298305cc43dbec906ceb1caae1187a8d16a3f45b945442ae7339d746"
  },
  {
    "counter": 1,
    "privkey": "7fe5104204360ed5e2710dfcd351f2091f1e2acf2f5eb9b0ac2ed34b0e120bb8",
    "pubkey": "0332ef3eb87a93da987406ed1fe96a44541ea0daa175e53e7ffc1155bb09b47b38"
  }
]
```
