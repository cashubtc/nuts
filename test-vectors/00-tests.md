# NUT-00 Test Vectors
## Blind Diffie-Hellman key exchange section
The following are test vectors related to the [Blind Diffie-Hellman key exchange section](https://github.com/cashubtc/nuts/blob/main/00.md#blind-diffie-hellmann-key-exchange-bdhke).

### Hash-to-curve function
The hash to curve function takes a message of any length and outputs a valid point on the secp256k1 curve.
```shell
# Test 1 (hex encoded)
Message: 0000000000000000000000000000000000000000000000000000000000000000
Point:   0266687aadf862bd776c8fc18b8e9f8e20089714856ee233b3902a591d0d5f2925

# Test 2 (hex encoded)
Message: 0000000000000000000000000000000000000000000000000000000000000001
Point:   02ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5

# Test 3 (hex encoded)
# Note that this message will take a few iterations of the loop before finding a valid point
Message: 0000000000000000000000000000000000000000000000000000000000000002
Point:   02076c988b353fcbb748178ecb286bc9d0b4acf474d4ba31ba62334e46c97c416a
````

### Blinded messages
These are test vectors for the public key `B_` Alice will send to the mint Bob given secret `x`  and random blinding factor `r`.
```shell
# Test 1
x: "test_message"
r: 0000000000000000000000000000000000000000000000000000000000000001 # hex encoded
B_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2

# Test 2
x: "hello"
r: 6d7e0abffc83267de28ed8ecc8760f17697e51252e13333ba69b4ddad1f95d05 # hex encoded
B_: 0249eb5dbb4fac2750991cf18083388c6ef76cde9537a6ac6f3e6679d35cdf4b0c
```

### Blinded keys
These are test vectors for the blinded key `C_` given the mint's private key `k` and Alice's blinded message containing `B_`.
```shell
# Test 1
mint private key: 0000000000000000000000000000000000000000000000000000000000000001
x: "test_message"
r: 0000000000000000000000000000000000000000000000000000000000000001 # hex encoded
B_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2
C_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2

# Test 2
mint private key: 7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f
x: "test_message"
r: 0000000000000000000000000000000000000000000000000000000000000001 # hex encoded
B_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2
C_: 0398bc70ce8184d27ba89834d19f5199c84443c31131e48d3c1214db24247d005d
````

## Serialization of TokenV3
The following are JSON-formatted v3 tokens and their serialized counterparts. Note that the JSON objects need to be stripped of all whitespace before the serialization step.
```shell
# "Pretty print" JSON format
{
  "token": [
    {
      "mint": "https://8333.space:3338",
      "proofs": [
        {
          "id": "DSAl9nvvyfva",
          "amount": 2,
          "secret": "EhpennC9qB3iFlW8FZ_pZw",
          "C": "02c020067db727d586bc3183aecf97fcb800c3f4cc4759f69c626c9db5d8f5b5d4"
        },
        {
          "id": "DSAl9nvvyfva",
          "amount": 8,
          "secret": "TmS6Cv0YT5PU_5ATVKnukw",
          "C": "02ac910bef28cbe5d7325415d5c263026f15f9b967a079ca9779ab6e5c2db133a7"
        }
      ]
    }
  ],
  "memo": "Thank you."
}

# JSON ready for serialization
{"token":[{"mint":"https://8333.space:3338","proofs":[{"id":"DSAl9nvvyfva","amount":2,"secret":"EhpennC9qB3iFlW8FZ_pZw","C":"02c020067db727d586bc3183aecf97fcb800c3f4cc4759f69c626c9db5d8f5b5d4"},{"id":"DSAl9nvvyfva","amount":8,"secret":"TmS6Cv0YT5PU_5ATVKnukw","C":"02ac910bef28cbe5d7325415d5c263026f15f9b967a079ca9779ab6e5c2db133a7"}]}],"memo":"Thank you."}

# Serialized token
cashuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJpZCI6IkRTQWw5bnZ2eWZ2YSIsImFtb3VudCI6Miwic2VjcmV0IjoiRWhwZW5uQzlxQjNpRmxXOEZaX3BadyIsIkMiOiIwMmMwMjAwNjdkYjcyN2Q1ODZiYzMxODNhZWNmOTdmY2I4MDBjM2Y0Y2M0NzU5ZjY5YzYyNmM5ZGI1ZDhmNWI1ZDQifSx7ImlkIjoiRFNBbDludnZ5ZnZhIiwiYW1vdW50Ijo4LCJzZWNyZXQiOiJUbVM2Q3YwWVQ1UFVfNUFUVktudWt3IiwiQyI6IjAyYWM5MTBiZWYyOGNiZTVkNzMyNTQxNWQ1YzI2MzAyNmYxNWY5Yjk2N2EwNzljYTk3NzlhYjZlNWMyZGIxMzNhNyJ9XX1dLCJtZW1vIjoiVGhhbmt5b3UuIn0=
```

## Deserialization of TokenV3
The following are incorrectly formatted serialized v3 tokens.
```shell
# Incorrect prefix (casshuA)
casshuAeyJ0b2tlbiI6IFt7InByb29mcyI6IFt7ImlkIjogIkplaFpMVTZuQ3BSZCIsICJhbW91bnQiOiAyLCAic2VjcmV0IjogIjBFN2lDazRkVmxSZjVQRjFnNFpWMnciLCAiQyI6ICIwM2FiNTgwYWQ5NTc3OGVkNTI5NmY4YmVlNjU1ZGJkN2Q2NDJmNWQzMmRlOGUyNDg0NzdlMGI0ZDZhYTg2M2ZjZDUifSwgeyJpZCI6ICJKZWhaTFU2bkNwUmQiLCAiYW1vdW50IjogOCwgInNlY3JldCI6ICJzNklwZXh3SGNxcXVLZDZYbW9qTDJnIiwgIkMiOiAiMDIyZDAwNGY5ZWMxNmE1OGFkOTAxNGMyNTliNmQ2MTRlZDM2ODgyOWYwMmMzODc3M2M0NzIyMWY0OTYxY2UzZjIzIn1dLCAibWludCI6ICJodHRwOi8vbG9jYWxob3N0OjMzMzgifV19

# No prefix
eyJ0b2tlbiI6IFt7InByb29mcyI6IFt7ImlkIjogIkplaFpMVTZuQ3BSZCIsICJhbW91bnQiOiAyLCAic2VjcmV0IjogIjBFN2lDazRkVmxSZjVQRjFnNFpWMnciLCAiQyI6ICIwM2FiNTgwYWQ5NTc3OGVkNTI5NmY4YmVlNjU1ZGJkN2Q2NDJmNWQzMmRlOGUyNDg0NzdlMGI0ZDZhYTg2M2ZjZDUifSwgeyJpZCI6ICJKZWhaTFU2bkNwUmQiLCAiYW1vdW50IjogOCwgInNlY3JldCI6ICJzNklwZXh3SGNxcXVLZDZYbW9qTDJnIiwgIkMiOiAiMDIyZDAwNGY5ZWMxNmE1OGFkOTAxNGMyNTliNmQ2MTRlZDM2ODgyOWYwMmMzODc3M2M0NzIyMWY0OTYxY2UzZjIzIn1dLCAibWludCI6ICJodHRwOi8vbG9jYWxob3N0OjMzMzgifV19
```

The following is a correctly serialized v3 token.
```shell
cashuAeyJ0b2tlbiI6W3sibWludCI6Imh0dHBzOi8vODMzMy5zcGFjZTozMzM4IiwicHJvb2ZzIjpbeyJpZCI6IkRTQWw5bnZ2eWZ2YSIsImFtb3VudCI6Miwic2VjcmV0IjoiRWhwZW5uQzlxQjNpRmxXOEZaX3BadyIsIkMiOiIwMmMwMjAwNjdkYjcyN2Q1ODZiYzMxODNhZWNmOTdmY2I4MDBjM2Y0Y2M0NzU5ZjY5YzYyNmM5ZGI1ZDhmNWI1ZDQifSx7ImlkIjoiRFNBbDludnZ5ZnZhIiwiYW1vdW50Ijo4LCJzZWNyZXQiOiJUbVM2Q3YwWVQ1UFVfNUFUVktudWt3IiwiQyI6IjAyYWM5MTBiZWYyOGNiZTVkNzMyNTQxNWQ1YzI2MzAyNmYxNWY5Yjk2N2EwNzljYTk3NzlhYjZlNWMyZGIxMzNhNyJ9XX1dLCJtZW1vIjoiVGhhbmt5b3UuIn0=
```
