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

### TokenV3

What follows is a TokenV3 Token serialized in its raw binary form. `h''` values are bytes in hex notation.

Token:

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

Serialized to raw binary:

`h'6372617741a365746f6b656e81a2646d696e747768747470733a2f2f383333332e73706163653a333333386670726f6f667382a466616d6f756e740262696470303039613166323933323533653431656673656372657478403430373931356263323132626536316137376533653664326165623463373237393830626461353163643036613661666332396532383631373638613738333761437842303262633930393739393764383161666232636337333436623565343334356139333436626432613530366562373935383539386137326630636638353136336561a466616d6f756e74086269647030303961316632393332353365343165667365637265747840666531353130393331346536316437373536623066386565306632336136323461636161336634653034326636313433336337323863373035376239333162656143784230323965386535303530623839306137643663303936386462313662633164356435666130343065613164653238346636656336396436313239396636373130353964756e697463736174646d656d6f6a5468616e6b20796f752e'`

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
