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
