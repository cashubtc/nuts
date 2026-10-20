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

These are test vectors for the the blinded secret (public key) `B_` Alice sends to the mint Bob given a secret `x` and a random blinding factor `r`.

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

The following are JSON-formatted v3 tokens and their serialized counterparts.

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

Encoded:

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

One 8-sat proof per token, mint `https://mint.test`, unit `sat`, keyset id `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6`, `C` = `84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327`.

Tokens use the short keyset id form. Each shape decodes to the stated `spend_info` fields and re-encodes to the same string.

Bearer (`si.k`, secret is the bare key of `k`):

```json
{
  "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
  "spend_info": {
    "k": "47196dc081150ce13fd0e478b8b71831b825be389211c9c56a8062a61af70347"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmU2ZTdjZmE3YjgyZDRiM2I0NDlmYTY0NjZjODkzNDY5YTcyN2QwMjE0ZDQ4ZGI0OTU2YTYwNTRiODAyMmEyOWJhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFrWCBHGW3AgRUM4T_Q5Hi4txgxuCW-OJIRycVqgGKmGvcDRw"
}
```

Receiver-keyed, no conditions (`si.e` only):

```json
{
  "secret": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4"
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwM2EzZTEyY2MwNzdlNTYwNWYzNjQ0MTA0NmY1MGMxMTRmY2M4ODNiMDc5YTM0MDI4YmVkNjY3MzJlM2E0MTllNTFhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpoWFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-Q"
}
```

Receiver-keyed with a disclosed tree (`si.e` + `si.t`; the receiver derives `K` from `E`):

```json
{
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "spend_info": {
    "E": "022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmQzMTBhNGQ2NjFlMzE1OGU3ZDM2MDYxN2U3MzlkNmJhY2JmMDE1NDMxYjI0YTQzMTY4ZGIwYWI5OWVmOGY4MjhhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpomFlWCECL4veTRoHIJNVtKclClxRKOiLhL3cYZq3y6jVabJA7-RhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

A disclosed tree with an explicit internal key (`si.i` + `si.t`; no key handed over, the third-party-signer shape):

```json
{
  "secret": "02d310a4d661e3158e7d360617e739d6bacbf015431b24a43168db0ab99ef8f828",
  "spend_info": {
    "K": "03a3e12cc077e5605f36441046f50c114fcc883b079a34028bed66732e3a419e51",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMmQzMTBhNGQ2NjFlMzE1OGU3ZDM2MDYxN2U3MzlkNmJhY2JmMDE1NDMxYjI0YTQzMTY4ZGIwYWI5OWVmOGY4MjhhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpomFpWCEDo-EswHflYF82RBBG9QwRT8yIOweaNAKL7WZzLjpBnlFhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

Script-only (`si.i` + `si.u` + `si.t`). `u` is fixed for a stable vector; a real send uses a fresh one per proof.

```json
{
  "secret": "0251a4f35fa38c5edce83e16596de02be4e87ec6a91c5fd80ab577c22668fb6dd5",
  "spend_info": {
    "K": "0308ca9ef021bf7ec241dbef7fa31aec8e63b41be200eb7530cd3d67d2a2c7d096",
    "u": "4af68649f3230c5589879f0cf33fd6d9f007cd3a54a2e6ed8699a576630fc025",
    "tree": [
      "00020200010104002102e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd1306000468a3be80"
    ]
  },
  "token": "cashuBo2FtcWh0dHBzOi8vbWludC50ZXN0YXVjc2F0YXSBomFpSAK34HfQIPq-YXCBpGFhCGFzeEIwMjUxYTRmMzVmYTM4YzVlZGNlODNlMTY1OTZkZTAyYmU0ZTg3ZWM2YTkxYzVmZDgwYWI1NzdjMjI2NjhmYjZkZDVhY1gwhNG3KRrlc388hRqjPK_g96_rXMtNoIbEgruFt1JeYVR_G1ptGgGx_tH5YNGp0DMnYnNpo2FpWCEDCMqe8CG_fsJB2-9_oxrsjmO0G-IA63UwzT1n0qLH0JZhdVggSvaGSfMjDFWJh58M8z_W2fAHzTpUoubthpmldmMPwCVhdIFYMQACAgABAQQAIQLkk9vxwQ2A81geSQSTCxQEzGwTkA7gdYR0-pSr6MTNEwYABGijvoA"
}
```

## Transaction transcripts

`input_digest` is [`tagged_hash`](../00.md#tagged-hashes) under `Cashu_TransactionInput`, with `SHA256("Cashu_TransactionInput")` = `4996fee585f625e6a33865ce975efc32c42d2b1b95328385ce45f5209a16e9ec`. Signatures use BIP-340 with auxiliary randomness fixed to 32 zero bytes; verifiers **MUST** accept any valid signature. Keyset `02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6` (v3). Proofs use [NUT-13 V3](13-tests.md) counter `0`, and `1` in the multi-input vector. `digest` is the transaction digest. A blinded output's container carries `SHA256(B_)`, so a request shows `B_` where its transcript shows the hash.

**Swap.** A `PostSwapRequest` ([NUT-03](../03.md)) spending one 8-sat proof into two 4-sat outputs:

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
      "C": "84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327"
    }
  ],
  "outputs": [
    {
      "amount": 4,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    },
    {
      "amount": 4,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

serializes to the following transcript and digest:

```json
{
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "b5a50082d44bdb0d9f9e91896fbe0f8f9052baf0ca7c8930c8987790164f277c",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "eca67b680015d42ffb9339b8c0475a90d162d189bd36a15d8b6910de48927edd"
}
```

and the input's key-path witness over its `input_digest` is:

```json
{
  "signatures": [
    "5b4b2cbdb5ea75dd2a6451bf2f348e8b837438375dd5e78ba5cb2f3c549258df8ff274e8de9987e7dab88c221f0de820546e42907cec816e2b290af814030a94"
  ]
}
```

**Multiple proof inputs.** The swap above plus a second proof (the [NUT-13 V3](13-tests.md) counter `1` secret, same `C`), with outputs of `8` and `4`:

```json
{
  "amount": 4,
  "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
  "secret": "03a882e17eb79f4f87313b299e208f9109734d0211a8df307b1570dbad2cdf74bf",
  "C": "84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327"
}
```

The transaction and per-input digests, with each proof's key-path signature:

```json
{
  "digest": "638facdb740dcd6909c5934208a421dafa1b3756aa5fc4a0e5d1bd341f28fbc6",
  "inputs": [
    {
      "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
      "input_digest": "d8fcb88ff0252fc13519cf28a23e7b65278db09a4d8c1e82b27f692ea53bb5a7",
      "signature": "11f5af9cf93204f816b4328f47de2b6368eaa26d584c4a5f0eca9268ed94aa39093faad5e6d4fce3674851e3c506cd0af35c0a58f913d7853e51b80e39976499"
    },
    {
      "input_id": "0182252f564bf76e42e45514955b50c6bd6381b6c4971c8027cd5a6a90817c4b",
      "input_digest": "28e4afd844e0fb8a3c3e71fdb82abdecf263d25b4de1cfd96d0d5c620c69c1d1",
      "signature": "35482c41545a8a1dd1343678952085390c2ac0a056f28bb36c1623ceadece35181d0526386bc8feb5ab15ba71a608a1a51f4f302ca1e11c903d1255e9d039d0a"
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
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "secret": "02e6e7cfa7b82d4b3b449fa6466c893469a727d0214d48db4956a6054b8022a29b",
      "C": "84d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327"
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
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    },
    {
      "amount": 2,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

Each input's `Y` and container record, then the transcript and digests. Only the v3 input signs an input digest; the pre-v3 input's `input_id` is listed only to check the container bytes:

```json
{
  "inputs": [
    {
      "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
      "container": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d03327",
      "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
      "input_digest": "764a2f46843cdefb389d2cf45807b569d646e51780265e1c28e0ac42cdb067e6",
      "signature": "affda39eba371dc7fe506e50ea9e97bea55d24bca91039f399dcbbcc00528c648fb4ba1dcb257851c4bb28e3bb869f2da13232ba539cfc67336276113adad289"
    },
    {
      "Y": "029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae",
      "container": "1100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2",
      "input_id": "efbdd5d14874cb021fc962d93a9848553ca65ae101e9b57f6678aa37ffe1ebd9"
    }
  ],
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033271100570100010202000800456a94ab4e1c46030021029ef117210f475254efd911de93a9d22d471e356f5b1e3f00df8c24bbb37bd3ae04002102a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba221004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004b0100010202002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "74e13e494841037a8578176a18a25e412ef5b86e35e2de6f0bff5f30f79405b4"
}
```

**Mint.** Mint quote `quote-mint-0001` (amount 8, none issued) with one 8-sat output, locked to the [NUT-13 quote lock key](13-tests.md#version-3-secret-derivation) of counter `0` (`0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812`):

```json
{
  "outputs": [
    {
      "amount": 8,
      "id": "02b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6",
      "B_": "b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55"
    }
  ]
}
```

```json
{
  "transcript": "12003d0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000021004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "3f2ed71b538ba1cdb59b7d176dae4709c5db6b30d2c364fc231bfd2985d9f845",
  "input_id": "d294012dd54976b05eb3e36eb218b9a6d66b19d79ec122944a35b99b8ddd8839",
  "input_digest": "cd149490f31c836c3f4bab5e401242100a1522e7e5e0af2db4da4020bb894af1"
}
```

**Partial mint.** Issuing 4 against 8-sat mint quote `quote-mint-0004` with 3 already issued, with one 4-sat output:

```
12 003e | 01 0001 04 | 02 000f 71756f...303034 | 03 0021 029290...209812 | 04 0001 03
```

```json
{
  "transcript": "12003e0100010402000f71756f74652d6d696e742d303030340300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d2098120400010321004b0100010402002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "93379041ba7dd1166d7dc1b028305a22470c461f62907982565a2343148cb64b",
  "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
  "input_id": "c2e4168d079d7ccc6c9fc80c480e75a255282ec41e660afad42cf743c95f14e3",
  "input_digest": "3e22290842db64b0c8417b72e16bf0965d5ee304815978d3b8c2d53574a60ebb",
  "signature": "5055a075e7534502457e914c81768d29bae3d0be046d106a8a6529507c3bdc851cbecd9654454d22efe88658803d4a96d8c2ba53716b9846da08411fbabf71de"
}
```

The signature **MUST NOT** verify over a transcript that commits amount `8` or `issued` `0`.

**Batched mint.** A [NUT-29](../29.md) batch of `quote-mint-0002` and `quote-mint-0003` with `quote_amounts` of `[5, 3]` and the mint vector's 8-sat output:

```
12 003d | 01 0001 05 | 02 000f 71756f...303032 | 03 0021 029290...209812 | 04 0000
12 003d | 01 0001 03 | 02 000f 71756f...303033 | 03 0021 02b357...99615d | 04 0000
```

```json
{
  "transcript": "12003d0100010502000f71756f74652d6d696e742d303030320300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000012003d0100010302000f71756f74652d6d696e742d3030303303002102b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d04000021004b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "bf866b675bf6730b94f556095a22f4ac094fb3fe5d65d777dd05a41ebfb6f4ed",
  "inputs": [
    {
      "quote_id": "quote-mint-0002",
      "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
      "input_id": "8c7f916779dfba1b7ea2e0d3e69d1ee7eed1895af2891406fe8bdb7fbe0f39aa",
      "input_digest": "dbc45733112ba2e7fad938d62de00c13c085309c9330d082cadee0c6dfeca85f",
      "signature": "e0520f39e881481c7f6f12f987d09483c14b4bb3fbeea8f35d238f53bf0448be53db93f3a61ab882e50c8a96d26a87f48ded963ff5a585e404834f8c13b00e20"
    },
    {
      "quote_id": "quote-mint-0003",
      "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
      "input_id": "f7a60306c44e910fd5dea355541c4a4bb251220690688279bf08e7d19b3e9e45",
      "input_digest": "f14225ec0ff74cae090865a5d852b9cd8b06827d3f459ad2d6a5ce4cc1e91dac",
      "signature": "e726ee0cef6b2431850f4f5f7b5745d8810ead54888db3aae12c30d151049810c72dbe9f3d07812719fd1e2c8d55df91cec1e9a81e8cfe557485cefcb4e6447f"
    }
  ]
}
```

**Melt.** Paying melt quote `quote-melt-0001` (amount 8, fee reserve 0, no change outputs) with the swap's 8-sat proof:

```json
{
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d033272200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "1b9e4e88ad05d873bee5b00a3d621e9a6565bb611a27174dfc17d268dffd38c2",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "5319b114091bd127f42fd209b4b363d13a145da174c534fb8fa4c584a8405c0f"
}
```

The melt shares the swap's `input_id` but not its `input_digest`, so neither witness verifies in the other transaction.

**Melt with change.** The same melt with two [NUT-08](../08.md) blank outputs (amount 0) on the swap's keyset and `B_`. They precede the melt quote in the transcript, and each zero amount encodes as `010000`:

```json
{
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332721004a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee21004a01000002002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee2200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "adac16b768b73d5137096faf62a1b3b035cb8fd27e2a22c3159d99d1f2415c60",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "c5692db35c58c47c70aa4dab49d2ede41adec95f00a231bf40cc8af5ddee030f"
}
```

**Mint quote to melt.** Paying melt quote `quote-melt-0001` straight from mint quote `quote-mint-0001` in one transaction ([NUT-XX](../XX.md)): no proofs and no change outputs, so the transcript is the mint vector's quote input container followed by the melt vector's melt quote container. The quote input's bytes are unchanged, so it keeps the mint vector's `input_id`; the new transcript gives it a new `input_digest`, which its lock key signs:

```json
{
  "transcript": "12003d0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d2098120400002200160100010802000f71756f74652d6d656c742d30303031",
  "digest": "8c54caecbdd6fdc5ae77bea97ed63dbf94a6919d6bc5d71cd7145765b52e49f3",
  "input_id": "d294012dd54976b05eb3e36eb218b9a6d66b19d79ec122944a35b99b8ddd8839",
  "input_digest": "492728212791e2222a327b9c4fe6c17e2da0e9e7d1aebbe0062c3585909edb57"
}
```

**Proof to two fixed txout quotes.** Splitting the swap's 8-sat proof between fixed [txout quotes](../XX.md#fixed-txout-quote) of 3 and 5, with the lock keys and `id_preimage`s a seeded wallet derives at quote counters 2 and 3 of the [NUT-13](13-tests.md) test seed and identity, in that request order:

```json
{
  "mint_quote_outputs": [
    {
      "id_preimage": "2caf99f5aef46b625beb02484fc76b467cd9c025c68ce8af02b70b65b6d21f1d",
      "pubkey": "03db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b",
      "amount": 3
    },
    {
      "id_preimage": "132004e11a17cea14291ed197bef25252fc1d5340fb23b401f4ac9d399d07b8a",
      "pubkey": "02ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae2",
      "amount": 5
    }
  ]
}
```

Each container carries its amount first, and each quote id is `hex(tagged_hash("Cashu_QuoteId", id_preimage))` as UTF-8:

```
23 006b | 01 0001 03 | 02 0021 03db67...26d38b | 03 0040 utf8("48f528...109815")
23 006b | 01 0001 05 | 02 0021 02ccde...f18ae2 | 03 0040 utf8("7db215...ec52ae")
```

The proof input keeps the swap's `input_id`:

```json
{
  "mint_quote_output_containers": [
    "23006b0100010302002103db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b03004034386635323834646435356433626161653463343361356336636630646562306562613061316337653031653738386634353365323466343866313039383135",
    "23006b0100010502002102ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae203004037646232313538366635626664383935383936316364396134616339373233326162333735366165666233396136613365306366613434616462656335326165"
  ],
  "quote_ids": [
    "48f5284dd55d3baae4c43a5c6cf0deb0eba0a1c7e01e788f453e24f48f109815",
    "7db21586f5bfd8958961cd9a4ac97232ab3756aefb39a6a3e0cfa44adbec52ae"
  ],
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332723006b0100010302002103db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b0300403438663532383464643535643362616165346334336135633663663064656230656261306131633765303165373838663435336532346634386631303938313523006b0100010502002102ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae203004037646232313538366635626664383935383936316364396134616339373233326162333735366165666233396136613365306366613434616462656335326165",
  "digest": "1e96a6c5f15dffea09102e335b02923c17f5c91fef9410d3d874ca1be04fa85f",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "35e5ebc93588d09d19b7595d732210c3f462d98363f3aaead6a8d6d00d7d412f"
}
```

**Input-bound txout quote.** The swap's proof and the mint vector's quote input (16 in), into the 3-sat quote above and a 13-sat quote locked to quote counter 3's key with no `id_preimage`. Its id is bound to the inputs, `hex(tagged_hash("Cashu_InputQuoteId", SHA256(input section) || u32_BE(1)))`, the input section being the two input containers as serialized:

```json
{
  "mint_quote_outputs": [
    {
      "id_preimage": "2caf99f5aef46b625beb02484fc76b467cd9c025c68ce8af02b70b65b6d21f1d",
      "pubkey": "03db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b",
      "amount": 3
    },
    {
      "pubkey": "02ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae2",
      "amount": 13
    }
  ]
}
```

```json
{
  "input_section_hash": "e3e06afdc3dfecf19c58797baebc07b939aa70f4f35f89685a91e699d15e171f",
  "quote_ids": [
    "48f5284dd55d3baae4c43a5c6cf0deb0eba0a1c7e01e788f453e24f48f109815",
    "55b8704228307aacfa9ac19243e9872c8aceee6673f9f7b28b115320369d5e14"
  ],
  "transcript": "11008e0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a7304003084d1b7291ae5737f3c851aa33cafe0f7afeb5ccb4da086c482bb85b7525e61547f1b5a6d1a01b1fed1f960d1a9d0332712003d0100010802000f71756f74652d6d696e742d303030310300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000023006b0100010302002103db67a892bc5c2c37c1a7979ba28706732deef4b92d69a5f68ad0ab448126d38b0300403438663532383464643535643362616165346334336135633663663064656230656261306131633765303165373838663435336532346634386631303938313523006b0100010d02002102ccdef4b1ff9e02ee1c142505aa501f2ae3ef30ad9837234d501c26e974f18ae203004035356238373034323238333037616163666139616331393234336539383732633861636565653636373366396637623238623131353332303336396435653134",
  "digest": "49d39125cfa48a8bfc262286981a80e7d4d2366bed606cb86618a2b1479b4a64",
  "input_id": "900fb575d55eed27f7f52db079a2bf4843e674c461726eca70b90943cb3c7d07",
  "input_digest": "788bfa90df7349b1db06750fcf53f230a3c85f1d319c4776ac3024f34c1873ae"
}
```
