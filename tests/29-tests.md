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

A [v3 batch](../29.md#nutroot-transactions-v3-keysets) is one transaction with every quote as an input, so `signatures[i]` signs quote `i`'s own [NUT-10 input digest](10-tests.md#transaction-transcripts) over the shared transcript. Combining two locked quotes (`quote-mint-0002` for 5 sats, `quote-mint-0003` for 3 sats) into the [NUT-10 mint vector](10-tests.md#transaction-transcripts)'s 8-sat output, with the [NUT-13 quote lock keys](13-tests.md#version-3-secret-derivation) of counters `0` and `1` as the lock keys:

```json
{
  "transcript": "0200160100010502000f71756f74652d6d696e742d303030320200160100010302000f71756f74652d6d696e742d3030303303005b0100010802002102b7e077d020fabed456a6be138a8e20e9ef40b44d873fa12c005b656eb0cf99f6030030b42a0bcc39598db1dca617aeea6bc367f2566636826dc961a54faae15b3b8d10afc1cb0206e70ab3b0e12c2b9478cd55",
  "digest": "7309fef139318f9dc3faa7ec0b92208e6ff231ad007c6c3fcfc80343b4ad5bb7"
}
```

The per-quote digests and signatures; neither signature verifies against the shared `digest` or at the other input:

```json
[
  {
    "quote_id": "quote-mint-0002",
    "lock_pubkey": "0292905560a6a511a13e383ee27e220aeffc85b7a7bc293e6935b1d3678d209812",
    "input_id": "aaf0905f583d015ad1640e530c768797eab855034051e74fb7f725b5bdb96131",
    "input_digest": "04b6a1306d1a12640a91421b0117bbdf2880e6f186a0cbd2211db077e82019f0",
    "signature": "ee4e7131dad86f2d5c3f25f021e437cdeefe68ceff2bbe95e4a36974f4d78358b633ed7eb2cab2cac0d36f05669b1568c4b8b86cd4274cba0a596e5d87d63f6b"
  },
  {
    "quote_id": "quote-mint-0003",
    "lock_pubkey": "02b357c1ec7bdd73e4ede25d68619ee607c632409e89bcc518a82370b3f499615d",
    "input_id": "9976dbe45223a102e176fa2ede6973244157c5b82257d6e3e0f4977b32f0c706",
    "input_digest": "27aa267c0541b638c93b3d8c6324005654e9ac2663795c100c1d7dc8370dc2c5",
    "signature": "83a816f0bb9137e3523711e6136ce565229d0bd45ef2d0090a89b1c653046fc5fa067210310990ab3aed1ffabcb24a67f2db7d7700cc1243c5de20017b717728"
  }
]
```
