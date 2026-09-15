# NUT-XX: Transactions

`optional`

`depends on: NUT-04 NUT-05 NUT-08 NUT-10`

---

This document describes a single endpoint that carries any [NUT-10][10] transaction: proofs and paid mint quotes in, blinded messages and a melt quote out, in one request. The fixed-shape endpoints of [NUT-03][03], [NUT-04][04] and [NUT-05][05] remain for the operations they name; this endpoint carries those and every other combination, for example paying an invoice straight from a paid mint quote, or minting a quote and consolidating proofs in one swap.

## Request

```http
POST https://mint.host:3338/v1/transaction
```

The request is the [transaction transcript](10.md#the-transaction-transcript) in JSON, one array per container type:

```json
{
  "proofs": <Array[Proof]>,
  "quotes": <Array[QuoteInput]>,
  "outputs": <Array[BlindedMessage]>,
  "melts": <Array[str]>,
  "prefer_async": <bool> // optional: false if omitted
}
```

where `proofs` and `outputs` are as in [NUT-00][00], `melts` holds melt quote ids ([NUT-05][05]), and a `QuoteInput` is a paid mint quote ([NUT-04][04]) with its witness:

```json
{
  "quote": <str>,
  "witness": <str>
}
```

`witness` has the same grammar as `Proof.witness` ([NUT-10](10.md#witnesses)): a key-path signature or a script-path witness over the quote input's [input digest](10.md#the-transaction-transcript). The quote's face `amount` is not sent; the mint holds it and the transcript commits it.

Any array **MAY** be empty or omitted. A blinded message with `amount` `0` is a blank change output ([NUT-08][08]); every other output has a fixed amount.

### Rules

- The transaction **MUST** have at least one input and one output, and **MUST NOT** repeat a proof `Y` or a mint quote id ([NUT-10][10]).
- Every v3 input **MUST** carry a witness over its input digest; pre-v3 proofs keep their own rules, per [NUT-10](10.md#the-signing-rule).
- Every mint quote **MUST** be locked, in the transaction's unit, and have a positive mintable amount, `amount_paid - amount_issued` ([NUT-04][04]).
- All fixed and blank `outputs` **MUST** share one keyset in the transaction's unit ([NUT-04](04.md#nutroot-transactions-v3-keysets)).
- `melts` **MUST NOT** hold more than one quote; multi-melt is reserved for future specification. The quote **MUST** be in the transaction's unit, and its method is the one it was quoted under.

### Balance

```
required  = sum(fixed outputs) + melt.amount + melt.fee_reserve + fee
draw      = required - sum(proofs)
```

`fee` is the input fee of the proofs ([NUT-02][02]) plus the [quote input fee](#quote-input-fee). `draw` is what the transaction takes from the mint quotes: it **MUST NOT** exceed their combined mintable amount, and it is taken from the quotes in the order listed, each in full until the last, which is drawn in part. Quotes are drawn exactly as a partial mint draws them ([NUT-04][04]): `amount_issued` grows by each quote's draw and the remainder stays mintable.

If the proofs alone exceed `required`, the excess is change. After settlement the mint imprints `change = sum(proofs) + draw - fee - sum(fixed outputs) - melt.amount - fee_paid` into the blank outputs per [NUT-08][08]. A transaction with no melt quote and no blank outputs **MUST** balance exactly.

### Settlement

A transaction with a melt quote follows [NUT-05][05]'s pending and settlement handling, including `prefer_async`: the proofs and the quote draws are pending while the payment is in flight, the outputs are signed only once it succeeds, and a failed payment leaves the proofs unspent and the quotes' mintable amounts untouched. A transaction with no melt quote settles at once.

## Response

```json
{
  "signatures": <Array[BlindSignature|null]>,
  "melts": <Array[MeltQuoteResponse]>
}
```

`signatures` has one entry per element of `outputs`, in request order: a blind signature for every fixed output and for every blank output that received change, and `null` for a blank output imprinted with `0`. `melts` holds the [NUT-05][05] melt quote response for each entry of the request's `melts`, in order, and is empty if there were none. A pending transaction returns its melt quote with state `PENDING` and `signatures` empty, to be fetched as [NUT-05][05] describes once the quote is `PAID`.

## Quote input fee

A mint **MAY** charge for quote inputs so that minting and melting in one transaction is not cheaper than doing it in two. A quote input contributes `popcount(mintable) * quote_input_fee_ppk` to the ppk sum, the fee its mintable amount would carry as proofs of the minimal split, and [NUT-02][02]'s single rounding applies to the whole transaction:

```
fee = (sum(proof input_fee_ppk) + sum(popcount(mintable) * quote_input_fee_ppk) + 999) // 1000
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
[08]: 08.md
[10]: 10.md
