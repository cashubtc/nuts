# NUT-29 Test Vectors

## Request Signature Validation

The following test vectors can be used to verify the signature required for the `POST /v1/mint/quote/{method}/pubkey` request.

The user generates a private key and derives the public key:

`private_key`: `1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef`
`pubkey`: `02bb50e2d89a4ed70663d080659fe0ad4b9bc3e06c17a227433966cb59ceee020d`

The user wants to look up quotes for this public key. The request contains the following parameters:

`timestamp`: `1714521600`
`mint_pubkey`: `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798`

The message to sign `msg_to_sign` is the concatenation of `pubkey || timestamp || mint_pubkey`:
`msg_to_sign`: `02bb50e2d89a4ed70663d080659fe0ad4b9bc3e06c17a227433966cb59ceee020d17145216000279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798`

The SHA-256 hash of `msg_to_sign` is:
`hash`: `8802cf9f257a9d8e9ad702b2eb6e6b98016b866ae6d8593840c0cfa115985d3e`

The Schnorr signature (BIP340) on the `hash` using the `private_key` is:
`signature`: `51efc2cedc082bce9780cf428f534a008150e699383b017950944271bfd8806a01eeb7a3833187d25c675062239cbd6567ca1d28dd2c38f841debee8524b9b9a`

The wallet sends the following `PostMintQuotesByPubkeyRequest`:

```json
{
  "pubkeys": [
    "02bb50e2d89a4ed70663d080659fe0ad4b9bc3e06c17a227433966cb59ceee020d"
  ],
  "pubkey_signatures": [
    "51efc2cedc082bce9780cf428f534a008150e699383b017950944271bfd8806a01eeb7a3833187d25c675062239cbd6567ca1d28dd2c38f841debee8524b9b9a"
  ],
  "timestamp": 1714521600
}
```
