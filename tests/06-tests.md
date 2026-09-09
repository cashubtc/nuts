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

## Signature message hash

The message hash is `tagged_hash("Cashu_MintInfo_v1", bytes)`, where `bytes` is the canonical UTF-8 JSON after removing only `signature`. The UTF-8 tag hashes to `916a34ebf6f2244d64490e8eb2b5e7af19cdc45aa6176160186fc6543aa20d9b`. Decode this hex value into the raw 32-byte `tag_hash`; the message hash is `SHA256(tag_hash || tag_hash || bytes)`.

## Minimal signed response with a challenge

Request:

```http
GET https://mint.host:3338/v1/info?challenge=000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
```

Response:

```json
{
  "pubkey": "0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da",
  "signature": "e22072aff2d70f9cb210ae5bb9a1d3fe44349cbde03fcd26a73e0c10e30bb3b801046db0b096d02f25c8cf76dd24ffd6c1906c3cbc98193c7d2d8d6978c95f0a",
  "challenge": "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
  "time": 1725304480
}
```

After removing only `signature`, the canonical UTF-8 JSON is the following single line, without a trailing newline:

```text
{"challenge":"000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f","pubkey":"0338596797cef0627f653cd6568387361b00314add55d9f1ea9c94f46ae421e3da","time":1725304480}
```

The tagged message hash signed by the mint is:

```text
374353ff76b340d0010379009839f8b29152808ec393409cfb79abf4b19e65bc
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
| Change the first signature byte from `0xe2` to `0xe3`            | Reject          | Invalid signature                                                     |
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

The complete response in the [NUT-06 example](../06.md#example) uses the same seed, challenge, timestamp, and auxiliary randomness. After removing only `signature` and canonicalizing the remaining object, the expected tagged message hash and signature are:

```json
{
  "message_hash": "3c08960dfc7c5f62e489271ed44cf82240b3fe48a13968179683461444855db6",
  "signature": "e91f667871ff922f7430aee729bc0252ff893ec2b05ef2b0f98376f7f5119b152029b363f89c35ffa2d8e3395c889c5caa2484c8b716cc18881dad7b6ef9a739"
}
```

## Untagged signatures (invalid)

The following signatures were made over plain `SHA256(bytes)` using the same identity key and auxiliary randomness. Substituting each signature into its corresponding response above **MUST** fail verification against the tagged message hash:

```json
{
  "minimal_with_challenge": "77cc645a451e744ef2d0d05ef09166cae27e9baf38afd5ab1301739d5444e144db224b0f29bfa0941ec3d228a74c50a5287bb6664333e4261d641f806bc4a672",
  "minimal_without_challenge": "446f52ec13fea5410092eb2d26c28cd9c56b141fa9feb3c60c3845766038905ba44480bc24b0e202278634d724c07560d9f8528ee64db016e48016cb03c409a0",
  "full_example": "6495ee5d693994f9a7e821e5baaf87791c50eb98bae9b2047bdb18cfbed4d92298816032c97aa6382ce6b4226efc8401d1ef7e2d8731bbb658bb6c44acc86df5"
}
```
