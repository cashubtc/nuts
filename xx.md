# NUT-XX: Batched Mint

`optional`

`depends on: NUT-04`

This spec describes how a wallet can mint multiple quotes in one batch operation.

---

## 1. Checking Quote Status

Before minting, the wallet must verify that each mint quote has been paid.
It does this by sending:

```http
POST https://mint.host:3338/v1/mint/{method}/check
Content-Type: application/json

{
  "quote": [ "quote_id_1", "quote_id_2", … ]
}
```

- **quote**: an array of **unique** quote IDs previously obtained via the [NUT-04 creation process][04-creation].

The mint returns a JSON array of quote objects, each containing:

```json
[
  {
    "quote": "quote_id_1",
    "request": "payment_request_1",
    "unit": "UNIT_NAME"
    // …plus any additional fields specific to {method}
  },
  {
    "quote": "quote_id_2",
    "request": "payment_request_2",
    "unit": "UNIT_NAME"
    // …
  }
]
```

- **quote**: the original quote ID
- **request**: the payment request string for that quote
- **unit**: the unit type, matching what was requested

NOTE: If a `quote_id` is not known by the mint it SHOULD omit it from the response.

---

## 2. Executing the Batched Mint

Once all quoted payments are confirmed, the wallet mints the tokens by calling:

```http
POST https://mint.host:3338/v1/mint/{method}
Content-Type: application/json

{
  "quote":   [ "quote_id_1", "quote_id_2", … ],
  "outputs": [ BlindedMessage_1, BlindedMessage_2, … ],
  "signature": [signature_1, signature_2, ... ]
}
```

- **quote**: an array of **unique** quote IDs previously obtained via the [NUT-04 creation process][04-creation].
- **outputs**: an array of blinded messages (see [NUT-00][00]).
  - The total value represented by these blinded messages must equal the sum of the quote amounts.
- **signature**: The signature for a NUT-20 locked quote. See [NUT-20 Support][nut-20-support]
  The mint responds with:

```json
{
  "signatures": [ BlindSignature_1, BlindSignature_2, … ]
}
```

- **signatures**: blind signatures corresponding to each provided blinded message.

## NUT-20 support

The `signature` field of the request can be used to add matching NUT-20 signatures to a batch mint. Signatures can be mapped to their quotes using both indexes in the request body. As long as there is a single NUT-20 quote in the request this field is mandatory, otherwise it can be fully omitted.

- Signatures for NUT-20 quotes can be added to the `signature` key of the request.
- Signatures need to be in the same index as the matching quote_id in the `quote` key.
- If a request contains both signed and unsigned quotes, all unsigned quotes need to map to `null` in the `signature` array.
- As soon as there is a single signed quote in the request: `quote.length === signature.length`

Example:

```json
{
  "quote":   [ "locked_quote_id_1", "quote_id_2", "locked_quote_id_3" ],
  "outputs": [ BlindedMessage_1, BlindedMessage_2, ... ],
  "signature": [signature_1, null, signature_3 ]
}
```

[00]: 00.md
[04-creation]: 04.md#requesting-a-mint-quote
[nut-20-support]: #nut-20-support
