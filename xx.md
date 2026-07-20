# NUT-XX: Quote Offers

`optional`

`depends on: NUT-04, NUT-05, NUT-20`

---

This NUT introduces a standardised format for quote offers. A quote offer is prepared by an operator (e.g. a teller, a point of sale, or a payment processor connected to the mint) and handed to a wallet, which uses it to create a mint or melt quote for itself. This enables payment methods where an operation is initiated by the counterparty instead of the wallet, without ever displaying a quote ID.

## Flow

1. The operator registers a ticket with the mint's payment backend, encodes it as a quote offer, and displays it to the wallet
2. The wallet scans the offer and requests a mint or melt quote from the mint, referencing the ticket
3. The mint accepts the first quote request referencing the ticket and rejects all subsequent ones
4. The operation proceeds as a regular mint ([NUT-04][04]) or melt ([NUT-05][05]) operation

## Quote Offer

A quote offer is defined as follows

```json
{
  "m": str,
  "o": str,
  "h": str,
  "u": str,
  "t": str,
  "a": int <optional>,
  "d": str <optional>,
  "e": int <optional>
}
```

Here, the fields are

- `m`: The URL of the mint
- `o`: The operation of the offer, either `"mint"` or `"melt"`
- `h`: The payment method to use
- `u`: The unit of the offer
- `t`: The ticket, an identifier for the offered operation issued by the mint's payment backend
- `a`: The amount of the offer (MUST be set if the method's quote request requires an amount)
- `d`: A human readable description that the wallet displays after scanning the offer
- `e`: The Unix timestamp until which the offer can be claimed

A ticket is single-use: it can be claimed by exactly one quote. The mint **MUST** reject a quote request whose parameters do not match the ticket.

## Claiming a mint offer

To claim a mint offer, the wallet requests a mint quote as described in [NUT-04][04], including the ticket:

```json
{
  "unit": <str_enum[UNIT]>,
  "amount": <int>,
  "pubkey": <str>,
  "ticket": <str>
}
```

`pubkey` is a [NUT-20][20] public key. It is required: the mint **MUST NOT** create a quote for a ticket without one. The wallet **SHOULD** derive it using the deterministic derivation described in [NUT-20][20]. The resulting quote is locked to the wallet's key and minting proceeds as described in [NUT-20][20].

> [!CAUTION]
> An offer is public once displayed. An attacker who scans it can claim the ticket first, but only with a quote locked to the attacker's own key. In that case the payer's claim fails visibly, and the operator voids the ticket and issues a new offer. The operator **MUST NOT** accept payment for an offer before the payer confirms that their wallet holds the claimed quote.

## Claiming a melt offer

To claim a melt offer, the wallet requests a melt quote as described in [NUT-05][05], using the ticket as the payment request:

```json
{
  "request": <str>, // the ticket
  "unit": <str_enum[UNIT]>
}
```

Melt requests for quotes claimed from an offer are always asynchronous (see [NUT-05][05]). The mint **MUST** return a `"PENDING"` state after validating the melt request, and the wallet **MUST** monitor the quote state until completion.

Since the quote ID of a claimed melt quote is known only to the wallet and the mint, the wallet can present it (or a code derived from it) as proof that it initiated the payment. The operator **MUST NOT** pay out before the melt quote is `"PENDING"` and **SHOULD** verify the payer's quote ID before paying out.

## Serialization

The quote offer is serialized using CBOR, encoded in `base64_urlsafe`, together with a prefix `cquote` and a version `A`:

`"cquote" + "A" + base64_urlsafe(CBOR(QuoteOffer))`

### Example

This is an example quote offer expressed as JSON:

```json
{
  "m": "https://mint.example.com",
  "o": "mint",
  "h": "branch",
  "u": "ora",
  "a": 500,
  "t": "0198c0ef-3f11-7000-a3f7-2f4b6e2d9c1a",
  "d": "Cash deposit"
}
```

This quote offer serializes to:

```sh
cquoteAp2FteBhodHRwczovL21pbnQuZXhhbXBsZS5jb21hb2RtaW50YWhmYnJhbmNoYXVjb3JhYWEZAfRhdHgkMDE5OGMwZWYtM2YxMS03MDAwLWEzZjctMmY0YjZlMmQ5YzFhYWRsQ2FzaCBkZXBvc2l0
```

## Errors

See [Error Codes][errors]:

- `20010`: Offer ticket is unknown or expired
- `20011`: Offer ticket has already been claimed

## Settings

The settings for this NUT indicate support for quote offers. They are part of the info response of the mint ([NUT-06][06]) which reads

```json
{
  "XX": {
    "supported": <bool>
  }
}
```

[04]: 04.md
[05]: 05.md
[06]: 06.md
[20]: 20.md
[errors]: error_codes.md
