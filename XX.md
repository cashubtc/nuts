# NUT-XX: Compact state filters

`optional`
`depends on: NUT-07`
`uses: NUT-04, NUT-05`

---

This NUT defines compact filters over the mint's state changes that the mint publishes for everyone, and that wallets match locally. Following ecash today means naming it: both `POST /v1/checkstate` ([NUT-07][07]) and a [NUT-17][17] subscription carry the exact identifiers a wallet is asking about. A filter carries none, so a wallet learns when its ecash has been spent, or when its quote has been paid, without telling the mint which. The same filters let it finish a seed restore without disclosing what it recovered.

Testing an object against a filter returns one of two answers: no, or maybe. The encoding has no false negatives, so anything the mint put in a filter always matches it, and an object that does not match is not in that filter at all. A match is the weaker answer: it is almost always real, but about one test in 268 million is spurious at the recommended parameter, so a wallet confirms a match through [NUT-07][07] before acting. A wallet following its ecash therefore gets a negative answer almost every time, and makes an identifying request only when something has probably happened.

Neither side does work that scales with the other. The mint builds one filter per epoch, once, and serves the same bytes to every wallet from a cache. The wallet fetches those bytes and tests as many of its own objects against them as it likes, offline.

## Specifications

### Elements

For every object whose observable state changes during an epoch, the mint inserts exactly one element into that epoch's filter:

```
E = SHA256(DOMAIN_SEPARATOR || len32(kind) || kind || len32(id) || id || len32(state) || state)
```

Where:

- `DOMAIN_SEPARATOR` is the constant byte string `b"Cashu_StateFilter_v1"` as raw ASCII bytes, not length-prefixed
- `len32(x)` is the byte length of `x` as a 32-bit unsigned integer in big-endian format
- `kind` is one of the UTF-8 encoded strings in the table below
- `id` identifies the object, and depends on `kind`
- `state` is the new state of the object, and depends on `kind`

| `kind`        | `id`                                     | `state`                               |
| ------------- | ---------------------------------------- | ------------------------------------- |
| `proof_state` | the 33 bytes of the compressed point `Y` | `"UNSPENT"`, `"PENDING"` or `"SPENT"` |
| `mint_quote`  | the UTF-8 encoded mint quote ID          | the empty string                      |
| `melt_quote`  | the UTF-8 encoded melt quote ID          | `"UNPAID"`, `"PENDING"` or `"PAID"`   |

The length prefixes keep the three fields unambiguous so that you can add a new kind without a registry of tags. A kind names the operation, not the payment method: BOLT11 ([NUT-23][23]), BOLT12 ([NUT-25][25]) and onchain ([NUT-30][30]) all share the melt state enum of [NUT-05][05], no mint quote carries a state in any method, and quote IDs are unique per mint ([NUT-04][04]) rather than per method. One filter sequence covers every kind and every method; splitting it would shrink the anonymity set and leak the method on a match.

Mints **MUST** hash the quote ID exactly as it was returned to the wallet. Implementations **MUST NOT** normalize its case and **MUST NOT** strip its hyphens. A published filter lets an attacker test a guessed quote ID, so a mint that publishes filters for a quote kind **MUST** generate that kind's quote IDs as [NUT-04][04] recommends, UUIDv7 with all 74 variable bits from a CSPRNG, and **MUST NOT** advertise a quote kind whose IDs are generated any other way.

Binding `state` into the element keeps a proof state private end to end: a match reports the new state directly, so the wallet never has to send `Y` to learn it, and it computes one candidate per state it cares about, at most three per proof. Mint quotes carry no state because their accounting fields would disclose amounts, so a match means only that the quote changed and the wallet follows it with `GET /v1/mint/quote/{method}/{quote_id}`.

### Filter encoding

A filter is a Golomb-Rice coded set of the positions of its elements, following the construction of [BIP-158](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki). With `P` the Golomb-Rice parameter:

1. Remove duplicate elements. `N` is the number of distinct elements that remain.
2. For each element `E`, let `v` be the first 8 bytes of `E` read as a 64-bit unsigned integer in big-endian format, and compute the position `pos = (v * N * 2^P) >> 64`. This multiplication **MUST** be carried out in at least 128-bit arithmetic.
3. Sort the positions in ascending order. Positions are **NOT** deduplicated: two distinct elements can land on the same position, which encodes as a difference of `0`.
4. Compute the difference `d` between each position and its predecessor, taking `0` as the predecessor of the first.
5. Encode each `d` as a Rice code: the quotient `d >> P` as that many `1` bits followed by a single `0` bit, then the low `P` bits of `d` in big-endian order.
6. Concatenate all codes and pad the result with `0` bits to a byte boundary.

Decoding reverses this. A decoder reads Rice codes while at least `P + 1` bits remain unread, and `N` is the number of values it read. This terminates because a code is at least `P + 1` bits long and the padding of step 6 is at most 7 bits, so padding can never complete one, and it is why `P` **MUST** be at least `7`. `N` is therefore not transmitted, and a wallet decodes a filter before it can place its own candidate. Deduplicating elements rather than positions in step 1 is what makes `N` recoverable: every distinct element contributes exactly one encoded value.

This differs from [BIP-158](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki) in two ways, both to cut the primitives an implementation needs. There is no SipHash step, because `E` is already a SHA-256 digest over a domain-separated preimage. And `M` is fixed to `2^P` rather than `1.497137 * 2^P`, which makes this Rice coding with a single parameter, at about half a bit per element.

The probability that an element that is not in the filter matches it is `2^-P`, whatever `N` is. At the recommended `P = 28` an element costs about 29.6 bits, or 3.7 bytes, so a filter's size follows the number of state changes in its epoch while its false-positive rate does not. `P` **SHOULD** be chosen so that false positives stay rare across every filter a wallet tests, not one filter at a time, and mints **SHOULD NOT** use a `p` below `24`. Mints that consider their volume sensitive **MAY** pad a filter with elements drawn uniformly at random, which costs 3.7 bytes each and is undetectable because wallets test only specific candidates.

### The `Filter` object

```json
{
  "start": <int>,
  "end": <int>,
  "data": <hex_str>
}
```

Where:

- `start` is the Unix timestamp at which the epoch began
- `end` is the Unix timestamp at which the epoch ended
- `data` is the hex-encoded Golomb-Rice coded set

Epochs **MUST** be contiguous: a filter's `start` **MUST** equal the `end` of the filter before it. An epoch in which nothing changed **MUST** still produce a filter, with `data` set to the empty string, so that the history never has gaps. That chain is what a wallet checks to know it holds the whole history; nothing in a filter attests to its origin.

### Fetching filters

The mint publishes the parameters of its filters:

```http
GET https://mint.host:3338/v1/filters/info
```

The mint responds with a `GetFiltersInfoResponse`:

```json
{
  "p": <int>,
  "epoch": <int>,
  "kinds": <str[]>,
  "page_size": <int>,
  "first_page": <int>,
  "current_page": <int>,
  "current_page_count": <int>,
  "earliest_start": <int>,
  "latest_end": <int>,
  "pending": <bool>
}
```

Where:

- `p` is the Golomb-Rice parameter `P`
- `epoch` is the epoch duration in seconds; `3600` is **RECOMMENDED**, and mints **MAY** use longer
- `kinds` are the `kind` values covered by the filters, each for every payment method the mint supports
- `page_size` is the number of filters on a full page
- `first_page` is the lowest page number the mint still serves
- `current_page` is the page still being filled; every page below it is complete
- `current_page_count` is how many filters `current_page` holds so far
- `earliest_start` is the `start` of the oldest filter the mint still serves
- `latest_end` is the `end` of the most recent filter
- `pending` is whether the mint serves the pending filter described below

A value of `50` is **RECOMMENDED** for `page_size`. Filters grow with the mint's volume: at an hourly epoch and one state change per second, a filter is about 13 KB, so a page of 50 is about 650 KB, and a busier mint **SHOULD** advertise a smaller `page_size`.

Filters are numbered from the mint's first epoch, oldest first. Page `k` holds the filters at positions `k * page_size` to `k * page_size + page_size - 1` in that numbering:

```http
GET https://mint.host:3338/v1/filters/{page}
```

The mint responds with a `GetFiltersResponse`:

```json
{
  "page": <int>,
  "filters": <Array[Filter]>
}
```

Within a page, the filters **MUST** be in ascending order of `start`. Mints **MUST** return an error for a page above `current_page` or below `first_page`.

Page numbers are absolute: page `k` always names the same epochs, and pruning raises `first_page` without renumbering anything. Every page below `current_page` is full and never changes again, so mints **SHOULD** serve it with a long-lived immutable cache directive, and wallets **MAY** keep it indefinitely. Only `current_page` grows, once per epoch, so mints **MUST NOT** serve it with a cache lifetime longer than `epoch`. A page response carries nothing that changes, which is what lets a complete page stay byte-identical for every requester forever.

A wallet records the last page it fetched in full and resumes there, fetching through `current_page`. Re-fetching `current_page` returns the filters it already holds plus any epoch that has closed since, so it **MUST** deduplicate on `start`. A wallet recovering from a seed ([NUT-13][13]) starts at `first_page`.

Filters are public and identical for every requester. Mints **MAY** serve them from a cache, a mirror, or a content delivery network, and wallets **MAY** fetch them through any transport. A wallet that uses a mirror trusts it not to withhold filters, and a withheld filter looks exactly like an epoch in which nothing happened. Wallets **SHOULD** fetch filters over a transport that does not link them to their minting and melting requests, such as the mint's onion address if one is listed in `urls` ([NUT-06][06]).

Mints **SHOULD** retain their entire filter history, which is what lets a wallet recover offline after a seed restore. It grows by about 117 MB a year at one state change per second, and a restore reads all of it.

### The pending filter

A closed epoch is up to `epoch` seconds behind. A wallet that wants a faster answer **MAY** poll the filter of the epoch that is still open, if the mint advertises `pending`:

```http
GET https://mint.host:3338/v1/filters/pending
```

The mint responds with a `PendingFilterResponse`:

```json
{
  "start": <int>,
  "data": <hex_str>
}
```

The pending filter is built and matched exactly like any other, but it has no `end` because its epoch has not closed. `start` is the moment that epoch began, and the closed filter carrying the same `start` supersedes it. Mints **MUST NOT** serve it from a cache and **SHOULD** mark it uncacheable. A mint that does not offer one **MUST** return `40001`.

`data` changes from one request to the next, and so does the `N` decoded from it, so a wallet **MUST** recompute the position of every candidate for every response it receives.

### Matching

To follow an object, the wallet computes the element `E` for each state it is interested in, and for each filter computes `pos` from `E` using the `N` decoded from that filter and the mint's `p`. The object matches if `pos` is among the positions encoded in the filter. Wallets **MUST** match on the position computed with the filter's own `N`: because `pos` depends on `N`, an element has a different position in every filter, and positions **MUST NOT** be cached across filters.

Wallets **MUST NOT** treat a filter as authoritative:

- A match **MAY** be a false positive, with probability `2^-P` per test.
- The absence of a match is not evidence that no state change occurred. Filters can be delayed, pruned, or withheld.

Before any irreversible action, such as deleting proofs from its database or releasing goods, a wallet **MUST** confirm the state through [NUT-07][07] or through the corresponding quote endpoint.

> [!CAUTION]
>
> Filters give the sender of a token a passive way to observe when it is redeemed. The sender knows `Y`, so it can compute the element and watch for it indefinitely at no cost. This cannot be fixed in any design of this kind, because before a token is redeemed the sender and the receiver hold byte-identical secrets. Receivers **SHOULD** swap incoming ecash immediately ([NUT-03][03]), which reduces what a sender can observe to the moment of receipt, and senders **SHOULD** discard `Y` once a token has been handed over.

### Wallet recovery

A seed restore ([NUT-13][13]) ends with a [NUT-07][07] request carrying every recovered `Y`, including unspent ones, which is the heaviest disclosure a wallet makes. Filters replace that step: the wallet computes the `SPENT` element of each restored proof and tests it against the history, sending nothing. They do not replace [NUT-09][09], because the mint only learns `Y` when a proof is presented to it, so a proof that was issued and never spent has never appeared in a filter.

A cold restore reads the whole retained history, far more bytes than the one `checkstate` it replaces, while a wallet already following filters pays nothing extra. Absence of a match means unspent only if the wallet holds every filter back to the first epoch in which the proof could have been spent, and a wallet whose `earliest_start` is later than that point **MUST** confirm the gap through [NUT-07][07].

## Example

A mint whose history is two epochs long has one page, still filling:

```bash
curl -X GET https://mint.host:3338/v1/filters/0
```

Response from the mint:

```json
{
  "page": 0,
  "filters": [
    {
      "start": 1701704757,
      "end": 1701708357,
      "data": "047ea0665b049eabb17be54217aa442744d190"
    },
    {
      "start": 1701708357,
      "end": 1701711957,
      "data": ""
    }
  ]
}
```

## Error codes

See [Error Codes][errors]:

- `40001`: Filter not available
- `40002`: Filter page out of range

## Mint info setting

Mints signal support for compact state filters via [NUT-06][06] using the following setting:

```json
"nuts": {
    "XX": {
      "supported": true,
      "kinds": ["proof_state", "mint_quote", "melt_quote"]
    }
}
```

`kinds` is the array of `kind` values covered by the mint's filters. A mint that advertises a kind covers it for every payment method it supports; partial coverage is not expressible, because a match would then disclose the method. The filters' parameters are served by `GET /v1/filters/info` to provide a single source of truth.

[00]: 00.md
[01]: 01.md
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
[12]: 12.md
[13]: 13.md
[17]: 17.md
[23]: 23.md
[25]: 25.md
[30]: 30.md
[errors]: error_codes.md
