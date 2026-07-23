# NUT-Exchange: Atomic Multi-Asset Exchange

`draft`

`optional`

`depends on: NUT-02, NUT-03, NUT-06, NUT-07, NUT-09, NUT-10, NUT-11, NUT-12`

---

This NUT defines an atomic exchange of two existing Cashu asset classes at one
mint. Two or more participants each contribute bearer proofs of one asset class
and commit to exact blinded receive outputs of the other class. The mint spends
every input and signs every output in a single database transaction, or changes
nothing.

This NUT transfers **existing typed assets only**. It does not create or destroy
asset classes. Final NUT name, number, and NUT-10 `kind` are provisional.

## Premise

### The problem

A client-to-client atomic swap of Cashu tokens (for example an HTLC or
adaptor-signature swap) requires both wallets to remain available while they
exchange keys, commitments, signatures, mint requests, and claims. It exposes a
free-option locktime race: the party holding the swap secret (the leader) picks
when to trigger settlement inside the locktime window — completing only if price
has moved in its favor, otherwise letting the swap lapse — a free American option
on the locked rate. And a party matched against several counterparties starts
several independent protocols; sequential execution puts several network paths
on the critical path.

A Cashu mint already validates proof signatures, maintains spentness, and issues
blind signatures. This NUT uses that existing authority as the atomic settlement
layer, removing the interactive claim sequence entirely.

### Model

Each participant first locks its bearer proofs to an exact receive-output
commitment via a [NUT-10][10] `PAY_TO_UNLOCK` condition. The participants'
conditioned proofs and public receive descriptors are assembled into one
settlement request and submitted to the mint. The mint validates every condition
and conserves each asset class independently, then commits all input spends and
all output signatures in one transaction — or changes nothing.

This is the duty separation of a smart-contract exchange — independently enforced
authorization, atomic asset transition — but the trust boundary is that of a
Cashu mint, not a public blockchain.

Two preparation patterns are supported: a **direct two-party swap** where both
participants are online, and a **coordinator-mediated swap** where a relay
assembles matched participants' material (see [Preparation](#preparation)). A
coordinator or relay is **optional** and has no on-mint authority; see
[Coordinator and relay role](#coordinator-and-relay-role).

### Trust boundary and anonymity

The mint is trusted for the same things [NUT-11][11] P2PK already trusts it
(rejecting invalid spends, maintaining spentness, blind signing) **plus one
atomic database commit**. No transparency or accountability layer is defined
here. Two mitigations bound the added trust:

1. **A violation is transcript-checkable.** Any party holding the full transcript
   (inputs, conditions, output commitments, signatures) can prove the mint
   accepted an exchange that violates a condition or a conservation rule. This
   is incidental verifiability, not a published audit log.
2. **Anonymity makes betrayal indiscriminate.** Fresh per-authorization `nonce`,
   refund key, proof secret, and output secret carry no stable owner identity,
   so the mint cannot _selectively_ betray a user. It can still censor, deny
   service, or betray an exchange wholesale — the same issuer trust NUT-11
   carries.

### Scope

Version 1 supports:

- one mint;
- two or more participants in one atomic exchange (a star: one party on one side,
  one or more on the other — e.g. one taker against one or more makers);
- exactly two existing asset classes, one offered per side;
- exact, owner-precommitted blinded receive outputs;
- per-asset-class conservation; and
- one atomic commit (all participants settle or none).

Version 1 does **not** support: a coordinator as a required party; cross-mint
settlement; general N-way cycles (A wants B, B wants C, C wants A) that would
require a solver; partial fills of one authorization; a mutable remaining
balance; a venue-selected price or amount range; asset creation or destruction;
or public-consensus enforcement.

Independent atomic exchanges are unrelated: a failure or retry of one never
rolls back another, since each is its own database transaction.

## Protocol

### Terminology

- **Asset class**: a mint keyset identified by its [NUT-02][02] `id`. A keyset's
  unit is part of the class identity. Amounts from different classes MUST NOT be
  added or compared.
- **Participant**: one owner in an exchange. Each offers one asset class and
  receives the other.
- **Submitter**: whoever posts the settlement request to the mint — a participant
  or a relay. It is not a custody role.

### `PAY_TO_UNLOCK` condition

A new [NUT-10][10] well-known secret `kind` named `PAY_TO_UNLOCK`. A proof
carrying it authorizes one exact exchange (bilateral or N-party star).

```json
[
  "PAY_TO_UNLOCK",
  {
    "nonce": "<hex_str: 32 bytes>",
    "data": "<hex_str: H_recv>",
    "tags": [
      ["offer_keyset", "<keyset_id>"],
      ["receive_keyset", "<keyset_id>"],
      ["refund", "<xonly_pubkey_hex>"]
    ]
  }
]
```

- `data` is `H_recv`, the commitment to this participant's complete ordered
  receive-output list (see [Receive-output commitment](#receive-output-commitment)).
- `offer_keyset` / `receive_keyset` bind the two asset classes. They MUST differ.
- `refund` is a fresh x-only public key whose private half the owner retains. A
  signature under it authorizes the reclaim path (see
  [Refund](#refund)). It is the sole owner-authorization key and cannot be
  omitted; see [Refund](#refund) for why.

The condition answers one question:

> May this proof be consumed by a transaction that atomically creates exactly
> these blinded outputs of `receive_keyset`?

Every proof contributed by one participant MUST carry the same `offer_keyset`,
`receive_keyset`, `H_recv`, and `refund`. Across the exchange, the multiset of
offered keysets MUST equal the multiset of received keysets — i.e. every asset
class received by some participant is offered by some other participant. In the
common star shape, one side offers class `X` and receives `Y`; the other side
offers `Y` and receives `X`.

### Receive-output commitment

The receive destination is the owner's ordered list of `BlindedMessage` values.
The canonical encoding of one entry is:

```json
{"amount": <uint>, "id": "<keyset_id>", "B_": "<hex_str>"}
```

The commitment is a BIP-340 tagged hash over the length-prefixed concatenation
of entries in declared order. Each `entry_canonical` is the entry serialized with
the [RFC 8785][rfc8785] JSON Canonicalization Scheme (JCS): UTF-8, object keys in
lexicographic order, minimal number serialization, no insignificant whitespace.
The length prefix is a 4-byte little-endian unsigned integer (output lists are
not capped at 255):

```
recv_canonical = uint32_le(len) || entry[0]_canonical || ... || entry[n-1]_canonical
H_recv = tagged_hash("Cashu/PAY_TO_UNLOCK/recv", recv_canonical)
```

where `tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)`.

Duplicate entries, unknown fields, non-canonical encodings, and list-prefix
matches MUST be rejected. A separate receive public key is not required: only the
wallet that created the blinded messages knows the secrets and blinding factors
needed to unblind the mint's signatures.

### Canonical encodings

- **Participant record**: the JSON object `{"inputs": [...], "outputs": [...]}`,
  with `inputs` sorted by `(keyset_id, secret)` and `outputs` in declared order,
  serialized via [RFC 8785][rfc8785] JCS. Each `Proof` and `BlindedMessage` uses
  exactly the field set defined in [NUT-00][00]; unknown or extra fields MUST be
  rejected.
- **Participant order**: records are ordered by the lexicographically smallest
  `(keyset_id, secret)` among each participant's inputs. Proof secrets are unique
  across the whole request, so this is a strict total order even when several
  participants share an `offer_keyset`.
- **Request digest**:

```
req_canonical = participant[0]_canonical || ... || participant[n-1]_canonical
request_digest = tagged_hash("Cashu/exchange/request", req_canonical)
```

The request digest is the sole idempotency and replay key: a byte-identical
retry yields the same digest and returns the committed result; any input proof
can be spent only once.

Every signature or hash in this NUT is over these canonical encodings.

### Preparation

A `PAY_TO_UNLOCK` proof is reusable settlement material: once minted it is
consumed by the first `/v1/exchange` request that respects its committed terms,
or reclaimed by its owner. There are two preparation patterns.

#### Two-party direct swap

Two participants agree on an exact exchange of asset `A` for asset `B` (e.g. an
OTC trade or a direct match). Both are online. Each participant:

1. prepares blinded receive outputs for the agreed amount of the other class and
   computes `H_recv`;
2. uses an ordinary [NUT-03][03] swap to convert its bearer proofs of its offered
   class into `PAY_TO_UNLOCK` proofs committed to `H_recv`, choosing a fresh
   `refund` key it retains;
3. verifies the [NUT-12][12] DLEQ proofs on the returned blind signatures and
   checks that the conditioned proofs encode the agreed terms;
4. one participant assembles both participants' conditioned proofs and public
   receive `BlindedMessage` lists and POSTs `/v1/exchange`.

If the request fails validation, no proof is spent; each participant refunds its
own conditioned proofs and retries or walks away.

#### Coordinator-mediated swap

A matching engine pairs orders and a relay assembles and submits the settlement
request. What a participant must know up front depends on its order type:

- **Fill-or-Kill (FOK) taker — may go offline.** A FOK order has a single exact
  fill amount, so the taker knows its receive amount at order placement. It
  prepares its conditioned proofs then (steps 1–3 above), attaches them and its
  public receive descriptors to the order, and disconnects. At match the relay
  uses this pre-committed material; the taker later recovers its outputs via
  [NUT-09][09].
- **Makers and Fill-and-Kill (FAK) takers — must be online at match.** A resting
  maker may be partially filled and a FAK taker's fill amount is unknown until
  match, so neither knows its exact receive amount at preparation time. They
  prepare conditioned proofs after a match is agreed (deriving receive amounts
  from the matched terms) and hand them to the relay.

The relay assembles every matched participant's conditioned proofs and public
receive descriptors into one `/v1/exchange` request and submits it.

> **Blinding-budget lemma.** Blind issuance requires the recipient to supply —
> and later unblind — its own `BlindedMessage` values, so a participant can
> disconnect only if it has pre-committed outputs for its exact fill amount. This
> is why only exact-fill (FOK) orders are offline-capable; partially fillable
> orders would need a pre-committed pool of lot-granularity authorizations, which
> is out of scope for v1.

In both patterns the mint does not learn the condition during blind preparation;
it first sees the plaintext condition at settlement or refund, as with other
NUT-10 conditions.

### Settlement request

```http
POST https://mint.host:3338/v1/exchange
```

```json
{
  "participants": [
    {
      "inputs": "<Array[Proof]>",
      "outputs": "<Array[BlindedMessage]>"
    },
    { "...": "one record per participant; N >= 2" }
  ]
}
```

The `participants` array contains one record per participant (`N >= 2`). Records
MUST appear in canonical participant order.

```bash
curl -X POST https://mint.host:3338/v1/exchange \
  -H "Content-Type: application/json" \
  -d '{"participants":[...]}'
```

#### Mint validation

Before any mutation, the mint MUST verify all of the following:

1. The request has two or more participant records. Advertised limits
   (`max_participants`, `max_inputs`, `max_outputs`, `max_request_bytes`) MUST be
   respected.
2. Every proof is authentic, unspent, unique in the request, and signed by an
   active or still-spendable keyset.
3. Every proof carries a supported, canonical `PAY_TO_UNLOCK` condition.
4. No input proof is reused across records and every input is unique in the
   request.
5. Each participant's inputs are all of that participant's `offer_keyset`.
6. Each participant's `outputs` list hashes exactly to that participant's
   `H_recv`.
7. Every output in a participant's `outputs` list has `id` equal to that
   participant's `receive_keyset`.
8. Exactly two distinct keysets appear across all participants' `offer_keyset`
   and `receive_keyset` values, and every participant's `receive_keyset` differs
   from its own `offer_keyset`. (Per-class amount conservation is rule 10; it does
   not require equal participant counts per class, so a one-taker/multi-maker star
   is valid.)
9. Every blinded output is unique, valid, uses an accepted keyset, and has not
   been signed before.
10. For each asset class `c` independently, summed over all participants:
    `sum(inputs_c) == sum(outputs_c) + input_fees_c`, where
    `input_fees_c = (sum(input_fee_ppk over inputs with id == c) + 999) // 1000`
    per [NUT-02][02]. Fees are computed and rounded **per class**, not globally.
    No additional operation fee is defined in v1.

**Processing order.** The mint first canonicalizes the request and computes
`request_digest`. If a committed response already exists for that digest, it is
returned unchanged (idempotent retry) without re-running the rules below. Only
otherwise are rules 1–10 applied, then the atomic commit. The mint MUST finish
validation before any expensive signing or durable mutation.

#### Atomic commit

The mint MUST commit these effects in one database transaction:

1. mark every selected input proof spent;
2. sign every selected blinded output;
3. persist every `BlindedMessage` and corresponding `BlindSignature` for
   [NUT-09][09] restoration; and
4. persist an idempotent response keyed by `request_digest`.

If any validation, signing, or persistence step fails, none of these effects may
commit. A byte-identical retry MUST return the previously committed result. An
input proof that already appears in a committed response under a conflicting
`request_digest` MUST fail without mutation.

#### Response

```json
{
  "signatures": [
    "<Array[BlindSignature] for participant[0] outputs>",
    "...",
    "<Array[BlindSignature] for participant[N-1] outputs>"
  ]
}
```

`signatures` has one entry per participant, in canonical participant order.

### Recovery

Recovery does not depend on the submitter. Because each owner created and
retained its receive `BlindedMessage` values, an owner can recover directly from
the mint:

1. Check its conditioned inputs with [NUT-07][07].
2. If they are spent, send the known blinded messages to [NUT-09][09].
3. The mint returns the signatures it already committed; the owner unblinds
   locally.

A wallet SHOULD retry [NUT-09][09] with bounded backoff when an input is spent
but no response was received. Wallets seeking stronger metadata privacy SHOULD
use an anonymity-preserving transport for recovery polling.

### Refund

A `PAY_TO_UNLOCK` proof is spendable in exactly two ways:

- **Settlement** — as an input to a valid `/v1/exchange` request (rules above).
- **Refund** — through an ordinary [NUT-03][03] swap to fresh outputs of the
  offered asset class, authorized by a signature from the `refund` key. The swap
  request MUST include, for each refunded input, a `Proof.witness` with a Schnorr
  signature by the `refund` private key over
  `refund_digest = tagged_hash("Cashu/PAY_TO_UNLOCK/refund", canonical_swap_request)`.
  The mint verifies the signature under the condition's `refund` public key;
  otherwise the refund is rejected. A refund is accepted **at any time**, so a
  participant can abort a failed exchange or withdraw a resting order whenever it
  chooses.

Settlement and refund serialize on proof spentness: the first valid mint
transaction to commit wins, and the loser's transaction is rejected without
effect (no funds are stranded). This is the same single-spend arbitration NUT-11
uses.

**Why the `refund` key is required.** A `PAY_TO_UNLOCK` proof is bearer and is
not spendable in a normal `/v1/swap` — that lock is precisely what prevents a
relay or counterparty from redirecting its value. Because the proof is bearer,
the refund path must be owner-gated: without a signature, any holder (the relay
that assembles the request, or the counterparty) could refund it to its own
outputs. Settlement needs no signature — the condition, `H_recv`, and per-class
conservation authorize it structurally — so the `refund` key is the sole
owner-authorization key and cannot be omitted. A wallet MUST use a fresh refund
key per authorization and MUST NOT share its private half.

Order validity windows, stale-price protection, and similar operational policy
are not defined here; they are the coordinator's concern (see
[Coordinator and relay role](#coordinator-and-relay-role)). A participant that
wants an authorization to lapse simply refunds it. A keyset's own
[activation/expiry lifecycle][02] bounds how long any proof — conditioned or not
— remains settellable.

### Fees

Input fees follow [NUT-02][02] per-keyset rules, computed and rounded **per asset
class** as defined in validation rule 10, and are included in that class's
conservation. The receiver's committed amount therefore equals the offered amount
minus that asset class's input fees. No additional operation fee is defined in v1;
a mint MAY advertise one in a later revision via an explicit condition tag.

### Mint info

Support MUST be advertised through [NUT-06][06]:

```json
{
  "exchange": {
    "supported": true,
    "version": 1,
    "max_participants": "<uint>",
    "max_inputs": "<uint>",
    "max_outputs": "<uint>",
    "max_request_bytes": "<uint>"
  }
}
```

`max_participants` bounds `N` in one atomic exchange.

A wallet MUST NOT create `PAY_TO_UNLOCK` proofs unless the mint advertises this
NUT and suitable bounds. Specific error codes are defined in
[error_codes.md](error_codes.md).

## Coordinator and relay role

A coordinator (or relay) is an **optional** deployment convenience used in the
coordinator-mediated pattern: it assembles the participants' conditioned proofs
and public receive descriptors and submits the settlement request on their
behalf. It is never required for correctness or recovery, and it has no special
on-mint role: any holder of all the valid authorizations may submit a request,
because custody does not depend on who submits (see the FAQ). Participants that
want a specific party to submit simply hand their authorizations only to that
party over their chosen off-mint transport.

Operational policy — order validity windows, stale-price handling, matching and
batching rules, anti-spam deposits, reputation — lives entirely at the
coordinator and is out of scope for this NUT. Recovery is always the direct
[NUT-07][07]/[NUT-09][09] path, independent of any coordinator.

## Resting-order optionality and relay discretion

A resting order — whether an offline FOK taker's pre-committed proofs or an
online maker's limit order waiting in a book — offers the market a free option:
it is most likely to fill exactly when price has moved against it (adverse
selection). This is the standard limit-order property of every order book, not a
settlement-atomicity problem, and it is unrelated to the adaptor-sig locktime
race this NUT removes. Separately, a relay has grouping and timing discretion
over which pre-authorized proofs it assembles into a request and when it submits;
it cannot redirect value or alter price (outputs and amounts are bound by
`H_recv`), but it can choose match timing and pairing. Mitigations for both are
order-book-level: batch auctions, validity windows enforced by the coordinator,
post-only orders, and reputation. None is a theft or safety violation.

## FAQ

**Why commit to blinded outputs rather than a receive public key?**
A `BlindedMessage` already commits to amount, receive keyset, and the
wallet-chosen blinded point `B_`. Only the wallet that knows the secret and
blinding factor can unblind the signature and build the proof. An unblinded
destination key would not give the same blind-issuance guarantee and would weaken
Cashu privacy.

**Can a submitter or coordinator steal the funds?**
No. (1) It receives only the _blinded_ receive messages `B_`; without the
blinding factors it cannot unblind the returned signatures into spendable proofs,
so it cannot steal what is received. (2) The input proofs it relays are locked by
`PAY_TO_UNLOCK` to the owner's exact receive outputs, so it cannot redirect the
value to itself — it can only submit the one authorized exchange. (3) The only
theft vector is the refund key; the owner keeps a fresh refund key per
authorization and never shares its private half. A coordinator can therefore at
worst delay notification or refuse to submit.

**What if the response is withheld?**
A withheld response can delay notification; it cannot redirect outputs, cannot
make the submitter spend the resulting proofs (it lacks the output secrets), and
cannot permanently deny a committed output while the mint complies with
[NUT-09][09]. Withholding is bounded to a notification delay.

**Can the mint link exchanges to an owner?**
Not from condition fields: fresh per-authorization `nonce`, refund key, proof
secret, and output secret carry no stable identity. The mint sees asset classes,
amounts, and timing per settlement transaction. It cannot achieve
identity-selective censorship from protocol fields alone.

**When is an N-party (star) exchange useful?**
An N-party atomic exchange commits one party on one side and one or more on the
other in a single database transaction. A typical use case is a matching engine
settling a taker's **Fill-or-Kill** (FOK) order against several makers: the
engine assembles one request and the mint settles all legs or none, so the taker
is never left with a partial fill because one maker's input was stale. General
N-way cycles (A->B->C->A) that would require a solver are out of scope for v1;
only star shapes (one side vs one or more of the other) are supported.

**Can a participant go offline after placing an order?**
Only for an exact-fill order. A Fill-or-Kill (FOK) taker knows its receive amount
at order placement, so it can pre-commit its conditioned proofs and disconnect;
the relay settles later and the taker recovers via [NUT-09][09]. A Fill-and-Kill
(FAK) taker and a resting maker do not know their fill amount until matched, so
they must be online at match to produce the exact receive outputs. (Blind
issuance requires the recipient to pre-commit its exact outputs — see the
blinding-budget lemma.)

**Is a refund key really necessary?**
Yes. See [Refund](#refund): a conditioned proof is bearer and not normal-spendable,
so the refund path must be owner-gated by a signature or any holder could refund
it to itself. Settlement needs no signature, so the refund key is the sole
owner-authorization key.

**Is there an expiry or validity window?**
Not in this NUT. A proof is settellable until it is spent or refunded, and a
participant withdraws an authorization simply by refunding it. Order validity and
staleness are the coordinator's operational concern; a keyset's own lifecycle
bounds how long any proof remains settellable.

**Can this represent a partially fillable standing order?**
Not in v1. A single-use proof has no mutable remaining allowance; standing orders
need additional machinery (pre-split funding lots, successor-proof chaining, or
mint-side state) and are deferred.

## References

- [NUT-02](02.md) · [NUT-03](03.md) · [NUT-06](06.md) · [NUT-07](07.md) ·
  [NUT-09](09.md) · [NUT-10](10.md) · [NUT-11](11.md) · [NUT-12](12.md) · [NUT-21](21.md) · [NUT-22](22.md)
- [Maurice Herlihy, Atomic Cross-Chain Swaps](https://arxiv.org/abs/1801.09515)
  — leader/follower topology and timelock hierarchy (the *structure* of an
  adaptor-sig/HTLC swap).
- [Mazumdar et al., Towards Faster Settlement in HTLC-based Cross-Chain
  Swaps](https://arxiv.org/abs/2211.15804) — the American-call-option-without-premium
  framing of the free-option locktime race this NUT removes.

[00]: 00.md
[02]: 02.md
[03]: 03.md
[06]: 06.md
[07]: 07.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[21]: 21.md
[22]: 22.md
[rfc8785]: https://www.rfc-editor.org/rfc/rfc8785.html
