# NUT-18 Test Vectors

## Payment Request Encoding/Decoding

The following are JSON-formatted payment requests and their encoded counterparts.

### Basic Payment Request

A basic payment request with required fields.

```json
{
  "i": "b7a90176",
  "a": 10,
  "u": "sat",
  "m": ["https://8333.space:3338"],
  "t": [
    {
      "t": "nostr",
      "a": "nprofile1qqsgm6qfa3c8dtz2fvzhvfqeacmwm0e50pe3k5tfmvpjjmn0vj7m2tgpz3mhxue69uhhyetvv9ujuerpd46hxtnfduq3wamnwvaz7tmjv4kxz7fw8qenxvewwdcxzcm99uqs6amnwvaz7tmwdaejumr0ds4ljh7n",
      "g": [["n", "17"]]
    }
  ]
}
```

Encoded (CBOR serialized to base64url):

```
creqApWF0gaNhdGVub3N0cmFheKlucHJvZmlsZTFxcXNnbTZxZmEzYzhkdHoyZnZ6aHZmcWVhY213bTBlNTBwZTNrNXRmbXZwamptbjB2ajdtMnRncHozbWh4dWU2OXVoaHlldHZ2OXVqdWVycGQ0Nmh4dG5mZHVxM3dhbW53dmF6N3RtanY0a3h6N2Z3OHFlbnh2ZXd3ZGN4emNtOTl1cXM2YW1ud3Zhejd0bXdkYWVqdW1yMGRzNGxqaDduYWeBgmFuYjE3YWloYjdhOTAxNzZhYQphdWNzYXRhbYF3aHR0cHM6Ly84MzMzLnNwYWNlOjMzMzg
```

### HTTP Transport Payment Request

A payment request using HTTP POST transport.

```json
{
  "i": "a2c12f45",
  "a": 50,
  "u": "sat",
  "m": ["https://cashu.example.com"],
  "t": [
    {
      "t": "post",
      "a": "https://api.example.com/receive"
    }
  ]
}
```

Encoded:

```
creqApWF0gaNhdGRwb3N0YWF4H2h0dHBzOi8vYXBpLmV4YW1wbGUuY29tL3JlY2VpdmVhZ/dhaWhhMmMxMmY0NWFhGDJhdWNzYXRhbYF4GWh0dHBzOi8vY2FzaHUuZXhhbXBsZS5jb20=
```

### Nostr Transport Payment Request

A payment request using Nostr transport with NIP-17 support.

```json
{
  "i": "f92a51b8",
  "a": 100,
  "u": "sat",
  "m": ["https://mint1.example.com", "https://mint2.example.com"],
  "t": [
    {
      "t": "nostr",
      "a": "npub1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq28spj3",
      "g": [
        ["n", "17"],
        ["n", "9735"]
      ]
    }
  ]
}
```

Encoded:

```
creqApWF0gaNhdGVub3N0cmFheD9ucHViMXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXFxcXEyOHNwajNhZ4KCYW5iMTeCYW5kOTczNWFpaGY5MmE1MWI4YWEYZGF1Y3NhdGFtgngZaHR0cHM6Ly9taW50MS5leGFtcGxlLmNvbXgZaHR0cHM6Ly9taW50Mi5leGFtcGxlLmNvbQ==
```

### Minimal Payment Request

A payment request with only required fields and no transport specified (implying in-band transport).

```json
{
  "i": "7f4a2b39",
  "u": "sat",
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
creqAo2FpaDdmNGEyYjM5YXVjc2F0YW2BeBhodHRwczovL21pbnQuZXhhbXBsZS5jb20=
```

### Preferred Mint List with Supported Methods

A payment request specifying a preferred mint list with `mp` set to `true` and the supported payment methods (`sm`). `bolt12` carries a per-method fee (`mf`) that applies to payments from non-preferred mints.

```json
{
  "i": "preferred_fee_methods",
  "a": 100,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "mp": true,
  "sm": [{ "mn": "bolt11" }, { "mn": "bolt12", "mf": 5 }]
}
```

Encoded:

```
creqApmFpdXByZWZlcnJlZF9mZWVfbWV0aG9kc2FhGGRhdWNzYXRhbYF4GGh0dHBzOi8vbWludC5leGFtcGxlLmNvbWJtcPVic22CoWJtbmZib2x0MTGiYm1uZmJvbHQxMmJtZgU=
```

### Nutroot Locking

A request for 8 sat to the payee's static key (well-known test key `3`), under a requested `after` leaf naming a co-signer key (test key `4`) that its owner tags blind-me; the payee relays the tag in `b`. The leaf bytes are the payer's to reproduce exactly ([NUT-18](../18.md#nutroot-locking-v3-keysets)). Paid with ephemeral key `5`, the resulting proof's internal key and blinded leaf are the [NUT-28 slot-map vectors](28-tests.md#nutroot-secrets-v3-the-slot-map)' `slot0_blinded` and `leaf_with_blinded_slot1`.

```json
{
  "a": 8,
  "u": "sat",
  "nutroot": {
    "k": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
    "l": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ],
    "b": ["02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13"]
  }
}
```

#### NUMS (leaves-only) request

A request locking payments to their leaves only: `k` is the [NUMS point](../10.md#the-internal-key), and the leaf's key (test key `4`) is tagged blind-me, so the payment's ephemeral travels. The payer derives `K = H + u*G` with a fresh `u` per output; `u` is fixed to the scalar of a small test key here for a stable vector.

```json
{
  "a": 8,
  "u": "sat",
  "nutroot": {
    "k": "0250929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0",
    "l": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ],
    "b": ["02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13"]
  }
}
```

Encoded:

```
creqAo2FhCGF1Y3NhdGdudXRyb290o2FreEIwMjUwOTI5Yjc0YzFhMDQ5NTRiNzhiNGI2MDM1ZTk3YTVlMDc4YTVhMGYyOGVjOTZkNTQ3YmZlZTlhY2U4MDNhYzBhbIF4YjAwMDIwMjAwMDEwMTA0MDAyMTAyZTQ5M2RiZjFjMTBkODBmMzU4MWU0OTA0OTMwYjE0MDRjYzZjMTM5MDBlZTA3NTg0NzRmYTk0YWJlOGM0Y2QxMzA2MDAwNDY4YTNiZTgwYWKBeEIwMmU0OTNkYmYxYzEwZDgwZjM1ODFlNDkwNDkzMGIxNDA0Y2M2YzEzOTAwZWUwNzU4NDc0ZmE5NGFiZThjNGNkMTM=
```

Paying it with ephemeral key `5` and `u` = scalar `7` blinds the leaf key at slot 1 (the [NUT-28 vectors](28-tests.md)' blinded leaf, byte for byte); the resulting proof carries:

```json
{
  "secret": "02fb23814e330739413a6e3982a21916002962002bc101ac105a28e0cf3bcb46d1",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "K": "028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407",
    "u": "0000000000000000000000000000000000000000000000000000000000000007",
    "tree": [
      "000202000101040021039ca57991c48db95252bff61e02c31cf9b1e9ec2ef27d9dee33db6f0324e6ca8106000468a3be80"
    ]
  }
}
```

The same request without its `b` entry blinds nothing, so no ephemeral is picked and none travels: spend info **MUST** omit `E`. Paid with `u` = scalar `9`, the requested leaf comes back verbatim:

```json
{
  "secret": "030b5dc180dd2ef76be0f0319fc5c254511fede8c8563a823d3b0fcd6f9012a0b2",
  "spend_info": {
    "K": "03b948fab26606a34380c4515ece4c27d25fcf53eb95d1041630ab44f2be4f7331",
    "u": "0000000000000000000000000000000000000000000000000000000000000009",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  }
}
```

A second payment picks a fresh `u` (and, where the request blinds, a fresh ephemeral) and lands on a different secret.
