# NUT-XX Test Vectors

## Successful batch mint

The following is a valid batch mint request combining two bolt11 quotes (`quote_id_a` for 5 sats and `quote_id_b` for 3 sats) into a single 8 sat output.

```json
{
  "quotes": ["quote_id_a", "quote_id_b"],
  "quote_amounts": [5, 3],
  "outputs": [
    { "amount": 8, "id": "keyset_1", "B_": "<blinded_message>" }
  ]
}
```

The following is the corresponding response with a blind signature.

```json
{
  "signatures": [
    { "amount": 8, "id": "keyset_1", "C_": "<blind_signature>" }
  ]
}
```

## Check endpoint with unknown quotes

The following is a check request containing unknown quote IDs that are omitted from the response.

```json
{ "quotes": ["known-1", "bogus", "unknown-2"] }
```

The following is the response containing only the known quote.

```json
[
  {
    "quote": "known-1",
    "request": "lnbc...",
    "state": "PAID",
    "unit": "sat",
    "amount": 100,
    "expiry": 1234567890
  }
]
```

## Batch mint atomic failure

The following is an invalid batch mint request containing one unknown quote ID, causing the entire batch to fail atomically with no partial minting.

```json
{
  "quotes": ["valid_quote_id", "unknown_quote_id"],
  ...
}
```

## NUT-20 signature with valid ordering

The following is a valid NUT-20 batch mint request where the signature correctly covers all outputs in order. The quote has pubkey `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798` (sk = 1).

```shell
quote: "locked-quote"
pubkey: 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
msg_to_sign_bytes: utf8("locked-quote") || B0 || B1
msg_hash: 5ac550d5416e81c613b58e3f1fb095390fb828b55e8991fd9de231ca8e31e859
signature[0]: 9408920d0b94cee5eb6df20f14d2a655e7ce2ce309dc1f1aeb69b219efe76716933b2206eba3a54f9a953c92edaa922ab3e6912e02383dda42a193409567a0dc
```

```json
{
  "quotes": ["locked-quote"],
  "outputs": [
    {"amount":1,"id":"010000000000000000000000000000000000000000000000000000000000000000","B_":"036d6caac248af96f6afa7f904f550253a0f3ef3f5aa2fe6838a95b216691468e2"},
    {"amount":1,"id":"010000000000000000000000000000000000000000000000000000000000000000","B_":"021f8a566c205633d029094747d2e18f44e05993dda7a5f88f496078205f656e59"}
  ],
  "signatures": ["9408920d0b94cee5eb6df20f14d2a655e7ce2ce309dc1f1aeb69b219efe76716933b2206eba3a54f9a953c92edaa922ab3e6912e02383dda42a193409567a0dc"]
}
```
