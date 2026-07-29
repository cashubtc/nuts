# NUT-Exchange: Atomic Multi-Asset Exchange

`draft` (final NUT name, number, and NUT-10 `kind` are provisional)

`optional`

`depends on: NUT-02, NUT-03, NUT-06, NUT-07, NUT-09, NUT-10, NUT-11, NUT-12`

---

This NUT defines an atomic exchange of two existing Cashu asset classes at one
mint. Two or more participants each contribute bearer proofs of one asset class
and commit to blinded receive outputs of the other class. The mint spends every
input and signs every output in a single database transaction, or changes
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

Each participant first locks its bearer proofs to a receive-output commitment
via a [NUT-10][10] `PAY_TO_UNLOCK` condition. The participants' conditioned
proofs and public receive descriptors are assembled into one settlement request
and submitted to the mint. The mint validates every condition and conserves
each asset class independently, then commits all input spends and all output
signatures in one transaction — or changes nothing.

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
- two or more participants in one atomic two-class exchange (any N-vs-M shape);
- exactly two existing asset classes, one offered per side;
- owner-precommitted blinded receive outputs, with optional change outputs in the
  offer keyset and alternative output bundles for FAK-style orders;
- per-asset-class conservation; and
- one atomic commit (all participants settle or none).

Version 1 does **not** support: a coordinator as a required party; cross-mint
settlement; general N-way cycles that would require a solver; asset creation or
destruction.

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
- **Change output**: an output in the participant's offer keyset, returning
  unspent input value. Enabled by the condition's `allow_change` tag (see below).

### `PAY_TO_UNLOCK` condition

A [NUT-10][10] well-known secret `kind` named `PAY_TO_UNLOCK`. A proof carrying
it authorises one exact exchange — or, if `alt_outputs` is present, one exchange
chosen from a finite set of owner-authorised output bundles.

```json
[
  "PAY_TO_UNLOCK",
  {
    "nonce": "<hex_str: 32 bytes>",
    "data": "<hex_str: H_recv (primary bundle)>",
    "tags": [
      ["offer_keyset", "<keyset_id>"],
      ["expiry", "<unix_seconds_str>"],
      ["refund", "<xonly_pubkey_hex>"],
      ["coordinator_pubkey", "<xonly_pubkey_hex>"],
      ["alt_outputs", "<H_recv_alt_1>", "<H_recv_alt_2>", "..."],
      ["allow_change"],
      ["min_output_amount", "<uint_str>"]
    ]
  }
]
```

**Required tags** (MUST appear exactly once):

- `offer_keyset`: binds the participant's offered asset class. The mint MUST
  verify `offer_keyset == Proof.id` on every input (prevents keyset-ID relabeling
  when verification keys are shared across keysets).
- `expiry`: unix timestamp. Settlement valid only before it; refund only after.
- `refund`: fresh x-only public key whose private half the owner retains.

**Optional tags** (MAY appear; each at most once):

- `alt_outputs`: authorises a finite set of alternative output bundles in
  addition to the primary `data`. Each value is a `H_recv` computed identically
  to `data`. The submitted output bundle MUST hash to `data` or any listed
  alternative. Enables FAK-style orders where the actual fill amount varies (each
  bundle includes a different change amount). All inputs in one participant
  record MUST carry the identical `alt_outputs` set.
- `allow_change`: if present, outputs MAY include entries in the offer keyset
  (change outputs) in addition to entries in the receive keyset. Without this
  tag, all outputs MUST use a single keyset (the receive keyset). See [Change
  outputs](#change-outputs).
- `min_output_amount`: minimum total receive-keyset output amount (excluding
  change). The mint MUST reject if the actual receive output is below this floor.
  Prevents a coordinator from filling a tiny amount to consume the authorization
  and force a refund.
- `coordinator_pubkey`: optional BIP-340 x-only public key (64 lowercase hex
  chars / 32 bytes) binding these proofs to one coordinator. If present on any
  input, the settlement requires `coordinator_sig` (see Mint validation);
  permitted in standard and pool mode. It prevents the same authorization being
  submitted to two coordinators — only the bound key can authorize a distinct
  settlement.

Unknown tags MUST be rejected. `expiry` is decimal unix seconds without leading
zeros. Keyset IDs use their [NUT-02][02] canonical form; the refund key is a
BIP-340 x-only pubkey in hex.

Every proof contributed by one participant MUST carry a `PAY_TO_UNLOCK`
condition with the same `data` (`H_recv`), the same tags (`offer_keyset`,
`expiry`, `refund`, and any optional tags), but a **unique `nonce` per proof**.
The `nonce` provides per-proof anti-replay; the meaningful authorisation fields
are shared. This allows multiple proofs (e.g., micro-denomination inputs) in one
record without duplicate secrets. Across the exchange, the set of `offer_keyset`
values MUST equal the set of receive keysets.

### Change outputs

When `allow_change` is present, a participant's output bundle MAY contain entries
in both the receive keyset and the offer keyset. The receive-keyset entries are
the participant's desired receive amount; the offer-keyset entries are change
returned from unspent input.

Change is determined by per-class conservation (rule 10) at the aggregate level.
The change outputs MUST be included in the committed bundle (`H_recv` or an
`alt_outputs` entry) — the coordinator cannot insert its own change outputs
because it lacks the owner's blinding factors.

Change outputs do NOT add a third asset class. The exchange still has exactly two
keysets: the offer keyset (now appearing on both input and output sides) and the
receive keyset.

### Receive-output commitment

The receive destination is the owner's ordered list of `BlindedMessage` values,
including any change outputs. The canonical encoding of one entry is:

```json
{"amount": <uint>, "id": "<keyset_id>", "B_": "<hex_str>"}
```

The commitment is a BIP-340 tagged hash over the length-prefixed concatenation
of entries in declared order. Each `entry_canonical` is the entry serialized with
the [RFC 8785][rfc8785] JSON Canonicalization Scheme (JCS): UTF-8, object keys in
lexicographic order, no insignificant whitespace. **Amounts are encoded as
decimal strings** (not JSON numbers) in the canonical form to avoid IEEE-754
precision loss above 2^53. The length prefix is a 4-byte little-endian unsigned
integer recording the **entry count** (not byte length):

```
recv_canonical = uint32_le(len) || entry[0]_canonical || ... || entry[n-1]_canonical
H_recv = tagged_hash("Cashu/PAY_TO_UNLOCK/recv", recv_canonical)
```

where `tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)` and
each `entry_canonical` is `{"amount":"<decimal_str>","id":"<keyset_id>","B_":"<hex>"}`.
Amounts are unsigned 64-bit integers; the mint MUST reject outputs whose amounts
are not representable as u64.

Duplicate entries, unknown fields, non-canonical encodings, and list-prefix
matches MUST be rejected.

### Canonical encodings

- **Participant record**: the JSON object `{"inputs": [...], "outputs": [...]}`,
  with `inputs` sorted by `(id, secret)` and `outputs` in declared order,
  serialized via [RFC 8785][rfc8785] JCS. **All `amount` fields (`Proof.amount`
  and `BlindedMessage.amount`) are encoded as decimal strings** (not JSON numbers)
  in the canonical form, to avoid IEEE-754 precision loss above 2^53. Amounts
  MUST be unsigned integers in `[0, 2^64)` with no leading zeros. The mint MUST
  use checked, non-wrapping arithmetic for all sums.
- **`PAY_TO_UNLOCK` condition**: the three required tags (`offer_keyset`,
  `expiry`, `refund`) MUST each appear exactly once. Optional tags (`alt_outputs`,
  `allow_change`, `min_output_amount`, `coordinator_pubkey`) MAY each appear at
  most once. Unknown tags
  MUST be rejected. `alt_outputs` values MUST be distinct 64-char hex strings;
  the mint MUST reject if `alt_outputs` count exceeds advertised `max_alt_outputs`.
  `min_output_amount` is a minimal unsigned decimal string (no leading zeros).
- **Participant order**: records are ordered by the lexicographically smallest
  `(id, secret)` among each participant's inputs. Proof secrets are unique
  across the whole request, so this is a strict total order.
- **Request digest** (optional, for idempotent retries):

```
req_canonical = participant[0]_canonical || ... || participant[n-1]_canonical
request_digest = tagged_hash("Cashu/exchange/request", req_canonical)
coordinator_digest = tagged_hash("Cashu/PAY_TO_UNLOCK/coordinator", req_canonical)
```

`coordinator_sig` signs `coordinator_digest` and is excluded from `req_canonical`,
which already binds each proof secret (hence `coordinator_pubkey` and the spent
identifier `Y`), the outputs, and any pool manifest/selection.

If the mint supports idempotent retries (advertised via `idempotent_retries` in
[NUT-06][06] info), the request digest enables fast retry: a byte-identical
request returns the cached response instead of failing on double-spend. Without
this feature, clients fall back to [NUT-09][09] recovery.

### Preparation

#### Two-party direct swap

Two participants agree on an exact exchange. Both are online. Each participant:

1. prepares blinded receive outputs and computes `H_recv`;
2. uses an ordinary [NUT-03][03] swap to convert its bearer proofs into
   `PAY_TO_UNLOCK` proofs committed to `H_recv`;
3. verifies the [NUT-12][12] DLEQ proofs;
4. one participant assembles both participants' material and POSTs
   `/v1/exchange`.

#### Coordinator-mediated swap with FAK support

A matching engine pairs orders. For exact-fill orders (FOK), each participant
prepares one `H_recv` as above. For variable-fill orders (FAK), a participant
uses `alt_outputs` + `allow_change` + `min_output_amount`:

1. Generate the receive outputs for the **maximum** fill (e.g., 100 USD).
2. For each possible fill amount (one per price tick), generate a complete bundle:
   receive outputs + change outputs in the offer keyset for the unspent portion.
3. Compute `H_recv` for each bundle. Set `data` to the max-fill bundle; list the
   rest in `alt_outputs`.
4. Set `min_output_amount` to the minimum acceptable receive amount.
5. Lock the full input amount in one `PAY_TO_UNLOCK` proof (one NUT-03 swap).
6. The coordinator picks the matching bundle at match time.

One proof, one swap, tick-level granularity. The coordinator can only select
among owner-authorised bundles; it cannot alter any bundle's contents.

A participant that has pre-committed sufficient bundles may disconnect before
matching. Unused proofs are reclaimed via refund after `expiry`.

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
  ],
  "coordinator_sig": "<hex_str: 128 chars; present iff any input carries coordinator_pubkey>"
}
```

#### Mint validation

Before any mutation, the mint MUST verify:

1. Two or more participant records, each with ≥1 input and ≥1 output. Advertised
   limits respected.
2. Every proof is authentic, unspent, unique in the request, and signed by an
   active or still-spendable keyset.
3. Every proof carries a canonical `PAY_TO_UNLOCK` condition: the three required
   tags each exactly once; optional tags at most once; no unknown tags.
4. No input proof is reused across records; every input is unique.
5. Each input's `Proof.id == offer_keyset` (prevents keyset relabeling).
6. Each participant's `outputs` list hashes to the condition's `data` **or** an
   `alt_outputs` entry. (If `alt_outputs` is absent, must match `data` exactly.)
7. If `allow_change` is absent: every output `id` is the same (the receive
   keyset), and that keyset differs from `offer_keyset`. If `allow_change` is
   present: every output `id` is either the receive keyset or the `offer_keyset`;
   at least one output MUST use the receive keyset; the receive keyset MUST differ
   from `offer_keyset`.
8. Exactly two distinct keysets appear across all participants' `offer_keyset`
   values and receive keysets. Per-class conservation (rule 10) does not require
   equal participant counts per class, so any two-class shape is valid: 1-vs-N,
   N-vs-M, or N-vs-N.
9. Every blinded output is unique, valid, uses an accepted keyset, and has not
   been signed before.
10. For each asset class `c` independently, with checked, non-wrapping u64
    arithmetic: `sum(inputs_c) == sum(outputs_c) + input_fees_c`, where
    `input_fees_c = (sum(input_fee_ppk over inputs with id == c) + 999) // 1000`
    per [NUT-02][02]. Fees are computed and rounded **per class**, not globally.
11. The request is submitted before the minimum `expiry` across all participants'
    conditions.
12. If `min_output_amount` is present: the total receive-keyset output amount for
    that participant MUST be ≥ `min_output_amount`. (Change outputs in the offer
    keyset are excluded from this check.)
13. **Coordinator authentication.** If any input carries `coordinator_pubkey`
    (BIP-340 x-only key, 64 lowercase hex / 32 bytes), every such input MUST
    decode to the same key `K`, and the request MUST carry `coordinator_sig` — a
    BIP-340 signature (128 lowercase hex / 64 bytes) valid under `K` over
    `coordinator_digest` ([Canonical encodings](#canonical-encodings)). Version 1
    permits one `K` per request; if no input carries `coordinator_pubkey`,
    `coordinator_sig` MUST be absent. Reject with 15015 on key disagreement or a
    missing, invalid, or unexpected signature. The signature authorizes the
    request but does not assert inputs are unspent (rules 2 and 11 remain;
    [NUT-07][07] is advisory). Binding proofs to `K` prevents a _different_
    coordinator key from authorizing a distinct settlement.

**Processing order.** Verify coordinator authentication (rule 13) before any
idempotency-cache lookup. If idempotent retries are supported, canonicalize and
compute `request_digest` (excluding `coordinator_sig`) first; if a committed
response exists, return it. Otherwise apply rules 1–13, then atomic commit.

#### Atomic commit

The mint MUST commit in one transaction:

1. mark every input proof spent;
2. sign every blinded output;
3. persist every `BlindedMessage` / `BlindSignature` for [NUT-09][09] restoration;
4. if idempotent retries are supported, persist response keyed by `request_digest`.

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

### Recovery

Recovery is the direct [NUT-07][07]/[NUT-09][09] path. Because each **owner**
retained its own receive `BlindedMessage` values, the owner — not the submitter —
recovers signatures from the mint and unblinds locally. A wallet SHOULD retry
[NUT-09][09] with bounded backoff when an input is spent but no response was
received.

### Refund

A `PAY_TO_UNLOCK` proof has two mutually exclusive spend paths:

- **Before `expiry`**: only as an input to `/v1/exchange`.
- **At or after `expiry`**: only via an ordinary [NUT-03][03] swap to fresh
  outputs of the offered asset class, where each refunded input carries a
  `Proof.witness` containing a single BIP-340 Schnorr signature by the `refund`
  private key over:

  ```
  refund_digest = tagged_hash("Cashu/PAY_TO_UNLOCK/refund", canonical_refund_request)
  ```

  where `canonical_refund_request` is the [RFC 8785][rfc8785] JCS encoding of the
  swap request object `{inputs, outputs}`, with each input `Proof` serialized
  **without** its `witness` field (the witness carries the signature and cannot
  be included in its own preimage). **All `amount` fields are encoded as decimal
  strings** (same rule as participant canonicalization). The mint verifies:
  current time ≥ `expiry`; signature valid under `refund` public key; swap issues
  outputs in an active keyset of the same unit as `offer_keyset`. Otherwise
  rejected.

The `refund` signature owner-gates the reclaim path: without it, any holder of
the bearer proof could refund it to itself. Liveness is preserved: a failed
`/v1/exchange` commits nothing, and the owner reclaims via refund once `expiry`
passes.

### Fees

Input fees follow [NUT-02][02] per-keyset rules, computed and rounded **per asset
class** as defined in rule 10. Change outputs are in the offer keyset and are
included in that class's conservation (they reduce the fee-adjusted output to the
counterparty, not the change recipient).

### Mint info

```json
{
  "exchange": {
    "supported": true,
    "version": 1,
    "max_participants": "<uint>",
    "max_inputs": "<uint>",
    "max_outputs": "<uint>",
    "max_request_bytes": "<uint>",
    "idempotent_retries": "<bool>",
    "max_alt_outputs": "<uint>",
    "max_expiry_seconds": "<uint>"
  }
}
```

`max_alt_outputs` bounds the number of alternative `H_recv` values per
condition. `max_expiry_seconds` bounds condition lifetime at [NUT-03][03] swap
time.

## FAQ

**Why commit to blinded outputs rather than a receive public key?**
A `BlindedMessage` already commits to amount, receive keyset, and the
wallet-chosen blinded point `B_`. Only the wallet that knows the secret and
blinding factor can unblind the signature and build the proof.

**Can a submitter or coordinator steal the funds?**
No. (1) It receives only the _blinded_ receive messages; without the blinding
factors it cannot unblind signatures. (2) Inputs are locked by `PAY_TO_UNLOCK`
to owner-authorised bundles — including change outputs, which use the owner's
blinding factors. (3) The only theft vector is the refund key; the owner keeps
a fresh one per authorization.

**How does FAK work?**
Use `alt_outputs` + `allow_change` + `min_output_amount`. One proof authorises a
finite set of output bundles (one per price tick). The coordinator picks the
matching bundle. See [Coordinator-mediated swap](#coordinator-mediated-swap-with-fak-support).

## References

- [NUT-02](02.md) · [NUT-03](03.md) · [NUT-06](06.md) · [NUT-07](07.md) ·
  [NUT-09](09.md) · [NUT-10](10.md) · [NUT-11](11.md) · [NUT-12](12.md)
- [Maurice Herlihy, Atomic Cross-Chain Swaps](https://arxiv.org/abs/1801.09515)
- [Mazumdar et al., Towards Faster Settlement in HTLC-based Cross-Chain
  Swaps](https://arxiv.org/abs/2211.15804)

[00]: 00.md
[02]: 02.md
[03]: 03.md
[06]: 06.md
[07]: 07.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[rfc8785]: https://www.rfc-editor.org/rfc/rfc8785.html
