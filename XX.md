# NUT-XX: Mint Response Signatures

`optional`

`depends on: NUT-06, NUT-10`

---

This NUT defines a signature the mint attaches to every HTTP response, binding the response to the request the mint received. The signing key is the mint identity key of [NUT-06][06]. Wallets that have pinned that key can verify that a response was produced by the mint for the request the wallet sent, independent of the transport.

## Signature

For every response on a `/v1/` endpoint, the mint computes:

```
request_digest  = SHA256("Cashu_Transaction_v1" || authorized_request_container)
response_digest = SHA256(response_body)
message         = tagged_hash("Cashu_MintResponse_v1", request_digest || response_digest)
```

where:

- `authorized_request_container` is the [NUT-10][10] request transcript container (`0x05`: `01` method, `02` target, `03` body hash) built from the request as the mint received it. `request_digest` is the same value a [NUT-22][22] blind authentication token signs.
- `response_body` is the exact bytes of the HTTP response body. An empty body hashes the empty byte string.
- `tagged_hash` is the [BIP-340] tagged hash: `SHA256(SHA256(tag) || SHA256(tag) || msg)`.

The mint signs `message` with its identity key using [BIP-340] Schnorr over secp256k1 and returns the 64-byte signature, lowercase hex-encoded, in the response header:

```
Cashu-Signature: <hex_str>
```

The mint **MUST** include the header on every `/v1/` response, including error responses. The mint **MUST** relay `target` as sent and **MUST** ignore query parameters it does not recognize.

Intermediaries **MUST** relay the request body, the response body, and the `Cashu-Signature` header byte for byte. Mints serving browser wallets **MUST** list `Cashu-Signature` in `Access-Control-Expose-Headers`.

## Verification

The wallet reconstructs `request_digest` from the request it sent, computes `response_digest` from the body it received, and verifies the [BIP-340] Schnorr signature on `message` with the pinned [NUT-06][06] `pubkey` (the `02`/`03` prefix is dropped).

A wallet that has learned from a signed `GetInfoResponse` that the mint supports this NUT **MUST** treat a missing or invalid `Cashu-Signature` header as an invalid response.

The signature binds the response to a request, not to a point in time: a stored response to an identical request verifies again. [NUT-19][19] retries are therefore unaffected. Where a wallet needs proof that a response is current, it makes the request unique:

```
GET /v1/mint/quote/bolt11/{quote_id}?nonce=<hex_str>
```

`nonce` is 32 random bytes, hex-encoded, chosen by the wallet. It is part of `target` and so of `request_digest`; the mint does not interpret it. Wallets **MUST NOT** add a `nonce` to requests on [NUT-19][19] cached endpoints.

## Settings

Support is announced in the `nuts` field of the `GetInfoResponse` ([NUT-06][06]):

```json
"XX": {
  "supported": true
}
```

## Scope

[NUT-17][17] WebSocket messages carry no HTTP headers and are not covered. Replacement of the identity key is not covered: to a wallet, a mint with a new identity key is a new mint ([NUT-06][06]).

[06]: 06.md
[10]: 10.md
[17]: 17.md
[19]: 19.md
[22]: 22.md
[BIP-340]: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
