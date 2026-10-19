# NUT-XX: Transactions

`optional`

`depends on: NUT-04 NUT-05 NUT-10`

---

This document describes a single endpoint that carries any [NUT-00](00.md#the-transaction-transcript) transaction: proofs and paid mint quotes in, blinded messages and a melt quote out, in one request. The fixed-shape endpoints of [NUT-03][03], [NUT-04][04] and [NUT-05][05] remain for the operations they name; this endpoint carries those and every other combination, for example paying an invoice straight from a paid mint quote, or minting a quote and consolidating proofs in one swap.

## Request

```http
POST https://mint.host:3338/v1/transaction
```

The request carries the transaction's elements; its [transcript](00.md#the-transaction-transcript), which every input signs, commits to each as NUT-00 serializes it, a blinded message by `SHA256(B_)`. The request is JSON, one array per container type:

```json
{
  "proof_inputs": <Array[Proof]>,
  "mint_quote_inputs": <Array[QuoteInput]>,
  "blinded_outputs": <Array[BlindedMessage]>,
  "melt_quote_outputs": <Array[MeltOutput]>,
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

`witness` has the same grammar as `Proof.witness` ([NUT-00](00.md#witnesses)): a key-path signature or a script-path witness over the quote input's [input digest](00.md#the-transaction-transcript).

A `MeltOutput` is a melt quote ([NUT-05][05]), the fee reserve this transaction commits to it, and for a quote offering `fee_options` ([NUT-30][30]) the selected fee option:

```json
{
  "quote": <str>,
  "fee_reserve": <int>,
  "fee_index": <int> // only if the quote offers fee_options
}
```

Any array **MAY** be empty or omitted, and each is subject to the mint's [NUT-06][06] `max_array_length`. A blinded message with `amount` `0` is a [NUT-08][08] blank output, allowed only beside a melt quote; otherwise it **MUST** be rejected.

### Rules

- The transaction **MUST** have at least one input and one output, and **MUST NOT** repeat a proof `Y`, a mint quote id ([NUT-00](00.md#the-transaction-transcript)) or a `B_` ([NUT-00][00]).
- Every v3 input **MUST** carry a witness over its input digest; pre-v3 proofs keep their own rules, per [NUT-00](00.md#the-signing-rule). A pre-v3 proof with `SIG_ALL` ([NUT-11][11]) **MUST** be rejected: NUT-11 defines no `SIG_ALL` message for this endpoint.
- Every mint quote **MUST** be locked and in the transaction's unit. Its `amount` **MUST** be positive and **MUST NOT** exceed its mintable amount, `amount_paid - amount_issued` ([NUT-04][04]).
- All `blinded_outputs` **MUST** share one keyset in the transaction's unit ([NUT-04](04.md#nutroot-transactions-v3-keysets)). Beside a melt quote, that keyset's `final_expiry` ([NUT-02][02]) **MUST NOT** be earlier than the melt quote's `expiry`.
- `melt_quote_outputs` **MUST NOT** hold more than one quote; multi-melt is reserved for future specification. The quote **MUST** be in the transaction's unit, and its method is the one it was quoted under. Its `fee_reserve` **MUST** equal the quote's `fee_reserve`, or the `fee_reserve` of the entry its `fee_index` names. A melt quote is payable from proof inputs alone, on this endpoint as on [NUT-05][05].

### Balance

```
amount_in  = sum(proof_inputs) + sum(mint quote input amounts)
amount_out = sum(blinded_outputs) + melt.amount + melt.fee_reserve + fee
change     = melt.fee_reserve - melt_fee_paid
```

Proofs are spent in full. Each quote's `amount_issued` grows by its input `amount`, as in a partial mint ([NUT-04][04]), and the rest stays mintable. `fee` is the input fee of the proofs ([NUT-02][02]) plus the [quote input fee](#quote-input-fee), and `amount_out` includes it. `melt_fee_paid` is what the payment actually cost, known only at settlement; it never exceeds `melt.fee_reserve`.

`amount_in` **MUST** equal `amount_out`. After settlement, `change` is returned in blank outputs ([NUT-08][08]): each, in request order, takes the largest amount of the blinded outputs' keyset that does not exceed what is left of it. Any change left over stays with the mint, as in a [NUT-05][05] melt.

### Settlement

A transaction with no melt quote settles at once, like a swap ([NUT-03][03]), and its response carries the outcome. A wallet that lost the response recovers as after a swap: [NUT-07][07] shows whether its proofs were spent, and [NUT-09][09] returns its blind signatures.

A transaction with a melt quote follows [NUT-05][05]'s pending and settlement handling, including `prefer_async`: the proofs and input quotes are pending while the payment is in flight; the blinded messages are signed and each quote's `amount_issued` raised only once it succeeds, and a failed payment leaves the proofs unspent and the quotes untouched. While an input quote is pending, it reports its settled `amount_issued`, and the mint **MUST** reject any other transaction or mint request ([NUT-04][04]) that draws on it, with error `20005`.

Before it initiates the payment, the mint **MUST** complete every check that signing the blinded messages depends on.

A transaction with a melt quote is recorded by that quote, as in a [NUT-05][05] melt: it reaches `PAID` only once the transaction has settled, and its `change` field ([NUT-08][08]) then carries the blind signatures for `blinded_outputs` as `signatures` does. A wallet waiting on a pending transaction polls the melt quote, or subscribes to it ([NUT-17][17]).

Either way, a mint supporting [NUT-19][19] **MAY** cache this endpoint's responses, so a wallet that lost one can resend the request.

## Response

```json
{
  "state": <str_enum[STATE]>,
  "signatures": <Array[BlindSignature]>,
  "melt_quotes": <Array[MeltQuoteResponse]>
}
```

- `state` is `PENDING` while a melt payment is in flight, `PAID` once the transaction has settled, or `FAILED` if the payment failed and the inputs were released.
- `signatures` has one blind signature per element of `blinded_outputs`, in request order, omitting a blank output left at zero ([NUT-08][08]). It is empty unless `state` is `PAID`.
- `melt_quotes` holds the [NUT-05][05] melt quote response for each entry of the request's `melt_quote_outputs`, in order, and is empty if there were none. Its `change` field carries the same blind signatures as `signatures`, once `state` is `PAID`.

## Quote input fee

A mint **MAY** charge for quote inputs so that minting and melting in one transaction is not cheaper than doing it in two. A quote input contributes `popcount(amount) * quote_input_fee_ppk` to the ppk sum, the fee its `amount` would carry as proofs of the minimal split, and [NUT-02][02]'s single rounding applies to the whole transaction:

```
fee = (sum(proof input_fee_ppk) + sum(popcount(quote amount) * quote_input_fee_ppk) + 999) // 1000
```

A mint that does not charge advertises `0`.

The fee is a live setting: a transaction built against an earlier value fails the [balance](#balance).

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
[06]: 06.md
[07]: 07.md
[08]: 08.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[17]: 17.md
[19]: 19.md
[30]: 30.md
