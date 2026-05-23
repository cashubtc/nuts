# NUT-XX: Payjoin for Onchain Payment Method

`optional`

`depends on: NUT-04 NUT-05 NUT-20 NUT-30`

---

This document describes Payjoin support for the `onchain` payment method. It is
an extension of [NUT-30][30] and uses [BIP77][bip77] Payjoin v2.

If `payjoin` is present, the payer **MAY** attempt Payjoin and **MAY** fall back
to the direct NUT-30 payment. The payer is the wallet for mint quotes and the
mint for melt quotes.

## Types

### `Payjoin`

```json
{
  "endpoint": <str>,
  "ohttp_keys": <str>,
  "receiver_key": <str>,
  "expires_at": <int>
}
```

When `payjoin` is present, all fields in `Payjoin` are required:

- `endpoint` is the BIP77 mailbox endpoint URL, without receiver fragment
  parameters. When assembled into a `pj` URI parameter, the endpoint value
  **MUST** be encoded according to BIP77.
- `ohttp_keys` is the BIP77 `OH` value encoding the OHTTP key material needed by
  the sender. The value excludes the `OH1` parameter key and separator.
- `receiver_key` is the BIP77 `RK` value encoding the receiver session key. The
  value excludes the `RK1` parameter key and separator.
- `expires_at` is the decoded BIP77 `EX` session expiration as a Unix timestamp.
  When assembled into a `pj` URI parameter, it **MUST** be encoded as the BIP77
  `EX` fragment parameter. The Payjoin parameters **MUST NOT** be used after
  this timestamp.

> [!NOTE]
>
> Cashu API fields do not carry a BIP21 or BIP321 URI. Wallets that need one
> **SHOULD** assemble `pj` from `payjoin` according to BIP77.

## Mint Quote

For the `onchain` method, the wallet includes the following specific
`PostMintQuoteOnchainRequest` data:

```json
{
  "unit": <str_enum[UNIT]>,
  "pubkey": <str>
}
```

The mint responds with a `PostMintQuoteOnchainResponse` that can include
`payjoin`:

```json
{
  "quote": <str>,
  "request": <str>,
  "unit": <str_enum[UNIT]>,
  "expiry": <int|null>,
  "pubkey": <str>,
  "amount_paid": <int>,
  "amount_issued": <int>,
  "payjoin": <Payjoin|null> // Optional
}
```

Where:

- `payjoin` is optional Payjoin parameters for this quote
- `payjoin.expires_at` **MUST** be less than or equal to `expiry` if `expiry` is
  not `null`

Quote state responses use the same `PostMintQuoteOnchainResponse` shape. If
`payjoin` was provided in the mint quote response, the mint **MUST** include the
same `payjoin` value in quote state responses until the quote expires.

### Example

**Request**:

```json
{
  "unit": "sat",
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac"
}
```

**Response**:

```json
{
  "quote": "DSGLX9kevM...",
  "request": "bc1q...",
  "unit": "sat",
  "expiry": 1701704757,
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "amount_paid": 0,
  "amount_issued": 0,
  "payjoin": {
    "endpoint": "HTTPS://PAYJOIN.EXAMPLE/TXJCGKTKXLUUZ",
    "ohttp_keys": "QYPM59NK2LXXS4890SUAXXYT25Z2VAPHP0X7YEYCJXGWAG6UG9ZU6NQ",
    "receiver_key": "Q0DJS3VVDXWQQTLQ8022QGXSX7ML9PHZ6EDSF6AKEWQG758JPS2EV",
    "expires_at": 1701704757
  }
}
```

## Minting tokens

The wallet mints tokens as in NUT-30. A mint quote can be paid by either a
direct transaction to `request` or a Payjoin transaction. For Payjoin, a
confirmed transaction can increase `amount_paid` only by the value of eligible
outputs that are spendable by the mint and explicitly associated with the quote.
Receiver-controlled outputs unrelated to the quote **MUST NOT** increase
`amount_paid`.

## Mint Settings

A `payjoin.receive` option **SHOULD** be set to indicate whether the `onchain`
payment method backend supports receiving Payjoin payments.

If `payjoin.receive` is absent or `false`, wallets **SHOULD** treat receiving
Payjoin payments as unsupported and use plain NUT-30 minting.

### Example `MintMethodSetting`

```json
{
  "method": "onchain",
  "unit": <str>,
  "min_amount": <int|null>,
  "max_amount": <int|null>,
  "options": {
    "confirmations": <int>,
    "payjoin": {
      "receive": true
    }
  }
}
```

## Melt Quote

For the `onchain` method, the wallet includes the following specific
`PostMeltQuoteOnchainRequest` data:

```json
{
  "request": <str>,
  "unit": <str_enum[UNIT]>,
  "amount": <int>,
  "payjoin": <Payjoin|null> // Optional
}
```

Where:

- `payjoin` is optional Payjoin parameters for this quote
- `request` is the fallback Bitcoin address that should receive the onchain
  payment
- if `payjoin` is present and `payjoin.expires_at` is already expired, the mint
  **MUST** reject the quote request

The mint responds with a `PostMeltQuoteOnchainResponse`:

```json
{
  "quote": <str>,
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "state": <str_enum[STATE]>,
  "expiry": <int>,
  "request": <str>,
  "fee_options": [
    {
      "fee_index": <int>,
      "fee_reserve": <int>,
      "estimated_blocks": <int>
    }
  ],
  "selected_fee_index": <int|null>,
  "outpoint": <str|null>,
  "payjoin": <Payjoin|null> // Optional
}
```

If `payjoin` is present in the response, it **MUST** be identical to the
accepted `PostMeltQuoteOnchainRequest.payjoin`. If the mint declines Payjoin, it
**MAY** omit `payjoin` from the response and process the quote as a plain NUT-30
melt quote.

Quote state responses and melt responses use the same extended
`PostMeltQuoteOnchainResponse` shape. If `payjoin` was accepted for the quote,
the mint **MUST** include the same `payjoin` value in quote state responses and
melt responses.

### Example

**Request**:

```json
{
  "request": "bc1q...",
  "unit": "sat",
  "amount": 666666,
  "payjoin": {
    "endpoint": "HTTPS://PAYJOIN.EXAMPLE/TXJCGKTKXLUUZ",
    "ohttp_keys": "QYPM59NK2LXXS4890SUAXXYT25Z2VAPHP0X7YEYCJXGWAG6UG9ZU6NQ",
    "receiver_key": "Q0DJS3VVDXWQQTLQ8022QGXSX7ML9PHZ6EDSF6AKEWQG758JPS2EV",
    "expires_at": 1701704757
  }
}
```

**Response**:

```json
{
  "quote": "TRmjduhIsPxd...",
  "amount": 666666,
  "unit": "sat",
  "state": "UNPAID",
  "expiry": 1701704757,
  "request": "bc1q...",
  "fee_options": [
    {
      "fee_index": 0,
      "fee_reserve": 5000,
      "estimated_blocks": 1
    }
  ],
  "selected_fee_index": null,
  "outpoint": null,
  "payjoin": {
    "endpoint": "HTTPS://PAYJOIN.EXAMPLE/TXJCGKTKXLUUZ",
    "ohttp_keys": "QYPM59NK2LXXS4890SUAXXYT25Z2VAPHP0X7YEYCJXGWAG6UG9ZU6NQ",
    "receiver_key": "Q0DJS3VVDXWQQTLQ8022QGXSX7ML9PHZ6EDSF6AKEWQG758JPS2EV",
    "expires_at": 1701704757
  }
}
```

## Melting tokens

The wallet executes a melt quote as in NUT-30. If the quote has accepted
Payjoin parameters:

- the mint **SHOULD** attempt Payjoin
- the mint **MAY** pay `request` directly if Payjoin fails or expires
- the Payjoin transaction **MUST** satisfy the accepted fee constraints
- the mint **MUST** reject proposals that exceed the selected fee reserve
- `outpoint` **MUST** refer to the transaction that satisfied the quote

## Melt Settings

A `payjoin.send` option **SHOULD** be set to indicate whether the `onchain`
payment method backend supports sending Payjoin payments.

If `payjoin.send` is absent or `false`, wallets **SHOULD** treat sending Payjoin
payments as unsupported and create plain NUT-30 melt quotes.

### Example `MeltMethodSetting`

```json
{
  "method": "onchain",
  "unit": <str>,
  "min_amount": <int|null>,
  "max_amount": <int|null>,
  "options": {
    "payjoin": {
      "send": true
    }
  }
}
```

## Errors

If a request includes malformed or expired Payjoin parameters, the mint **MUST**
reject the request with error code `20010`.

See [Error Codes][errors].

[bip77]: https://bips.dev/77/
[30]: 30.md
[errors]: error_codes.md
