# NUT-00 Test Vectors

### Hash-to-curve function

The hash to curve function takes a message of any length and outputs a valid point on the secp256k1 curve. Note that unless you are using complex spend conditions ([NUT-10]), standardized secrets (random 32-bytes-long byte arrays) should be used in order to prevent wallet fingerprinting.

```shell
# Test 1 (hex encoded)
Message: 0000000000000000000000000000000000000000000000000000000000000000
Point:   024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725

# Test 2 (hex encoded)
Message: 0000000000000000000000000000000000000000000000000000000000000001
Point:   022e7158e11c9506f1aa4248bf531298daa7febd6194f003edcd9b93ade6253acf

# Test 3 (hex encoded)
# Note that this message will take a few iterations of the loop before finding a valid point
Message: 0000000000000000000000000000000000000000000000000000000000000002
Point:   026cdbe15362df59cd1dd3c9c11de8aedac2106eca69236ecd9fbe117af897be4f
```

### Blinded messages

These are test vectors for the blinded secret (public key) `B_` Alice sends to the mint Bob given a secret `x` and a random blinding factor `r`.

```shell
# Test 1
x:  d341ee4871f1f889041e63cf0d3823c713eea6aff01e80f1719f08f9e5be98f6   # hex encoded byte array
r:  99fce58439fc37412ab3468b73db0569322588f62fb3a49182d67e23d877824a   # hex encoded private key
B_: 033b1a9737a40cc3fd9b6af4b723632b76a67a36782596304612a6c2bfb5197e6d # hex encoded public key

# Test 2
x:  f1aaf16c2239746f369572c0784d9dd3d032d952c2d992175873fb58fae31a60   # hex encoded byte array
r:  f78476ea7cc9ade20f9e05e58a804cf19533f03ea805ece5fee88c8e2874ba50   # hex encoded private key
B_: 029bdf2d716ee366eddf599ba252786c1033f47e230248a4612a5670ab931f1763 # hex encoded public key
```

### Blinded signatures

These are test vectors for the blinded key `C_` given the mint's private key `k` and Alice's blinded message containing `B_`.

```shell
# Test 1
mint private key: 0000000000000000000000000000000000000000000000000000000000000001
B_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2
C_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2

# Test 2
mint private key: 7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f
B_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2
C_: 0398bc70ce8184d27ba89834d19f5199c84443c31131e48d3c1214db24247d005d
```

### BLS12-381 (v3) round-trip

Test vectors for `hash_to_curve_G1`, multiplicative blinding `B_ = r·Y`, blind signing `C_ = a·B_`, and unblinding `C = r⁻¹·C_`, for keysets with version byte `02` (see [Pairing-based BDHKE (BLS12-381)](../00.md#pairing-based-bls-blind-signatures)).

```shell
# Test 1
secret: "test_message"                                                                                                                                                                            # UTF-8 bytes
r: 0000000000000000000000000000000000000000000000000000000000000003 # scalar in Fr
a: 0000000000000000000000000000000000000000000000000000000000000002 # mint secret in Fr
Y: 860d58e5aeda1376185436ed96412313424cc079e056d1dab595e6db4c2c9685fec7da052c8db68d88985b75a42388ad # G1 compressed
K: aa4edef9c1ed7f729f520e47730a124fd70662a904ba1074728114d1031e1572c6c886f6b57ec72a6178288c47c335771638533957d540a9d2370f17cc7ed5863bc0b995b8825e0ee1ea1e1e4d00dbae81f14b0bf3611b78c952aacab827a053 # G2 compressed
B_: 8e88c5f6a93f653784a66b033a00e52128499e18b095c2a56f080d1c2a937ffc9ef4600804a48d087bbd1f662f6b068f # G1 compressed
C_: 8d52d7a6cbe5e99858d5c15c092d11a0c387c78917471211082a6e5afc2a79680dfa188fafe5d4a51c5398ce160e7a16 # G1 compressed
C: b7a4881059133fd91a8753600d9a5e524c65d6224f6fe2d5aef9e59f1507fdad90b3b4d48ee46da5c8dfaa0b88e28b69 # G1 compressed
```

`hash_to_curve_G1` uses the DST `CASHU_BLS12_381_G1_XMD:SHA-256_SSWU_RO_` (ASCII bytes, no trailing null). `Y = hash_to_curve_G1(secret)`, `K = a·g2`, and the pairing equality `e(C, g2) == e(Y, K)` holds.

### BLS12-381 (v3) batch verification

Test vector for the multi-pairing batch check with deterministic weight derivation (see [Batch Verification](../00.md#optional-batch-verification)). Two proofs signed under the same mint key `K = 2·g2`.

```shell
K: aa4edef9c1ed7f729f520e47730a124fd70662a904ba1074728114d1031e1572c6c886f6b57ec72a6178288c47c335771638533957d540a9d2370f17cc7ed5863bc0b995b8825e0ee1ea1e1e4d00dbae81f14b0bf3611b78c952aacab827a053

# Proof 1
secret_1: "batch_proof_1" # UTF-8 bytes
r_1: 0000000000000000000000000000000000000000000000000000000000000005
C_1: acebf797506a7031cef3189904715cb22792528f1ea0e6ab25341401d245539438ed97122f00e38ee6185cc20b09ba11 # G1 compressed

# Proof 2
secret_2: "batch_proof_2" # UTF-8 bytes
r_2: 0000000000000000000000000000000000000000000000000000000000000007
C_2: 9776497ad47a00f8a56233fb88f939b0572cf174a4c6d2446c0b1060434e305fae6845fd1f68b70376ba53ffe67f0414 # G1 compressed

# Derived
challenge: 539b5df396e82adab0760459590d38122d2552bc74f6bd860e915ff3b95e550a
weight_1:  0e7ff8be2ccb756d4ef390991bdd77eb65e8db624a2729fa1657c3cf8d7d4b55
weight_2:  6d026a181a6215b233e73b121d01908a1a1eb6911955bea5130bbf2f2966554d

verify: true
```

This vector intentionally exercises both code paths. `weight_1` accepts at `ctr = 4` and `weight_2` accepts at `ctr = 0`.

## Serialization of TokenV3

The following is a JSON-formatted v3 token and its serialized counterpart.

```json
{
  "token": [
    {
      "mint": "https://8333.space:3338",
      "proofs": [
        {
          "amount": 2,
          "id": "009a1f293253e41e",
          "secret": "407915bc212be61a77e3e6d2aeb4c727980bda51cd06a6afc29e2861768a7837",
          "C": "02bc9097997d81afb2cc7346b5e4345a9346bd2a506eb7958598a72f0cf85163ea"
        },
        {
          "amount": 8,
          "id": "009a1f293253e41e",
          "secret": "fe15109314e61d7756b0f8ee0f23a624acaa3f4e042f61433c728c7057b931be",
          "C": "029e8e5050b890a7d6c0968db16bc1d5d5fa040ea1de284f6ec69d61299f671059"
        }
      ]
    }
  ],
  "unit": "sat",
  "memo": "Thank you."
}
```

Serialized:

```
cashuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJhbW91bnQiOjIsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6IjQwNzkxNWJjMjEyYmU2MWE3N2UzZTZkMmFlYjRjNzI3OTgwYmRhNTFjZDA2YTZhZmMyOWUyODYxNzY4YTc4MzciLCJDIjoiMDJiYzkwOTc5OTdkODFhZmIyY2M3MzQ2YjVlNDM0NWE5MzQ2YmQyYTUwNmViNzk1ODU5OGE3MmYwY2Y4NTE2M2VhIn0seyJhbW91bnQiOjgsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6ImZlMTUxMDkzMTRlNjFkNzc1NmIwZjhlZTBmMjNhNjI0YWNhYTNmNGUwNDJmNjE0MzNjNzI4YzcwNTdiOTMxYmUiLCJDIjoiMDI5ZThlNTA1MGI4OTBhN2Q2YzA5NjhkYjE2YmMxZDVkNWZhMDQwZWExZGUyODRmNmVjNjlkNjEyOTlmNjcxMDU5In1dfV0sInVuaXQiOiJzYXQiLCJtZW1vIjoiVGhhbmsgeW91LiJ9
```

## Deserialization of TokenV3

The following are incorrectly formatted serialized v3 tokens.

```shell
# Incorrect prefix (casshuA)
casshuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJhbW91bnQiOjIsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6IjQwNzkxNWJjMjEyYmU2MWE3N2UzZTZkMmFlYjRjNzI3OTgwYmRhNTFjZDA2YTZhZmMyOWUyODYxNzY4YTc4MzciLCJDIjoiMDJiYzkwOTc5OTdkODFhZmIyY2M3MzQ2YjVlNDM0NWE5MzQ2YmQyYTUwNmViNzk1ODU5OGE3MmYwY2Y4NTE2M2VhIn0seyJhbW91bnQiOjgsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6ImZlMTUxMDkzMTRlNjFkNzc1NmIwZjhlZTBmMjNhNjI0YWNhYTNmNGUwNDJmNjE0MzNjNzI4YzcwNTdiOTMxYmUiLCJDIjoiMDI5ZThlNTA1MGI4OTBhN2Q2YzA5NjhkYjE2YmMxZDVkNWZhMDQwZWExZGUyODRmNmVjNjlkNjEyOTlmNjcxMDU5In1dfV0sInVuaXQiOiJzYXQiLCJtZW1vIjoiVGhhbmsgeW91LiJ9

# No prefix
eyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJhbW91bnQiOjIsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6IjQwNzkxNWJjMjEyYmU2MWE3N2UzZTZkMmFlYjRjNzI3OTgwYmRhNTFjZDA2YTZhZmMyOWUyODYxNzY4YTc4MzciLCJDIjoiMDJiYzkwOTc5OTdkODFhZmIyY2M3MzQ2YjVlNDM0NWE5MzQ2YmQyYTUwNmViNzk1ODU5OGE3MmYwY2Y4NTE2M2VhIn0seyJhbW91bnQiOjgsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6ImZlMTUxMDkzMTRlNjFkNzc1NmIwZjhlZTBmMjNhNjI0YWNhYTNmNGUwNDJmNjE0MzNjNzI4YzcwNTdiOTMxYmUiLCJDIjoiMDI5ZThlNTA1MGI4OTBhN2Q2YzA5NjhkYjE2YmMxZDVkNWZhMDQwZWExZGUyODRmNmVjNjlkNjEyOTlmNjcxMDU5In1dfV0sInVuaXQiOiJzYXQiLCJtZW1vIjoiVGhhbmsgeW91LiJ9
```

The following is a correctly serialized v3 token.

```shell
cashuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJhbW91bnQiOjIsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6IjQwNzkxNWJjMjEyYmU2MWE3N2UzZTZkMmFlYjRjNzI3OTgwYmRhNTFjZDA2YTZhZmMyOWUyODYxNzY4YTc4MzciLCJDIjoiMDJiYzkwOTc5OTdkODFhZmIyY2M3MzQ2YjVlNDM0NWE5MzQ2YmQyYTUwNmViNzk1ODU5OGE3MmYwY2Y4NTE2M2VhIn0seyJhbW91bnQiOjgsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6ImZlMTUxMDkzMTRlNjFkNzc1NmIwZjhlZTBmMjNhNjI0YWNhYTNmNGUwNDJmNjE0MzNjNzI4YzcwNTdiOTMxYmUiLCJDIjoiMDI5ZThlNTA1MGI4OTBhN2Q2YzA5NjhkYjE2YmMxZDVkNWZhMDQwZWExZGUyODRmNmVjNjlkNjEyOTlmNjcxMDU5In1dfV0sInVuaXQiOiJzYXQiLCJtZW1vIjoiVGhhbmsgeW91LiJ9
```

Both of the following v3 tokens are valid, one includes padding characters at the end and the other does not.

```shell
# Clients should be able to deserialize both
cashuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJhbW91bnQiOjIsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6IjQwNzkxNWJjMjEyYmU2MWE3N2UzZTZkMmFlYjRjNzI3OTgwYmRhNTFjZDA2YTZhZmMyOWUyODYxNzY4YTc4MzciLCJDIjoiMDJiYzkwOTc5OTdkODFhZmIyY2M3MzQ2YjVlNDM0NWE5MzQ2YmQyYTUwNmViNzk1ODU5OGE3MmYwY2Y4NTE2M2VhIn0seyJhbW91bnQiOjgsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6ImZlMTUxMDkzMTRlNjFkNzc1NmIwZjhlZTBmMjNhNjI0YWNhYTNmNGUwNDJmNjE0MzNjNzI4YzcwNTdiOTMxYmUiLCJDIjoiMDI5ZThlNTA1MGI4OTBhN2Q2YzA5NjhkYjE2YmMxZDVkNWZhMDQwZWExZGUyODRmNmVjNjlkNjEyOTlmNjcxMDU5In1dfV0sInVuaXQiOiJzYXQiLCJtZW1vIjoiVGhhbmsgeW91IHZlcnkgbXVjaC4ifQ==
cashuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJhbW91bnQiOjIsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6IjQwNzkxNWJjMjEyYmU2MWE3N2UzZTZkMmFlYjRjNzI3OTgwYmRhNTFjZDA2YTZhZmMyOWUyODYxNzY4YTc4MzciLCJDIjoiMDJiYzkwOTc5OTdkODFhZmIyY2M3MzQ2YjVlNDM0NWE5MzQ2YmQyYTUwNmViNzk1ODU5OGE3MmYwY2Y4NTE2M2VhIn0seyJhbW91bnQiOjgsImlkIjoiMDA5YTFmMjkzMjUzZTQxZSIsInNlY3JldCI6ImZlMTUxMDkzMTRlNjFkNzc1NmIwZjhlZTBmMjNhNjI0YWNhYTNmNGUwNDJmNjE0MzNjNzI4YzcwNTdiOTMxYmUiLCJDIjoiMDI5ZThlNTA1MGI4OTBhN2Q2YzA5NjhkYjE2YmMxZDVkNWZhMDQwZWExZGUyODRmNmVjNjlkNjEyOTlmNjcxMDU5In1dfV0sInVuaXQiOiJzYXQiLCJtZW1vIjoiVGhhbmsgeW91IHZlcnkgbXVjaC4ifQ
```

## Serialization of TokenV4

The following are JSON-formatted v4 tokens and their serialized counterparts. The `h''` values are `bytes` but displayed as hex strings here.

### Single keyset

Token from a single keyset and including a memo.

```json
{
    "t": [
        {
            "i": h'00ad268c4d1f5826',
            "p": [
                {
                    "a": 1,
                    "s": "9a6dbb847bd232ba76db0df197216b29d3b8cc14553cd27827fc1cc942fedb4e",
                    "c": h'038618543ffb6b8695df4ad4babcde92a34a96bdcd97dcee0d7ccf98d472126792',
                },
            ],
        },
    ],
    "d": "Thank you",
    "m": "http://localhost:3338",
    "u": "sat",
}
```

Serialized:

```
cashuBpGF0gaJhaUgArSaMTR9YJmFwgaNhYQFhc3hAOWE2ZGJiODQ3YmQyMzJiYTc2ZGIwZGYxOTcyMTZiMjlkM2I4Y2MxNDU1M2NkMjc4MjdmYzFjYzk0MmZlZGI0ZWFjWCEDhhhUP_trhpXfStS6vN6So0qWvc2X3O4NfM-Y1HISZ5JhZGlUaGFuayB5b3VhbXVodHRwOi8vbG9jYWxob3N0OjMzMzhhdWNzYXQ=
```

### Multiple keysets

The token below includes proofs from two different keysets.

```json
{
    "t": [
        {
            "i": h'00ffd48b8f5ecf80',
            "p": [
                {
                    "a": 1,
                    "s": "acc12435e7b8484c3cf1850149218af90f716a52bf4a5ed347e48ecc13f77388",
                    "c": h'0244538319de485d55bed3b29a642bee5879375ab9e7a620e11e48ba482421f3cf',
                },
            ],
        },
        {
            "i": h'00ad268c4d1f5826',
            "p": [
                {
                    "a": 2,
                    "s": "1323d3d4707a58ad2e23ada4e9f1f49f5a5b4ac7b708eb0d61f738f48307e8ee",
                    "c": h'023456aa110d84b4ac747aebd82c3b005aca50bf457ebd5737a4414fac3ae7d94d',
                },
                {
                    "a": 1,
                    "s": "56bcbcbb7cc6406b3fa5d57d2174f4eff8b4402b176926d3a57d3c3dcbb59d57",
                    "c": h'0273129c5719e599379a974a626363c333c56cafc0e6d01abe46d5808280789c63',
                },
            ],
        },
    ],
    "m": "http://localhost:3338",
    "u": "sat",
}
```

Serialized:

```
cashuBo2F0gqJhaUgA_9SLj17PgGFwgaNhYQFhc3hAYWNjMTI0MzVlN2I4NDg0YzNjZjE4NTAxNDkyMThhZjkwZjcxNmE1MmJmNGE1ZWQzNDdlNDhlY2MxM2Y3NzM4OGFjWCECRFODGd5IXVW-07KaZCvuWHk3WrnnpiDhHki6SCQh88-iYWlIAK0mjE0fWCZhcIKjYWECYXN4QDEzMjNkM2Q0NzA3YTU4YWQyZTIzYWRhNGU5ZjFmNDlmNWE1YjRhYzdiNzA4ZWIwZDYxZjczOGY0ODMwN2U4ZWVhY1ghAjRWqhENhLSsdHrr2Cw7AFrKUL9Ffr1XN6RBT6w659lNo2FhAWFzeEA1NmJjYmNiYjdjYzY0MDZiM2ZhNWQ1N2QyMTc0ZjRlZmY4YjQ0MDJiMTc2OTI2ZDNhNTdkM2MzZGNiYjU5ZDU3YWNYIQJzEpxXGeWZN5qXSmJjY8MzxWyvwObQGr5G1YCCgHicY2FtdWh0dHA6Ly9sb2NhbGhvc3Q6MzMzOGF1Y3NhdA
```

## Raw Token Serialization

### TokenV4

What follows is a TokenV4 Token serialized in its raw binary form. `h''` values are bytes in hex notation.

Token:

```json
{
    "t": [
        {
            "i": h'00ad268c4d1f5826',
            "p": [
                {
                    "a": 1,
                    "s": "9a6dbb847bd232ba76db0df197216b29d3b8cc14553cd27827fc1cc942fedb4e",
                    "c": h'038618543ffb6b8695df4ad4babcde92a34a96bdcd97dcee0d7ccf98d472126792',
                },
            ],
        },
    ],
    "d": "Thank you",
    "m": "http://localhost:3338",
    "u": "sat",
}
```

Serialized to raw binary:

`h'6372617742a4617481a261694800ad268c4d1f5826617081a3616101617378403961366462623834376264323332626137366462306466313937323136623239643362386363313435353363643237383237666331636339343266656462346561635821038618543ffb6b8695df4ad4babcde92a34a96bdcd97dcee0d7ccf98d4721267926164695468616e6b20796f75616d75687474703a2f2f6c6f63616c686f73743a33333338617563736174'`

[NUT-10]: ../10.md

## V4 tokens with spend info

One 8-sat proof per token, mint `https://mint.test`, unit `sat`, keyset id `022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701`. Each shape's `C` is its own proof's signature.

Tokens use the short keyset id form. Each shape decodes to the stated `spend_info` fields and re-encodes to the same string.

Bearer (`si.k`, secret is the bare key of `k`):

```json
{
  "secret": "0240c186f3e19f6f8cd00db81c5266d5c74ddca48ff848efd0e3e125b2846f30d9",
  "C": "a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b6",
  "spend_info": {
    "k": "930c88ad9dc8531c147862d4ef9c0981200ff1f510c0a9e1c024db725a1d56c6"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAIlRqsKLe6fYXCBpGFhCGFzeEIwMjQwYzE4NmYzZTE5ZjZmOGNkMDBkYjgxYzUyNjZkNWM3NGRkY2E0OGZmODQ4ZWZkMGUzZTEyNWIyODQ2ZjMwZDlhY1gwoz3U3ibqlQBgrlxFvcQI1yqvUbqfTM3u5KBA3wZ8qHx5mkBv7IjCoyi3WykOJ_e2YnNpoWFrWCCTDIitnchTHBR4YtTvnAmBIA_x9RDAqeHAJNtyWh1Wxg"
}
```

Receiver-keyed, no conditions (`si.e` only):

```json
{
  "secret": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "C": "8ebb4624404a3ea52ae2eed274c2997ad6c698505cacf2011e521c915c59690981c36c1a2cb8453e37de7d4ce58b2336",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAIlRqsKLe6fYXCBpGFhCGFzeEIwM2EzZTEyY2MwNzdlNTYwNWYzNjQ0MTA0NmY1MGMxMTRmY2M4ODNiMDc5YTM0MDI4YmVkNjY3MzJlM2E0MTllNTFhY1gwjrtGJEBKPqUq4u7SdMKZetbGmFBcrPIBHlIckVxZaQmBw2waLLhFPjfefUzliyM2YnNpoWFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-Q"
}
```

Receiver-keyed with a disclosed tree (`si.e` + `si.t`; the receiver derives `K` from `E`):

```json
{
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "C": "84da102b0f13957bbea4a92665c31bff64a8c7a5c00867c3f54dae1579ad7c641ba87c35de54db0868934a0b966e3d4c",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAIlRqsKLe6fYXCBpGFhCGFzeEIwMmQzMTBhNGQ2NjFlMzE1OGU3ZDM2MDYxN2U3MzlkNmJhY2JmMDE1NDMxYjI0YTQzMTY4ZGIwYWI5OWVmOGY4MjhhY1gwhNoQKw8TlXu-pKkmZcMb_2Sox6XACGfD9U2uFXmtfGQbqHw13lTbCGiTSguWbj1MYnNpomFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-RhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

A disclosed tree with an explicit internal key (`si.i` + `si.t`; no key handed over, the third-party-signer shape):

```json
{
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "C": "84da102b0f13957bbea4a92665c31bff64a8c7a5c00867c3f54dae1579ad7c641ba87c35de54db0868934a0b966e3d4c",
  "spend_info": {
    "K": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAIlRqsKLe6fYXCBpGFhCGFzeEIwMmQzMTBhNGQ2NjFlMzE1OGU3ZDM2MDYxN2U3MzlkNmJhY2JmMDE1NDMxYjI0YTQzMTY4ZGIwYWI5OWVmOGY4MjhhY1gwhNoQKw8TlXu-pKkmZcMb_2Sox6XACGfD9U2uFXmtfGQbqHw13lTbCGiTSguWbj1MYnNpomFpWCEDo-EswHflYF82RBBG9QwRT8yIOweaNAKL7WZzLjpBnlFhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

Script-only (`si.i` + `si.u` + `si.t`). `u` is fixed for a stable vector; a real send uses a fresh one per proof.

```json
{
  "secret": "035f02db4e3b429de04669e8fba1e786719de8336cedeff3048e944ebcfaf08e23",
  "C": "96a00e75fb006e1ebbeae860e0a0953c9da1aef46ba4616611c99191a31a96edf2a809cf365de4a4febc26413cb914cf",
  "spend_info": {
    "K": "031ed5e2846820073c39cca136f69aa3509b88b8f7f0e9f30159dea1178fa725f5",
    "u": "c4b697b346799e55a80ba7a0b6f7670a7f62a985c97de685dc693e87dc6d137a",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAIlRqsKLe6fYXCBpGFhCGFzeEIwMzVmMDJkYjRlM2I0MjlkZTA0NjY5ZThmYmExZTc4NjcxOWRlODMzNmNlZGVmZjMwNDhlOTQ0ZWJjZmFmMDhlMjNhY1gwlqAOdfsAbh676uhg4KCVPJ2hrvRrpGFmEcmRkaMalu3yqAnPNl3kpP68JkE8uRTPYnNpo2FpWCEDHtXihGggBzw5zKE29pqjUJuIuPfw6fMBWd6hF4-nJfVhdVggxLaXs0Z5nlWoC6egtvdnCn9iqYXJfeaF3Gk-h9xtE3phdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

## Transaction transcripts

`input_digest` is [`tagged_hash`](../00.md#tagged-hashes) under `Cashu_TransactionInput`, with `SHA256("Cashu_TransactionInput")` = `4996fee585f625e6a33865ce975efc32c42d2b1b95328385ce45f5209a16e9ec`. Signatures use BIP-340 with auxiliary randomness fixed to 32 zero bytes; verifiers **MUST** accept any valid signature. Keyset `022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701`, [NUT-02](02-tests.md#version-3) V3 vector 1, whose mint scalars are `7`, `13`, `29` and `71` for amounts `1`, `2`, `4` and `8`. Proofs use [NUT-13 V3](13-tests.md) counter `0`, and `1` in the multi-input vector. `digest` is the transaction digest. A blinded output's container carries `SHA256(B_)`, so a request shows `B_` where its transcript shows the hash.

**Swap.** A `PostSwapRequest` ([NUT-03](../03.md)) spending one 8-sat proof into two 4-sat outputs:

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "secret": "0240c186f3e19f6f8cd00db81c5266d5c74ddca48ff848efd0e3e125b2846f30d9",
      "C": "a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b6"
    }
  ],
  "outputs": [
    {
      "amount": 4,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    },
    {
      "amount": 4,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "B_": "a14669f181e074cc466e2a165c47ab7db5b3939e42b349f1201874033943ef279f36476e627ab1c937e8ea6a76448fc2"
    }
  ]
}
```

serializes to the following transcript and digest:

```json
{
  "transcript": "11008e01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d70103003090f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8040030a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b621004b01000104020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b01000104020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d7010300200081a8744c8f3309419a09b08f3ae7e8cdaaaaad64309b78f6fd91f61dfaf502",
  "digest": "e88d16feadb0abc0cf4a08a7f5929a3a7c5e595f8d4e659d9ba66086aead402e",
  "input_id": "194bd20817e5806bbe198206e63938c8f0ad38a0d89af2179bb517e24caf1db2",
  "input_digest": "88a664e4f25fbd76baf5846221aa8f9d95beb0341f67d5458332e4f6809abcde"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "3c2ce5dc36aea01a9b9f44287ef12e67a7fb0e0113720c3a000b5942835426e6635b09c087dbd30bde77ddf03b43b87858b3d2bf29d4b3ca7895f73e4839d3c2"
  ]
}
```

**Multiple proof inputs.** The swap above plus a second proof (the [NUT-13 V3](13-tests.md) counter `1` secret), with outputs of `8` and `4`:

```json
{
  "amount": 4,
  "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
  "secret": "0385fe6eb0608c6b5241e0fd86ebbd5dd30a6a97a0014a110c0c6297001147e5be",
  "C": "84c2b06e690cf434f38bca886cfe2ca2d8739231f14b350d907bd4dd62ef901c0c99453d30651d43727cdbb2f07fd1b3"
}
```

The transaction and per-input digests, with each proof's key-path signature:

```json
{
  "digest": "9430a89c2db9df2a8c645369ea6f8ca1100f21b3c365ac0bb153422d2fd7e483",
  "inputs": [
    {
      "input_id": "194bd20817e5806bbe198206e63938c8f0ad38a0d89af2179bb517e24caf1db2",
      "input_digest": "56a8a7ea8c0e785f2c4b77b99648daca04f7e110dac4c86b2d6372a34ce9393e",
      "signature": "d390c4ad38c949c3dceb1d6a75de4bbb68291e2a72a4abef26ea3a0d373a24840572aef6d4359f8baea1ae2ed62336c8d833e91aaf3e78f32c7cf9c0581c3552"
    },
    {
      "input_id": "810d7cc016b5e6af4dff55b4c96ee7ed397c5e845058abf04ecd479edc50b69a",
      "input_digest": "681a5a9f1881a685e5e8fb0d33dabd7c8987bf78a1e9424bb4535d124dfe6877",
      "signature": "f608bb156579e85c5788de9e7d89e10a0aeb39ba6983bc352583406cd8eab1743cdb1eb0b7fb31f2679a2f0c4138b72cfbc92888d409af26c4109016a378a74a"
    }
  ]
}
```

Each signature **MUST** verify only against its corresponding `input_digest`; neither signs the shared `digest`.

**Mixed keysets.** The swap's v3 input joined by a pre-v3 input on keyset `00456a94ab4e1c46` (a v0 id), paying two outputs of `8` and `2` on the v3 keyset:

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "secret": "0240c186f3e19f6f8cd00db81c5266d5c74ddca48ff848efd0e3e125b2846f30d9",
      "C": "a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b6"
    },
    {
      "amount": 2,
      "id": "00456a94ab4e1c46",
      "secret": "d341ee4871f1f889041e63cf0d3823c713eea6aff01e80f1719f08f9e5be98f6",
      "C": "02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2"
    }
  ],
  "outputs": [
    {
      "amount": 8,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    },
    {
      "amount": 2,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "B_": "a14669f181e074cc466e2a165c47ab7db5b3939e42b349f1201874033943ef279f36476e627ab1c937e8ea6a76448fc2"
    }
  ]
}
```

Each input's `Y` and container record, then the transcript and digests. Only the v3 input signs an input digest; the pre-v3 input's `input_id` is listed only to check the container bytes:

```json
{
  "inputs": [
    {
      "Y": "90f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8",
      "container": "11008e01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d70103003090f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8040030a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b6",
      "input_id": "194bd20817e5806bbe198206e63938c8f0ad38a0d89af2179bb517e24caf1db2",
      "input_digest": "94a0d329d7c66c55e0c968bbb680fbb4c7f4d01f6a29f93d6a5975dd15812776",
      "signature": "d5e861c7ee7635fa2b8dc58aabe2ceb0997651a6e1e85cc3aed31aad42871f4d2444707ad20337a21da5f35e561ca83ec36880ecb2fd8c25eccf33856b99ca93"
    },
    {
      "Y": "029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae",
      "container": "1100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2",
      "input_id": "efbdd5d14874cb021fc962d93a9848553ca65ae101e9b57f6678aa37ffe1ebd9"
    }
  ],
  "transcript": "11008e01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d70103003090f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8040030a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b61100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba221004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b01000102020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d7010300200081a8744c8f3309419a09b08f3ae7e8cdaaaaad64309b78f6fd91f61dfaf502",
  "digest": "c08be9ca9632ce753c31227e470ecb38ff19df071fd828d1818eb14ea4da489f"
}
```

**Mint.** Mint quote `quote-mint-0001` (amount 8, none issued) with one 8-sat output, locked to the [NUT-13 quote lock key](13-tests.md#version-3-secret-derivation) of counter `0` (`0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812`):

```json
{
  "outputs": [
    {
      "amount": 8,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

```json
{
  "transcript": "12003d0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000021004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "37e64e944b7580653f44cfa06b416fac9a548d5bbf372e6545c9c982e5a3a70f",
  "input_id": "d294012dd54976b05eb3e36eb218b9a6d66b19d79ec122944a35b99b8ddd8839",
  "input_digest": "b8218d99fe1d3138c16230ed0b119a8ea8a17975131fedd9b7459f2af9aa483a"
}
```

**Partial mint.** Issuing 4 against 8-sat mint quote `quote-mint-0004` with 3 already issued, with one 4-sat output:

```
12 003e | 01 0001 04 | 02 000f 71756f...303034 | 03 0021 029290...209812 | 04 0001 03
```

```json
{
  "transcript": "12003e0100010402000f71756f74652d6d696e742d303030340300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d2098120400010321004b01000104020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "90d943e1f02938e5d50a7ead9f04ec1a633bc207bf7976f54569632db62d8d4d",
  "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
  "input_id": "c2e4168d079d7ccc6c9fc80c480e75a255282ec41e660afad42cf743c95f14e3",
  "input_digest": "7754960e452ae522213f1112c6eb5946b0bac278b0a307e38927d59531ed558e",
  "signature": "c6709751b0d3c14fef333326f4cd9d45c7af327ea4659a7b4637e92d9a82b0f6c25a4bce9e99385f40f39ea6fe26af9ba07bfaf2c378f2f47a1eb2d474a0a7a6"
}
```

The signature **MUST NOT** verify over a transcript that commits amount `8` or `issued` `0`. The mint's blind signature on the output:

```json
{
  "signatures": [
    {
      "amount": 4,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "C_": "98a471f36a34323f96a1b5783bd98829f9fc69687a9c4f6774c23d89b8f0f2c93e8510992c7942e1980746138c90ae26"
    }
  ]
}
```

**Serialized quote witnesses.** A mint request's `signature` also accepts a serialized [witness](../00.md#witnesses). The partial mint's signature as a key-path witness:

```json
{
  "signature": "{\"signatures\":[\"c6709751b0d3c14fef333326f4cd9d45c7af327ea4659a7b4637e92d9a82b0f6c25a4bce9e99385f40f39ea6fe26af9ba07bfaf2c378f2f47a1eb2d474a0a7a6\"]}"
}
```

The mint vector with its quote locked to a script-only key, spent by a script-path witness:

```json
{
  "lock_pubkey": "034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af276",
  "transcript": "12003d0100010802000f71756f74652d6d696e742d30303031030021034b15129a9c665f37fbe9f6c80a7fe6ec0c809f34edde98d298aff94a1e8af27604000021004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "33d8def7c0f5235c150863773e105568d44d079aa2f1d59149bb72254dc6df05",
  "input_id": "a639745001afaad8964370e8ddc1406bbf14d478c6d56819f188c9b10392fe45",
  "input_digest": "7c0b3967b3b7ba4e5daa7e8ea11607cff36062d6ff24863c8bdf31ee8346f8e4",
  "signature": "{\"leaf\":\"00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9\",\"control\":{\"K\":\"028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407\",\"path\":[]},\"signatures\":[\"b0656dbde143bd6825e141551cae68f1428a62ee1d74c0f8df8f735d5841471d6f20f3946658bdad225b6b30dc90cea956a0aede132edf6eb1415f95afb30ca2\"]}"
}
```

**Batched mint.** A [NUT-29](../29.md) batch of `quote-mint-0002` and `quote-mint-0003` with `quote_amounts` of `[5, 3]` and the mint vector's 8-sat output:

```
12 003d | 01 0001 05 | 02 000f 71756f...303032 | 03 0021 029290...209812 | 04 0000
12 003d | 01 0001 03 | 02 000f 71756f...303033 | 03 0021 02b357...99615d | 04 0000
```

```json
{
  "transcript": "12003d0100010502000f71756f74652d6d696e742d303030320300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000012003d0100010302000f71756f74652d6d696e742d3030303303002102b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d04000021004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "8203006b339dd16a3f6293c0f300bebb3c9ad620755477b1372c0fa479540c72",
  "inputs": [
    {
      "quote_id": "quote-mint-0002",
      "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
      "input_id": "8c7f916779dfba1b7ea2e0d3e69d1ee7eed1895af2891406fe8bdb7fbe0f39aa",
      "input_digest": "5b87defd8dadbd2b0faf359f53b00a74b0642e5b91dd4046e0183738a812ed13",
      "signature": "badda23b373f0d1da963af4d424dbbbccce933ba0c81bc3e2c8ade13decdad8df57ca75efcb4eaa2e02eee9bd43066fce76fee22599f4a513354c138efa6bfb6"
    },
    {
      "quote_id": "quote-mint-0003",
      "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
      "input_id": "f7a60306c44e910fd5dea355541c4a4bb251220690688279bf08e7d19b3e9e45",
      "input_digest": "ac0d58749a343394a0fe5605771be16466ece1ecb331fa1aae0c92ac00136c13",
      "signature": "f272dca3c46470511b4ac1ab47a2135d1c7a6af4b6b49ec7c1d120f7704888cce5af8f2026c548a2d5201aebe384f2b798a2c1e439c89d9decc915bc890a4474"
    }
  ]
}
```

**Melt.** Paying melt quote `quote-melt-0001` (amount 8, fee reserve 0, no change outputs) with the swap's 8-sat proof:

```json
{
  "transcript": "11008e01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d70103003090f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8040030a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b62200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "f2fd9eaf27d572e47d776bd09856f760b3bb18338a9b497bee18b5ebec804048",
  "input_id": "194bd20817e5806bbe198206e63938c8f0ad38a0d89af2179bb517e24caf1db2",
  "input_digest": "e5bde063cdeb9187aafc8e521a63c3463188836ff8e1c6575e60c5a045f620b6"
}
```

The melt shares the swap's `input_id` but not its `input_digest`, so neither witness verifies in the other transaction.

**Melt with change.** Paying melt quote `quote-melt-0002` (amount 5, fee reserve 3) with the swap's 8-sat proof and two [NUT-08](../08.md) blank outputs (amount 0) carrying the swap's two `B_`. The melt quote output commits `8`, the amount plus the fee reserve. The blank outputs precede the melt quote in the transcript, and each zero amount encodes as `010000`:

```json
{
  "transcript": "11008e01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d70103003090f53b3088936b80ecfcc065a0746c5c1843ffd4527dbe3b9aba5a6109aed338ddc0f109511e9dfd37342aa99dd816d8040030a33dd4de26ea950060ae5c45bdc408d72aaf51ba9f4ccdeee4a040df067ca87c799a406fec88c2a328b75b290e27f7b621004a010000020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004a010000020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d7010300200081a8744c8f3309419a09b08f3ae7e8cdaaaaad64309b78f6fd91f61dfaf5022200160100010802000f71756f74652d6d656c742d30303032",
  "digest": "6649c7b016115b0d7f94fecef9af59ed616a32bb3e9f0313222427d29d087b80",
  "input_id": "194bd20817e5806bbe198206e63938c8f0ad38a0d89af2179bb517e24caf1db2",
  "input_digest": "b30a18aa22aabb380329dbf7e2c7915662b26a6f4b901f8799b068fb4ec2fc2f"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "8129d244fa8d370a70c511f934788f2327f35739b8a60dac4545f190882a72774a947323ef6399d3e5e16e8687810549c19dcaab054f700caf05cbcd2e9c457b"
  ]
}
```

The payment costs no fee, so the mint returns the 3-sat reserve as change on the blank outputs, in order:

```json
{
  "change": [
    {
      "amount": 1,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "C_": "b8323ba04c279ce45cfd572020ceedd2925f5112769fdc97f8669f9b0e9080d78cc28c1846d59157f8fa6e329c90ad3d"
    },
    {
      "amount": 2,
      "id": "022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701",
      "C_": "a5845c6eff7c6eb2a1b17e7579ed880c1b335e137f1527c143b82c7e606f366bee79d7f9937799fb9941f1e9a060c752"
    }
  ]
}
```
