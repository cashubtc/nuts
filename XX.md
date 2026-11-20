# NUT-XX: Compact state filters

`optional`
`depends on: NUT-07`
`uses: NUT-02, NUT-04, NUT-05, NUT-06, NUT-09, NUT-13`

---

This NUT defines compact filters over the mint's state changes that the mint publishes for everyone, and that wallets match locally. Following ecash today means naming it: both `POST /v1/checkstate` ([NUT-07][07]) and a [NUT-17][17] subscription carry the exact identifiers a wallet is asking about. A filter carries none, so a wallet learns when its ecash has been spent, or when its quote has been paid, without telling the mint which. The same filters let it finish a seed restore without disclosing most of what it recovered.

Testing an object against a filter returns one of two answers: no, or maybe. There are no false negatives, so anything the mint inserted into a filter always matches it, and an object that does not match is not in that filter. A match is the weaker answer: a fraction of matches are spurious, at a probability that follows the fraction of bits the bitmap has set, so a wallet confirms a match through [NUT-07][07] before acting. A wallet following its ecash gets a negative answer almost every time, and makes an identifying request only when something has probably happened.

The per-operation work is bounded. One insertion into one block is two SHA-256 compressions and at most 16 bit writes. Testing one candidate against one block is at most 16 bit reads, and fewer in practice because the test stops at the first clear bit. A candidate's hashing happens once and is reused for every block and every width. Total wallet work still scales with the number of candidates, the states it follows, the sequences it follows and the blocks it tests.

A sealed block never changes. The mint updates the block that is currently open, which is the only mutable thing it serves. Each kind of object has its own sequence of blocks, sized to the rate that kind runs at, so a quiet kind is not carried in a noisy one's bytes and a wallet downloads only the kinds it follows.

## Specifications

### Elements

An element is the hash of a kind, an object identifier and a state:

```
E = SHA256(DOMAIN_SEPARATOR || len32(kind) || kind || len32(id) || id || len32(state) || state)
```

Where:

- `DOMAIN_SEPARATOR` is the constant byte string `b"Cashu_StateFilter_v1"` as raw ASCII bytes, not length-prefixed
- `len32(x)` is the byte length of `x` as a 32-bit unsigned integer in big-endian format
- `kind` is one of the UTF-8 encoded strings in the table below
- `id` identifies the object, and depends on `kind`
- `state` is the new state of the object, and depends on `kind`

| `kind`            | `id`                                      | `state`                               |
| ----------------- | ----------------------------------------- | ------------------------------------- |
| `proof_state`     | the 33 bytes of the compressed point `Y`  | `"UNSPENT"`, `"PENDING"` or `"SPENT"` |
| `mint_quote`      | the UTF-8 encoded mint quote ID           | the empty string                      |
| `melt_quote`      | the UTF-8 encoded melt quote ID           | `"UNPAID"`, `"PENDING"` or `"PAID"`   |
| `blind_signature` | the 33 bytes of the compressed point `B_` | the empty string                      |

The length prefixes keep the three fields unambiguous, so a new kind can be added without a registry of tags. A kind names the operation rather than the payment method: BOLT11 ([NUT-23][23]), BOLT12 ([NUT-25][25]) and onchain ([NUT-30][30]) share the melt state enum of [NUT-05][05], no mint quote carries a state in any method, and quote IDs are unique per mint ([NUT-04][04]) rather than per method.

### Insertion events

A mint that advertises a kind **MUST** insert one element for each event in the table below, and **MUST NOT** insert an element for any other event of that kind.

| `kind`            | Insertion event                                                                                                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `proof_state`     | An existing proof transitions into the encoded state. The initial `UNSPENT` state created by issuance is not inserted. A transition back to `UNSPENT` after `PENDING` is inserted. |
| `mint_quote`      | An existing mint quote changes after its creation. Creation alone is not inserted.                                                                                                 |
| `melt_quote`      | An existing melt quote transitions into the encoded state after its creation. The initial state at creation is not inserted.                                                       |
| `blind_signature` | The blind signature has been durably persisted and can be returned by `POST /v1/restore` ([NUT-09][09]).                                                                           |

A `mint_quote` element carries the empty string as its state, so the same `E` is inserted again on every post-creation transition of that quote. A wallet that matches a `mint_quote` element learns only that the quote changed, and **MUST** fetch `GET /v1/mint/quote/{method}/{quote_id}` to learn its current state.

A mint **MUST** durably commit a state change or a signature before the insertion recording it becomes visible in any block it serves. A crash **MUST NOT** leave a published element whose object the corresponding authoritative endpoint cannot yet report.

Mints **MUST** hash the quote ID as it was returned to the wallet. Implementations **MUST NOT** normalize its case and **MUST NOT** strip its hyphens. A published filter lets an attacker test a guessed quote ID, so a mint that publishes filters for a quote kind **MUST** generate that kind's quote IDs as [NUT-04][04] recommends, UUIDv7 with all 74 variable bits from a CSPRNG, and **MUST NOT** advertise a quote kind whose IDs are generated any other way.

A `blind_signature` element records that the mint issued a signature on `B_`, which is what lets a wallet find its own past outputs without asking. It carries no state because issuance is a single event rather than an enum, and no amount because that would disclose one. It is also the only kind whose elements nobody but the issuing wallet can produce a candidate for: `B_ = Y + rG` needs the blinding factor as well as the secret, where a `proof_state` element needs only `Y`, which every previous holder of the proof knows.

This kind roughly doubles the elements a mint inserts, because a swap produces about as many outputs as it consumes inputs. Issuance has its own sequence and its own `b`, so covering it changes neither the rotation nor the block size of any other kind.

Binding `state` into the element keeps a proof state private end to end: a match reports the new state directly, so the wallet never has to send `Y` to learn it, and it computes one candidate per state it cares about, at most three per proof. Mint quotes carry no state because their accounting fields would disclose amounts.

A sequence covers one kind and, within that kind, every payment method. Splitting by method is forbidden: it would reveal which payment rail a wallet is following, it would fragment the anonymity set across several smaller sequences, and neither buys enough to justify the disclosure. Splitting by kind is what lets each kind be sized to the rate it runs at.

### Positions

An element sets up to 16 bits in a bitmap of `2^b` bits. Its positions are the 16 words of two SHA-256 digests:

```
W   = SHA256(E || u32be(0)) || SHA256(E || u32be(1))
w_i = the i-th 32-bit big-endian word of W, for i from 0 to 15
p_i = w_i >> (32 - b)
```

Where `u32be(j)` is a 32-bit unsigned counter in big-endian format.

Position `p` is bit `0x80 >> (p & 7)` of byte `p >> 3` of the bitmap, so position `0` is the most significant bit of byte `0`. Two digests supply exactly 16 words, so nothing is left over and no partial word has to be handled.

Positions are taken from fixed 32-bit windows rather than from packed `b`-bit slices of a digest, because fixed windows nest and packed slices do not. For any `b'` at most `b`, the position of an element at width `b'` is `p_i >> (b - b')`. A wallet **SHOULD** cache the 16 words of an object rather than its positions, 64 bytes regardless of `b`, and derive a position for any width with one shift. Nesting is what lets a mint narrow a bitmap at seal, or raise `b` later, without any wallet recomputing a hash.

Two of an element's words **MAY** map to the same position at a given `b`, in which case the insertion sets fewer than 16 distinct bits. This needs no special handling, and the insertion still counts once.

> [!NOTE]
>
> The positions could come from a single digest by double hashing, `p_i = (h1 + i * h2) mod 2^b`. That construction degenerates with a power-of-two modulus whenever `h2` is even, since the positions are then confined to a coset, and the corrections for it are the sort of detail three implementations get three different ways. Two digests per object, computed once for the life of that object, is not worth optimizing.

### Blocks

A block covers one kind. It is a bitmap of `2^b` bits, all zero when it opens. The mint inserts an element by setting each of its positions. Bits are never cleared, so a block only ever gains elements.

`count` is the number of insertion operations the mint has applied to the block. It is not published: the mint keeps it to know when to seal and how far to fold. Each operation increments `count` by one, whatever it sets, and this includes:

- a repeat of an element already inserted into that block,
- a noise insertion,
- an insertion whose positions collide with each other or with bits an earlier insertion set.

Defining `count` this way means a mint never has to keep an exact set of the elements in a block in order to deduplicate. Repeats and collisions leave the actual fill lower than `count` alone would suggest, so they cannot raise the false-positive probability above what the observed popcount indicates.

A block **MUST** be sealed when `count` reaches the capacity for its `b`, or when `timeout` seconds have elapsed since the block opened, whichever comes first. A mint **MUST NOT** insert an element into a sealed block, and **MUST NOT** let a block's `count` exceed the capacity for its `b`. A seal on `timeout` **MUST** produce a block even when `count` is `0`, so that the sequence keeps advancing and a wallet can bound how stale its view is.

Capacity is the insertion count at which the expected fill of the bitmap is approximately one half. `b` **MUST** be between `5` and `26`:

```
capacity = floor(2^b * 6931471805599453 / 160000000000000000)
```

That constant is the natural logarithm of two, and the expression is `2^b * ln2 / 16` rounded down. It is written as an integer ratio so that the seal point and the right-size fold land on the same value in every implementation, with no floating-point arithmetic in the rule. At `b = 20` it gives 45,426 insertions in a 128 KiB block.

The false-positive probability of a block follows its observed fill rather than its `count`. With `f` the fraction of bits set, measured by taking the popcount of the bitmap and dividing by `2^b`, a candidate that was never inserted matches with estimated probability `f^16`. When `f` is `1/2` that probability is `2^-16`, one test in 65,536. Wallets **MAY** compute `f` from the bitmap and use `f^16` as the cost of testing that block. The popcount is the only thing a bitmap reports about how full it is, and it is the quantity the probability depends on.

The expected fill at capacity is approximately one half, and the actual fill of any particular block is whatever its popcount says. Repeated elements, noise drawn on a position already set, and positions that collide all leave the actual fill lower, which lowers the false-positive probability rather than raising it.

Wallets **SHOULD NOT** discard a block whose fill is above one half. Overfilling raises the probability but introduces no false negatives, so a clear bit still proves absence and the block's answers stay sound. Discarding the block leaves a hole in the height sequence, and confirming that gap through [NUT-07][07] discloses more than the extra confirmations a high probability would have cost.

Sealing on fill is what bounds the probability. A bitmap's false-positive probability grows as it fills, so a filter sealed only by a clock would carry a probability that followed the mint's volume in that period, and the choice of 16 bits would mean nothing. Sealing on fill makes reaching the bound the event that ends the block, so a block sealed on saturation sits near it and one sealed on timeout sits below. The timeout is there for liveness rather than for the probability.

A mint **SHOULD** seal a block that reached its `timeout` at the smallest `b'` that still holds its `count`, and **MAY** instead keep `b` fixed. Positions nest, so a wallet needs no extra work to test a block at a smaller width, and the byte length of a narrowed bitmap discloses nothing that `count` does not already state. Without this a low-volume mint would publish a full-size, nearly empty bitmap on every timeout.

Mints that consider their activity sensitive **MAY** insert elements drawn uniformly at random alongside the real ones. A wallet cannot tell the two apart, because it only ever tests candidates it computed itself, and a random element matches one of those only at the block's false-positive probability. The popcount of a bitmap is the only estimate of how many insertions it holds, and it counts noise alongside the real ones, so what an observer reads off a block is not the number of objects whose state changed.

Noise adds no bytes to a block, because the bitmap is the same size whatever its fill, but it consumes capacity and so shortens the rotation. How much it hides depends on how it is drawn: an observer able to estimate the rate at which a mint adds noise can subtract it.

### Choosing `b`

A block seals when it fills, so at `R` insertions a day a sequence rotates every `capacity / R` days. That cadence is how stale a wallet's view of that kind can be when it follows sealed blocks alone, and the block still filling is what it polls for a fresher answer.

Mints **SHOULD** choose, for each kind, the smallest `b` whose capacity is at least the number of insertions they expect that kind to produce in a day, so that every sequence seals on saturation about once a day and the timeout stays a backstop rather than the usual case.

Rotation and yearly retention at `b = 20`:

| insertions/day | rotation at `b = 20` | retained per year |
| -------------- | -------------------- | ----------------- |
| 1,000          | every 45 days        | 1 MB              |
| 10,000         | every 5 days         | 11 MB             |
| 100,000        | every 10.9 hours     | 105 MB            |
| 1,000,000      | every 1.1 hours      | 1.1 GB            |

One `b` cannot serve that whole range, which is why `b` is chosen per kind rather than per mint. A kind doing 1,000 insertions a day at `b = 20` would rotate once every 45 days and publish a bitmap that is mostly empty; the rule puts it at `b = 15` and a 4 KiB block instead. A kind running at one insertion a second sits at `b = 21` and retains about 91 MB a year.

Sizing each kind on its own is what keeps a quiet kind out of a noisy one's blocks. A mint seeing 1,000,000 proof state changes and 100 melt quotes a day runs `proof_state` at `b = 25`, a 4 MiB block that rotates every 1.5 days, and `melt_quote` at `b = 12`, a 512 B block that rotates every 1.8 days. A single sequence would have to hold both in the 4 MiB block, and a wallet following only melt quotes would download it to test 100 elements.

A saturated block costs about `2 / ln2`, or 2.89, bytes per insertion whatever its `b`, so the bitmap bytes over a set of insertions are roughly the same however they are partitioned. Splitting by kind is not free beyond that. It adds:

- rounding at small widths, where capacity is rounded down and the cost per insertion rises, to 4 bytes at `b = 5`,
- blocks sealed on `timeout` rather than on fill, including empty ones,
- per-sequence metadata, one response per kind,
- an independently refreshed open block per sequence,
- HTTP and JSON framing per request.

What splitting buys is on the wallet's side: it downloads only the kinds it follows, at the width that kind needs.

### Sequences

A sequence is the ordered series of blocks for one kind. Each sequence numbers its blocks from `0` independently.

- A mint **MAY** begin covering a new kind at any time. That sequence begins at height `0`, and its first block's `start` is the first moment it covers.
- Absence of a match before a sequence's first `start` carries no meaning, because no element could have been inserted yet.
- A mint **MUST NOT** present a sequence as covering events that occurred before it began maintaining that sequence.
- A mint **MAY** stop covering a kind, and **MUST** then remove that kind from its [NUT-06][06] advertisement.
- Sealed blocks **MUST** keep the `kind` and `height` they were published with.
- A mint **MUST NOT** restart an existing kind at height `0` while presenting it as a continuation of the earlier sequence.

A wallet that still holds blocks of the old sequence can notice a restart, because the heights the mint lists no longer reach the ones it already has, or a height it kept comes back with different bytes, which the availability rule below forbids. A wallet holding nothing cannot tell a restart from a mint that has only just begun covering the kind.

### Fetching blocks

One sequence is described per request. A wallet learns which kinds exist from the `kinds` array of the [NUT-06][06] setting below, and asks about one of them:

```http
GET https://mint.host:3338/v1/filters/info/{kind}
```

The mint responds with a `GetFiltersInfoResponse`:

```json
{
  "b": <int>,
  "timeout": <int>,
  "open_interval": <int|null>,
  "blocks": [
    { "start": <int>, "end": <int|null> }
  ]
}
```

Where:

- `b` is the base-2 logarithm of the bitmap size in bits of the block now open
- `timeout` is the number of seconds after which an unsaturated block in that sequence seals; `604800` is **RECOMMENDED**, and mints **MUST NOT** use a value below `3600`
- `open_interval` is the number of seconds between refreshes of the open block, or `null` when the mint does not serve one
- `blocks` lists every block of that sequence, with the interval each one covers
- `start` is the Unix timestamp at which a block opened
- `end` is the Unix timestamp at which it was sealed, or `null` while it is still filling

The rules:

- A block's height is its index in `blocks`, so the first entry is height `0` and the list holds every height the sequence has ever had.
- The final entry is the block now filling, and is the only entry whose `end` is `null`. A sequence that has never sealed a block has exactly one entry.
- An entry's `end` **MUST** be greater than or equal to its `start`, and **MUST** equal the `start` of the entry after it, which is the contiguity rule stated where a wallet can check it.
- The open block can be fetched only when `open_interval` is not `null`.

Mints **MUST** return `40002` for a kind they do not cover. The request has no other failure of its own.

The response grows for the life of the sequence, about 40 bytes an entry, so a year of daily rotation adds some 15 KB. A wallet needs it when it starts and when it wants the interval a height covers, not on every poll: to follow the open block it re-fetches the height it holds as open and advances when that comes back sealed.

A sequence carries its own `timeout` as well as its own `b`, so a mint can give a quiet kind a shorter backstop than a noisy one. A mint **MAY** change a sequence's `b` for blocks it has not yet opened, which costs wallets nothing as long as they cache words rather than positions.

A block is fetched by its kind and its height:

```http
GET https://mint.host:3338/v1/filters/blocks/{kind}/{height}
```

The mint responds with the block's bitmap as `application/octet-stream`: the `2^b / 8` bytes and nothing else. Everything else about the block is already known. `kind` and `height` are the URL the wallet asked for, `start` and `end` are that height's entry in `blocks`, and `b` is the body length, which **MUST** be `2^b / 8` bytes for some `b` between `5` and `26`. A body of any other length **MUST** be rejected and the height treated as not yet obtained.

Every height below the last index of `blocks` is sealed. The last index is the block now filling, which is how a wallet reaches a state change without waiting for the rotation. Mints **MUST** return `40001` for a height above the last index of `blocks`, and for that height itself when `open_interval` is `null`. Mints **MUST** return `40002` for a kind they do not cover.

#### Open blocks

A block's bitmap says nothing about whether it is sealed. The `blocks` list of `/v1/filters/info/{kind}` is the only indication: every height below the last index is sealed, and the last index is open. Wallets **MUST NOT** infer protocol state from cache headers, and mints **MUST NOT** rely on cache headers to convey it.

Staleness in that list runs one way only, which is what makes it sufficient. A height the list reports as sealed is sealed permanently, because a sealed block never reopens. A height it reports as open may have sealed since the wallet read it, and the wallet learns that on its next read. So a wallet trusting a stale list can waste a fetch, but cannot mistake an open snapshot for a final block.

- A sealed block **SHOULD** be served with a long-lived immutable cache policy.
- An open block **MUST NOT** be served with `immutable`, and **SHOULD** be served with `max-age` equal to `open_interval`.
- An open block response **SHOULD** carry an `ETag`, and that `ETag` **MUST** change whenever the serialized block changes.
- Wallets **SHOULD** revalidate an open block with `If-None-Match`, and mints **MAY** answer `304 Not Modified`.
- A wallet **MUST NOT** bookmark an open snapshot or cache it permanently.
- A clear bit in an open snapshot proves absence only as of that snapshot.
- A wallet **MUST** eventually fetch the sealed representation of that height.

The same block URL returns an open block while that height is filling and its sealed final representation afterwards. A block is open in a response rather than in itself: a wallet that asks for the height it holds as open and receives a sealed block arrived after the seal and advances; one that receives an open block again did not. Neither is an error.

Those rules are what keep a design with no false negatives from acquiring one. An open snapshot is a prefix of the block that will seal at that height, so a wallet that recorded a negative from it and moved on would never look at what arrived afterwards.

Mints **SHOULD** refresh the open block on a fixed interval rather than serving the live bitmap, so that the moment an element arrived is disclosed at the granularity of `open_interval` rather than at whatever rate a client polls. Wallets **SHOULD NOT** poll faster than `open_interval`. The right-size fold can narrow `b` at seal, so the sealed block at a height may be narrower than the open block a wallet already tested; positions nest, so the candidate's words carry across unchanged.

#### Availability

A mint **MUST** retain every block it has sealed, and **MUST** return the same bytes for a height every time it serves it. Heights are therefore never dropped, which is what lets a block's position in `blocks` be its height, and what lets a wallet recover offline after a seed restore. Wallets and mirrors **MAY** retain sealed blocks indefinitely and serve them from anywhere.

Retention is unbounded, so a sequence's storage grows for its lifetime at the rate the table above gives. Raising `b` does not change that: a block costs about 2.89 bytes an insertion whatever its width, so a larger `b` cuts the number of blocks and the length of `blocks`, not the bytes the history occupies.

A mint **MAY** serve sealed blocks from a cache, a mirror or a content delivery network. A wallet that uses a mirror trusts it to serve what the mint published, and a block carries nothing binding it to its height, so a mirror answering one height with another's bytes is not detectable from the response. Wallets **SHOULD** fetch blocks over a transport that does not link them to their minting and melting requests, such as the mint's onion address if one is listed in `urls` ([NUT-06][06]).

A block is served as its bytes, so there is no encoding overhead to recover. A bitmap near half fill is close to incompressible by construction, so `Content-Encoding: gzip` buys little on a block; mints and wallets **SHOULD** support it for `/v1/filters/info/{kind}`, where a run of ascending timestamps compresses well.

> [!NOTE]
>
> Nothing a mint serves here attests to its own origin, so a mirror is trusted to the same degree the mint is. A future NUT could have the mint sign a commitment to its history, which would let a wallet verify any amount of mirrored data from one authenticated fetch. This NUT does not attempt it, because a mirror that alters a bitmap and a mint that never inserts an element are indistinguishable to a wallet, and the second is already accepted as undetectable.

### Matching

To follow an object, the wallet computes the element `E` for each state it is interested in and derives the 16 words of each. For a block at width `b`, it shifts each word to a position and reads that bit. The object matches if all 16 bits are set, and a wallet **SHOULD** stop at the first bit that is clear, which is after two reads on average against a block near half fill.

A candidate is tested only against the sequence for its kind. Its words are computed once and hold for every block in that sequence at any `b`, so the only per-candidate state is 64 bytes of words, and the only per-sequence state is one bookmark.

Wallets **MUST NOT** treat a filter as authoritative:

- A match **MAY** be a false positive, with estimated probability `f^16` for a block at observed fill `f`, which is `2^-16` at half fill.
- The absence of a match is not evidence that no state change occurred. Blocks can be delayed or withheld.
- The absence of a match in an open block means only that nothing had arrived as of that snapshot. Only a sealed block's absence covers its whole interval.
- Nothing here attests that the mint inserted everything it should have. A mint that never inserts an element publishes blocks that look entirely normal.

Before any irreversible action, such as deleting proofs from its database or releasing goods, a wallet **MUST** confirm the state through [NUT-07][07] or through the corresponding quote endpoint.

#### What a wallet discloses

Every false positive costs a [NUT-07][07] request that discloses the `Y` behind it, so what a wallet spends on privacy is its candidates times the blocks it tests times the probability. The block count follows the rotation cadence rather than the mint's volume, and each sequence is sized for that cadence on its own, so splitting by kind does not change the budget. At the one-a-day cadence the sizing rule aims for, a wallet following 50 proofs across two states expects about 0.56 false positives a year, and a 10,000-proof cold restore over a year of history about 111. A mint that wants to spend less of that raises `b`, which cuts the number of blocks without changing the bytes per insertion, at the price of a coarser rotation and a staler view.

Which sequences a wallet fetches says which kinds it follows. A wallet pulling only `blind_signature` is restoring; one pulling only `mint_quote` is waiting to be paid. Fetching every advertised sequence discloses no more than a single combined sequence would, and fetching a subset trades that distinction for bytes. Wallets that treat this as sensitive **SHOULD** fetch every advertised sequence when bandwidth allows; fetching a subset remains allowed as an explicit trade.

A sealed block discloses only that its insertions landed somewhere between `start` and `end`. An open block discloses more, because whoever polls it sees each insertion arrive within one `open_interval`. Everyone who has held a proof knows its `Y` and can watch for its redemption at no cost, so what an open block changes for them is the resolution: against sealed blocks they learn which rotation the redemption fell in, against an open block which interval. A mint that finds that trade bad serves no open block.

### Wallet recovery

A seed restore ([NUT-13][13]) is the most revealing thing a wallet does. It derives blinded messages in batches, posts each to `/v1/restore` ([NUT-09][09]), and stops only after three consecutive batches come back empty, so the requests cannot be pipelined: the next one depends on the answer to the last. It then checks every recovered proof with `POST /v1/checkstate` ([NUT-07][07]).

That hands the mint two things it did not have. The candidates it never signed disclose how far the wallet's counter ever ran, and the closing `checkstate` discloses `Y` for proofs the mint has never seen, which are the wallet's live money.

A mint that covers both `proof_state` and `blind_signature` removes both. A wallet **MAY** then restore as follows, and otherwise restores as [NUT-13][13] describes:

1. Fetch every keyset the mint has ever used with `GET /v1/keysets` ([NUT-02][02]). Restore runs per keyset, because [NUT-13][13] keeps a counter per keyset, and inactive keysets hold recoverable ecash.
2. Read the `blind_signature` and `proof_state` sequences from `/v1/filters/info/{kind}`, and start at height `0`. A wallet that knows when its seed was created can instead start at the last height whose `start` precedes that moment. The quote sequences play no part in a restore.
3. Fetch the blocks in that range. A wallet that already follows filters holds them.
4. For each keyset and each counter below the wallet's limit, derive `secret` and `r` as [NUT-13][13] prescribes, compute `B_`, and test its `blind_signature` element. This is local work and costs no request.
5. Send the matches to `POST /v1/restore` ([NUT-09][09]), in batches no larger than `max_array_length` ([NUT-06][06]).
6. Unblind each returned `BlindSignature` with the `r` from step 4 and assemble the proofs.
7. Test each recovered proof's `SPENT` element against the `proof_state` sequence to learn which are probably already spent.

Step 5 cannot be removed. Only the mint holds the private key, so only the mint can produce `C_`, and the amount rides on the mint's per-amount key rather than on the wallet's secret, so the mint supplies that too. The `amount` a wallet sends in step 5 is not used to find the signature; the mint looks the output up by `B_` and returns the amount it actually signed.

Wallets **MUST NOT** discard a recovered proof because its `SPENT` element matched. A match is probabilistic and deleting is not: a live proof matches somewhere in a year of blocks about once in one hundred and eighty, so a wallet holding five hundred live proofs would destroy roughly three of them on every restore. Step 7 ranks proofs, it does not remove them, and the rule above stands: confirm through [NUT-07][07] first. This is why step 5 asks for every issuance match rather than only the live ones.

The same probability bounds how far to scan. [NUT-13][13] stops after three hundred counters because every extension costs a round trip; here an extension costs no request, and the per-candidate work is the derivation a wallet would have performed anyway to build a message to send. But a candidate matches spuriously at that same probability, and each one puts a `B_` the mint never signed into the restore request, which is the disclosure this removes. Scanning is bought at roughly half a percent of the swept range. [NUT-13][13] discloses three hundred unused candidates per keyset unconditionally, so a wallet can sweep some fifty thousand counters per keyset before matching that, and discloses no `Y` at any range. Wallets **SHOULD** choose the limit against that budget rather than against how fast they can derive.

Absence of a match means unspent only if the wallet holds every block back to the first one in which the proof could have been spent. A wallet whose proofs predate the mint's `proof_state` sequence, because the mint began covering that kind later, **MUST** confirm the gap through [NUT-07][07].

> [!NOTE]
>
> `B_` identifies the wallet that created it more strongly than `Y` identifies the wallet holding it, because `B_ = Y + rG` can only be reproduced by whoever knows the blinding factor, while `Y` is known to everyone who has ever held the proof. Sending a `B_` the mint has already signed tells it nothing new; sending one it has not tells it the sender authored that output.

A wallet restoring against a mint that publishes no filters **SHOULD** still avoid [NUT-13][13]'s order, which sends every candidate `B_` and then every recovered `Y`. Deriving `Y` for the range, checking it with [NUT-07][07] in batches, and calling [NUT-09][09] only for what came back unspent reaches the same result in far fewer requests, disclosing far fewer `B_`. It discloses `Y` instead, so it is second best. This is also the answer to the alternative [NUT-13][13] leaves open, downloading the mint's entire database: filters are that idea done compactly, and a full dump of every signature ever issued carries the same information at many times the size without removing step 5.

## Test vectors

The element construction, the position derivation, the nesting rule and the bitmap layout are covered by [test vectors][tests]. They are normative: an implementation that does not reproduce them will not interoperate. Every value there is produced by a reference script included in the same file.

## Example

A wallet reads a sequence, then fetches a block from it:

```bash
curl -X GET https://mint.host:3338/v1/filters/info/proof_state
```

```json
{
  "b": 10,
  "timeout": 604800,
  "open_interval": 60,
  "blocks": [
    { "start": 1701704757, "end": 1701708357 },
    { "start": 1701708357, "end": null }
  ]
}
```

Height `0` is sealed and height `1` is filling. Fetching the sealed one:

```bash
curl -X GET https://mint.host:3338/v1/filters/blocks/proof_state/0
```

The response is 128 bytes of `application/octet-stream`, which tells the wallet `b = 10`, and in hex is:

```
00080020400014820048000000000208020000400800100200402200000400200000000400000000
000a408000002400000202400000000010800000008001c3000810000480010000c04004001240080
800011000080002080100000008000000c0000004000000014400800080000000002004400000000
000000085010800
```

That bitmap is the five `proof_state` `SPENT` elements of the test vectors, 76 of its 1024 bits set. `b = 10` holds only 44 insertions, so no real mint would use it; it is small enough to print.

## Error codes

See [Error Codes][errors]:

- `40001`: Filter block out of range
- `40002`: Unknown filter kind

## Mint info setting

Mints signal support for compact state filters via [NUT-06][06] using the following setting:

```json
"nuts": {
    "XX": {
      "supported": true,
      "kinds": ["proof_state", "mint_quote", "melt_quote", "blind_signature"]
    }
}
```

`kinds` is the array of `kind` values covered by the mint's filters, one sequence each. A mint that advertises a kind covers it for every payment method it supports; partial coverage is not expressible. A mint that stops covering a kind **MUST** remove it from this array. This array is how a wallet discovers which kinds exist. Each sequence's parameters and heights are served by `GET /v1/filters/info/{kind}`, which is the single source of truth for them.

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
[tests]: tests/XX-tests.md
