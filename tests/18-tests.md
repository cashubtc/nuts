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
creqApWF0gaNhdGVub3N0cmFheKlucHJvZmlsZTFxeTI4d3VtbjhnaGo3dW45ZDNzaGp0bnl2OWtoMnVld2Q5aHN6OW1od2RlbjV0ZTB3ZmprY2N0ZTljdXJ4dmVuOWVlaHFjdHJ2NWhzenJ0aHdkZW41dGUwZGVoaHh0bnZkYWtxcWd5ZGFxeTdjdXJrNDM5eWtwdGt5c3Y3dWRoZGh1NjhzdWNtMjk1YWtxZWZkZWhrZjBkNDk1Y3d1bmw1YWeBgmFuYjE3YWloYjdhOTAxNzZhYQphdWNzYXRhbYF4Imh0dHBzOi8vbm9mZWVzLnRlc3RudXQuY2FzaHUuc3BhY2U=
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
