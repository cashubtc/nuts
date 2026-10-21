# NUT-XX: Transactions

`optional`

`depends on: NUT-04 NUT-05 NUT-10`

---

This document describes a single endpoint that carries any [NUT-00](00.md#the-transaction-transcript) transaction: proofs and paid mint quotes in, blinded messages, a melt quote and txout quotes out, in one request. The fixed-shape endpoints of [NUT-03][03], [NUT-04][04] and [NUT-05][05] remain; this endpoint carries any combination, eg paying an invoice straight from a paid mint quote.

## Request

```http
POST https://mint.host:3338/v1/transaction
```

The request is JSON, one array per [transcript](00.md#the-transaction-transcript) container type:

```json
{
  "proof_inputs": <Array[Proof]>,
  "mint_quote_inputs": <Array[QuoteInput]>,
  "blinded_outputs": <Array[BlindedMessage]>,
  "melt_quote_outputs": <Array[MeltOutput]>,
  "mint_quote_outputs": <Array[MintQuoteOutput]>,
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

`witness` is serialized as `Proof.witness` is ([NUT-00](00.md#witnesses)), over the quote input's [input digest](00.md#the-transaction-transcript).

A `MeltOutput` is a melt quote ([NUT-05][05]), the fee reserve this transaction commits to it, and for a quote offering `fee_options` ([NUT-30][30]) the selected fee option:

```json
{
  "quote": <str>,
  "fee_reserve": <int>,
  "fee_index": <int> // only if the quote offers fee_options
}
```

A `MintQuoteOutput` is a [fixed txout quote](#fixed-txout-quote) this transaction creates. Its `pubkey` is the quote's lock key, a 33-byte compressed secp256k1 public key, and `id_preimage` the optional 32-byte preimage of its id:

```json
{
  "pubkey": <hex_str>,
  "amount": <int>,
  "id_preimage": <hex_str> // optional
}
```

Any array **MAY** be empty or omitted, and each is subject to the mint's [NUT-06][06] `max_array_length`. A blinded message with `amount` `0` is a [NUT-08][08] blank output, allowed only beside a melt quote; otherwise it **MUST** be rejected.

### Rules

- The transaction follows NUT-00's [transaction](00.md#the-transaction-transcript) and [signing](00.md#the-signing-rule) rules. A pre-v3 proof with `SIG_ALL` ([NUT-11][11]) **MUST** be rejected.
- Every mint quote **MUST** be locked and in the transaction's unit, and its `amount` **MUST** be positive.
- All `blinded_outputs` **MUST** share one keyset in the transaction's unit ([NUT-04](04.md#nutroot-transactions-v3-keysets)). Beside a melt quote, that keyset's `final_expiry` ([NUT-02][02]) **MUST NOT** be earlier than the melt quote's `expiry`.
- A mint quote output's `amount` **MUST** be positive. An `id_preimage` **MUST NOT** repeat within the request, or derive an id that is already [claimed](04.md#derived-quote-ids); the mint rejects either with error `11008`. Lock keys may repeat, but for privacy each **SHOULD** be fresh.
- A transaction with a txout quote among its `mint_quote_inputs` **MUST NOT** carry a mint quote output.
- `melt_quote_outputs` **MUST NOT** hold more than one quote. The quote **MUST** be in the transaction's unit, and its `fee_reserve` **MUST** equal the quote's `fee_reserve`, or the `fee_reserve` of the entry its `fee_index` names.

### Balance

```
amount_in  = sum(proof_inputs) + sum(mint quote input amounts)
amount_out = sum(blinded_outputs) + sum(mint quote output amounts) + melt.amount + melt.fee_reserve + fee
change     = melt.fee_reserve - melt_fee_paid
```

Each quote's `amount_issued` grows by its input `amount`, as in a partial mint ([NUT-04][04]). `fee` is the input fee of the proofs ([NUT-02][02]) plus the [quote input fee](#quote-input-fee). `melt_fee_paid` is what the payment actually cost, known only at settlement; it never exceeds `melt.fee_reserve`.

`amount_in` **MUST** equal `amount_out`. After settlement, `change` is returned in blank outputs ([NUT-08][08]): each, in request order, takes the largest amount of the blinded outputs' keyset that does not exceed what is left of it.

### Settlement

A transaction with no melt quote settles at once, like a swap ([NUT-03][03]).

A transaction with a melt quote follows [NUT-05][05]'s pending and settlement handling, including `prefer_async`: the proofs and input quotes are pending while the payment is in flight, the blinded messages are signed, the txout quotes created and each quote's `amount_issued` raised only once it succeeds, and a failed payment leaves the proofs unspent and the quotes untouched. While an input quote is pending, it reports its settled `amount_issued`, and the mint **MUST** reject any other transaction or mint request ([NUT-04][04]) that issues from it, with error `20005`.

Before it initiates the payment, the mint **MUST** complete every check that signing the blinded messages and creating the txout quotes depend on.

A transaction with a melt quote is recorded by that quote, as in a [NUT-05][05] melt: the quote reaches `PAID` only once the transaction has settled.

## Txout quote

A txout quote is a [NUT-04][04] mint quote created by a transaction. Its method is `txout`, a name reserved for these quotes.

A txout quote is fetched at `GET /v1/mint/quote/txout/{quote_id}` and redeemed in full: at `POST /v1/mint/txout`, or as a quote input whose `amount` is its whole mintable amount. Only a transaction creates one. An id that names no quote **MUST** be answered with error `20010`.

### Fixed txout quote

A mint quote output creates a fixed txout quote on settlement, for its `amount`, in the transaction's unit and locked to its `pubkey`, with `request` the empty string and `expiry` `null`. Its id is [derived](04.md#derived-quote-ids) from the output's `id_preimage`. Without one, the mint computes it from the transaction's inputs:

```
quote_id = hex(tagged_hash("Cashu_InputQuoteId", SHA256(input section) || u32_BE(k)))
```

where the input section is the transcript's input containers (`0x1n`) as serialized ([NUT-00](00.md#the-transaction-transcript)) and `k` is the output's position among the request's mint quote outputs, from 0. An id derived from `id_preimage` is claimed once a transaction naming it is accepted, and is released only if its payment fails.

A seeded wallet **SHOULD** derive each of its own fixed txout quotes' lock key and `id_preimage` from one quote counter value per [NUT-13](13.md#v3-message). A fixed txout quote paying another party in a transaction signed for later **SHOULD** take an id bound to the inputs.

## Response

```json
{
  "state": <str_enum[STATE]>,
  "signatures": <Array[BlindSignature]>,
  "melt_quotes": <Array[MeltQuoteResponse]>,
  "mint_quotes": <Array[MintQuoteResponse|null]>
}
```

- `state` is `PENDING` while a melt payment is in flight, `PAID` once the transaction has settled, or `FAILED` if the payment failed and the inputs were released.
- `signatures` has one blind signature per element of `blinded_outputs`, in request order, omitting a blank output left at zero ([NUT-08][08]). It is empty unless `state` is `PAID`.
- `melt_quotes` holds the [NUT-05][05] melt quote response for each entry of the request's `melt_quote_outputs`, in order, and is empty if there were none. Its `change` field carries the same blind signatures as `signatures`, once `state` is `PAID`.
- `mint_quotes` holds one entry per element of the request's `mint_quote_outputs`, in order: the quote's [NUT-04][04] response once it is created, and a `null` entry until then.

## Quote input fee

A mint **MAY** charge for quote inputs. A quote input contributes `popcount(amount) * quote_input_fee_ppk` to the ppk sum, and [NUT-02][02]'s single rounding applies to the whole transaction:

```
fee = (sum(proof input_fee_ppk) + sum(popcount(quote amount) * quote_input_fee_ppk) + 999) // 1000
```

A mint that does not charge advertises `0`.

## Settings

```json
{
  "XX": {
    "supported": <bool>,
    "quote_input_fee_ppk": <int>,
    "fixed_txout_quotes": <bool>
  }
}
```

A mint with `fixed_txout_quotes` `true` accepts mint quote outputs; without it, `mint_quote_outputs` **MUST** be empty.

[00]: 00.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[08]: 08.md
[10]: 10.md
[11]: 11.md
[30]: 30.md
