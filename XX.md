# NUT-XX: Payment Method: Onchain

`optional`

`depends on: NUT-04 NUT-05 NUT-20`

---

This document describes minting and melting ecash with the `onchain` payment method, which uses Bitcoin onchain payments. It is an extension of [NUT-04][04] and [NUT-05][05] which cover the protocol steps of minting and melting ecash shared by any supported payment method.

## Mint Quote

For the `onchain` method, the wallet includes the following specific `PostMintQuoteOnchainRequest` data:

```json
{
  "unit": <str_enum[UNIT]>,
  "pubkey": <str>
}
```

> **Note:** A [NUT-20][20] `pubkey` is required in this NUT and the mint **MUST NOT** issue a mint quote if one is not included.

> **Privacy:** To prevent linking multiple mint quotes together, wallets **SHOULD** generate a unique public key for each mint quote request.

The mint responds with a `PostMintQuoteOnchainResponse`:

```json
{
  "quote": <str>,
  "request": <str>,
  "unit": <str_enum[UNIT]>,
  "expiry": <int|null>,
  "pubkey": <str>,
  "amount_paid": <int>,
  "amount_issued": <int>
}
```

Where:

- `quote` is the quote ID
- `request` is the Bitcoin address to send funds to
- `expiry` is the Unix timestamp until which the mint quote is valid
- `pubkey` is the public key from the request
- `amount_paid` is the total confirmed amount paid to the request
- `amount_issued` is the amount of ecash that has been issued for the given mint quote

If `expiry` is not `null`, the wallet **SHOULD NOT** send payments to the request after `expiry`. Mints **MUST** keep monitoring transactions they detected before `expiry` until the transaction reaches the required number of confirmations or is evicted or replaced. Payments first detected by the mint after `expiry` **MUST NOT** increase `amount_paid`.

### Example Response

```json
{
  "quote": "DSGLX9kevM...",
  "request": "bc1q...",
  "unit": "sat",
  "expiry": 1701704757,
  "pubkey": "03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "amount_paid": 0,
  "amount_issued": 0
}
```

### Minting Tokens

The quote state will only update to show `amount_paid` once the Bitcoin transaction has reached the minimum number of confirmations specified in the mint's settings.

For the `onchain` method, the wallet includes the following specific `PostMintOnchainRequest` data:

```json
{
  "quote": <str>,
  "outputs": <Array[BlindedMessage]>,
  "signature": <str>
}
```

Since onchain mint quotes require a `pubkey`, the wallet **MUST** include a [NUT-20][20] `signature` in the mint request.

## Multiple Deposits

Onchain addresses can receive multiple payments, allowing the wallet to mint multiple times for one quote. The wallet can call the check onchain endpoint, where the mint will return the `PostMintQuoteOnchainResponse` including `amount_paid` and `amount_issued`. The difference between these values represents how much the wallet can mint by calling the mint endpoint. Wallets `MAY` mint any amount up to this available difference; in particular, they can mint less than the amount mintable. Mints `MUST` accept mint requests whose total output amount is less than or equal to (`amount_paid` - `amount_issued`).

## Mint Settings

A `confirmations` option **SHOULD** be set to indicate the minimum depth in the blockchain for a transaction to be considered confirmed.

### Example `MintMethodSetting`

```json
{
  "method": "onchain",
  "unit": <str>,
  "min_amount": <int|null>,
  "max_amount": <int|null>,
  "options": {
    "confirmations": <int>
  }
}
```

## Melt Quote

For the `onchain` method, the wallet includes the following specific `PostMeltQuoteOnchainRequest` data:

```json
{
  "request": <str>,
  "unit": <str_enum[UNIT]>,
  "amount": <int>
}
```

Where:

- `request` is the Bitcoin address that should receive the onchain payment
- `unit` is the unit the wallet would like to pay with
- `amount` is the amount to send in the specified unit

Unlike other melt methods, a single `onchain` melt quote can contain multiple fee options for the same payment. This allows the wallet to choose between different fee and confirmation estimates while preserving a single quote ID.

The mint responds with a `PostMeltQuoteOnchainResponse`:

```json
{
  "quote": <str>,
  "request": <str>,
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "fee_options": [
    {
      "fee": <int>,
      "estimated_blocks": <int>
    }
  ],
  "selected_estimated_blocks": <int|null>,
  "state": <str_enum[STATE]>,
  "expiry": <int>,
  "outpoint": <str|null>
}
```

Each item in `fee_options` represents one available fee and confirmation estimate for the same payment. The wallet selects one of these options when executing the melt quote by including the option's `estimated_blocks` value in the melt request. The mint **MUST** return at least one `fee_options` item and **MUST NOT** return multiple `fee_options` items with the same `estimated_blocks` value in one quote. The returned `fee_options` are fixed for the lifetime of the quote.

Where `fee` is the absolute onchain transaction fee for that option, and `estimated_blocks` is the estimated number of blocks until confirmation. `selected_estimated_blocks` is `null` before the quote is executed and is set to the selected `estimated_blocks` value once the wallet executes the quote. The mint expects the wallet to include `Proofs` of exactly `total_amount = amount + selected_fee + input_fee` where `selected_fee` is the `fee` from the selected `fee_options` item and `input_fee` is calculated from the keyset's `input_fee_ppk` as described in [NUT-02][02]. [NUT-08][08] does not apply to the `onchain` melt method, so the mint **MUST NOT** return `change` outputs and **MUST** reject melt requests whose input amount is not exactly `total_amount`.

`state` is an enum string field with possible values `"UNPAID"`, `"PENDING"`, `"PAID"`:

- `"UNPAID"` means that the transaction has not been broadcast yet.
- `"PENDING"` means that the transaction is being processed by the mint but not yet mined.
- `"PAID"` means that the transaction has been mined.

`outpoint` is the transaction ID and output index of the payment in the format `txid:vout`, present once the transaction has been broadcast.

### Melting Tokens

For the `onchain` method, the wallet includes the following specific `PostMeltOnchainRequest` data:

```json
{
  "quote": <str>,
  "estimated_blocks": <int>,
  "inputs": <Array[Proof]>
}
```

Where `estimated_blocks` is one of the values returned in the quote's `fee_options`. The mint **MUST** reject a melt request with an `estimated_blocks` value that was not returned in the quote. Once `selected_estimated_blocks` is set, the mint **MUST NOT** execute the quote again with a different `estimated_blocks` value.

### Example Response

```json
{
  "quote": "TRmjduhIsPxd...",
  "request": "bc1q...",
  "amount": 100000,
  "unit": "sat",
  "fee_options": [
    {
      "fee": 5000,
      "estimated_blocks": 1
    },
    {
      "fee": 2000,
      "estimated_blocks": 6
    },
    {
      "fee": 800,
      "estimated_blocks": 144
    }
  ],
  "selected_estimated_blocks": null,
  "state": "UNPAID",
  "expiry": 1701704757,
  "outpoint": null
}
```

The wallet selects one of the returned `fee_options` by including that option's `estimated_blocks` value in the melt request. Once the quote is executed, quote state checks return the same response shape with `selected_estimated_blocks` set to the selected value and `outpoint` set once the transaction has been broadcast.

### Example `MeltMethodSetting`

```json
{
  "method": "onchain",
  "unit": <str>,
  "min_amount": <int|null>,
  "max_amount": <int|null>
}
```

[02]: 02.md
[04]: 04.md
[05]: 05.md
[08]: 08.md
[20]: 20.md
