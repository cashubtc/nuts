# NUT-Exchange: Atomic Multi-Asset Exchange

`draft` (final NUT name, number, and NUT-10 `kind` are provisional)

`optional`

`depends on: NUT-02, NUT-03, NUT-06, NUT-07, NUT-09, NUT-10, NUT-11, NUT-12`

---

This NUT defines an atomic exchange of two existing Cashu asset classes at one
mint. Two or more participants each contribute bearer proofs of one asset class
and commit to exact blinded receive outputs of the other class. The mint spends
every input and signs every output in a single database transaction, or changes
nothing.

## Premise

### The problem

A client-to-client atomic swap of Cashu tokens (for example an HTLC or
adaptor-signature swap) requires both wallets to remain available while they
exchange keys, commitments, signatures, mint requests, and claims. It exposes a
free-option locktime race: the party holding the swap secret (the leader) picks
when to trigger settlement inside the locktime window — completing only if price
has moved in its favor, otherwise letting the swap lapse — a free American option
on the locked rate. And a peer-to-peer swap cannot batch several independent
swaps into one mint transaction: each must be settled separately.

A Cashu mint already validates proof signatures, maintains spentness, and issues
blind signatures. This NUT uses that existing authority as the atomic settlement
layer, removing the interactive claim sequence and the locktime free option it
creates.

### Model

Each participant first locks its bearer proofs to an exact receive-output
commitment via a [NUT-10][10] `PAY_TO_UNLOCK` condition. The participants'
conditioned proofs and public receive descriptors are assembled into one
settlement request and submitted to the mint. The mint validates every condition
and conserves each asset class independently, then commits all input spends and
all output signatures in one transaction — or changes nothing.

Two preparation patterns are supported: a **direct two-party swap** where both
participants are online, and a **coordinator-mediated swap** where a relay
assembles matched participants' material (see [Preparation](#preparation)). A
coordinator or relay is **optional** and has no on-mint authority: any holder of
all the valid authorizations may submit a request.

### Trust boundary and anonymity

The mint is trusted for the same things [NUT-11][11] P2PK already trusts it
(rejecting invalid spends, maintaining spentness, blind signing) **plus one
atomic database commit**. No transparency or accountability layer is defined
here. Two mitigations bound the added trust:

1. **A violation is transcript-checkable.** Any party holding the full transcript
   (inputs, conditions, output commitments, signatures, expiry) can prove the mint
   accepted an exchange that violates a condition or a conservation rule. This
   is incidental verifiability, not a published audit log.
2. **Protocol fields carry no stable owner identity.** Fresh per-authorization
   `nonce`, refund key, proof secret, and output secret prevent the mint from
   performing _identity-selective_ betrayal from protocol fields alone. The mint
   still sees asset classes, amounts, timing, and transport metadata, and may
   still censor, deny service, or betray an exchange wholesale — the same issuer
   trust NUT-11 carries.

### Scope

Version 1 supports:

- one mint;
- two or more participants in one atomic two-class exchange (any N-vs-M shape,
  e.g. one taker against one or more makers, or multiple makers on both sides);
- exactly two existing asset classes, one offered per side;
- exact, owner-precommitted blinded receive outputs;
- per-asset-class conservation; and
- one atomic commit (all participants settle or none).

Version 1 does **not** support: a coordinator as a required party; cross-mint
settlement; general N-way cycles (A wants B, B wants C, C wants A) that would
require a solver; partial fills of one authorization; a mutable remaining
balance; a venue-selected price or amount range; asset creation or destruction.

Separate `/v1/exchange` calls are independent: a failure or retry of one never
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
carrying it authorizes one exact exchange.

```json
[
  "PAY_TO_UNLOCK",
  {
    "nonce": "<hex_str: 32 bytes>",
    "data": "<hex_str: H_recv>",
    "tags": [
      ["offer_keyset", "<keyset_id>"],
      ["expiry", "<unix_seconds_str>"],
      ["refund", "<xonly_pubkey_hex>"]
    ]
  }
]
```

- `data` is `H_recv`, the commitment to this participant's complete ordered
  receive-output list (see [Receive-output commitment](#receive-output-commitment)).
- `offer_keyset` binds the participant's offered asset class. The receive asset class is the common `id` of all entries in the output bundle (authenticated by `H_recv`).
- `expiry` is a unix timestamp checked against the mint clock. It is the binding
  window of the commitment: settlement is valid only before it and refund only
  after it (the two states are mutually exclusive). It MUST be set; a short window
  (seconds to minutes) keeps a resting offer reliable without long lockup.
- `refund` is a fresh x-only public key whose private half the owner retains. A
  signature under it authorizes the reclaim path, valid only after `expiry`. A
  wallet MUST use a fresh refund key per authorization and MUST NOT share its
  private half (see [Refund](#refund)).

The condition answers one question:

> May this proof be consumed by a transaction that atomically creates exactly
> these blinded outputs?

Every proof contributed by one participant MUST carry the same `offer_keyset`,
`H_recv`, `expiry`, and `refund`. Across the exchange, the set of `offer_keyset`
values MUST equal the set of receive keysets (the common output `id` of each
participant's bundle, authenticated by `H_recv`) — i.e. every asset class offered
by some participant is received by some (other) participant, and vice versa.
Per-class amount conservation is rule 10's job, so
the count of participants on each side is unconstrained: 1-vs-N, N-vs-M, and
N-vs-N are all valid two-class shapes. In the common shape, one side offers
class `X` and receives `Y`; the other side offers `Y` and receives `X`.

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
The length prefix is a 4-byte little-endian unsigned integer recording the
**entry count** (not byte length; output lists are not capped at 255):

```
recv_canonical = uint32_le(len) || entry[0]_canonical || ... || entry[n-1]_canonical
H_recv = tagged_hash("Cashu/PAY_TO_UNLOCK/recv", recv_canonical)
```

where `tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)`.
Amounts are unsigned 64-bit integers; the mint MUST reject outputs whose amounts
are not representable as u64.

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
- **Amounts**: encoded as JSON numbers per JCS, MUST be unsigned integers in
  `[0, 2^64)`. The mint MUST use checked, non-wrapping arithmetic for all sums
  in validation rule 10.
- **`PAY_TO_UNLOCK` condition**: each of the three tags (`offer_keyset`,
  `expiry`, `refund`) MUST appear exactly once; unknown or duplicate tags MUST be
  rejected. `expiry` is decimal unix seconds without leading zeros or fractional
  part. Keyset IDs use their [NUT-02][02] canonical form; the refund key is a
  BIP-340 x-only pubkey in hex.
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
   class into `PAY_TO_UNLOCK` proofs committed to `H_recv`, choosing an `expiry`
   and a fresh `refund` key it retains;
3. verifies the [NUT-12][12] DLEQ proofs on the returned blind signatures and
   checks that the conditioned proofs encode the agreed terms;
4. one participant assembles both participants' conditioned proofs and public
   receive `BlindedMessage` lists and POSTs `/v1/exchange`.

If the request fails validation, no proof is spent; each participant reclaims its
own conditioned proofs via refund after `expiry`, then retries or walks away.

#### Coordinator-mediated swap

A matching engine pairs orders and a relay assembles and submits the settlement
request. Each participant prepares its conditioned proofs as in the two-party
flow above. A participant that wants offline capability may prepare **multiple
lots**, each a separate `PAY_TO_UNLOCK` authorization with its own `H_recv`, its
own inputs, and its own `expiry`; each lot becomes its own participant record in
`/v1/exchange`. The submitter includes only the lots it actually matches; unused
lots remain unspent and are reclaimed by their owner via refund after their own
`expiry`. A participant that has pre-committed sufficient lots to cover any
acceptable match may disconnect before matching; a participant that prepares
conditioned proofs only after a match is agreed must be online at match time.

The relay assembles every matched participant's conditioned proofs and public
receive descriptors into one `/v1/exchange` request and submits it.

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

1. The request has two or more participant records, each containing at least one
   input and one output. Advertised limits (`max_participants`, `max_inputs`,
   `max_outputs`, `max_request_bytes`) MUST be respected.
2. Every proof is authentic, unspent, unique in the request, and signed by an
   active or still-spendable keyset.
3. Every proof carries a supported, canonical `PAY_TO_UNLOCK` condition (each of
   the four tags appearing exactly once, no unknown tags; see [Canonical
   encodings](#canonical-encodings)).
4. No input proof is reused across records and every input is unique in the
   request.
5. Each participant's inputs are all of that participant's `offer_keyset`.
6. Each participant's `outputs` list hashes exactly to that participant's
   `H_recv`.
7. Every output in a participant's `outputs` list shares the same `id`; that
   common `id` is the participant's receive keyset (authenticated by `H_recv`).
8. Exactly two distinct keysets appear across all participants' `offer_keyset`
   values and their derived receive keysets, and every participant's receive
   keyset differs from its own `offer_keyset`. Per-class amount conservation
   (rule 10) does not require equal participant counts per class, so any
   two-class shape is valid:
   1-vs-N, N-vs-M, or N-vs-N.
9. Every blinded output is unique, valid, uses an accepted keyset, and has not
   been signed before.
10. For each asset class `c` independently, summed over all participants with
    checked, non-wrapping unsigned 64-bit arithmetic:
    `sum(inputs_c) == sum(outputs_c) + input_fees_c`, where amounts are unsigned
    64-bit integers and
    `input_fees_c = (sum(input_fee_ppk over inputs with id == c) + 999) // 1000`
    per [NUT-02][02]. Fees are computed and rounded **per class**, not globally.
    No additional operation fee is defined in v1.
11. The request is submitted before the minimum `expiry` across all
    participants' conditions (mint clock); an expired proof is not settleable.

**Processing order.** The mint first canonicalizes the request and computes
`request_digest`. If a committed response already exists for that digest, it is
returned unchanged (idempotent retry) without re-running the rules below. Only
otherwise are rules 1–11 applied, then the atomic commit. The mint MUST finish
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

Recovery is the direct [NUT-07][07]/[NUT-09][09] path, with one note: because
each **owner** retained its own receive `BlindedMessage` values, the owner — not
the submitter — recovers signatures from the mint and unblinds locally. A wallet
SHOULD retry [NUT-09][09] with bounded backoff when an input is spent but no
response was received. Wallets seeking stronger metadata privacy SHOULD use an
anonymity-preserving transport for recovery polling.

### Refund

A `PAY_TO_UNLOCK` proof has two mutually exclusive spend paths selected by the
mint clock:

- **Before `expiry`**: only as an input to a valid `/v1/exchange` (rules above).
- **At or after `expiry`**: only via an ordinary [NUT-03][03] swap to fresh
  outputs of the offered asset class, where each refunded input carries a
  `Proof.witness` containing a single BIP-340 Schnorr signature by the `refund`
  private key over

  ```
  refund_digest = tagged_hash("Cashu/PAY_TO_UNLOCK/refund", canonical_swap_request)
  ```

  where `canonical_swap_request` is the [RFC 8785][rfc8785] JCS encoding of the
  NUT-03 swap request object `{inputs, outputs}` (same canonicalization rule as
  the settlement request). The mint verifies that the current time is at or past
  the condition's `expiry`, that the signature is valid under the condition's
  `refund` public key, and that the swap issues refund outputs in an **active
  keyset of the same unit** as the condition's `offer_keyset` (not necessarily
  the same keyset ID, since the original keyset may have been rotated and
  [NUT-02][02] forbids new outputs from inactive keysets). Otherwise the refund
  is rejected. The mint MUST NOT accept a refund before `expiry`, and MUST NOT
  accept an expired proof in a `/v1/exchange` settlement.

The proof is therefore committed until `expiry` — settlement is the only valid
spend — and reclaimable by the owner afterwards — refund is the only valid spend.
The `refund` signature owner-gates the reclaim path: without it, any holder of
the bearer proof could refund it to itself.

Liveness is preserved: a `/v1/exchange` that fails validation commits nothing
(inputs stay unspent), and the owner reclaims its conditioned proofs via refund
once `expiry` passes. A keyset's own [activation/expiry lifecycle][02] is a
separate, coarse issuer-level bound and does not replace the per-authorization
`expiry`.

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
    "max_request_bytes": "<uint>",
    "max_expiry_seconds": "<uint>"
  }
}
```

`max_participants` bounds `N` in one atomic exchange. `max_expiry_seconds` bounds
the lifetime of a `PAY_TO_UNLOCK` condition: the mint MUST reject any
[NUT-03][03] swap that mints a `PAY_TO_UNLOCK` proof whose `expiry` exceeds the
current mint clock plus `max_expiry_seconds`.

A wallet MUST NOT create `PAY_TO_UNLOCK` proofs unless the mint advertises this
NUT and suitable bounds. Specific error codes are defined in
[error_codes.md](error_codes.md).

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

## References

- [NUT-02](02.md) · [NUT-03](03.md) · [NUT-06](06.md) · [NUT-07](07.md) ·
  [NUT-09](09.md) · [NUT-10](10.md) · [NUT-11](11.md) · [NUT-12](12.md) · [NUT-21](21.md) · [NUT-22](22.md)
- [Maurice Herlihy, Atomic Cross-Chain Swaps](https://arxiv.org/abs/1801.09515)
  — leader/follower topology and timelock hierarchy (the _structure_ of an
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
