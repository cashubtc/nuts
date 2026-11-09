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

## Payer refund path

Vectors for [Payer refund path](../18.md#payer-refund-path). Keys, nonce and times:

| Name                          | Value                                                                | Source                                                      |
| ----------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------- |
| `D` (payee key)               | `02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331` | "Payment Request with NUT-10 Locking" above                 |
| `R1` (payer refund key)       | `0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122` | tests/11-test.md, refund vector with `locktime` 21          |
| `R2` (second refund key)      | `026acbcd0fff3a424499c83ec892d3155c9d1984438659f448d9d0f1af3e92276a` | tests/11-test.md, refund vector with `locktime` 99999999999 |
| `K1` (another key)            | `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798` | tests/11-test.md, SIG_INPUTS 2-of-2 vector                  |
| `NONCE`                       | `0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1`   | tests/11-test.md, SIG_INPUTS 2-of-2 vector                  |
| `T` (acceptance time)         | `1700000000`                                                         | chosen                                                      |
| `<seconds>`                   | `604800`                                                             | chosen                                                      |
| payer margin, payee tolerance | `0`                                                                  | chosen, so the floor is `T + 604800` = `1700604800`         |

Secrets are compact JSON with key order `nonce`, `data`, `tags`, as in tests/11-test.md. `Y` is `hash_to_curve` of the secret's UTF-8 bytes ([NUT-00](../00.md)), as compressed hex.

### Request with a refund delay

```json
{
  "i": "c9e45d2a",
  "a": 500,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "nut10": {
    "k": "P2PK",
    "d": "02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331",
    "t": [["refund_delay", "604800"]]
  }
}
```

Encoded:

```
creqApWFpaGM5ZTQ1ZDJhYWEZAfRhdWNzYXRhbYF4GGh0dHBzOi8vbWludC5leGFtcGxlLmNvbWVudXQxMKNha2RQMlBLYWR4QjAyYzNiNWJiMjdlMzYxNDU3YzkyZDkzZDc4ZGQ3M2QzZDUzNzMyMTEwYjJjZmU4YjUwZmJjMGFiYzYxNWU5YzMzMWF0gYJscmVmdW5kX2RlbGF5ZjYwNDgwMA
```

The `creqB` form is in tests/26-test.md, "Payment Request with a Refund Delay".

### Payer construction

From the request above at time `T`, with refund key `R1` and margin 0:

```
["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
```

`Y` = `022eec557bb99699bdbadddfc2cace786f7bfae6b61755afcf1dd0af69750d5ce2`

### Payee acceptance

The payee holds key `D`, accepts at time `T` with tolerance 0, and does not use its option to refuse a `locktime` without `refund`. Each proof has a valid DLEQ proof, is `UNSPENT`, and has not been seen before. Every secret uses `NONCE`, and `data` = `D` unless the row says otherwise.

| Row | `tags`                                                                | Verdict                                                                       | `Y`                                                                  |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| a   | omitted                                                               | accept: permanent lock                                                        | `029f1d2769c56e956772197c02dc96628c5618a2d84cd695ff62445c17aafc91c0` |
| b   | `[["locktime","1700604800"],["refund",R1]]`                           | accept: refund path at the floor (inclusive)                                  | `022eec557bb99699bdbadddfc2cace786f7bfae6b61755afcf1dd0af69750d5ce2` |
| c   | `[["locktime","1700604800"],["refund",R1,R2],["n_sigs_refund","2"]]`  | accept: refund path with two refund keys                                      | `02ad4edd08acaa24792cc07060f48f459f18958fcf35c1d589a6f8e9fdfabc4ed8` |
| d   | `[["locktime","1700604800"],["refund",R1],["sigflag","SIG_INPUTS"]]`  | accept: explicit default sigflag                                              | `02e8bc9046cd6312570dafb0781b3162e3344d419e96ef79d56152c40e94d05a87` |
| e   | `[["locktime","1700604800"],["refund",R1],["n_sigs","1"]]`            | accept: explicit default n_sigs                                               | `024c50bf3f974000fce3be2657410e4b7c5d22af7c6d4028a89488510de506c165` |
| f   | `[["refund_delay","604800"],["locktime","1700604800"],["refund",R1]]` | accept: marker copied into the secret                                         | `0218b0c776ef46431a4059d9c989542758324f85d9a84d5b1c686ce8665b8506cd` |
| g   | `[["refund_delay","604800"]]`                                         | accept: marker copied, permanent lock                                         | `02ce4bf227049e7a8e1bdfe8dcead64f331b16fe181ad8021ea5e66bd45b146044` |
| h   | `[["refund",R1]]`                                                     | accept: refund without locktime, a permanent lock under NUT-11                | `020bc32a31401a31eb26bc7fd0d9e5caedd3d0778886cf370c09a2786ed7da8bff` |
| i   | `[["locktime","1700604800"]]`                                         | accept: locktime without refund                                               | `02e254181e0e61ac508ea187e3f4129887997bb540f1bbe3de050c803035ac8d7b` |
| j   | `[["locktime","1700604799"],["refund",R1]]`                           | reject: locktime below the floor                                              | `0257447c1fbab1dc08a541110b1e7411454375632bc7efdf89dc9b5c8d08aeddbe` |
| k   | `data` = K1, tags omitted                                             | reject: data is not the requested key                                         | `02a0af9c23f06ef1bd6867791de1ee7fba64dfe1a511bced3a40c24806c262490b` |
| l   | `[["pubkeys",R1]]`                                                    | reject: pubkeys not in the request                                            | `0271bcd9fdfd602bfb5ba5d7ae6e05e65efc7fe8ffcf0945a70450898bd6b0d1ae` |
| m   | `[["locktime","1700604800"],["refund",R1],["sigflag","SIG_ALL"]]`     | reject: sigflag not in the request                                            | `0277f5d067318b92664f5ed9c95d8dd1ea679a04c1a1e4e5126c55e11f5a100e97` |
| n   | `[["locktime","1700604800"],["locktime","1700604800"],["refund",R1]]` | reject: repeated tag, malformed under NUT-11                                  | `02d65e1a4394bc25e4c7ff98486637f5436b80fa1541ff9ce6ce69ff1b20f494a5` |
| o   | `[["locktime","1700604800"],["refund",R1,R2],["n_sigs_refund","3"]]`  | reject: n_sigs_refund above the number of refund keys, malformed under NUT-11 | `020ef39aa82efeca527dd5a89bdb1a7e5db598fdd23072abbbb49ff32a99aa3871` |
| p   | `[["locktime","abc"],["refund",R1]]`                                  | reject: locktime is not a decimal integer                                     | `025cbea91a7c5c40487775c0e8ae9e21a43ceb91abc445a969c706304aa3c305a6` |

Full secrets:

```
a ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331"}]
b ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
c ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122","026acbcd0fff3a424499c83ec892d3155c9d1984438659f448d9d0f1af3e92276a"],["n_sigs_refund","2"]]}]
d ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"],["sigflag","SIG_INPUTS"]]}]
e ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"],["n_sigs","1"]]}]
f ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["refund_delay","604800"],["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
g ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["refund_delay","604800"]]}]
h ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
i ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"]]}]
j ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604799"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
k ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"}]
l ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["pubkeys","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
m ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"],["sigflag","SIG_ALL"]]}]
n ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
o ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","1700604800"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122","026acbcd0fff3a424499c83ec892d3155c9d1984438659f448d9d0f1af3e92276a"],["n_sigs_refund","3"]]}]
p ["P2PK",{"nonce":"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1","data":"02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331","tags":[["locktime","abc"],["refund","0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122"]]}]
```
