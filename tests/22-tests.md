# NUT-22 Test Vectors

These vectors cover [nutroot blind authentication](../22.md#nutroot-blind-authentication-v3-keysets) (v3 auth keysets). The signature is BIP-340 with the auxiliary randomness fixed to 32 zero bytes, which makes it reproducible; verifiers **MUST** accept any valid signature. The BAT secret key is the well-known test key `3` ([NUT-10 vectors](10-tests.md)).

## Request transcript

A BAT authorizing `POST /v1/swap`. The body is illustrative: `body_hash = SHA256("illustrative request body")`. The transcript is one authorized-request container (`0x05`); `msg = "Cashu_Transaction_v1" || transcript` and `digest = SHA256(msg)` as for any transcript ([NUT-10](../10.md#the-transaction-transcript)).

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
  "digest": "ed581b087f06e474da2417eaf96d358244cb1b1b14464b2e3d8706f9a67bc10c",
  "witness": {
    "signatures": [
      "6a120a859e0cb85f9cb3d7a69c756d4f4f8ac0954785d7c9a9262ed937ddb3123d10a296a5ded693974f2b4722f89f9d00498d50f0706eb94bd967e5f3c7b85c"
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
  "digest": "6ed8e3a69429d4845ddcfa8728c7461c97b0c189592228c25266c630f62b1680",
  "witness": {
    "signatures": [
      "9306bc19ad0e497185a34ec9a49de0bd8161bcdf1c58f0fd9f108a7603affb1d24b1a2fd6d513bf843ac92c29c95614beb535ace4e3a4a8677d688388209fb88"
    ]
  }
}
```

A signer or verifier that reconstructs the target from parsed URL components must reproduce these bytes exactly: re-sorting the parameters or re-encoding `%20` changes the digest.
