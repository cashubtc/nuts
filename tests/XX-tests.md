# NUT-XX Test Vectors

The identity key is the [NUT-06](../06.md) example key (`secret_key` `3842a716975d6611d7ae4b36e28068c963e6d8ddb2b70d031d46a79d1df24c3c`, `pubkey` `0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da`). Signatures use [BIP-340] with the auxiliary randomness fixed to 32 zero bytes, which makes them reproducible; verifiers **MUST** accept any valid signature.

`SHA256("Cashu_MintResponse_v1")` = `133cc400b500d17eada7719b4610c620c4e769c7dc409496a3848b4235d51df2`.

Bodies are illustrative and hashed exactly as written, with no whitespace.

## Quote lookup with a nonce

`GET` with no body. The `nonce` rides along in `target` and is otherwise ignored by the mint.

```json
{
  "method": "GET",
  "target": "/v1/mint/quote/bolt11/quote123?nonce=0f1e2d3c4b5a69788796a5b4c3d2e1f00f1e2d3c4b5a69788796a5b4c3d2e1f0",
  "body_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "transcript": "0500910100034745540200652f76312f6d696e742f71756f74652f626f6c7431312f71756f74653132333f6e6f6e63653d30663165326433633462356136393738383739366135623463336432653166303066316532643363346235613639373838373936613562346333643265316630030020e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "request_digest": "e27b207f741271e090d8b90a48518f84f81aef4fbdbfaff102a4db5c100bfaf0",
  "response_body": "{\"quote\":\"quote123\",\"request\":\"lnbc...\",\"amount\":10,\"unit\":\"sat\",\"state\":\"UNPAID\",\"expiry\":1725308080}",
  "response_digest": "e74cffa8590914b749f949322bde19dc0c75413c0b2c70e63b8845e8ab135596",
  "message": "a686e57abb4d1eb56697f448723a6ca06bdadd55b870ae64ca2347fd98a6eff3",
  "signature": "982b6c2de95fb7bcc2cace1e07fffc063f8fd3d8b8a98f40e92e90d50c8bafd3fbcf7af37fdc7b58d8e31d2b8e2e6d53ad5da321c96f52375c0083f2fbff9588"
}
```

## State check

`POST` with a body.

```json
{
  "method": "POST",
  "target": "/v1/checkstate",
  "request_body": "{\"Ys\":[\"02d1a26a5b4f8e4a9bd7f2cd1f0e7a41c3e2f5b6a7c8d9e0f1a2b3c4d5e6f7a8b9\"]}",
  "body_hash": "d667ba0e0a052c46027973ce5779b7084557672a499acca9adccd1278bfe5344",
  "transcript": "05003b010004504f535402000e2f76312f636865636b7374617465030020d667ba0e0a052c46027973ce5779b7084557672a499acca9adccd1278bfe5344",
  "request_digest": "eba696acf48335e34dfee2f3ef8cf2c160299b29a047db10372d4e939268e3e1",
  "response_body": "{\"states\":[{\"Y\":\"02d1a26a5b4f8e4a9bd7f2cd1f0e7a41c3e2f5b6a7c8d9e0f1a2b3c4d5e6f7a8b9\",\"state\":\"UNSPENT\",\"witness\":null}]}",
  "response_digest": "ad31e3b071d4d96303bf333225ce8315b0c8be70ea8617644050215c84ff8699",
  "message": "28bafc7a7bbda7aa4b431fe0198f38f57bf4d5cff7be3545951b3fa0b4e39e00",
  "signature": "7c29827bdd37f0c174854ec350fc48aca0d15c0cedb5b8889416b30d7674a831b4041fb8c5429a9e0b2ee773b55740b9fd9626662f623a02ea510cc612ad6856"
}
```

[BIP-340]: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
