# NUT-28 Test Vectors

## Quote Lookup Signature

The following test vectors use the public key `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac` with the corresponding private key `0000000000000000000000000000000000000000000000000000000000000001` (for testing purposes only).

### Valid Quote Lookup Request

The following is a `PostMintQuotesByPubkeyRequest` with a valid signature:

```json
{
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "timestamp": 1701704800,
  "signature": "f36fa5dc74a5be8ccf3a2ccaaa0efbf4f1f15a9916c9d3aa30058e3ab8ac9b7e4b1d92a17a7e4f2c8b6d0e9f1a3c5b7d9e2f4a6c8d0b3e5f7a9c1d3b5e7f9a1c3d5",
  "state": "PAID"
}
```

### Message to Sign

The message to sign for the above request is constructed as:

```
msg_to_sign = "quote_lookup" || pubkey || timestamp
            = "quote_lookup" || "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac" || "1701704800"
```

The concatenated UTF-8 string (without quotes):

```
quote_lookup03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac1701704800
```

As a byte array (UTF-8 encoded):

```
[113, 117, 111, 116, 101, 95, 108, 111, 111, 107, 117, 112, 48, 51, 100, 53, 54, 99, 101, 52, 101, 52, 52, 54, 97, 56, 53, 98, 98, 100, 97, 97, 53, 52, 55, 98, 52, 101, 99, 50, 98, 48, 55, 51, 100, 52, 48, 102, 102, 56, 48, 50, 56, 51, 49, 51, 53, 50, 98, 56, 50, 55, 50, 98, 55, 100, 100, 55, 97, 52, 100, 101, 53, 97, 55, 99, 97, 99, 49, 55, 48, 49, 55, 48, 52, 56, 48, 48]
```

The SHA-256 hash of this message is then signed using BIP340 Schnorr signature.

### Invalid Signature Example

The following is a `PostMintQuotesByPubkeyRequest` with an invalid signature (signature from a different private key):

```json
{
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "timestamp": 1701704800,
  "signature": "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "state": "PAID"
}
```

This should return error code `20010` (Signature for quote lookup invalid).

## Timestamp Validation

### Expired Timestamp

The following request has a timestamp that is too old (assuming current time is significantly later):

```json
{
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "timestamp": 1000000000,
  "signature": "...",
  "state": "PAID"
}
```

This should return error code `20011` (Timestamp outside valid window).

### Future Timestamp

The following request has a timestamp too far in the future:

```json
{
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "timestamp": 9999999999,
  "signature": "...",
  "state": "PAID"
}
```

This should return error code `20011` (Timestamp outside valid window).

## Quote Lookup Response

### Successful Response with Quotes

When quotes are found for the public key:

```json
{
  "quotes": [
    {
      "quote": "9d745270-1405-46de-b5c5-e2762b4f5e00",
      "request": "lnbc1000n1pj4apw9...",
      "amount": 100,
      "unit": "sat",
      "state": "PAID",
      "expiry": 1701704757,
      "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac"
    },
    {
      "quote": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
      "request": "lnbc500n1pj5bpw8...",
      "amount": 50,
      "unit": "sat",
      "state": "PAID",
      "expiry": 1701705000,
      "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac"
    }
  ]
}
```

### Empty Response

When no quotes are found for the public key:

```json
{
  "quotes": []
}
```

## Minting from Third-Party Quote

After discovering a quote via the lookup endpoint, Bob uses the standard NUT-20 flow to mint. The signature scheme is identical to NUT-20.

See [20-test.md](20-test.md) for minting signature test vectors.
