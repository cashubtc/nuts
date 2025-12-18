# NUT-26 Test Vectors

## Payment Request Bech32m Encoding/Decoding

The following are JSON-formatted payment requests and their Bech32m-encoded counterparts using TLV serialization.

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
      "a": "nprofile1qy28wumn8ghj7un9d3shjtnyv9kh2uewd9hsz9mhwden5te0wfjkccte9curxven9eehqctrv5hszrthwden5te0dehhxtnvdakqqgydaqy7curk439ykptkysv7udhdhu68sucm295akqefdehkf0d495cwunl5",
      "g": [["n", "17"]]
    }
  ]
}
```

Encoded (Bech32m):

```
CREQB1QYQQSC3HVYUNQVFHXCPQQZQQQQQQQQQQQQ9QXQQPQQZSQ9MGW368QUE69UHNSVENXVH8XURPVDJN5VENXVUQWQREQYQQZQGZQQSGM6QFA3C8DTZ2FVZHVFQEACMWM0E50PE3K5TFMVPJJMN0VJ7M2TGRQQZSZMSZXYMSXQQHQ9EPGAMNWVAZ7TMJV4KXZ7FWV3SK6ATN9E5K7QCQRGQHY9MHWDEN5TE0WFJKCCTE9CURXVEN9EEHQCTRV5HSXQQSQ9EQ6AMNWVAZ7TMWDAEJUMR0DSACM0T5
```

---

### Nostr Transport Payment Request

A payment request using Nostr transport with multiple mints.

```json
{
  "i": "f92a51b8",
  "a": 100,
  "u": "sat",
  "m": ["https://mint1.example.com", "https://mint2.example.com"],
  "t": [
    {
      "t": "nostr",
      "a": "npub1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzqujme",
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
CREQB1QYQQSE3EXFSN2VTZ8QPQQZQQQQQQQQQQQPJQXQQPQQZSQXTGW368QUE69UHK66TWWSCJUETCV9KHQMR99E3K7MG9QQVKSAR5WPEN5TE0D45KUAPJ9EJHSCTDWPKX2TNRDAKSWQPEQYQQZQGZQQSQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQRQQZSZMSZXYMSXQQ8Q9HQGWFHXV6SM2EPL3
```

---

### Minimal Payment Request

A minimal payment request with only required fields (no transport specified).

```json
{
  "i": "7f4a2b39",
  "u": "sat",
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
CREQB1QYQQSDMXX3SNYC3N8YPSQQGQQ5QPS6R5W3C8XW309AKKJMN59EJHSCTDWPKX2TNRDAKSYP0LHG
```

---

### Payment Request with NUT-10 Locking

A payment request requiring P2PK-locked tokens with timeout tag.

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
CREQB1QYQQSCEEV56R2EPJVYPQQZQQQQQQQQQQQ86QXQQPQQZSQXRGW368QUE69UHK66TWWSHX27RPD4CXCEFWVDHK6ZQQTYQSQQGQQGQYYVPJVVEKYDTZVGERWEFNXCCNGDFHVVUNYEPEXDJRWWRYVSMNXEPNVS6NXDENXGCNZVRZXF3KVEFCVG6NQENZVVCXZCNRXCCN2EFEVVENXVGRQQXSWARFD4JK7AT5QSENVVPS2N5FAS
```

---

### HTTP POST Transport (kind=2)

A payment request using HTTP POST transport with custom tags.

```json
{
  "i": "http_test",
  "a": 250,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "t": [
    {
      "t": "post",
      "a": "https://api.example.com/v1/payment",
      "g": [["custom", "value1", "value2"]]
    }
  ]
}
```

Encoded:

```
CREQB1QYQQJ6R5W3C97AR9WD6QYQQGQQQQQQQQQQQ05QCQQYQQ2QQCDP68GURN8GHJ7MTFDE6ZUETCV9KHQMR99E3K7MG8QPQSZQQPQGPQQGNGW368QUE69UHKZURF9EJHSCTDWPKX2TNRDAKJ7A339ACXZ7TDV4H8GQCQZ5RXXATNW3HK6PNKV9K82EF3QEMXZMR4V5EQYMWA48
```

---

### In-Band Transport (kind=0)

A payment request using in-band transport (tokens sent directly in the response).

```json
{
  "i": "in_band_test",
  "a": 100,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "t": [
    {
      "t": "in_band",
      "a": ""
    }
  ]
}
```

Encoded:

```
CREQB1QYQQC6TWTA3XZMNYTA6X2UM5QGQQSQQQQQQQQQQQVSPSQQGQQ5QPS6R5W3C8XW309AKKJMN59EJHSCTDWPKX2TNRDAKSWQQYQYQQZQQZ0MXTG
```

---

### Relay Tag Extraction from nprofile

A payment request with relays embedded in the nprofile (demonstrates "r" tag tuple encoding).

```json
{
  "i": "relay_test",
  "a": 100,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "t": [
    {
      "t": "nostr",
      "a": "nprofile1qqsrhuxx8l9ex335q7he0f09aej04zpazpl0ne2cgukyawd24mayt8gpz4mhxue69uhhyetvv9ujuerpd46hxtnfduhszrthwden5te0dehhxtnvdakqz9thwden5te0v9cxjv3wv4uxzmtsd3jjucm0d5q3vamnwvaz7tmjv4kxz7fw0ys"
    }
  ]
}
```

Encoded:

```
CREQB1QYQQ5UN9D3SHJHM5V4EHGQSQPQQQQQQQQQQQQEQRQQQSQPGQRP58GARSWVAZ7TMDD9H8GTN90PSK6URVV5HXXMMDQUQGZQGQQYQSYQPQ80CVV07TJDRRGPA0J7J7TMNYL2YR6YR7L8J4S3EVF6U64TH6GKWSXQQMQ9EPSAMNWVAZ7TMJV4KXZ7F39EJHSCTDWPKX2TNRDAKSXQQMQ9EPSAMNWVAZ7TMJV4KXZ7FJ9EJHSCTDWPKX2TNRDAKSXQQMQ9EPSAMNWVAZ7TMJV4KXZ7FN9EJHSCTDWPKX2TNRDAKS2AH7LM
```

---

### Description Field

A payment request with a description field.

```json
{
  "i": "desc_test",
  "a": 100,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "d": "Test payment description"
}
```

Encoded:

```
CREQB1QYQQJER9WD347AR9WD6QYQQGQQQQQQQQQQQXGQCQQYQQ2QQCDP68GURN8GHJ7MTFDE6ZUETCV9KHQMR99E3K7MGXQQV9GETNWSS8QCTED4JKUAPQV3JHXCMJD9C8G6T0DCFLJJRX
```

---

### Single-Use Field (true)

A payment request with single_use set to true.

```json
{
  "i": "single_use_true",
  "a": 100,
  "u": "sat",
  "s": true,
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
CREQB1QYQQ7UMFDENKCE2LW4EK2HM5WF6K2QSQPQQQQQQQQQQQQEQRQQQSQPQQQYQS2QQCDP68GURN8GHJ7MTFDE6ZUETCV9KHQMR99E3K7MGX0AYM7
```

---

### Single-Use Field (false)

A payment request with single_use set to false.

```json
{
  "i": "single_use_false",
  "a": 100,
  "u": "sat",
  "s": false,
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
CREQB1QYQPQUMFDENKCE2LW4EK2HMXV9K8XEGZQQYQQQQQQQQQQQRYQVQQZQQYQQQSQPGQRP58GARSWVAZ7TMDD9H8GTN90PSK6URVV5HXXMMDQ40L90
```

---

### Non-Sat Unit (msat)

A payment request using millisatoshi unit (string encoding, not 0x00).

```json
{
  "i": "unit_msat",
  "a": 1000,
  "u": "msat",
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
CREQB1QYQQJATWD9697MTNV96QYQQGQQQQQQQQQQP7SQCQQ3KHXCT5Q5QPS6R5W3C8XW309AKKJMN59EJHSCTDWPKX2TNRDAKSYYMU95
```

---

### Non-Sat Unit (usd)

A payment request using USD unit (string encoding).

```json
{
  "i": "unit_usd",
  "a": 500,
  "u": "usd",
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
CREQB1QYQQSATWD9697ATNVSPQQZQQQQQQQQQQQ86QXQQRW4EKGPGQRP58GARSWVAZ7TMDD9H8GTN90PSK6URVV5HXXMMDEPCJYC
```

---

### Multiple Transports

A payment request with multiple transport options (Nostr + HTTP POST), demonstrating priority ordering.

```json
{
  "i": "multi_transport",
  "a": 500,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "d": "Payment with multiple transports",
  "t": [
    {
      "t": "nostr",
      "a": "npub180cvv07tjdrrgpa0j7j7tmnyl2yr6yr7l8j4s3evf6u64th6gkwsyjh6w6",
      "g": [["n", "17"]]
    },
    {
      "t": "post",
      "a": "https://api1.example.com/payment"
    },
    {
      "t": "post",
      "a": "https://api2.example.com/payment",
      "g": [["priority", "backup"]]
    }
  ]
}
```

Encoded:

```
CREQB1QYQQ7MT4D36XJHM5WFSKUUMSDAE8GQSQPQQQQQQQQQQQRAQRQQQSQPGQRP58GARSWVAZ7TMDD9H8GTN90PSK6URVV5HXXMMDQCQZQ5RP09KK2MN5YPMKJARGYPKH2MR5D9CXCEFQW3EXZMNNWPHHYARNQUQZ7QGQQYQSYQPQ80CVV07TJDRRGPA0J7J7TMNYL2YR6YR7L8J4S3EVF6U64TH6GKWSXQQ9Q9HQYVFHQUQZWQGQQYPQYQPQDP68GURN8GHJ7CTSDYCJUETCV9KHQMR99E3K7MF0WPSHJMT9DE6QWQP6QYQQZQSZQQSXSAR5WPEN5TE0V9CXJV3WV4UXZMTSD3JJUCM0D5HHQCTED4JKUAQRQQGQSURJD9HHY6T50YRXYCTRDD6HQ6E8MEJ
```

---

### Minimal Nostr Transport (pubkey only)

A minimal Nostr transport with just the pubkey (no relays, no tags).

```json
{
  "i": "minimal_nostr",
  "u": "sat",
  "m": ["https://mint.example.com"],
  "t": [
    {
      "t": "nostr",
      "a": "npub180cvv07tjdrrgpa0j7j7tmnyl2yr6yr7l8j4s3evf6u64th6gkwsyjh6w6"
    }
  ]
}
```

Encoded:

```
CREQB1QYQQ6MTFDE5K6CTVTAHX7UM5WGPSQQGQQ5QPS6R5W3C8XW309AKKJMN59EJHSCTDWPKX2TNRDAKSWQP8QYQQZQGZQQSRHUXX8L9EX335Q7HE0F09AEJ04ZPAZPL0NE2CGUKYAWD24MAYT8GGJD0H8
```

---

### Minimal HTTP POST Transport (URL only)

A minimal HTTP POST transport with just the URL (no tags).

```json
{
  "i": "minimal_http",
  "u": "sat",
  "m": ["https://mint.example.com"],
  "t": [
    {
      "t": "post",
      "a": "https://api.example.com"
    }
  ]
}
```

Encoded:

```
CREQB1QYQQCMTFDE5K6CTVTA58GARSQVQQZQQ9QQVXSAR5WPEN5TE0D45KUAPWV4UXZMTSD3JJUCM0D5RSQ8SPQQQSYQSQZA58GARSWVAZ7TMPWP5JUETCV9KHQMR99E3K7MG5V34PA
```

---

### NUT-10 HTLC Locking (kind=1)

A payment request requiring HTLC-locked tokens with preimage tag.

```json
{
  "i": "htlc_test",
  "a": 1000,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "nut10": {
    "k": "HTLC",
    "d": "a]a0bPdf5jLl)B",
    "t": [
      ["preimage", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"],
      ["pubkeys", "02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331"],
      ["locktime", "1750000000"],
      ["refund", "03c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331"]
    ]
  }
}
```

Encoded:

```
CREQB1QYQQJ6R5D3347AR9WD6QYQQGQQQQQQQQQQP7SQCQQYQQ2QQCDP68GURN8GHJ7MTFDE6ZUETCV9KHQMR99E3K7MGXQQF5S4ZVGVSXCMMRDDJKGGRSV9UK6ETWWSYQPTGPQQQSZQSQGFS46VR9XCMRSV3SVFNXYDP3XGERZVNRVCMKZC3NV3JKYVP5X5UKXEFJ8QEXZVTZXQ6XVERPXUMX2CFKXQERVCFKXAJNGVTPV5ERVE3NV33SXQQ5PPKX7CMTW35K6EG2XYMNQVPSXQCRQVPSQVQY5PNJV4N82MNYGGCRXVEJ8QCKXVEHXCMNWETPXGMNXETZXUCNSVMZXUURXVPKXANR2V35XSUNXVM9VCMNSEPCVVEKVVF4VGCKZDEHVD3RYDPKXQUNJCEJXEJS4EHJHC
```

---

### Custom Currency Unit

A payment request using a custom currency unit (string encoding, not a known unit).

```json
{
  "i": "custom_unit",
  "a": 100,
  "u": "gold",
  "m": ["https://mint.example.com"]
}
```

Encoded:

```
CREQB1QYQQKCM4WD6X7M2LW4HXJAQZQQYQQQQQQQQQQQRYQVQQXCN5VVZSQXRGW368QUE69UHK66TWWSHX27RPD4CXCEFWVDHK6PZHCW8
```

---

## Notes on Test Vectors

### Encoding Details

1. **TLV Format**: Each TLV entry consists of:
   - Type (1 byte)
   - Length (2 bytes, big-endian)
   - Value (variable length)

2. **Unit Encoding**:
   - `0x00` represents `sat` (satoshis)
   - Other units are UTF-8 encoded strings

3. **Boolean Values**:
   - `0x00` = false
   - `0x01` = true

4. **Transport Kind Values**:
   - `0x00` = in-band (not explicitly included if no transport specified)
   - `0x01` = nostr
   - `0x02` = http_post

5. **NUT-10 Kind Values**:
   - `0x00` = P2PK
   - `0x01` = HTLC

### Case Sensitivity

All test vectors are provided in uppercase for optimal QR code compatibility. Decoders must accept both uppercase and lowercase variants.

### Validation

When implementing these test vectors:

1. Decode the Bech32m string
2. Parse the TLV structure
3. Validate field types and values
4. Compare with the expected JSON representation
5. Re-encode and verify the output matches the original
