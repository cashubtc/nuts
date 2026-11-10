# NUT-29 Test Vectors

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

## Nutroot batch mint (v3 keysets)

A [v3 batch](../29.md#nutroot-transactions-v3-keysets) is one transaction with every quote as an input, so `signatures[i]` signs quote `i`'s own [NUT-00 input digest](00-tests.md#transaction-transcripts) over the shared transcript. Combining two locked quotes (`quote-mint-0002` for 5 sats, `quote-mint-0003` for 3 sats) into the [NUT-00 mint vector](00-tests.md#transaction-transcripts)'s 8-sat output, with the [NUT-13 quote lock keys](13-tests.md#version-3-secret-derivation) of counters `0` and `1` as the lock keys:

```json
{
  "transcript": "12003d0100010502000f71756f74652d6d696e742d303030320300210292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d20981204000012003d0100010302000f71756f74652d6d696e742d3030303303002102b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d04000021004b01000108020021022546ab0a2dee9f79510f4e20a4e3d9e894a97361047c594902573a7e64f9d701030020567b4ba980dd0c51c80919633b384c0764b30e5250c4a8b8e3957c9f4208cdee",
  "digest": "8203006b339dd16a3f6293c0f300bebb3c9ad620755477b1372c0fa479540c72"
}
```

The per-quote digests and signatures; neither signature verifies against the shared `digest` or at the other input:

```json
[
  {
    "quote_id": "quote-mint-0002",
    "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
    "input_id": "8c7f916779dfba1b7ea2e0d3e69d1ee7eed1895af2891406fe8bdb7fbe0f39aa",
    "input_digest": "5b87defd8dadbd2b0faf359f53b00a74b0642e5b91dd4046e0183738a812ed13",
    "signature": "badda23b373f0d1da963af4d424dbbbccce933ba0c81bc3e2c8ade13decdad8df57ca75efcb4eaa2e02eee9bd43066fce76fee22599f4a513354c138efa6bfb6"
  },
  {
    "quote_id": "quote-mint-0003",
    "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
    "input_id": "f7a60306c44e910fd5dea355541c4a4bb251220690688279bf08e7d19b3e9e45",
    "input_digest": "ac0d58749a343394a0fe5605771be16466ece1ecb331fa1aae0c92ac00136c13",
    "signature": "f272dca3c46470511b4ac1ab47a2135d1c7a6af4b6b49ec7c1d120f7704888cce5af8f2026c548a2d5201aebe384f2b798a2c1e439c89d9decc915bc890a4474"
  }
]
```
