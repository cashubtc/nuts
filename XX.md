# NUT-XX: Transactions

`optional`

`depends on: NUT-04 NUT-05 NUT-10`

---

This document describes a single endpoint that carries any [NUT-10][10] transaction: proofs and paid mint quotes in, blinded messages, a melt quote and change quotes out, in one request. The fixed-shape endpoints of [NUT-03][03], [NUT-04][04] and [NUT-05][05] remain for the operations they name; this endpoint carries those and every other combination, for example paying an invoice straight from a paid mint quote, or minting a quote and consolidating proofs in one swap.

## Request

```http
POST https://mint.host:3338/v1/transaction
```

The request is the [transaction transcript](10.md#the-transaction-transcript) in JSON, one array per container type:

```json
{
  "proof_inputs": <Array[Proof]>,
  "mint_quote_inputs": <Array[QuoteInput]>,
  "blinded_outputs": <Array[BlindedMessage]>,
  "melt_quote_outputs": <Array[MeltOutput]>,
  "change_quote_outputs": <Array[ChangeOutput]>,
  "prefer_async": <bool> // optional: false if omitted
}
```

where `proof_inputs` and `blinded_outputs` are as in [NUT-00][00], and a `QuoteInput` is a paid mint quote ([NUT-04][04]), the amount this transaction issues against it, and its witness:

```json
{
  "quote": <str>,
  "amount": <int>,
  "witness": <str>
}
```

`witness` has the same grammar as `Proof.witness` ([NUT-10](10.md#witnesses)): a key-path signature or a script-path witness over the quote input's [input digest](10.md#the-transaction-transcript).

A `MeltOutput` is a melt quote ([NUT-05][05]), the fee reserve this transaction commits to it, and for a quote offering `fee_options` ([NUT-30][30]) the selected fee option:

```json
{
  "quote": <str>,
  "fee_reserve": <int>,
  "fee_index": <int> // only if the quote offers fee_options
}
```

A `ChangeOutput` is a [change quote](#change-quote) this transaction creates: its lock key, a 33-byte compressed secp256k1 public key, and its amount:

```json
{
  "pubkey": <hex_str>,
  "amount": <int> // omitted on the remainder quote
}
```

Any array **MAY** be empty or omitted. A blinded message with `amount` `0` **MUST** be rejected: change goes to a change quote.

### Rules

- The transaction **MUST** have at least one input and one output, and **MUST NOT** repeat a proof `Y`, a mint quote id ([NUT-10][10]) or a `B_` ([NUT-00][00]).
- Every v3 input **MUST** carry a witness over its input digest; pre-v3 proofs keep their own rules, per [NUT-10](10.md#the-signing-rule). A pre-v3 proof with `SIG_ALL` ([NUT-11][11]) **MUST** be rejected: NUT-11 defines no `SIG_ALL` message for this endpoint.
- Every mint quote **MUST** be locked and in the transaction's unit. Its `amount` **MUST** be positive and **MUST NOT** exceed its mintable amount, `amount_paid - amount_issued` ([NUT-04][04]).
- All `blinded_outputs` **MUST** share one keyset in the transaction's unit ([NUT-04](04.md#nutroot-transactions-v3-keysets)).
- A change quote output with an `amount` **MUST** be positive. At most one change quote output **MAY** omit `amount`: the **remainder quote**, which takes the [balance](#balance) after settlement. Lock keys **MUST NOT** repeat within the request or name an existing [change quote](#change-quote).
- `melt_quote_outputs` **MUST NOT** hold more than one quote; multi-melt is reserved for future specification. The quote **MUST** be in the transaction's unit, and its method is the one it was quoted under. Its `fee_reserve` **MUST** equal the quote's `fee_reserve`, or the `fee_reserve` of the entry its `fee_index` names.
- A transaction with a melt quote and `blinded_outputs` **MUST** carry a remainder quote: the outputs cannot be signed if their keyset is inactivated before the payment settles ([NUT-02](02.md#active-keysets)), and the remainder quote is where their value goes.

### Balance

```
amount_in  = sum(proof_inputs) + sum(mint quote input amounts)
amount_out = sum(blinded_outputs) + sum(change quote output amounts) + melt.amount + melt.fee_reserve + fee
change     = amount_in - amount_out + melt.fee_reserve - melt_fee_paid
```

Proofs are spent in full. Each quote's `amount_issued` grows by its input `amount`, as in a partial mint ([NUT-04][04]), and the remainder stays mintable. `fee` is the input fee of the proofs ([NUT-02][02]) plus the [quote input fee](#quote-input-fee), and `amount_out` includes it. `melt_fee_paid` is what the payment actually cost, known only at settlement; it never exceeds `melt.fee_reserve`.

Without a remainder quote, `amount_in` **MUST** equal `amount_out`. With one, `amount_in` **MUST NOT** be less than `amount_out`, and after settlement the balance is returned as `change`, the remainder quote's amount.

A melt output without a remainder quote leaves its unspent fee reserve with the mint, as in a [NUT-05][05] melt without change outputs.

### Settlement

A transaction with a melt quote follows [NUT-05][05]'s pending and settlement handling, including `prefer_async`: the proofs and each quote input's `amount` are pending while the payment is in flight, the blinded messages are signed and the change quotes created only once it succeeds, and a failed payment leaves the proofs unspent and the quotes' mintable amounts untouched.

Before it initiates the payment, the mint **MUST** complete every check that signing the blinded messages and creating the change quotes depend on, so that once the payment succeeds only keyset inactivation can prevent settlement.

If the keyset of `blinded_outputs` has been inactivated by the time the payment settles, the mint cannot sign them ([NUT-02](02.md#active-keysets)). It then settles as if the request had no `blinded_outputs`: `signatures` is empty and their amount goes to the remainder quote. A transaction with no melt quote settles at once.

The mint **MUST** keep a record of every transaction it accepts, keyed by its transaction digest ([NUT-10](10.md#the-transaction-transcript)), holding the state and, once settled, the signatures and change quotes. The digest is the transaction's id: the wallet computes it to sign, and the mint computes it to verify.

## Change quote

On settlement, the mint creates for each change quote output a [NUT-04][04] mint quote with method `change`, in the transaction's unit, locked to its `pubkey`, with `amount_paid` and a method-specific `amount` equal to the output's `amount`, or to `change` for the remainder quote, and `request` the transaction digest. The method name `change` is reserved for these quotes. A remainder quote with zero change is not created.

Its id is derived from the lock key, not assigned:

```
quote_id = hex(tagged_hash("Cashu_QuoteId", pubkey))
```

with `tagged_hash` as in [NUT-10](10.md#nutroot-secrets-v3-keysets) over the 33-byte compressed key. One lock key therefore names one change quote: the mint **MUST** reject a transaction naming a lock key whose change quote exists or is held for a pending transaction. A `template` leaf ([NUT-10](10.md#condition-leaves)) naming change quotes can therefore be exercised only once.

A seeded wallet **SHOULD** derive its own change quote lock keys per [NUT-13](13.md#v3-message) with `derivation_type_byte` `0x04`. A wallet that lost its state can recover them without their ids: derive lock keys by counter, fetch each derived id, and stop after a run of unknown ids, as the [NUT-13](13.md#restore-from-seed-phrase) restore procedure does for proofs over [NUT-09][09].

A change quote is fetched at `GET /v1/mint/quote/change/{quote_id}` and redeemed like any locked quote: at `POST /v1/mint/change`, or as a quote input to another transaction. There is no `POST /v1/mint/quote/change`; only a transaction creates one.

## Response

```json
{
  "digest": <hex_str>,
  "state": <str_enum[STATE]>,
  "signatures": <Array[BlindSignature]>,
  "melt_quotes": <Array[MeltQuoteResponse]>,
  "change_quotes": <Array[MintQuoteResponse|null]>
}
```

- `digest` is the transaction digest.
- `state` is `PENDING` while a melt payment is in flight, `PAID` once the transaction has settled, or `FAILED` if the payment failed and the inputs were released.
- `signatures` has one blind signature per element of `blinded_outputs`, in request order. It is empty unless `state` is `PAID`.
- `melt_quotes` holds the [NUT-05][05] melt quote response for each entry of the request's `melt_quote_outputs`, in order, and is empty if there were none. Its `change` field is not used.
- `change_quotes` holds one entry per element of the request's `change_quote_outputs`, in order: the quote's [NUT-04][04] response once `state` is `PAID`, and `null` otherwise, including a remainder quote with zero change.

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
[09]: 09.md
[10]: 10.md
[11]: 11.md
[30]: 30.md
