# NUT-06 Test Vectors

These vectors use fixed challenges and timestamps for reproducibility. Wallets that include challenges generate fresh random challenges for actual requests as specified in [NUT-06](../06.md).

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

## Minimal signed response with a challenge

Request:

```http
GET https://mint.host:3338/v1/info?challenge=000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
```

Response:

```json
{
  "pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da",
  "signature": "77cc645a451e744ef2d0d05ef09166cae27e9baf38afd5ab1301739d5444e144db224b0f29bfa0941ec3d228a74c50a5287bb6664333e4261d641f806bc4a672",
  "challenge": "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
  "time": 1725304480
}
```

After removing only `signature`, the canonical UTF-8 JSON is the following single line, without a trailing newline:

```text
{"challenge":"000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f","pubkey":"0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da","time":1725304480}
```

The SHA-256 hash signed by the mint is:

```text
a586404ca44b8dbffbd732a1dc881905411d7558c40bb7c63855ffc9a0b1e913
```

With the request challenge above and the wallet's current Unix time set to `1725304480`, both signature verification and response validation succeed.

## Minimal signed response without a challenge

Request:

```http
GET https://mint.host:3338/v1/info
```

The mint omits `challenge` and signs the response using the same identity key and auxiliary randomness:

```json
{
  "pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da",
  "signature": "446f52ec13fea5410092eb2d26c28cd9c56b141fa9feb3c60c3845766038905ba44480bc24b0e202278634d724c07560d9f8528ee64db016e48016cb03c409a0",
  "time": 1725304480
}
```

After removing only `signature`, the canonical UTF-8 JSON is the following single line, without a trailing newline:

```text
{"pubkey":"0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da","time":1725304480}
```

The SHA-256 hash signed by the mint is:

```text
10f9a05585b71ce112269d10a16acbe1f81835958be3fcfc1d8b63cbbef0bb55
```

With no request challenge and the wallet's current Unix time set to `1725304480`, both signature verification and response validation succeed.

## Response verification cases

Each row starts from the minimal signed response with a challenge, its request challenge, and the wallet time `1725304480`. Apply only the indicated change; keep the original signature. `C` denotes the example challenge, and `Z` denotes 64 zero characters, a different valid challenge.

| Change                                                           | Expected result | Reason                                                                |
| ---------------------------------------------------------------- | --------------- | --------------------------------------------------------------------- |
| None                                                             | Accept          | Valid signature, matching challenge, and current timestamp            |
| Reorder JSON members or change whitespace                        | Accept          | Canonical signed payload is unchanged                                 |
| Request challenge is `Z`; response still contains `C`            | Reject          | Challenge mismatch, even though the signature remains valid           |
| Response challenge is `Z`; request still contains `C`            | Reject          | Challenge mismatch and invalid signature                              |
| Both request and response challenges are `Z`                     | Reject          | Challenge matches, but the signature does not cover the new challenge |
| Remove `challenge`                                               | Reject          | Challenge was requested but is missing                                |
| Uppercase the response challenge                                 | Reject          | Malformed challenge                                                   |
| Set response challenge to JSON number `0`                        | Reject          | Malformed challenge                                                   |
| Remove `pubkey`, `signature`, or `time`, testing each separately | Reject          | Missing required field                                                |
| Set `time` to JSON string `"1725304480"`                         | Reject          | Malformed timestamp                                                   |
| Set `time` to `1725304481`                                       | Reject          | Timestamp is within the allowed window, but the signature is invalid  |
| Add `"name": "Another mint"`                                     | Reject          | Every response member except `signature` is signed                    |
| Change the first signature byte from `0x77` to `0x76`            | Reject          | Invalid signature                                                     |
| Wallet time is `1725300880`                                      | Accept          | Mint time is exactly 3600 seconds ahead                               |
| Wallet time is `1725308080`                                      | Accept          | Mint time is exactly 3600 seconds behind                              |
| Wallet time is `1725300879`                                      | Reject          | Mint time is 3601 seconds ahead                                       |
| Wallet time is `1725308081`                                      | Reject          | Mint time is 3601 seconds behind                                      |

The following cases start from the minimal signed response without a challenge, a request without a challenge, and the wallet time `1725304480`. Apply only the indicated change; keep the original signature unless specified otherwise.

| Change                                                                                        | Expected result | Reason                                                                          |
| --------------------------------------------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------- |
| None                                                                                          | Accept          | Valid signed response to a request without a challenge                          |
| Request challenge is `C`                                                                      | Reject          | Challenge was requested but is missing, even though the signature remains valid |
| Replace the signature with the minimal response's signature from the example with a challenge | Reject          | That signature covers a payload containing `challenge`                          |
| Add `"challenge": C` and set the request challenge to `C`                                     | Reject          | Challenge matches, but the signature does not cover the added member            |

## Request validation cases

`C` denotes the example challenge above. All lengths below refer to the URL-decoded query parameter value. Values longer than 64 characters are rejected before hex decoding or constructing and signing a response, without truncation. A valid format alone does not demonstrate that a challenge was generated randomly; generating a fresh random challenge is the wallet's responsibility.

| Query                                                                                                       | Expected result                                     |
| ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `?challenge=C` with `C` substituted                                                                         | Valid request                                       |
| No query parameter                                                                                          | Valid request; response omits `challenge`           |
| `?challenge=`                                                                                               | HTTP `400`                                          |
| Challenge is `C` with its final two characters removed (62 characters)                                      | HTTP `400`                                          |
| Challenge is `C` with `0` appended (65 characters)                                                          | HTTP `400`; exceeds the length limit                |
| Challenge is `C` with `00` appended (66 characters)                                                         | HTTP `400`                                          |
| Challenge is `0` repeated 4096 times (4096 characters)                                                      | HTTP `400`; exceeds the length limit                |
| Challenge is `C` with every character percent-encoded (64 characters after URL decoding)                    | Valid request; response echoes `C`                  |
| Challenge is `C` with `0` appended, with every character percent-encoded (65 characters after URL decoding) | HTTP `400`; exceeds the length limit                |
| Challenge is `C` with its final character removed (63 characters)                                           | HTTP `400`                                          |
| Challenge is the uppercase encoding of `C`                                                                  | HTTP `400`                                          |
| Challenge is `C` with its first character replaced by `g`                                                   | HTTP `400`                                          |
| Two separate requests with `?challenge=C`, with `C` substituted                                             | Both valid; the mint does not track challenge reuse |

## Full NUT-06 example

The complete response in the [NUT-06 example](../06.md#example) uses the same seed, challenge, timestamp, and auxiliary randomness. After removing only `signature` and canonicalizing the remaining object, the expected hash and signature are:

```json
{
  "sha256": "5c318faedf41fb96835b18c775abf2f24bb5712310585aaf8a8d101ff2533344",
  "signature": "6495ee5d693994f9a7e821e5baaf87791c50eb98bae9b2047bdb18cfbed4d92298816032c97aa6382ce6b4226efc8401d1ef7e2d8731bbb658bb6c44acc86df5"
}
```
