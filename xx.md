# NUT-XX: Batched Mint

`optional`

`depends on: NUT-04`

This spec describes how a wallet can mint multiple proofs in one batch operation.

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

- **quote**: an array of quote IDs previously obtained via the [NUT-04 creation process][04-creation].

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

---

## 2. Executing the Batched Mint

Once all quoted payments are confirmed, the wallet mints the tokens by calling:

```http
POST https://mint.host:3338/v1/mint/{method}
Content-Type: application/json

{
  "quote":   [ "quote_id_1", "quote_id_2", … ],
  "outputs": [ BlindedMessage_1, BlindedMessage_2, … ]
}
```

- **quote**: an array of quote IDs previously obtained via the [NUT-04 creation process][04-creation].
- **outputs**: an array of blinded messages (see [NUT-00][00]).
  - The total value represented by these blinded messages must equal the sum of the quote amounts.

The mint responds with:

```json
{
  "signatures": [ BlindSignature_1, BlindSignature_2, … ]
}
```

- **signatures**: blind signatures corresponding to each provided blinded message.

[00]: 00.md
[04-creation]: 04.md#requesting-a-mint-quote
