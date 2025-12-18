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
CREQB1QYQQSC3HVYUNQVFHXCPQQZQQQQQQQQQQQQ9QXQQPQQZSQ9MGW368QUE69UHNSVENXVH8XURPVDJN5VENXVUQWQRDQYQQZQGZQQSGM6QFA3C8DTZ2FVZHVFQEACMWM0E50PE3K5TFMVPJJMN0VJ7M2TGRQQPQQYGYQQ28WUMN8GHJ7UN9D3SHJTNYV9KH2UEWD9HSGQQHWAEHXW309AEX2MRP0YHRSVENXVH8XURPVDJJ7PQQP4MHXUE69UHKUMMN9EKX7MQ8402ZW
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
CREQB1QYQQSE3EXFSN2VTZ8QPQQZQQQQQQQQQQQPJQXQQPQQZSQXTGW368QUE69UHK66TWWSCJUETCV9KHQMR99E3K7MG9QQVKSAR5WPEN5TE0D45KUAPJ9EJHSCTDWPKX2TNRDAKSWQPWQYQQZQGZQQSQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQRQQZQQYFXQU6YHAEU
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
   - `0x0000` = P2PK
   - `0x0001` = HTLC

### Case Sensitivity

All test vectors are provided in uppercase for optimal QR code compatibility. Decoders must accept both uppercase and lowercase variants.

### Validation

When implementing these test vectors:

1. Decode the Bech32m string
2. Parse the TLV structure
3. Validate field types and values
4. Compare with the expected JSON representation
5. Re-encode and verify the output matches the original
