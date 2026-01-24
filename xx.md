# NUT-XX: Batched Mint

`optional`

`depends on: NUT-04, NUT-20 (for signature support)`

This spec describes how a wallet can mint multiple quotes in one batch operation by requesting blind signatures for multiple quotes in a single atomic request.

---

## 1. Checking Quote Status

Before minting, the wallet SHOULD verify that each mint quote has been paid.
It does this by sending:

```http
POST https://mint.host:3338/v1/mint/{method}/check
Content-Type: application/json

{
  "quotes": [ "quote_id_1", "quote_id_2", … ]
}
```

- **quotes**: an array of **unique** mint quote IDs.

The mint returns a JSON array of quote status objects. Each object uses the quote response format defined by the payment method's NUT specification.

The response MUST include at minimum:

- **quote**: The quote ID
- **state**: Quote state (`UNPAID`, `PAID`, or `ISSUED`)
- **unit**: The currency unit

Example for bolt11:

```json
[
  {
    "quote": "quote_id_1",
    "request": "lnbc...",
    "state": "PAID",
    "unit": "sat",
    "amount": 100,
    "expiry": 1234567890
  },
  {
    "quote": "quote_id_2",
    "request": "lnbc...",
    "state": "UNPAID",
    "unit": "sat",
    "amount": 50,
    "expiry": 1234567890
  }
]
```

**Note on Error Handling:**

This is a query endpoint that returns available information without side effects:

- If a `quote_id` is not known by the mint, it SHOULD be omitted from the response
- If a `quote_id` cannot be parsed (invalid format), it SHOULD be omitted from the response
- The response array MAY be shorter than the request array if some quotes are unknown or invalid

This partial-response behavior differs from the batch mint endpoint, which requires all quotes to be valid and uses atomic all-or-nothing processing.

---

## 2. Executing the Batched Mint

Once all quoted payments are confirmed, the wallet mints the proofs by calling:

```http
POST https://mint.host:3338/v1/mint/{method}/batch
Content-Type: application/json

{
  "quotes":   [ "quote_id_1", "quote_id_2", … ],
  "quote_amounts": [ 50, 50 ],
  "outputs": [ BlindedMessage_1, BlindedMessage_2, … ],
  "signatures": [signature_1, signature_2, ... ]
}
```

- **quotes**: an array of **unique** quote IDs.
  - **All quotes MUST be from the same payment method** (indicated by `{method}` in the URL path).
  - **All quotes MUST use the same currency unit**.
- **quote_amounts**: array of expected mint amounts per quote, in the same order as `quotes`.
  - REQUIRED for bolt12 batches; OPTIONAL for bolt11.
  - For bolt11, each entry MUST equal the quoted amount. For bolt12, each entry MUST NOT exceed the quote's remaining mintable amount. In all cases, the sum of `quote_amounts` MUST equal the sum of `outputs`.
- **outputs**: an array of blinded messages (see [NUT-00][00]).
  - The total value represented by all blinded messages must equal the sum of all quote amounts.
- **signatures**: array of signatures for NUT-20 locked quotes. See [NUT-20 Support][nut-20-support]

The mint responds with:

```json
{
  "signatures": [ BlindSignature_1, BlindSignature_2, … ]
}
```

- **signatures**: an array of blind signatures, **one for each provided blinded message**, in the same order as the `outputs` array.

## Request Validation

The mint MUST validate the following before processing a batch mint request:

1. **Non-empty batch**: The `quotes` array MUST NOT be empty
2. **Unique quotes**: All quote IDs in the `quotes` array MUST be unique (no duplicates)
3. **Valid quote IDs**: All quote IDs MUST be parseable and exist in the mint's database
4. **Payment method consistency**: All quotes MUST have the same payment method, matching `{method}` in the URL path
5. **Currency unit consistency**: All quotes MUST use the same currency unit
6. **Quote state**: All quotes MUST be in PAID state (or have mintable amount for BOLT12)
7. **Amount balance**: The sum of output amounts MUST equal the sum of `quote_amounts` (bolt11) or MUST NOT exceed it (bolt12)
8. **Signature validation (NUT-20)**: The `signature` array length MUST match the `quotes` array length; locked quotes MUST include a valid signature; unlocked quotes MUST NOT include one

Implementations MAY impose additional constraints such as maximum batch size based on their resource limitations. If any validation fails, the mint MUST reject the entire batch and return an appropriate error without minting any quotes.

## NUT-20 support

Per [NUT-20][20], quotes can require authentication via signatures. When using batch minting with NUT-20 locked quotes:

### Signature Structure

**Array structure:**

- The `signature` field is an array with length equal to `quote.length` (one entry per quote)
- `signatures[i]` corresponds to `quotes[i]`

**Per-quote signatures:**

- **Locked quotes** (with `pubkey`): `signature[i]` contains the signature string
- **Unlocked quotes**: `signatures[i]` is `null`

**Field requirement:**

- **Required**: If ANY quote is locked
- **Optional**: May be omitted entirely if all quotes are unlocked

### Signature Message

Following the [NUT-20 message aggregation][20-msg-agg] pattern, the signature for `quotes[i]` is computed as:

```
msg_to_sign = quote_id[i] || B_0 || B_1 || ... || B_(n-1)
```

Where:

- `quote_id[i]` is the UTF-8 encoded quote ID at index `i`
- `B_0 ... B_(n-1)` are **all blinded messages** from the `outputs` array (regardless of amount splitting)
- `||` denotes concatenation

The signature is a BIP340 Schnorr signature on the SHA-256 hash of `msg_to_sign`.

### Signature Validation Failure

If **any signature in the batch is invalid**, the mint MUST reject the **entire batch** and return an error. This maintains atomicity: all quotes must be successfully authenticated and minted together, or none at all.

### Example

```json
{
  "quotes": ["locked_quote_id_1", "unlocked_quote_id_2", "locked_quote_id_3"],
  "outputs": [
    { "amount": 64, "id": "keyset_1", "B_": "..." },
    { "amount": 64, "id": "keyset_1", "B_": "..." },
    { "amount": 22, "id": "keyset_1", "B_": "..." }
  ],
  "signatures": [
    "d9be080b...", // Signature for quote[0], covers ALL 3 outputs
    null, // Quote[1] is unlocked
    "a1c5f7e2..." // Signature for quote[2], covers ALL 3 outputs
  ]
}
```

## Implementation Notes

### Batch Size Limits

Implementations MAY advertise a maximum batch size through the mint info endpoint (NUT-06). The batch size limit is included in the `nuts` object under the `XX` key:

```json
{
  "nuts": {
    "XX": {
      "max_batch_size": 100,
      "methods": ["bolt11", "bolt12"]
    }
  }
}
```

Fields:

- `max_batch_size` (optional): Maximum number of quotes allowed in a single batch request. If omitted, the batch size limit is implementation-defined and clients MUST handle `BATCH_SIZE_EXCEEDED` errors gracefully.
- `methods` (optional): Array of payment methods supported for batch minting. If omitted, all methods supported by the mint (per NUT-04) are available for batching.

[00]: 00.md
[20]: 20.md
[20-msg-agg]: 20.md#message-aggregation
[nut-20-support]: #nut-20-support
