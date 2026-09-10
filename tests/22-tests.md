# NUT-22 Test Vectors

These vectors cover [nutroot blind authentication](../22.md#nutroot-blind-authentication-v3-keysets) (v3 auth keysets). The signature is BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes it reproducible; verifiers **MUST** accept any valid signature. The BAT secret key is the well-known test key `3` ([NUT-10 vectors](10-tests.md)).

## Request transcript

A BAT authorizing `POST /v1/swap`. The body is illustrative: `body_hash = SHA256("illustrative request body")`. The transcript is one authorized-request container (`0x05`); `request_digest = SHA256(transcript)` and the witness signs `digest = tagged_hash("Cashu_AuthorizedRequest", request_digest)` ([NUT-22](../22.md#nutroot-blind-authentication-v3-keysets)), where `SHA256("Cashu_AuthorizedRequest")` = `00cb1b132a603b708bb3b1f56c64d64647b7bbc378f136fc53f66dc21ef325ec`.

The transcript, spelled out (`504f5354` is `POST`, `2f76312f73776170` is `/v1/swap`):

```
05 0035 | 01 0004 504f5354 | 02 0008 2f76312f73776170 | 03 0020 bc1423...edce19
```

```json
{
  "secret": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "method": "POST",
  "target": "/v1/swap",
  "body_hash": "bc14236ec9e2bf6d961268b7463d7be83e01554adfd063361e9e3ae985edce19",
  "transcript": "050035010004504f53540200082f76312f73776170030020bc14236ec9e2bf6d961268b7463d7be83e01554adfd063361e9e3ae985edce19",
  "request_digest": "a950e32c5747b244597d7fcb8deb164e09882f75a2033956c7bfcf65b905346d",
  "digest": "d1e1e96f321842c6a3fc4805c67cb6886b2ec5ec8d41a14712d8c64c4daf5024",
  "witness": {
    "signatures": [
      "f6a405d660003c1b79c0c118f95173e6d5f376bbca6f915ddc2a9d421cb7858d1799930cfb3b066af72def5ea7b09ced08734bb593cd40aa5d4fb8d9d20ee7ee"
    ]
  }
}
```

The signature verifies against the BAT's `secret`; the BAT itself never appears in the transcript. A request without a body signs `body_hash = SHA256("")` = `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Request transcript with a query string

A BAT authorizing `GET /v1/mint/quote/bolt11/quote123?b=2&a=1&q=a%20b` with no body. The query parameters are illustrative: no current endpoint takes any, and the vector pins the target encoding, not an API shape. The target is the origin-form request-target exactly as sent: the query string rides along unsorted and percent-encoded as transmitted, and the absent body hashes the empty byte string.

```json
{
  "secret": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "method": "GET",
  "target": "/v1/mint/quote/bolt11/quote123?b=2&a=1&q=a%20b",
  "body_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "transcript": "05005a01000347455402002e2f76312f6d696e742f71756f74652f626f6c7431312f71756f74653132333f623d3226613d3126713d6125323062030020e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "request_digest": "66f0fe8517af59aa7d90f369a585cea2b2ec5c0b55c656cb4f17265496a74bb1",
  "digest": "8d98e2e2adef927be5beb69f352b0e160d33831b4e73ae7259aedbfe9fcb6129",
  "witness": {
    "signatures": [
      "440b6e51cdc21d8c6f2bb092fa8fe44f2a77428ccabbcdc2acff2cbcf04cec69b3c8f8336244600bacccbd29335b5116d5ba0f734d9f4666662f00d6c61b5d2c"
    ]
  }
}
```

A signer or verifier that reconstructs the target from parsed URL components must reproduce these bytes exactly: re-sorting the parameters or re-encoding `%20` changes the digest.
