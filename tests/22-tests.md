# NUT-22 Test Vectors

These vectors cover [nutroot blind authentication](../22.md#nutroot-blind-authentication-v3-keysets) (v3 auth keysets). The signature is BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes it reproducible; verifiers **MUST** accept any valid signature. The BAT secret key is the well-known test key `3` ([NUT-10 vectors](10-tests.md)).

## Request transcript

A BAT authorizing `POST /v1/swap`. The body is illustrative: `body_hash = SHA256("illustrative request body")`. The transcript is one authorized-request container (`0xF1`); `request_digest = SHA256(transcript)` and the witness signs `digest = tagged_hash("Cashu_AuthorizedRequest", request_digest)` ([NUT-22](../22.md#nutroot-blind-authentication-v3-keysets)), where `SHA256("Cashu_AuthorizedRequest")` = `00cb1b132a603b708bb3b1f56c64d64647b7bbc378f136fc53f66dc21ef325ec`.

The transcript, spelled out (`504f5354` is `POST`, `2f76312f73776170` is `/v1/swap`):

```
f1 0035 | 01 0004 504f5354 | 02 0008 2f76312f73776170 | 03 0020 bc1423...edce19
```

```json
{
  "secret": "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
  "method": "POST",
  "target": "/v1/swap",
  "body_hash": "bc14236ec9e2bf6d961268b7463d7be83e01554adfd063361e9e3ae985edce19",
  "transcript": "f10035010004504f53540200082f76312f73776170030020bc14236ec9e2bf6d961268b7463d7be83e01554adfd063361e9e3ae985edce19",
  "request_digest": "b4832c2f7390f933e17d2c70e2a4b99306782fd5f0ee2e5675cb96f67abb5556",
  "digest": "aaa50f1820f34bc7109b375c9a41e444ce362aabbb5aa6a18b2dbff75d03a54d",
  "witness": {
    "signatures": [
      "775fdc83744bd6f9b2b051ade53cd979f5a3552cb1f53c13be694a559ef2adc6feaf69b1901a4c0dce20fc17bdc3ae20aa077a703ab7d370f47a4c491de60260"
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
  "transcript": "f1005a01000347455402002e2f76312f6d696e742f71756f74652f626f6c7431312f71756f74653132333f623d3226613d3126713d6125323062030020e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "request_digest": "ca24b57145758188f31dc08588de1862dcc3aba143fa8b0dcffb29b423ce9142",
  "digest": "ccddd0edd33747425ab506ed56ab5c0f8e83e3fd24b67282239cec87b2e98ec2",
  "witness": {
    "signatures": [
      "0621ea88520bbf8e0519e0bbc5653040b1a10cac36a4891ba9fe354fed2b1990b8a68d918e024083c91fe875695c965c54aac75b830e180381073f63a684d980"
    ]
  }
}
```

A signer or verifier that reconstructs the target from parsed URL components must reproduce these bytes exactly: re-sorting the parameters or re-encoding `%20` changes the digest.
