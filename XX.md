# NUT-XX: Transactions

`optional`

`depends on: NUT-04 NUT-05 NUT-10`

---

This document describes a single endpoint that carries any [NUT-10][10] transaction: proofs and paid mint quotes in, blinded messages, a melt quote and a change quote out, in one request. The fixed-shape endpoints of [NUT-03][03], [NUT-04][04] and [NUT-05][05] remain for the operations they name; this endpoint carries those and every other combination, for example paying an invoice straight from a paid mint quote, or minting a quote and consolidating proofs in one swap.

## Request

```http
POST https://mint.host:3338/v1/transaction
```

The request is the [transaction transcript](10.md#the-transaction-transcript) in JSON, one array per container type:

```json
{
  "proofs": <Array[Proof]>,
  "quotes": <Array[QuoteInput]>,
  "blinded_messages": <Array[BlindedMessage]>,
  "melts": <Array[str]>,
  "change": <hex_str>, // optional
  "prefer_async": <bool> // optional: false if omitted
}
```

where `proofs` and `blinded_messages` are as in [NUT-00][00], `melts` holds melt quote ids ([NUT-05][05]), `change` is the lock key of the [change quote](#change-quote), a 33-byte compressed secp256k1 public key, and a `QuoteInput` is a paid mint quote ([NUT-04][04]), the amount this transaction issues against it, and its witness:

```json
{
  "quote": <str>,
  "amount": <int>,
  "witness": <str>
}
```

`witness` has the same grammar as `Proof.witness` ([NUT-10](10.md#witnesses)): a key-path signature or a script-path witness over the quote input's [input digest](10.md#the-transaction-transcript).

Any array **MAY** be empty or omitted. A blinded message with `amount` `0` **MUST** be rejected: change goes to the change quote.

### Rules

- The transaction **MUST** have at least one input and one output, and **MUST NOT** repeat a proof `Y` or a mint quote id ([NUT-10][10]).
- Every v3 input **MUST** carry a witness over its input digest; pre-v3 proofs keep their own rules, per [NUT-10](10.md#the-signing-rule). A pre-v3 proof with `SIG_ALL` ([NUT-11][11]) **MUST** be rejected: NUT-11 defines no `SIG_ALL` message for this endpoint.
- Every mint quote **MUST** be locked and in the transaction's unit. Its `amount` **MUST** be positive and **MUST NOT** exceed its mintable amount, `amount_paid - amount_issued` ([NUT-04][04]).
- All `blinded_messages` **MUST** share one keyset in the transaction's unit ([NUT-04](04.md#nutroot-transactions-v3-keysets)).
- `melts` **MUST NOT** hold more than one quote; multi-melt is reserved for future specification. The quote **MUST** be in the transaction's unit, and its method is the one it was quoted under.

### Balance

```
inputs    = sum(proofs) + sum(quote amounts)
required  = sum(blinded_messages) + melt.amount + melt.fee_reserve + fee
```

Proofs are spent in full. Each quote's `amount_issued` grows by its input `amount`, as in a partial mint ([NUT-04][04]), and the remainder stays mintable. `fee` is the input fee of the proofs ([NUT-02][02]) plus the [quote input fee](#quote-input-fee).

Without a `change` output, `inputs` **MUST** equal `required`. With a `change` output, `inputs` **MUST NOT** be less than `required`, and after settlement the balance is returned as change:

```
change = inputs - fee - sum(blinded_messages) - melt.amount - fee_paid
```

A melt output without a `change` output leaves its unspent fee reserve with the mint, as in a [NUT-05][05] melt without change outputs.

### Settlement

A transaction with a melt quote follows [NUT-05][05]'s pending and settlement handling, including `prefer_async`: the proofs and each quote input's `amount` are pending while the payment is in flight, the blinded messages are signed and the change quote created only once it succeeds, and a failed payment leaves the proofs unspent and the quotes' mintable amounts untouched. A transaction with no melt quote settles at once.

The mint **MUST** keep a record of every transaction it accepts, keyed by its transaction digest ([NUT-10](10.md#the-transaction-transcript)), holding the state and, once settled, the signatures and change quote. The digest is the transaction's id: the wallet computes it to sign, and the mint computes it to verify.

## Change quote

On settlement with positive change, the mint creates a [NUT-04][04] mint quote with method `change`, in the transaction's unit, locked to the `change` key, with `amount_paid` and a method-specific `amount` equal to the change, and `request` the transaction digest. Its id is a fresh quote id, as for any mint quote. The method name `change` is reserved for these quotes. With zero change, no quote is created.

A change quote is fetched at `GET /v1/mint/quote/change/{quote_id}` and redeemed like any locked quote: at `POST /v1/mint/change`, or as a quote input to another transaction. There is no `POST /v1/mint/quote/change`; only a transaction creates one.

A wallet that lost its state finds its change quotes by lock key, like any locked quote, under the method `change`.

## Response

```json
{
  "digest": <hex_str>,
  "state": <str_enum[STATE]>,
  "signatures": <Array[BlindSignature]>,
  "melts": <Array[MeltQuoteResponse]>,
  "change": <MintQuoteResponse|null>
}
```

- `digest` is the transaction digest.
- `state` is `PENDING` while a melt payment is in flight, `PAID` once the transaction has settled, or `FAILED` if the payment failed and the inputs were released.
- `signatures` has one blind signature per element of `blinded_messages`, in request order. It is empty unless `state` is `PAID`.
- `melts` holds the [NUT-05][05] melt quote response for each entry of the request's `melts`, in order, and is empty if there were none. Its `change` field is not used.
- `change` is the change quote's [NUT-04][04] response once `state` is `PAID` and the change is positive, and `null` otherwise.

### Fetching a transaction

```http
GET https://mint.host:3338/v1/transaction/{digest}
```

returns the same response for a transaction the mint holds. Wallets poll it, not the melt quote, for a pending transaction. A `POST` whose digest the mint holds as `PENDING` or `PAID` **MUST** return that record rather than treat the inputs as spent again, so a wallet that lost the response can safely resend the request. A `FAILED` transaction **MAY** be resubmitted, and replaces its record.

## Quote input fee

A mint **MAY** charge for quote inputs so that minting and melting in one transaction is not cheaper than doing it in two. A quote input contributes `popcount(amount) * quote_input_fee_ppk` to the ppk sum, the fee its `amount` would carry as proofs of the minimal split, and [NUT-02][02]'s single rounding applies to the whole transaction:

```
fee = (sum(proof input_fee_ppk) + sum(popcount(quote amount) * quote_input_fee_ppk) + 999) // 1000
```

A mint that does not charge advertises `0`.

## Settings

```json
{
  "XX": {
    "supported": <bool>,
    "quote_input_fee_ppk": <int>
  }
}
```

[00]: 00.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[10]: 10.md
[11]: 11.md
