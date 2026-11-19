# NUT-XX: Bid/Ask Pricing

`optional`

`depends on: NUT-04 NUT-05 NUT-06`

---

A mint holds liquidity separately for each payment method it supports for the same unit. Every mint and melt operation moves value between those holdings.

Today a mint has one price for that service: par, in both directions, for every method. It cannot pay for liquidity on a method that has run short, and it cannot charge more for liquidity on a method that is scarce.

This NUT lets a mint publish two prices per method-unit pair: a `bid` and an `ask`. Both are at or above par.

Prices are stated from the mint's point of view. The mint bids to receive liquidity, which applies to minting, and asks for markup to release liquidity, which applies to melting.

## Definitions

`par` is one unit of ecash for one unit received or sent by the mint, changing the mint's liquidity position for a specific payment method. Prices are stated as a deviation from par, in parts per million (ppm).

`received` is the amount of liquidity the mint obtains in settlement of a mint quote's `request`. For `bolt11` this is the settled invoice amount, for `bolt12` the sum of payments to the offer, and for `onchain` the sum of output values paying the address in eligible transactions. Network fees the payer spends to deliver a payment never reach the mint and are not part of `received`.

## Prices

A mint publishes two unsigned rates per method-unit pair:

- `bid_ppm` is what the mint adds when it receives value.
- `ask_ppm` is what the mint adds to its charge when it sends value.

Both are not absolute prices, but non-negative premia over par. Because they are unsigned, this NUT cannot express a charge on minting. If some payment method would cost the mint money to receive, such price should be included into its `request`.

The amounts derived from these rates are:

```python
def premium(received: int, bid_ppm: int) -> int:
    return (received * bid_ppm) // 1_000_000      # rounds down

def markup(amount: int, ask_ppm: int) -> int:
    return -((-amount * ask_ppm) // 1_000_000)    # rounds up
```

Both are computed on the payment method side of the operation, never on the ecash side: `received` when minting, and the `amount` delivered to `request` when melting.

Computing a premium on `amount_paid` instead, or a markup on the inputs provided, would put the bid and the ask on different scales and make a round trip through a single method profitable by roughly `bid_ppm * ask_ppm`.

Rounding is always toward the mint. The amount due on a sum is never less than the sum of the amounts due, so splitting an operation cannot produce a gain.

### The pricing rule

For every method-unit pair, a mint **MUST** publish and apply:

```text
bid_ppm <= ask_ppm
```

This alone prevents profitable cycles. No sequence of mint and melt operations that returns a taker to the method-unit pair it started from can profit, whatever the path, because returning liquidity costs the spread of every pair it passes through.

A mint's prices are typically set from outside the mint. The mint **MUST** validate every price change against this rule before applying it, and **MUST** reject the change as a whole if any method-unit pair would violate it, keeping the prices previously in force. How prices are submitted to the mint is out of scope of the protocol.

The `bid_ppm` of one pair **MAY** exceed the `ask_ppm` of another. This is intended: it is a public offer to move the mint's liquidity from the second pair to the first.

A taker also pays network costs on both operations and [NUT-02][02] input fees on the melt. Mints **MUST NOT** rely on those costs to keep a cycle unprofitable, because they belong to the taker and can approach zero.

### Price uniformity

A mint's price for a method-unit pair **MUST** depend only on the pair, the amount, and the time. It **MUST NOT** depend on the identity of the requester, on authentication, or on any other property of who is asking.

Prices **MAY** change at any time. A rate published or quoted earlier does not bind a payment priced later.

The fields defined here carry one rate per method-unit pair, so they cannot express a price that varies with the amount. A mint using them prices independently of amount.

## Minting

A mint quote response ([NUT-04][04]) includes `premium`, an unsigned amount in the quote's `unit`. The premium is credited on top of what the mint receives:

```text
premium     = premium(received, bid_ppm)
amount_paid = received + premium
```

`amount_paid` keeps its [NUT-04][04] role as the amount the wallet may issue against. Every NUT-04 rule on it still applies. Under this NUT it is the amount credited to the quote, which is no longer the amount received.

This NUT does not change the `request`. A payment method that fixes an amount creates a request for exactly that amount, as it does today.

### When the amount is fixed at quote creation

Some payment methods fix the amount to be paid in the quote request, such as [NUT-23][23]. For these, `received` is known when the quote is created, so `premium` is too.

Once the request is paid in full, the mint credits `amount_paid = amount + premium`.

With `bid_ppm = 5000`, a quote for `amount = 10000` has a `premium` of 50. The wallet pays the request for 10000 and may issue 10050.

### When the payer chooses the amount

Other payment methods let the payer choose the amount, such as [NUT-30][30] and [NUT-25][25]. For these, `received` is unknown at quote creation, so the quote response **MUST** also include `bid_ppm`:

```json
{
  "quote": <str>,
  "premium": <int>,
  "bid_ppm": <int>,
  "amount_paid": <int>,
  "amount_issued": <int>,
  ...
}
```

Each payment is priced when it is credited. For a credited payment of amount `r`, the mint adds `premium(r, bid_ppm)` to `premium` and `r + premium(r, bid_ppm)` to `amount_paid`.

`premium` is therefore cumulative and starts at `0`.

`bid_ppm` in a quote response is the rate that would apply to a payment credited now, and **MAY** differ from the rate shown when the quote was created.

This NUT adds no rules about `expiry`. A bid is never below par, so a payment credited late can earn a different premium but can never be charged.

With `bid_ppm = 5000`, credited payments of 100000 and 30000 give `premium = 650` and `amount_paid = 130650`.

### Capping the premium

A `request` whose amount is chosen by the payer can receive any amount, so the premium on it is unbounded unless the mint caps it.

A mint **MUST NOT** pay a premium on more than `max_amount` of `received` per quote, where `max_amount` is the value published for that method-unit pair ([NUT-04][04]). Anything above that is credited at par.

The cap is cumulative over the quote, not per payment.

A mint **MUST NOT** apply a non-zero `bid_ppm` to a method-unit pair for which it publishes no `max_amount`.

The largest premium a quote can earn is therefore `premium(max_amount, bid_ppm)`, which a wallet can compute before paying.

## Melting

A melt quote response ([NUT-05][05]) includes `markup`, an unsigned amount in the quote's `unit`:

```text
markup = markup(amount, ask_ppm)
```

`ask_ppm` is the mint's ask when the quote is created. `amount` keeps its meaning: what the mint delivers to `request`.

The wallet **MUST** provide inputs of at least:

```text
amount + markup + fee_reserve + input_fee
```

The mint **MUST** reject a melt whose inputs do not cover this total, with error `11005`.

`markup` is not part of `fee_reserve` and is never returned as [NUT-08][08] change.

## Settings

A mint publishes its current prices in its [NUT-06][06] info response. It **MUST NOT** apply a non-zero price to a method-unit pair it does not publish.

```json
{
  "XX": {
    "methods": [
      { "method": "bolt11", "unit": "sat", "bid_ppm": 5000, "ask_ppm": 6000 },
      { "method": "onchain", "unit": "sat", "bid_ppm": 0, "ask_ppm": 1000 }
    ]
  }
}
```

A pair that is absent has a `bid_ppm` and `ask_ppm` of `0`. Its ask of `0` is then crossed by any published bid above `0`, which is a standing offer the operator may not have intended to make. A mint that publishes a bid **SHOULD** publish every method-unit pair it supports for that unit.

Published prices are valid only at the point of requesting them. They **MAY** change between two requests. Wallets **MUST** use the quote to decide what they pay or receive.

## Wallet behaviour

- Wallets **MUST** include `markup` in the inputs of a melt.
- Wallets **SHOULD** display a non-zero `premium` or `markup`.
- Wallets **SHOULD** compare quoted amounts against published prices, and warn when a `markup` is higher than the published ask predicts.
- Wallets **MAY** use published prices to choose a payment method before requesting a quote.
- Wallets **SHOULD** treat a quote's `bid_ppm` as current rather than guaranteed, and re-check it before sending further payments to a long-lived request.

## Mint behaviour

How bids and asks are computed is out of scope. The mint validates the protocol invariants and applies the prices.

Mints **SHOULD** cap the total premium paid per period. `max_amount` bounds what a single quote can earn, not the sum across quotes.

## Interaction with other NUTs

- [NUT-02][02]: `input_fee_ppk` is unchanged and applies in addition to `markup`.
- [NUT-08][08]: unchanged. Change derives from `fee_reserve` only.
- [NUT-15][15]: each mint prices its own share of a multi-path payment.
- [NUT-29][29]: unchanged. Batched minting operates on `amount_paid - amount_issued`.
- [NUT-30][30]: unchanged. This NUT prices a payment when it is credited, and adds no rules about which payments are credited.

[02]: 02.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[08]: 08.md
[15]: 15.md
[23]: 23.md
[25]: 25.md
[29]: 29.md
[30]: 30.md
