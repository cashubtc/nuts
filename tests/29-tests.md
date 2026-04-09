# NUT-29 Test Vectors

## Successful batch mint

The following is a valid batch mint request combining two bolt11 quotes (`quote_id_a` for 5 sats and `quote_id_b` for 3 sats) into a single 8 sat output.

```json
{
  "quotes": ["quote_id_a", "quote_id_b"],
  "quote_amounts": [5, 3],
  "outputs": [{ "amount": 8, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

The following is the corresponding response with a blind signature.

```json
{
  "signatures": [{ "amount": 8, "id": "keyset_1", "C_": "<blind_signature>" }]
}
```

## Check endpoint with unknown quotes

The following is an invalid check request containing an unknown quote ID.

```json
{ "quotes": ["known-1", "bogus", "unknown-2"] }
```

Per NUT-29, quote check uses all-or-nothing error handling. If any quote is unknown, the entire request must be rejected.

```json
{
  "code": "UNKNOWN_QUOTE",
  "error": "one or more quote IDs are unknown"
}
```

## Batch mint atomic failure

The following is an invalid batch mint request containing one unknown quote ID, causing the entire batch to fail atomically with no partial minting.

```json
{
  "quotes": ["valid_quote_id", "unknown_quote_id"],
  ...
}
```

Expected behavior:

- The mint rejects the whole request with an error.
- No outputs are signed.
- No quote state is consumed/changed by partial processing.

## Batch mint rejects empty quotes array

The following is an invalid batch mint request with an empty `quotes` array.

```json
{
  "quotes": [],
  "outputs": [{ "amount": 1, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

Expected behavior:

- The mint rejects the request because `quotes` must be non-empty.
- No outputs are signed.

## Batch mint rejects duplicate quote IDs

The following is an invalid batch mint request with duplicate quote IDs.

```json
{
  "quotes": ["quote_id_dup", "quote_id_dup"],
  "outputs": [{ "amount": 2, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

Expected behavior:

- The mint rejects the request because quote IDs must be unique.
- No outputs are signed.

## Batch mint rejects mixed payment methods

The following is an invalid request to `/v1/mint/bolt11/batch` where one quote is bolt11 and one quote is bolt12.

```json
{
  "quotes": ["bolt11_quote_id", "bolt12_quote_id"],
  "quote_amounts": [5, 3],
  "outputs": [{ "amount": 8, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

Expected behavior:

- The mint rejects the request because all quotes must share the same payment method and match `{method}` in the URL.
- No outputs are signed.

## Batch mint rejects NUT-20 signature length mismatch

The following is an invalid batch mint request where `signatures` length does not match `quotes` length.

```json
{
  "quotes": ["locked_quote_id_1", "locked_quote_id_2"],
  "outputs": [
    { "amount": 1, "id": "keyset_1", "B_": "<blinded_message_0>" },
    { "amount": 1, "id": "keyset_1", "B_": "<blinded_message_1>" }
  ],
  "signatures": ["<sig_for_quote_1_only>"]
}
```

Expected behavior:

- The mint rejects the request because `signatures[i]` must exist for each `quotes[i]` when signatures are required.
- No outputs are signed.

## NUT-20 signature with valid ordering

The following is a valid NUT-20 batch mint request where the signature correctly covers all outputs in order. The quote has pubkey `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798` (sk = 1).

```shell
quote: "locked-quote"
pubkey: 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
msg_to_sign_bytes: utf8("locked-quote") || utf8(B0) || utf8(B1)
msg_hash: a62f12934711693d6045ed2843ae4c5b33fd156df029fb9337dea3175c438263
signature[0]: bd4d55f3fda33109fe3694c041aa9358c8e6e581236245ee310e7e225dfb075d9a2799b9672e646cb7e9fad9887f5b42a04d307a238d219783a4790b323194c0
```

```json
{
  "quotes": ["locked-quote"],
  "outputs": [
    {
      "amount": 1,
      "id": "010000000000000000000000000000000000000000000000000000000000000000",
      "B_": "036d6caac248af96f6afa7f904f550253a0f3ef3f5aa2fe6838a95b216691468e2"
    },
    {
      "amount": 1,
      "id": "010000000000000000000000000000000000000000000000000000000000000000",
      "B_": "021f8a566c205633d029094747d2e18f44e05993dda7a5f88f496078205f656e59"
    }
  ],
  "signatures": [
    "bd4d55f3fda33109fe3694c041aa9358c8e6e581236245ee310e7e225dfb075d9a2799b9672e646cb7e9fad9887f5b42a04d307a238d219783a4790b323194c0"
  ]
}
```
