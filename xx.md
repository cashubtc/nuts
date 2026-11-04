# NUT-XX: Non-Interactive Mint Delegation on Liveness Failure

`optional`

`depends on: NUT-02, NUT-06, NUT-07, NUT-12`

---

This NUT improves the **liveness** guarantees of custodial ecash mints that hold on-chain reserves. It lets a mint operator delegate control of its reserves to one or more third-party mints in a **non-interactive** way: while the original mint keeps renewing its reserve, it retains custody; after renewal stops, an eligible delegate can claim the reserve and process redemptions whose eligibility it can establish.

A mint can nominate multiple delegates with increasing eligibility delays. Recovery depends on a successful reserve claim, sufficient backing and complete proof-state information. Nomination alone does not establish unconditional **1-of-n liveness**.

> [!IMPORTANT]
> This is **ordered custodial failover, not trustless unilateral exit.** It improves recovery from liveness failures, not from malicious custody. Users are **not** protected if the original mint steals reserves before failing or is insolvent, and after failover they inherit the usual custodial trust assumptions under the delegate mint. It provides a recovery path when reserve ownership and proof eligibility can be established; it does not guarantee redemption after every failure.

## Overview

The scheme has four parts, three of which are wire-protocol concerns specified normatively here, and one (the on-chain reserve) which is informational:

1. **Advertisement** — a mint announces its delegates, the keysets it backs, and its spent-proof feed via [NUT-06][06] (normative).
2. **Spent-proof firehose** — a sequenced feed of proof-state changes that delegate mints subscribe to and mirror locally (normative).
3. **Failover redemption** — how a delegate accepts and pays out the original mint's proofs after taking over (normative).
4. **Reserve construction** — a recommended on-chain Taproot construction that enforces delegate eligibility delays (informational, see [Appendix](#appendix-reserve-construction-informational)).

Throughout, the original/custodial mint is **Bob** and a delegate mint is **Dave**.

### Trust and security model

- Delegates mirror events in the background but do not co-sign, receive Bob's reserve key or gate his normal spending.
- The handover is triggered by Bitcoin consensus (relative timelocks), not by any interaction with Bob, who may be permanently gone.
- Delegates are ordered from most to least trusted. Later delegates become eligible after longer delays; earlier delegates remain eligible. Only a successful spend of the reserve excludes other claims to that output.
- Public proof verification ([NUT-12][12]) lets Dave validate proofs it never signed, using only Bob's public keys.

## Advertisement

A mint signals support and announces its delegation arrangement via its [NUT-06][06] info endpoint (see [Mint info setting](#mint-info-setting)). Two roles are advertised:

- **As a custodian**: the delegates it has nominated, in priority order, and where its spent-proof firehose lives.
- **As a delegate**: the mints it backs and the keysets it will honor on failover, so wallets can discover where to take a dead mint's tokens.

## Spent-proof firehose

The original mint exposes changes from its existing proof-state storage as an append-only **firehose**. It includes spent proofs, pending spends and definitive releases of pending spends. Each delegate persists its own local mirror. This NUT requires no third-party journal service and no delegate acknowledgement in the primary mint's spend path.

A consumer with contiguous events through sequence `n` knows the published state through `n`. This does not establish that `n` is the final state when the primary disappears; see [Consistency model](#consistency-model).

### Multiple source mints

A delegate MAY use one local store for every mint it backs. Imported proof states and locally redeemed proofs MUST be scoped by the original mint and `Y`; each original mint has its own sequence and resume cursor. The source is the mint associated with the advertised feed, not inferred from the event's keyset ID alone. Keyset rotation MUST NOT reset that mint's sequence.

The original mint's mirror and the delegate's own proof state are separate logical namespaces; this NUT does not prescribe physical SQL tables. Replaying source events MUST NOT clear a proof that the delegate has already redeemed. If an input keyset cannot be associated unambiguously with one backed issuer, the delegate MUST reject it.

### Proof-state event

The proof identifier reuses `Y = hash_to_curve(secret)` from [NUT-00][00] / [NUT-07][07], no new identifier is introduced. A `ProofStateEvent` is:

```json
{
  "seq": <int>,
  "Y": <hex_str>,
  "id": <hex_str>,
  "amount": <int>,
  "state": <"PENDING"|"SPENT"|"UNSPENT">,
  "witness": <str|null>
}
```

- `seq` is a strictly increasing, gap-free integer sequence number assigned by the original mint across all its keysets. It MUST start at `0` and increment by exactly `1` per event. It MUST NOT be reordered or reused.
- `Y` is the proof's identifier, the hex-encoded compressed point `Y = hash_to_curve(secret)`.
- `id` is the keyset ID ([NUT-02][02]) the proof was signed under.
- `amount` is the proof's amount.
- `state` is `PENDING` for an input reserved for spending, `SPENT` when finalized, or `UNSPENT` after a definitive release of a pending spend. A timeout or unknown payment outcome is not a definitive release. `SPENT` is terminal.
- `witness` is the serialized witness for a finalized `SPENT` proof with a [NUT-10][10] spending condition (as in [NUT-07][07]); it MUST be `null` otherwise.

Neither `secret`, `r` nor private keys are published. `C` is not required: `Y` identifies the proof for state lookup; signature verification uses the `C` supplied in the redemption request.

> [!IMPORTANT]
> The original mint MUST durably record one event for each transition to `PENDING`, `SPENT`, or a released `UNSPENT` state. The proof-state change and its event/sequence MUST commit atomically in the mint's storage. Only committed events may be served. Delivery MAY be asynchronous and replayed; it MUST be recoverable after restart. An in-memory notification alone does not satisfy this requirement. When enabling the feed on an existing database, its initial history MUST include the existing spent/pending records consistently with concurrent transitions.

### Real-time stream (Server-Sent Events)

For real-time mirroring, the firehose is exposed as a [Server-Sent Events][sse] stream at the mint's `/v1/firehose/sse` path. SSE is a good fit because the feed is strictly uni-directional (mint to delegate), runs over plain HTTP, and has native reconnection with resume.

```http
GET https://mint.host:3338/v1/firehose/sse
```

The mint responds with `Content-Type: text/event-stream` and emits one SSE event per proof-state change. The event's `id` field carries the `seq`, so it doubles as the resume cursor; the `data` field is the JSON-encoded `ProofStateEvent`:

```
id: 42
event: proof_state
data: {"seq": 42, "Y": "02...", "id": "00ad...", "amount": 2, "state": "SPENT", "witness": null}
```

**Reconnection.** A standard `EventSource` client reconnects automatically and sends the last received `id` back in the `Last-Event-ID` HTTP header. On reconnection with a `Last-Event-ID` of `n`, the mint MUST resume the stream from `seq == n + 1`, so no events are missed across a dropped connection without any application-layer handshake.

If the mint cannot resume from the requested `Last-Event-ID` (for example, its live stream only retains recent events), it MUST first emit a `reset` event giving the range it can serve, signalling that the client should bootstrap the missing prefix via the catch-up endpoint before trusting the live stream. Published history MUST remain retrievable through that endpoint:

```
event: reset
data: {"earliest": <int>, "latest": <int>}
```

### Catch-up (HTTP)

A delegate that is bootstrapping its mirror, or that needs to backfill events it could not resume over SSE, fetches them with a single batch request. The request can mix arbitrary `seq` ranges and individual `seq` indexes, so a client can fill several scattered gaps at once rather than only one consecutive block:

```http
POST https://mint.host:3338/v1/firehose/batch
```

```json
{
  "ranges": [
    { "from": <int>, "to": <int> },
    ...
  ],
  "indexes": [ <int>, ... ]
}
```

- `ranges` is an array of inclusive `[from, to]` `seq` ranges. A range that omits `to` means "from `from` up to the latest event", which is how a fresh delegate bootstraps the whole feed (`{ "from": 0 }`).
- `indexes` is an array of individual `seq` values to fetch.

Both fields are optional but at least one MUST be present. The mint responds with a `FirehoseResponse`:

```json
{
  "events": <Array[ProofStateEvent]>,
  "latest": <int>
}
```

- `events` contains every requested `ProofStateEvent` that exists, ascending by `seq`, with duplicates from overlapping ranges/indexes removed.
- `latest` is the highest committed event sequence, or `-1` for an empty feed. It is an observed head, not a final cutover boundary.

The mint MAY cap the number of events returned per request; a truncated response MUST be an ascending prefix of the requested events, so the client can continue after the last returned sequence. A client MUST ensure it has contiguous `seq` coverage from `0` to `latest` before treating its mirror as caught up to that observed head.

### Consistency checkpoint (optional)

To let a delegate periodically verify its mirror matches the source without replaying the whole feed, the mint MAY expose a checkpoint that buckets the spent set by a prefix of `Y` and returns a Merkle root per bucket:

```http
GET https://mint.host:3338/v1/firehose/checkpoint
```

```json
{
  "seq": <int>,
  "buckets": [
    { "prefix": <hex_str>, "root": <hex_str>, "count": <int> },
    ...
  ]
}
```

`seq` is the sequence number the checkpoint was taken at. A delegate compares each `root` against the same computation over its own mirror; a mismatch identifies which bucket diverged, and the delegate re-syncs it by fetching the affected `seq`s through the catch-up endpoint's `ranges`/`indexes`. The bucketing scheme (prefix length, hashing) is left to implementations and is out of scope for double-spend safety, it is a consistency aid, not a requirement for failover. It covers only the spent subset and MUST NOT be used to establish final-state completeness.

## Failover redemption

Dave may enter **failover mode** for Bob only after its reserve timelock matures, its claim to the reserve is confirmed and it can establish the proof-state coverage required by the [Consistency model](#consistency-model). HTTP unavailability alone MUST NOT authorize recovery. If claim confirmation is lost, Dave MUST suspend further reserve-backed recovery.

After losing authority over the reserve, Bob MUST NOT issue or redeem against that backing. Restarting Bob does not restore the lost authority. Requests while recovery is inactive return `33002`. Existing spent/pending errors `11001` and `11002` apply to known spent or pending inputs.

In failover mode, Dave exposes Bob's keysets as **inactive** keysets (`active: false`, [NUT-02][02]): they contain public verification keys only and may be accepted as inputs to swap ([NUT-03][03]) and melt ([NUT-05][05]) but are never used to sign new outputs. A user simply points their wallet at Dave and submits Bob's proofs as inputs in the normal `/v1/swap` (to receive fresh Dave ecash) or `/v1/melt` (to withdraw to Bitcoin/Lightning) flows.

For each input proof signed under a Bob keyset, Dave accepts it **only if all** of the following hold:

1. The proof's `id` belongs to a Bob keyset that Dave mirrors and has the public keys for.
2. The proof's signature **publicly verifies** via its DLEQ proof ([NUT-12][12]) against that keyset's amount public key. The wallet MUST include the DLEQ proof with the blinding factor `r` on the proof (the "user to user" `Proof` form of [NUT-12][12]) so Dave can verify without Bob's private key.
3. The proof is neither `SPENT` nor `PENDING` in the covered source state, and has not been redeemed or reserved by Dave for Bob. Unknown state coverage is not evidence that a proof is unspent.
4. Its spending conditions and the normal transaction checks, including units, fees and duplicate inputs, are satisfied.
5. The confirmed reserve recovered for Bob has enough unallocated backing for the operation.

Dave MUST atomically reserve the inputs and corresponding recovery budget before signing outputs or initiating payment. On success it records the inputs as redeemed for Bob. Pending payment outcomes remain reserved until definitively reconciled. The same recovered reserve MUST NOT be credited twice, including through different keysets of Bob.

Swap outputs and melt change MUST use Dave's own active keysets, never Bob's keys. Backing assigned to those new liabilities is no longer available for another recovery payment.

> [!NOTE]
> **Privacy cost today.** The NUT-12 proof refers to the blinded issuance points, so Dave needs `r` to reconstruct them. The recovery data permits linking to issuance if the corresponding issuance records are available; `r` alone is not the user's identity. A future blind-BLS ecash scheme could verify its unblinded signatures publicly without this DLEQ/blinding data. That would avoid this disclosure for BLS-issued tokens, not restore privacy already lost or replace spent-state checks. BLS is not a prerequisite for this NUT.

### Consistency model

Replication is asynchronous: Bob does not wait for a delegate acknowledgement before normal spending. A contiguous mirror through the last observed `latest` establishes only a published prefix. It does not establish the absence of later spent or pending inputs, and a confirmed reserve claim does not establish feed completeness.

Before accepting recovery, Dave MUST establish coverage of the authoritative final proof state for the claimed reserve period. It MUST reject unresolved pending inputs and MUST NOT infer unspent state from an incomplete or stale mirror. A recovered-reserve cap limits payouts; it is not a substitute for these checks.

**Open requirement:** this draft does not yet specify how to establish that final boundary after an uncoordinated primary failure using only an asynchronous feed. Until that requirement is satisfied, recovery whose eligibility cannot be established MUST remain disabled. This is a safety limitation, not a guarantee of redemption after every outage.

## Wallet considerations

Wallets do not maintain the delegates' proof-state mirrors or participate in reserve claims. Recovery uses the existing swap/melt flows, but the client must route the original proofs to an eligible delegate and preserve the NUT-12 `(e, s, r)` data required above. Normal wallet-to-mint paths that omit `r` are insufficient for this recovery flow. Automatic delegate discovery is optional; manual selection can use the same APIs. A successful swap yields Dave's tokens, not Bob's tokens with a changed mint URL.

## Circular delegation

A set of mints can each act as delegate for the others, e.g. for three mints:

```
Bob (custodian) -> Dave (delegate) -> Frank (delegate)
Dave (custodian) -> Frank (delegate) -> Bob (delegate)
Frank (custodian) -> Bob (delegate) -> Dave (delegate)
```

A surviving eligible mint may claim an original reserve that has not already been spent, subject to the ownership, state-coverage and backing requirements above. This does not establish recovery after an earlier delegate already claimed the reserve. Successor custody, state transfer and remaining backing after that claim are outside this draft; no unconditional circular 1-of-n recovery is claimed.

## Mint info setting

A mint signals support via [NUT-06][06] with the following setting. Both roles are optional and a mint may populate either or both:

```json
"nuts": {
  "xx": {
    "supported": true,
    "reserves": [
      {
        "method": "onchain",
        "descriptor": <str|null>,
        "address": <str|null>
      }
    ],
    "delegates": [
      {
        "mint_url": <str>,
        "pubkey": <hex_str>,
        "delay": <int>
      }
    ],
    "firehose": {
      "sse": <str>,
      "http": <str>
    },
    "delegate_for": [
      {
        "mint_url": <str>,
        "keysets": <Array[hex_str]>
      }
    ]
  }
}
```

- `reserves` describes the on-chain reserve(s) backed by this scheme. `descriptor`/`address` are informational and let third parties watch the reserve; they are not required for the wire protocol.
- `delegates` lists the nominated delegate mints **in priority order**. `pubkey` is the delegate's reserve script-path key and `delay` is the relative timelock (in blocks) after which that delegate becomes eligible. The first entry has the smallest `delay`.
- `firehose` gives the Server-Sent Events stream (`sse`) and the HTTP catch-up/batch (`http`) URLs for this mint's proof-state feed.
- `delegate_for` lists the mints this mint backs and the specific keyset IDs ([NUT-02][02]) it will honor on failover. Wallets use this to discover, ahead of time, where a given mint's tokens can be redeemed if it goes dark.

Example:

```json
"nuts": {
  "xx": {
    "supported": true,
    "reserves": [
      { "method": "onchain", "address": "bc1p...", "descriptor": null }
    ],
    "delegates": [
      { "mint_url": "https://dave.example", "pubkey": "02ab...", "delay": 1008 },
      { "mint_url": "https://frank.example", "pubkey": "03cd...", "delay": 1152 }
    ],
    "firehose": {
      "sse": "https://bob.example/v1/firehose/sse",
      "http": "https://bob.example/v1/firehose/batch"
    },
    "delegate_for": [
      { "mint_url": "https://dave.example", "keysets": ["00ad268c4d1f5826", "0193c8..."] }
    ]
  }
}
```

## Appendix: Reserve construction (informational)

This section is **non-normative**. It describes a recommended on-chain construction that enforces delegate eligibility delays; the Bitcoin-layer mechanics are outside the wallet↔mint HTTP API. See [NUT-30][30] for related onchain vocabulary.

A mint holds its reserve in a Taproot output that is:

- **Key path:** spendable immediately by the custodian (Bob).
- **Script path:** one leaf per delegate, each timelocked relative to the UTXO age with `OP_CHECKSEQUENCEVERIFY`. The first delegate's leaf becomes spendable after `delay₁` (e.g. ~7 days), the second after `delay₂` (e.g. ~8 days), and so on.

```
Bob reserve (Taproot output):
  key path:
    immediate:     Bob (custodian)
  script path:
    after ~7 days: <delay1> OP_CHECKSEQUENCEVERIFY OP_DROP <Dave pubkey> OP_CHECKSIG
    after ~8 days: <delay2> OP_CHECKSEQUENCEVERIFY OP_DROP <Frank pubkey> OP_CHECKSIG
```

While Bob is live, it periodically **consolidates** reserve funds by spending the UTXO back to the same script via the key path. This rolls deposits into a single reserve UTXO and **re-arms** the relative timelocks, so long as confirmed renewals occur before delegate eligibility. If Bob stops rolling the reserve, each delegate becomes eligible when its own delay matures. Earlier delegates remain eligible after later delays mature; the delays create head starts, not exclusive spending windows. A confirmed claim spends that output and excludes competing claims to it (see [BIP-112][csv]).

This pairs well with TEE-based mints. A TEE reduces custody trust but increases liveness risk (losing access to sealed key material can strand reserves). Naming a non-TEE mint as a delegate restores liveness and can remove the TEE from the disaster-recovery path entirely.

## Error codes

See [error_codes.md][errors]. Codes relevant to this NUT:

| Code  | Description                             |
| ----- | --------------------------------------- |
| 33001 | Proof from unknown or unmirrored keyset |
| 33002 | Delegation not active                   |
| 33003 | Recovered reserve exhausted             |
| 33004 | Proof DLEQ verification failed          |
| 33005 | Firehose sequence out of range          |

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
[14]: 14.md
[21]: 21.md
[22]: 22.md
[30]: 30.md
[errors]: error_codes.md
[sse]: https://html.spec.whatwg.org/multipage/server-sent-events.html
[csv]: https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki
