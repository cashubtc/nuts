# NUT-06 Test Vectors

These vectors use fixed request nonces and timestamps for reproducibility. Wallets that include request nonces generate fresh random request nonces for actual requests as specified in [NUT-06](../06.md).

## Identity key derivation

The seed is the UTF-8 encoding of `NUT-06 example mint seed`. With the domain separator `Cashu_Mint_Identity_v1` and the one-byte counter `0x00`, HMAC-SHA256 produces a valid secret key on the first attempt:

```json
{
  "seed_hex": "4e55542d3036206578616d706c65206d696e742073656564",
  "counter": 0,
  "secret_key": "3842a716975d6611d7ae4b36e28068c963e6d8ddb2b70d031d46a79d1df24c3c",
  "pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da",
  "aux_rand": "0000000000000000000000000000000000000000000000000000000000000000"
}
```

All signatures below use this identity key and the specified zero-filled BIP-340 auxiliary randomness. Verification uses the 32-byte x-coordinate of the compressed public key.

## Signature message hash

The message hash is `tagged_hash("Cashu_MintInfo_v1", bytes)`, where `bytes` is the canonical UTF-8 JSON after removing only `signature`. The UTF-8 tag hashes to `916a34ebf6f2244d64490e8eb2b5e7af19cdc45aa6176160186fc6543aa20d9b`. Decode this hex value into the raw 32-byte `tag_hash`; the message hash is `SHA256(tag_hash || tag_hash || bytes)`.

## Minimal signed response with a request nonce

Request:

```http
GET https://mint.host:3338/v1/info?request_nonce=000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
```

Response:

```json
{
  "pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da",
  "signature": "a2d6aefa3acbe4acf297225a4997153022be9439c8c83d7fc9e561f54baacade98a559ba28f444e2f9a543e4425d8d1c5fb0b20bfa647498509f244d9b4d9cff",
  "request_nonce": "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
  "time": 1725304480
}
```

After removing only `signature`, the canonical UTF-8 JSON is the following single line, without a trailing newline:

```text
{"pubkey":"0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da","request_nonce":"000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f","time":1725304480}
```

The tagged message hash signed by the mint is:

```text
6d1b435163023cbbc5045d83d90718b4439be44b0b7648c87a920d40ee8aee6a
```

With the request nonce above and the wallet's current Unix time set to `1725304480`, both signature verification and response validation succeed.

## Minimal signed response without a request nonce

Request:

```http
GET https://mint.host:3338/v1/info
```

The mint omits `request_nonce` and signs the response using the same identity key and auxiliary randomness:

```json
{
  "pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da",
  "signature": "1d48ab4a18f5680f9cbc28481c1c9921615cd0fbb8a8f3a015ec47ddf4720b69f7e870d8195c65b30445ce35b0d3035819ccc3adbea741873cf1e44cb9a48998",
  "time": 1725304480
}
```

After removing only `signature`, the canonical UTF-8 JSON is the following single line, without a trailing newline:

```text
{"pubkey":"0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da","time":1725304480}
```

The tagged message hash signed by the mint is:

```text
f50b2ddcbb72c59c25a17019d310ab5e73d2506f508522fa521fbd336aa9159c
```

With no request nonce and the wallet's current Unix time set to `1725304480`, both signature verification and response validation succeed.

## Response verification cases

Each row starts from the minimal signed response with a request nonce, its request nonce, and the wallet time `1725304480`. Apply only the indicated change; keep the original signature. `C` denotes the example request nonce, and `Z` denotes 64 zero characters, a different valid request nonce.

| Change                                                           | Expected result | Reason                                                                        |
| ---------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------- |
| None                                                             | Accept          | Valid signature, matching request nonce, and current timestamp                |
| Reorder JSON members or change whitespace                        | Accept          | Canonical signed payload is unchanged                                         |
| Request nonce is `Z`; response still contains `C`                | Reject          | Request nonce mismatch, even though the signature remains valid               |
| Response nonce is `Z`; request still contains `C`                | Reject          | Request nonce mismatch and invalid signature                                  |
| Both request and response nonces are `Z`                         | Reject          | Request nonce matches, but the signature does not cover the new request nonce |
| Remove `request_nonce`                                           | Reject          | Request nonce was requested but is missing                                    |
| Uppercase the response nonce                                     | Reject          | Malformed request nonce                                                       |
| Set response nonce to JSON number `0`                            | Reject          | Malformed request nonce                                                       |
| Remove `pubkey`, `signature`, or `time`, testing each separately | Reject          | Missing required field                                                        |
| Set `time` to JSON string `"1725304480"`                         | Reject          | Malformed timestamp                                                           |
| Set `time` to `1725304481`                                       | Reject          | Timestamp is within the allowed window, but the signature is invalid          |
| Add `"name": "Another mint"`                                     | Reject          | Every response member except `signature` is signed                            |
| Change the first signature byte from `0xa2` to `0xa3`            | Reject          | Invalid signature                                                             |
| Wallet time is `1725300880`                                      | Accept          | Mint time is exactly 3600 seconds ahead                                       |
| Wallet time is `1725308080`                                      | Accept          | Mint time is exactly 3600 seconds behind                                      |
| Wallet time is `1725300879`                                      | Reject          | Mint time is 3601 seconds ahead                                               |
| Wallet time is `1725308081`                                      | Reject          | Mint time is 3601 seconds behind                                              |

The following cases start from the minimal signed response without a request nonce, a request without a request nonce, and the wallet time `1725304480`. Apply only the indicated change; keep the original signature unless specified otherwise.

| Change                                                                                            | Expected result | Reason                                                                              |
| ------------------------------------------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------- |
| None                                                                                              | Accept          | Valid signed response to a request without a request nonce                          |
| Request nonce is `C`                                                                              | Reject          | Request nonce was requested but is missing, even though the signature remains valid |
| Replace the signature with the minimal response's signature from the example with a request nonce | Reject          | That signature covers a payload containing `request_nonce`                          |
| Add `"request_nonce": C` and set the request nonce to `C`                                         | Reject          | Request nonce matches, but the signature does not cover the added member            |

## Request validation cases

`C` denotes the example request nonce above. All lengths below refer to the URL-decoded query parameter value. Values longer than 64 characters are rejected before hex decoding or constructing and signing a response, without truncation. A valid format alone does not demonstrate that a request nonce was generated randomly; generating a fresh random request nonce is the wallet's responsibility.

| Query                                                                                                           | Expected result                                         |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `?request_nonce=C` with `C` substituted                                                                         | Valid request                                           |
| No query parameter                                                                                              | Valid request; response omits `request_nonce`           |
| `?request_nonce=`                                                                                               | HTTP `400`                                              |
| Request nonce is `C` with its final two characters removed (62 characters)                                      | HTTP `400`                                              |
| Request nonce is `C` with `0` appended (65 characters)                                                          | HTTP `400`; exceeds the length limit                    |
| Request nonce is `C` with `00` appended (66 characters)                                                         | HTTP `400`                                              |
| Request nonce is `0` repeated 4096 times (4096 characters)                                                      | HTTP `400`; exceeds the length limit                    |
| Request nonce is `C` with every character percent-encoded (64 characters after URL decoding)                    | Valid request; response echoes `C`                      |
| Request nonce is `C` with `0` appended, with every character percent-encoded (65 characters after URL decoding) | HTTP `400`; exceeds the length limit                    |
| Request nonce is `C` with its final character removed (63 characters)                                           | HTTP `400`                                              |
| Request nonce is the uppercase encoding of `C`                                                                  | HTTP `400`                                              |
| Request nonce is `C` with its first character replaced by `g`                                                   | HTTP `400`                                              |
| Two separate requests with `?request_nonce=C`, with `C` substituted                                             | Both valid; the mint does not track request nonce reuse |

## Full NUT-06 example

The complete response in the [NUT-06 example](../06.md#example) uses the same seed, request nonce, timestamp, and auxiliary randomness. After removing only `signature` and canonicalizing the remaining object, the expected tagged message hash and signature are:

```json
{
  "message_hash": "980585d03284414d98f1c21d32e9f6985a9fca94c69f6f56a7e3d40c89304b87",
  "signature": "a7e3a3bd6a1c4d6be9311f26c54617e51da8d8bc22fdbe78a61c6c824dec06845bd4d7fc9ee0db8e94837029913b9fbd034afd1f0a668d1e9f032af20c213004"
}
```

## Untagged signatures (invalid)

The following signatures were made over plain `SHA256(bytes)` using the same identity key and auxiliary randomness. Substituting each signature into its corresponding response above **MUST** fail verification against the tagged message hash:

```json
{
  "minimal_with_request_nonce": "6264f69d79bae5696b59080817e41612ac26f9539e1ae42900648d0b4ce48cb4cc1532eebd110a5a4c66cf130a11bc326c39c29ce969eeb32728e196c9605350",
  "minimal_without_request_nonce": "446f52ec13fea5410092eb2d26c28cd9c56b141fa9feb3c60c3845766038905ba44480bc24b0e202278634d724c07560d9f8528ee64db016e48016cb03c409a0",
  "full_example": "d14914e8d51baa3860c47145dc35c0d6c187b2df565e833a2ccbde2a45c6b7e19d42a9fc4d4f5209adee2cf407bb5b168be75149679412ef23bcdc0e7d177955"
}
```
