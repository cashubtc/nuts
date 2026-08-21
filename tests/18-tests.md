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

### Complete Payment Request

A payment request with all optional fields included.

```json
{
  "i": "4840f51e",
  "a": 1000,
  "u": "sat",
  "s": true,
  "m": ["https://mint.example.com"],
  "d": "Product purchase",
  "t": [
    {
      "t": "post",
      "a": "https://api.example.com/pay"
    }
  ],
  "nut10": {
    "k": "P2PK",
    "d": "03baf0c3ac220366c2c397bf930579c4163435584f573b10910987c544c59e61f1",
    "t": [["purpose", "offline"]]
  }
}
```

Encoded:

```
creqAqGF0gaNhdGRwb3N0YWF4G2h0dHBzOi8vYXBpLmV4YW1wbGUuY29tL3BheWFn92FpaDQ4NDBmNTFlYWEZA+hhdWNzYXRhbYF4GGh0dHBzOi8vbWludC5leGFtcGxlLmNvbWFkcFByb2R1Y3QgcHVyY2hhc2Vhc/VlbnV0MTCjYWtkUDJQS2FkeEIwM2JhZjBjM2FjMjIwMzY2YzJjMzk3YmY5MzA1NzljNDE2MzQzNTU4NGY1NzNiMTA5MTA5ODdjNTQ0YzU5ZTYxZjFhdIGCZ3B1cnBvc2Vnb2ZmbGluZQ==
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

### Payment Request with NUT-10 Locking

A payment request requiring P2PK-locked tokens.

```json
{
  "i": "c9e45d2a",
  "a": 500,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "nut10": {
    "k": "P2PK",
    "d": "02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331",
    "t": [["timeout", "3600"]]
  }
}
```

Encoded:

```
creqApWFpaGM5ZTQ1ZDJhYWEZAfRhdWNzYXRhbYF4GGh0dHBzOi8vbWludC5leGFtcGxlLmNvbWVudXQxMKNha2RQMlBLYWR4QjAyYzNiNWJiMjdlMzYxNDU3YzkyZDkzZDc4ZGQ3M2QzZDUzNzMyMTEwYjJjZmU4YjUwZmJjMGFiYzYxNWU5YzMzMWF0gYJndGltZW91dGQzNjAw
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

A request for 8 sat to the payee's static key (well-known test key `3`), under a requested `after` leaf naming a co-signer key (test key `4`) that its owner tags blind-me; the payee relays the tag in `b`. The leaf bytes are the payer's to reproduce exactly ([NUT-18](../18.md#nutroot-locking-v3-keysets)); the resulting proof appears in the [NUT-10 vectors](10-tests.md).

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

A request locking payments to their leaves only: `k` is the [NUMS point](../10.md#bare-empty-tweaked-and-script-only-secrets), used verbatim, and the leaf's key (test key `4`) is tagged blind-me, which a NUMS request **MUST** include: the blinded leaf key is what makes each payment's secret unique.

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
creqAo2FhCGF1Y3NhdGd0YXByb290o2FreEIwMjUwOTI5Yjc0YzFhMDQ5NTRiNzhiNGI2MDM1ZTk3YTVlMDc4YTVhMGYyOGVjOTZkNTQ3YmZlZTlhY2U4MDNhYzBhbIF4YjAwMDIwMjAwMDEwMTA0MDAyMTAyZTQ5M2RiZjFjMTBkODBmMzU4MWU0OTA0OTMwYjE0MDRjYzZjMTM5MDBlZTA3NTg0NzRmYTk0YWJlOGM0Y2QxMzA2MDAwNDY4YTNiZTgwYWKBeEIwMmU0OTNkYmYxYzEwZDgwZjM1ODFlNDkwNDkzMGIxNDA0Y2M2YzEzOTAwZWUwNzU4NDc0ZmE5NGFiZThjNGNkMTM=
```

Paying it with ephemeral key `5` leaves the internal key as the NUMS point verbatim and blinds the leaf key at slot 1 (the [NUT-28 vectors](28-tests.md)' blinded leaf, byte for byte); the resulting proof carries:

```json
{
  "secret": "0296b745e131e3bfdd030d5f0d99c2e292a98385531b8a8715efe26ae29da86b20",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "K": "0250929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0",
    "tree": [
      "000202000101040021039ca57991c48db95252bff61e02c31cf9b1e9ec2ef27d9dee33db6f0324e6ca8106000468a3be80"
    ]
  }
}
```

A second payment picks a fresh ephemeral, blinds the leaf key differently, and lands on a different secret.
