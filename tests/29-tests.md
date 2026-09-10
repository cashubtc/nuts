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

## Nutroot batch mint (v3 keysets)

A [v3 batch](../29.md#nutroot-transactions-v3-keysets) is one transaction with every quote as an input, so `signatures[i]` signs quote `i`'s own [NUT-10 input digest](10-tests.md#transaction-transcripts) over the shared transcript. Combining two locked quotes (`quote-mint-0002` for 5 sats, `quote-mint-0003` for 3 sats) into the [NUT-10 mint vector](10-tests.md#transaction-transcripts)'s 8-sat output, with the [NUT-20 v3 quote lock keys](20-test.md#deterministic-quote-locking-key-derivation-v3-keysets) of counters `0` and `1` as the lock keys:

```json
{
  "transcript": "0200160100010502000f71756f74652d6d696e742d303030320200160100010302000f71756f74652d6d696e742d3030303303005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "577f67746c7255f031f409601229309982b5a3ec1b32f1a5c75ad271346d0c32"
}
```

The per-quote digests and signatures; neither signature verifies against the shared `digest` or at the other input:

```json
[
  {
    "quote_id": "quote-mint-0002",
    "lock_pubkey": "039b390a9a298305cc43dbec906ceb1caae1187a8d16a3f45b945442ae7339d746",
    "input_id": "aaf0905f583d015ad1640e530c768797eab855034051e74fb7f725b5bdb96131",
    "input_digest": "ca742311db92f0829e44d3760d48a4ea1c524d58880a5fae3281cdeb54e9ce00",
    "signature": "52cdccf807eb622af34c5b31bff51db40971a49398d7f1d2b8b085e0772d3b76d5b4e4cdfeef409abb8505f09200a6e80f59bbebb6567958cc63ba0cfeb56444"
  },
  {
    "quote_id": "quote-mint-0003",
    "lock_pubkey": "0332ef3eb87a93da987406ed1fe96a44541ea0daa175e53e7ffc1155bb09b47b38",
    "input_id": "9976dbe45223a102e176fa2ede6973244157c5b82257d6e3e0f4977b32f0c706",
    "input_digest": "6d0c4ea825ae8550ef7438299079b4bc656d67c480884475df5b425c8bca45c4",
    "signature": "7b041b52eed0c9568b8ddd58d779665765f28ceaa4e773389da789e5512d5eda850666b576c5e6955aad5ba43c5624f398e763a79e4199a3828f117d26cc1807"
  }
]
```
