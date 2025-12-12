# NUT-XX: Batched Mint

`optional`

`depends on: NUT-04, NUT-20 (for signature support)`

This spec describes how a wallet can mint multiple proofs in one batch operation by requesting blind signatures for multiple quotes in a single atomic request. This is more efficient than individual mint requests.

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
  - **All quotes MUST be from the same payment method** (indicated by `{method}` in the URL path).
  - **All quotes MUST use the same currency unit**.
- **outputs**: an array of blinded messages (see [NUT-00][00]).
  - The total value represented by all blinded messages must equal the sum of all quote amounts.
- **signature**: array of signatures for NUT-20 locked quotes. See [NUT-20 Support][nut-20-support]

The mint responds with:

```json
{
  "signatures": [ BlindSignature_1, BlindSignature_2, … ]
}
```

- **signatures**: an array of blind signatures, **one for each provided blinded message**, in the same order as the `outputs` array.

## NUT-20 support

Per [NUT-20][20], quotes can require authentication via signatures. When using batch minting with NUT-20 locked quotes:

### Signature Structure

- The `signature` field is an **array with length equal to `quote.length`** (one entry per quote).
- `signature[i]` corresponds to `quote[i]`.
- For **locked quotes** (those with a `pubkey`): `signature[i]` contains the signature string.
- For **unlocked quotes**: `signature[i]` is `null`.
- The `signature` field is **required** if ANY quote is locked, otherwise it **MAY be omitted entirely**.

### Signature Message

Following the [NUT-20 message aggregation][20-msg-agg] pattern, the signature for `quote[i]` is computed as:

```
msg_to_sign = quote_id[i] || B_0 || B_1 || ... || B_(n-1)
```

Where:
- `quote_id[i]` is the UTF-8 encoded quote ID at index `i`
- `B_0 ... B_(n-1)` are **all blinded messages** from the `outputs` array (regardless of amount splitting)
- `||` denotes concatenation

This signature protects against:
1. Quote tampering (verification ties signature to specific quote ID)
2. Output tampering (signature covers all outputs, preventing malicious replacement or reordering)

The signature is a BIP340 Schnorr signature on the SHA-256 hash of `msg_to_sign`.

### Signature Validation Failure

If **any signature in the batch is invalid**, the mint MUST reject the **entire batch** and return an error. This maintains atomicity: all quotes must be successfully authenticated and minted together, or none at all.

### Example

```json
{
  "quote":   [ "locked_quote_id_1", "unlocked_quote_id_2", "locked_quote_id_3" ],
  "outputs": [
    { "amount": 64, "id": "keyset_1", "B_": "..." },
    { "amount": 64, "id": "keyset_1", "B_": "..." },
    { "amount": 22, "id": "keyset_1", "B_": "..." }
  ],
  "signature": [
    "d9be080b...",  // Signature for quote[0], covers ALL 3 outputs
    null,           // Quote[1] is unlocked
    "a1c5f7e2..."   // Signature for quote[2], covers ALL 3 outputs
  ]
}
```

In this example:
- Quote 0: 100 sats, locked, split across outputs[0:3]
- Quote 1: 50 sats, unlocked
- Quote 2: 75 sats, locked, split across outputs[0:3]
- Total: 225 sats across 3 outputs
- Both signatures cover all 3 outputs to prevent output tampering

## Mint Responsibilities

The mint MUST:
1. Verify all quote IDs are valid and in PAID state
2. Verify all quotes are from the same payment method as indicated by `{method}` in the URL path
3. Verify all quotes use the same currency unit
4. Verify the sum of output amounts equals the sum of quote amounts
5. Verify all NUT-20 signatures (if present) per [NUT-20][20] rules
6. Generate one blind signature per output
7. Return signatures in the same order as the outputs array

[00]: 00.md
[04-creation]: 04.md#requesting-a-mint-quote
[04]: 04.md
[20]: 20.md
[20-msg-agg]: 20.md#message-aggregation
[nut-20-support]: #nut-20-support
