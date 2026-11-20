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

After the batch succeeds, the mint increases `quote_id_a.amount_issued` by 5 and `quote_id_b.amount_issued` by 3.

## Successful batch mint with omitted quote amounts

For bolt11, `quote_amounts` can be omitted. The mint then uses the full currently mintable amount of each quote. Given `quote_id_a` with `amount_paid = 5` and `amount_issued = 2`, and `quote_id_b` with `amount_paid = 3` and `amount_issued = 0`, the following is a valid request for 6 sats:

```json
{
  "quotes": ["quote_id_a", "quote_id_b"],
  "outputs": [{ "amount": 6, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

After the batch succeeds, the mint atomically sets `quote_id_a.amount_issued` to 5 and `quote_id_b.amount_issued` to 3.

## Successful batch mint with an expired quote

Given an expired quote with `amount_paid = 5` and `amount_issued = 2`, the following request is valid because the quote still has a currently mintable amount of 3 sats:

```json
{
  "quotes": ["expired_quote_id"],
  "quote_amounts": [3],
  "outputs": [{ "amount": 3, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

The mint MUST NOT reject issuance solely because the quote's `expiry` has passed. After the batch succeeds, the mint sets `expired_quote_id.amount_issued` to 5.

## Batch mint rejects an amount exceeding a quote's balance

Given `quote_id_a` with `amount_paid = 5` and `amount_issued = 2`, the following request is invalid because its allocation of 4 sats exceeds the quote's currently mintable amount of 3 sats:

```json
{
  "quotes": ["quote_id_a"],
  "quote_amounts": [4],
  "outputs": [{ "amount": 4, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

Expected behavior:

- The mint rejects the whole request with an error.
- No outputs are signed.
- `quote_id_a.amount_issued` remains 2.

## Check endpoint marks unknown and malformed quotes

The following check request contains two known quote IDs, one malformed quote ID, and one unknown quote ID.

```json
{ "quotes": ["known-1", "not-a-valid-quote-id", "unknown-2", "known-2"] }
```

The mint returns one entry per requested quote ID, in request order. The malformed and unknown quote IDs are returned as `unknown` entries.

```json
[
  {
    "quote": "known-1",
    "amount_paid": 5,
    "amount_issued": 0,
    "updated_at": 1234567800
  },
  { "quote": "not-a-valid-quote-id", "unknown": true },
  { "quote": "unknown-2", "unknown": true },
  {
    "quote": "known-2",
    "amount_paid": 0,
    "amount_issued": 0,
    "updated_at": 1234567800
  }
]
```

Each unknown entry contains exactly `quote` and `unknown: true`. Known quote entries do not contain the `unknown` field.

If the mint cannot handle any of the requested quote IDs, every entry in the response is an `unknown` entry. The response is never shorter than the request.

For example:

```json
[
  { "quote": "not-a-valid-quote-id", "unknown": true },
  { "quote": "unknown-2", "unknown": true }
]
```

## Check endpoint is scoped to mint quotes for the requested method

The following request to `/v1/mint/quote/bolt11/check` contains a bolt11 mint quote ID, a bolt12 mint quote ID, and a melt quote ID.

```json
{ "quotes": ["bolt11-mint-quote", "bolt12-mint-quote", "bolt11-melt-quote"] }
```

Only the bolt11 mint quote is within the endpoint's scope. The other IDs are returned as `unknown` entries, even if the mint holds records for them elsewhere.

```json
[
  {
    "quote": "bolt11-mint-quote",
    "amount_paid": 5,
    "amount_issued": 0,
    "updated_at": 1234567800
  },
  { "quote": "bolt12-mint-quote", "unknown": true },
  { "quote": "bolt11-melt-quote", "unknown": true }
]
```

## Check endpoint accepts an empty quotes array

The following empty request is valid:

```json
{ "quotes": [] }
```

The mint returns an empty array:

```json
[]
```

## Check endpoint rejects duplicate quote IDs

The following request is invalid because the quote ID occurs twice:

```json
{ "quotes": ["quote_id_dup", "quote_id_dup"] }
```

Expected behavior:

- The mint rejects the entire request with error code `11016`.
- The mint does not return a partial or positional response.

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
- No quote's `amount_issued` is increased by partial processing.

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

- The mint rejects the request because quote IDs must be unique (error code `11016`).
- No outputs are signed.

## Batch mint rejects mixed payment methods

The following is an invalid request to `/v1/mint/bolt11/batch` where one quote is bolt11 and one quote is bolt12.

```json
{
  "quotes": [
    "019e6d5a-2347-7000-80fe-07ae8fa79774",
    "019e6d5a-2347-7000-8791-dbfba168f0ad"
  ],
  "quote_amounts": [5, 3],
  "outputs": [{ "amount": 8, "id": "keyset_1", "B_": "<blinded_message>" }]
}
```

Expected behavior:

- The mint rejects the request because all quotes must share the same payment method and match `{method}` in the URL.
- No outputs are signed.

## Batch mint rejects signatures array length mismatch

The following is an invalid batch mint request where `signatures` length does not match `quotes` length.

```json
{
  "quotes": [
    "019e6d5a-2347-7000-80fe-07ae8fa79774",
    "019e6d5a-2347-7000-8791-dbfba168f0ad"
  ],
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

## Batch mint with valid signature

The following is a valid NUT-29 batch mint request where the signature correctly covers all outputs in order. The quote has pubkey `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798` (sk = 1).

```shell
quote: "019e6d5a-2347-7000-8c81-a1e0dbf3299f"
pubkey: 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
msg_to_sign_bytes: 43617368755f4d696e7451756f74655369675f76310000002430313965366435612d323334372d373030302d386338312d613165306462663332393966000000010100000021036d6caac248af96f6afa7f904f550253a0f3ef3f5aa2fe6838a95b216691468e2000000010100000021021f8a566c205633d029094747d2e18f44e05993dda7a5f88f496078205f656e59
msg_hash: dad25acc587637206d73398894d337f983a0ca644746e8673727eaa0b29fa9b4
signature[0]: 0c39431338a0202568b9a1d4215c99f179cbb8ee5472ac5ae7133fbb8f99cafbb9e425ad33c60224c96b8f9f984f004379a18e9558468d129b6b03f0da6de162
```

```json
{
  "quotes": ["019e6d5a-2347-7000-8c81-a1e0dbf3299f"],
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
    "0c39431338a0202568b9a1d4215c99f179cbb8ee5472ac5ae7133fbb8f99cafbb9e425ad33c60224c96b8f9f984f004379a18e9558468d129b6b03f0da6de162"
  ]
}
```
