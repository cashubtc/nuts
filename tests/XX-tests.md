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
  "request_digest": "6fdde90d42e0a3b864c09613e84a052d66f6578553a10721f3228067ab0bd354",
  "response_body": "{\"quote\":\"quote123\",\"request\":\"lnbc...\",\"amount\":10,\"unit\":\"sat\",\"state\":\"UNPAID\",\"expiry\":1725308080}",
  "response_digest": "e74cffa8590914b749f949322bde19dc0c75413c0b2c70e63b8845e8ab135596",
  "message": "9ef8202ef88b55ac457eda6e109e3c6a5ed05576e06ce9ed8af1c38c1080a197",
  "signature": "d383f24d28a7b0ad0eb66106a95e42a71298bb1d43da48009c355e732c517cc41d95d6b94bd8aa960c99b4c9013f5cb7067b80f902c22e04348062c00ecd07d6"
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
  "request_digest": "66a74a4965625ac66e412531c16e8df0a6219158f6418c14585e18f42cfd96c5",
  "response_body": "{\"states\":[{\"Y\":\"02d1a26a5b4f8e4a9bd7f2cd1f0e7a41c3e2f5b6a7c8d9e0f1a2b3c4d5e6f7a8b9\",\"state\":\"UNSPENT\",\"witness\":null}]}",
  "response_digest": "ad31e3b071d4d96303bf333225ce8315b0c8be70ea8617644050215c84ff8699",
  "message": "7ec42c37f7e45911ba2577902458abbb6fab874a8fc1a14e92906d926aa5ce34",
  "signature": "c11cd4f2b88b921ac432ff9e0a66167898cab114ff899bb74d619572182aac26e7955c486a0f887c73c7a068f5512ce793c155aaa2529f09d5defc28c655d382"
}
```

[BIP-340]: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
