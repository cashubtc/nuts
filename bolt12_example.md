# Example: Adding BOLT12 Support to NUTS

This document provides a reference implementation for adding BOLT12 (Lightning Network offers) as a new payment method to the NUTS standard. It follows the modular structure outlined in the redesigned NUT-04 and NUT-05.

## 1. Adding BOLT12 to NUT-04 (Minting tokens)

To add BOLT12 support for minting tokens, you would add a new section to NUT-04 like this:

### Payment Method: BOLT12

This section describes the specifics for the `bolt12` payment method, which uses Lightning Network offers.

#### Mint Quote - BOLT12

For the `bolt12` method, the wallet includes the following specific `PostMintQuoteBolt12Request` data:

```json
{
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "offer_id": <str>,         // Optional: client-provided identifier for the offer
  "description": <str>      // Optional: description for the offer
}
```

The mint responds with a `PostMintQuoteBolt12Response`:

```json
{
  "quote": <str>,
  "offer": <str>,            // The BOLT12 offer string
  "request": <str>,          // The BOLT12 invoice request string (once generated)
  "amount": <int>,
  "unit":  <str_enum[UNIT]>,
  "state": <str_enum[STATE]>,
  "expiry": <int>
}
```

The BOLT12 flow has an additional step compared to BOLT11. After receiving the offer, the wallet must generate an invoice request by sending a `POST /v1/mint/quote/bolt12/{quote_id}/request` with any required parameters for the offer:

```json
{
  "payer_note": <str>,      // Optional: note from the payer
  "quantity": <int>         // Optional: for offers that support quantities
}
```

The mint then updates the quote with the invoice request string in the `request` field.

#### Example - BOLT12

Request with curl:

```bash
curl -X POST http://localhost:3338/v1/mint/quote/bolt12 -d '{"amount": 10, "unit": "sat"}' -H "Content-Type: application/json"
```

Response:

```json
{
  "quote": "FL32jmfK89...",
  "offer": "lno1qcp4...",
  "request": null,
  "amount": 10,
  "unit": "sat",
  "state": "UNPAID",
  "expiry": 1701704757
}
```

Generate invoice request:

```bash
curl -X POST http://localhost:3338/v1/mint/quote/bolt12/FL32jmfK89.../request -d '{"payer_note": "Minting tokens"}' -H "Content-Type: application/json"
```

Updated quote response:

```json
{
  "quote": "FL32jmfK89...",
  "offer": "lno1qcp4...",
  "request": "lnr1qcp4...",
  "amount": 10,
  "unit": "sat",
  "state": "UNPAID",
  "expiry": 1701704757
}
```

The payment flow then continues the same as with BOLT11, with the client using `/v1/mint/bolt12` to mint tokens after payment is complete.

#### Settings for BOLT12

Add BOLT12 to the mint's settings for NUT-04:

```json
{
  "method": "bolt12",
  "unit": "sat",
  "min_amount": 0,
  "max_amount": 10000,
  "description": true,
  "supports_quantities": true
}
```

## 2. Adding BOLT12 to NUT-05 (Melting tokens)

To add BOLT12 support for melting tokens, you would add a new section to NUT-05 like this:

### Payment Method: BOLT12

This section describes the specifics for the `bolt12` payment method, which uses Lightning Network offers.

#### Melt Quote - BOLT12

For the `bolt12` method, the wallet includes the following specific `PostMeltQuoteBolt12Request` data:

```json
{
  "offer": <str>,            // The BOLT12 offer to pay
  "unit": <str_enum[UNIT]>,
  "options": {              // Optional
    "quantity": <int>,      // For offers that support quantities
    "payer_note": <str>    // Note to include with payment
  }
}
```

The mint responds with a `PostMeltQuoteBolt12Response`:

```json
{
  "quote": <str>,
  "offer": <str>,
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "fee_reserve": <int>,
  "state": <str_enum[STATE]>,
  "expiry": <int>,
  "payment_hash": <str|null>,
  "payment_preimage": <str|null>
}
```

Where `fee_reserve` is the additional fee reserve required for the Lightning payment. The mint expects the wallet to include `Proofs` of _at least_ `total_amount = amount + fee_reserve + fee` where `fee` is calculated from the keyset's `input_fee_ppk` as described in [NUT-02][02].

#### Melting Tokens - BOLT12

Just as with BOLT11, the wallet can include an optional `outputs` field in the melt request to receive change for overpaid Lightning fees:

```json
{
  "quote": <str>,
  "inputs": <Array[Proof]>,
  "outputs": <Array[BlindedMessage]> // Optional
}
```

The response format is similar to BOLT11, with the addition of a `payment_hash` field that's specific to BOLT12:

```json
{
  "quote": <str>,
  "offer": <str>,
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "fee_reserve": <int>,
  "state": <str_enum[STATE]>,
  "expiry": <int>,
  "payment_hash": <str>,
  "payment_preimage": <str>,
  "change": <Array[BlindSignature]> // Present if outputs were included and there's change
}
```

#### Example - BOLT12

Melt quote request:

```bash
curl -X POST https://mint.host:3338/v1/melt/quote/bolt12 -d \
'{"offer": "lno1qcp4...", "unit": "sat", "options": {"payer_note": "Testing BOLT12 melting"}}'
```

Melt quote response:

```json
{
  "quote": "B2mFduh45Pxd...",
  "offer": "lno1qcp4...",
  "amount": 10,
  "unit": "sat",
  "fee_reserve": 2,
  "state": "UNPAID",
  "expiry": 1701704757
}
```

Melt request:

```bash
curl -X POST https://mint.host:3338/v1/melt/bolt12 -d \
'{"quote": "B2mFduh45Pxd...", "inputs": [...]}'
```

Successful melt response:

```json
{
  "quote": "B2mFduh45Pxd...",
  "offer": "lno1qcp4...",
  "amount": 10,
  "unit": "sat",
  "fee_reserve": 2, 
  "state": "PAID",
  "expiry": 1701704757,
  "payment_hash": "8e37c2a0f857c9457a54532ed2c9726d5f7b0c730f27d345dc7c4a9a2092266d",
  "payment_preimage": "e9d25f88cfbb82aff6a53f0522d2c7dfe3e1c51db895889f63a201fbe2e27885"
}
```

#### Settings for BOLT12

Add BOLT12 to the mint's settings for NUT-05:

```json
{
  "method": "bolt12",
  "unit": "sat",
  "min_amount": 100,
  "max_amount": 10000,
  "supports_quantities": true,
  "supports_payer_note": true
}
```

## Conclusion

By following this modular approach, new payment methods like BOLT12 can be added to the NUTS standard without modifying the core flow. The consistent structure allows wallets and mints to implement new methods while maintaining backward compatibility.