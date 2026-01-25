# NUT-XX: Batched Minting

`optional`

`depends on: NUT-04`

`uses: NUT-20`

This spec describes how a wallet can mint multiple quotes in one batched operation by requesting blind signatures for multiple multiple quotes in a single atomic request.

---

## 1. Batch Checking Quote State

Before minting, the wallet SHOULD verify that each mint quote has been paid. It does this by sending:

```http
POST https://mint.host:3338/v1/mint/quote/{method}/check
```

The wallet includes the following body in its request:

```json
{
  "quotes": <Array[str]>
}
```

where `quotes` is an array of _unique_ mint quote IDs.

The mint returns a JSON array of mint quotes objects as defined by the payment method's NUT specification.

#### Example

Below is an example for checking two bolt11 mint quotes.

##### Request

```http
POST https://mint.host:3338/v1/mint/quote/bolt11/check
Content-Type: application/json

{
  "quotes": [ "quote_id_1", "quote_id_2" ]
}
```

##### Response

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

#### Error Handling

This is a query endpoint that returns available information without side effects:

- If a `quote_id` is not known by the mint, it SHOULD be omitted from the response
- If a `quote_id` cannot be parsed (invalid format), it SHOULD be omitted from the response
- The response array MAY be shorter than the request array if some quotes are unknown or invalid

This partial-response behavior differs from the batch mint endpoint, which requires all quotes to be valid and uses atomic all-or-nothing processing.

---

## 2. Executing the Batched Mint

#### Request by wallet

Once all quoted payments are confirmed, the wallet mints the proofs by calling:

```http
POST https://mint.host:3338/v1/mint/{method}/batch
```

The wallet includes the following body in its request:

```json
{
  "quotes": <Array[str]>,
  "quote_amounts": <Array[int]|null>, // Optional
  "outputs": <Array[BlindedMessage]>,
  "signatures": <Array[BlindedMessage]|null> // Optional
}
```

- `quotes`: array of _unique_ quote IDs.
- `quote_amounts`: array of expected amounts to mint per quote, in the same order as `quotes`.
  - Required for payment methods that demand an amount like bolt12; Optional for other methods like bolt11.
- `outputs`: array of blinded messages (see [NUT-00][00]).
- `signatures`: array of signatures for NUT-20 locked quotes. See [NUT-20 Support][nut-20-support]

#### Response by mint

The mint responds with:

```json
{
  "signatures": <Array[BlindSignature]>
}
```

- `signatures`: an array of blind signatures, one for each provided blinded message, in the same order as the `outputs` array.

### Example

Below is an example for minting two NUT-20 locked bolt11 mint quotes.

##### Request

```http
POST https://mint.host:3338/v1/mint/bolt12/batch
Content-Type: application/json

{
  "quotes": [
    "quote_id_1",
    "quote_id_2"
  ],
  "quote_amounts": [
    100,
    50
  ],
  "signatures": [
    "d9be080b33179387e504bb6991ea41ae0dd715e28b01ce9f63d57198a095bccc776874914288e6989e97ac9d255ac667c205fa8d90a211184b417b4ffdd24092",
    "f2d97118390195cf5bef21d84c94e505dcdc2760154519536f74ba5e27f886f313b82296610df14db1d91d346e988ed384070bad084aaf06d14ccd7686157f24"
  ],
  "outputs": [
    {
      "amount": 128,
      "id": "009a1f293253e41e",
      "B_": "035015e6d7ade60ba8426cefaf1832bbd27257636e44a76b922d78e79b47cb689d"
    },
    {
      "amount": 16,
      "id": "009a1f293253e41e",
      "B_": "0288d7649652d0a83fc9c966c969fb217f15904431e61a44b14999fabc1b5d9ac6"
    },
    {
      "amount": 4,
      "id": "009a1f293253e41e",
      "B_": "03b85be0c0a9f51056375b632a2f2c8149831b9827fad677be9807455e7d84b584"
    },
    {
      "amount": 2,
      "id": "009a1f293253e41e",
      "B_": "0276bbcf69e1b1238e6d39fc14c84e7cdfd519fee07f3369d2b2b23045390e2efc"
    }
  ]
}
```

##### Response

```json
{
  "signatures": [
    "0208657b2917f469f275226cc931e5389451f6eed515d586ad16fa7a700eed4fb6",
    "037dc0b5e712a39ef22f5bba1d49bc65a323ab9e0b771f7281d8c33280e2e58dbc"
  ]
}
```

### Request Validation

The mint MUST validate the following before processing a batch mint request:

1. **Non-empty batch**: The `quotes` array MUST NOT be empty
2. **Unique quotes**: All quote IDs in the `quotes` array MUST be unique (no duplicates)
3. **Valid quote IDs**: All quote IDs MUST exist in the mint's database
4. **Payment method consistency**: All quotes MUST have the same payment method, matching `{method}` in the URL path
5. **Currency unit consistency**: All quotes MUST use the same currency unit
6. **Quote state**: All quotes MUST be in PAID state (or have a mintable amount for payment methods that allow multiple mint operations like bolt12)
7. **Amount balance**: The sum of amounts contained in the `outputs` MUST equal the sum of `quote_amounts` (bolt11) or MUST NOT exceed it (bolt12)
8. **Signature validation (NUT-20)**: The `signature` array length MUST match the `quotes` array length; locked quotes MUST include a valid signature; unlocked quotes MUST NOT include one

Implementations MAY impose additional constraints such as maximum batch size based on their resource limitations. If any validation fails, the mint MUST reject the entire batch and return an appropriate error without minting any quotes.

### NUT-20 support

Per [NUT-20][20], quotes can require authentication via signatures. When using batch minting with NUT-20 locked quotes:

#### Signature Array Structure

**Array structure:**

- The `signature` field is an array with length equal to `quote.length` (one entry per quote)
- `signatures[i]` corresponds to `quotes[i]`

**Per-quote signatures:**

- **Locked quotes** (with `pubkey`): `signature[i]` contains the signature string
- **Unlocked quotes**: `signatures[i]` is `null`

**Field requirement:**

- **Required**: If ANY quote is locked
- **Optional**: May be omitted entirely if all quotes are unlocked

#### Signature Message

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

Mints MAY advertise a maximum batch size through the [NUT-06][06] mint info endpoint. The batch size limit is included in the `nuts` object under the `XX` key:

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
[06]: 06.md
[20]: 20.md
[20-msg-agg]: 20.md#message-aggregation
[nut-20-support]: #nut-20-support
