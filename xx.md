# NUT-XX: Non-Interactive Mint Delegation on Liveness Failure

`optional`

`depends on: NUT-02, NUT-06, NUT-07, NUT-12`

---

This NUT improves the **liveness** guarantees of custodial ecash mints that hold on-chain reserves. It lets a mint operator delegate control of its reserves to one or more third-party mints in a **non-interactive** way: while the original mint is operating, it keeps unilateral control of the reserve; if it becomes unresponsive, a delegate mint can take over and process redemptions for the original mint's users.

A mint can delegate to multiple other mints. If a set of mints all act as delegates for each other, they collectively inherit a **1-of-n liveness** property: as long as one mint in the set stays online, the users of every mint in the set can redeem their funds.

> [!IMPORTANT]
> This is **ordered custodial failover, not trustless unilateral exit.** It improves recovery from liveness failures, not from malicious custody. Users are **not** protected if the original mint steals reserves before failing or is insolvent, and after failover they inherit the usual custodial trust assumptions under the delegate mint. It only ensures that _"the original mint disappeared"_ no longer means _"the funds are lost forever."_

## Overview

The scheme has four parts, three of which are wire-protocol concerns specified normatively here, and one (the on-chain reserve) which is informational:

1. **Advertisement** — a mint announces its delegates, the keysets it backs, and its spent-proof feed via [NUT-06][06] (normative).
2. **Spent-proof firehose** — a sequenced feed of spent-proof identifiers that delegate mints subscribe to and mirror locally (normative).
3. **Failover redemption** — how a delegate accepts and pays out the original mint's proofs after taking over (normative).
4. **Reserve construction** — a recommended on-chain Taproot construction that enforces the failover ordering (informational, see [Appendix](#appendix-reserve-construction-informational)).

Throughout, the original/custodial mint is **Bob** and a delegate mint is **Dave**.

### Trust and security model

- Delegates are **not** part of normal operation. They do not co-sign, do not see the reserve key, and have no influence over Bob's balance while it is live.
- The handover is triggered by Bitcoin consensus (relative timelocks), not by any interaction with Bob, who may be permanently gone.
- Delegates are ordered from most to least trusted. Adding later delegates never weakens earlier windows: a later delegate can only act if every earlier delegate fails to act before its own timelock matures.
- Public proof verification ([NUT-12][12]) lets Dave validate proofs it never signed, using only Bob's public keys.

## Advertisement

A mint signals support and announces its delegation arrangement via its [NUT-06][06] info endpoint (see [Mint info setting](#mint-info-setting)). Two roles are advertised:

- **As a custodian**: the delegates it has nominated, in priority order, and where its spent-proof firehose lives.
- **As a delegate**: the mints it backs and the keysets it will honor on failover, so wallets can discover where to take a dead mint's tokens.

## Spent-proof firehose

For a delegate to safely redeem the original mint's tokens without permitting double-spends, it needs an up-to-date copy of the original mint's spent-proof state **before** the original mint disappears. The original mint exposes this as a **firehose**: a continuous, append-only, sequenced feed of spent-proof identifiers. Delegate mints subscribe to it continuously and persist a local mirror.

The firehose carries no business logic and no spending semantics, it is an ordered event dump. A consumer that has every event up to sequence `n` has a complete view of the spent set as of that point.

### Spent event

The identifier of a spent proof reuses `Y = hash_to_curve(secret)` from [NUT-00][00] / [NUT-07][07], no new identifier is introduced. A `SpentEvent` is:

```json
{
  "seq": <int>,
  "Y": <hex_str>,
  "id": <hex_str>,
  "amount": <int>,
  "witness": <str|null>
}
```

- `seq` is a strictly increasing, gap-free integer sequence number assigned by the original mint. It MUST start at `0` and increment by exactly `1` per event. It MUST NOT be reordered or reused.
- `Y` is the spent proof's identifier, the hex-encoded compressed point `Y = hash_to_curve(secret)`.
- `id` is the keyset ID ([NUT-02][02]) the proof was signed under.
- `amount` is the proof's amount.
- `witness` is the serialized witness data if the proof carried a [NUT-10][10] spending condition (as in [NUT-07][07]), otherwise `null`.

> [!IMPORTANT]
> The original mint MUST publish exactly one `SpentEvent` for every proof it transitions to `SPENT` ([NUT-07][07]), and MUST do so durably (an event, once published, is never removed). The feed reflects only `SPENT` proofs; `PENDING` proofs are not published.

### Real-time stream (Server-Sent Events)

For real-time mirroring, the firehose is exposed as a [Server-Sent Events][sse] stream at the mint's `/v1/firehose/sse` path. SSE is a good fit because the feed is strictly uni-directional (mint to delegate), runs over plain HTTP, and has native reconnection with resume.

```http
GET https://mint.host:3338/v1/firehose/sse
```

The mint responds with `Content-Type: text/event-stream` and emits one SSE event per spent proof. The event's `id` field carries the `seq`, so it doubles as the resume cursor; the `data` field is the JSON-encoded `SpentEvent`:

```
id: 42
event: spent
data: {"seq": 42, "Y": "02...", "id": "00ad...", "amount": 2, "witness": null}
```

**Reconnection.** A standard `EventSource` client reconnects automatically and sends the last received `id` back in the `Last-Event-ID` HTTP header. On reconnection with a `Last-Event-ID` of `n`, the mint MUST resume the stream from `seq == n + 1`, so no events are missed across a dropped connection without any application-layer handshake.

If the mint cannot resume from the requested `Last-Event-ID` (for example, it only retains recent events and the requested `seq` has been pruned), it MUST first emit a `reset` event giving the range it can serve, signalling that the client should bootstrap the missing prefix via the catch-up endpoint before trusting the live stream:

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
  "events": <Array[SpentEvent]>,
  "latest": <int>
}
```

- `events` contains every requested `SpentEvent` that exists, ascending by `seq`, with duplicates from overlapping ranges/indexes removed.
- `latest` is the highest `seq` the mint has published, so the consumer knows whether more events remain beyond an open-ended range.

The mint MAY cap the number of events returned per request; a client that receives a truncated response narrows its `ranges` and requests the remainder. A client MUST ensure it has contiguous `seq` coverage from `0` to `latest` before treating its mirror as complete.

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

`seq` is the sequence number the checkpoint was taken at. A delegate compares each `root` against the same computation over its own mirror; a mismatch identifies which bucket diverged, and the delegate re-syncs it by fetching the affected `seq`s through the catch-up endpoint's `ranges`/`indexes`. The bucketing scheme (prefix length, hashing) is left to implementations and is out of scope for double-spend safety, it is a consistency aid, not a requirement for failover.

## Failover redemption

Once the relative timelock on the reserve matures and the delegate Dave has claimed the reserve UTXO on-chain (see the [Appendix](#appendix-reserve-construction-informational)), Dave enters **failover mode** for Bob.

In failover mode, Dave exposes Bob's keysets as **inactive** keysets (`active: false`, [NUT-02][02]): they are accepted as inputs to swap ([NUT-03][03]) and melt ([NUT-05][05]) but are never used to sign new outputs. A user simply points their wallet at Dave and submits Bob's proofs as inputs in the normal `/v1/swap` (to receive fresh Dave ecash) or `/v1/melt` (to withdraw to Bitcoin/Lightning) flows.

For each input proof signed under a Bob keyset, Dave accepts it **only if all** of the following hold:

1. The proof's `id` belongs to a Bob keyset that Dave mirrors and has the public keys for.
2. The proof's signature **publicly verifies** via its DLEQ proof ([NUT-12][12]) against that keyset's amount public key. The wallet MUST include the DLEQ proof with the blinding factor `r` on the proof (the "user to user" `Proof` form of [NUT-12][12]) so Dave can verify without Bob's private key.
3. The proof's `Y` is **not** present in Dave's mirrored spent set for Bob.
4. The claimable reserve recovered for Bob is **not** exhausted.

On success, Dave marks `Y` as spent in its mirror for Bob (so it cannot be redeemed twice within failover) and processes the payout.

> [!NOTE]
> **Privacy cost today.** Step 2 requires the wallet to reveal the blinding factor `r` to Dave, which lets Dave link the original `BlindSignature` to the `Proof` (see the privacy note in [NUT-12][12]). This is acceptable in a disaster-recovery context but is a real cost during normal-looking redemptions. A BLS-based ecash scheme with public verification would remove this trade-off; this NUT should adopt that path once Cashu supports it.

### Consistency model

The delegate's mirror does **not** need perfect consistency. If Dave is slightly behind the feed at the moment Bob fails, it may accept a small number of proofs that Bob had already marked spent, creating more valid claims than recovered reserve funds.

This is acceptable for disaster recovery. A correctly-synced delegate should never hit it. If it does, Dave simply stops processing redemptions once the recovered reserve is exhausted (error `33003`). It is better that 99% of users redeem than that all users lose their funds.

## Circular delegation

A set of mints can each act as delegate for the others, e.g. for three mints:

```
Bob (custodian) -> Dave (delegate) -> Frank (delegate)
Dave (custodian) -> Frank (delegate) -> Bob (delegate)
Frank (custodian) -> Bob (delegate) -> Dave (delegate)
```

If one mint dies, another takes over its reserve. If two die, the survivor can eventually take over both. This yields a 1-of-n liveness property for the whole set.

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
- `firehose` gives the Server-Sent Events stream (`sse`) and the HTTP catch-up/batch (`http`) URLs for this mint's spent-proof feed.
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

This section is **non-normative**. It describes a recommended on-chain construction that enforces the failover ordering; the Bitcoin-layer mechanics are outside the wallet↔mint HTTP API. See [NUT-30][30] for related onchain vocabulary.

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

While Bob is live, it periodically **consolidates** reserve funds by spending the UTXO back to the same script via the key path. This rolls deposits into a single reserve UTXO and **re-arms** the relative timelocks, so delegates can never reach the reserve during normal operation. If Bob stops rolling the reserve, the first delegate becomes eligible after its timelock; if that delegate fails to act before the next timelock matures, the next delegate becomes eligible, and so on.

This pairs well with TEE-based mints. A TEE reduces custody trust but increases liveness risk (losing access to sealed key material can strand reserves). Naming a non-TEE mint as a delegate restores liveness and can remove the TEE from the disaster-recovery path entirely.

## Error codes

See [error_codes.md][errors]. Codes relevant to this NUT:

| Code  | Description                             |
| ----- | --------------------------------------- |
| 33001 | Proof from unknown or unmirrored keyset |
| 33002 | Delegation window not yet open          |
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
