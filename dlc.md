NUT-DLC: Discreet Log Contracts
==========================

`optional`, `depends on: NUT-SCT`

---

This NUT describes a standard for mints and wallets to support settlement of [Discreet Log Contracts](https://bitcoinops.org/en/topics/discreet-log-contracts/) using ecash.

# DLCs

A Discreet Log Contract (DLC) is a conditional payment which a set of _participants_ can atomically commit money to. They depend on the existence of a semi-trusted Oracle. For the sake of brevity, this document elides any full description of DLCs. Instead we abstract a DLC as a set of input parameters agreed upon in-advance, known to all DLC participants.

These parameters are:

- The number of possible DLC outcomes `n`
- A vector of `n` _outcome blinding secrets_ (scalars) `[b1, b2, ... bn]` [^1]
- A vector of `n` _outcome locking points_ `[K1, K2, ... Kn]` [^2]
- A vector of `n` _payout structures_ `[P1, P2, ... Pn]`
- An optional timeout timestamp `t` and accompanying timeout payout structure `Pt`

[^1]: Wallet clients may opt out of outcome-blinding by setting all of the blinding secrets to zero.

[^2]: The outcome locking point vector abstraction covers both [enum events](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md#simple-enumeration) and [digit-decomposition events](https://github.com/discreetlogcontracts/dlcspecs/blob/master/Oracle.md#digit-decomposition). For an enum event, participants simply compute each of locking points from the announced outcome messages and nonce, in a 1:1 mapping. For a digit-decomposition event, participants compute locking points for each relevant outcome _range_ on a per-digit basis, aggregating (summing) the locking points where necessary to produce `[K1, K2, ... Kn]`.

## Locking Points

The locking points `[K1, K2, ... Kn]` are elliptic curve points, encoded in SEC1 compressed binary format.

The locking points are blinded by the participants, to obscure the nature of the DLC from the mint at settlement time. Blinded locking points are computed as:

```python
Ki_ = Ki + bi * G
```

...for some blinding secret `bi` known to all DLC participants. Each locking point SHOULD be allocated a _unique_ blinding secret.

## Payout Structures

Payout structures are serialized dictionaries which map `pubkey -> weight`.

```json
{
  <public_key_str>: <weight_int>,
  ...
}
```

This mapping defines how the money used to fund a DLC should be distributed if a particular outcome is settled. The pubkeys describe ownership rights and the weights describe how the funding amount must be allocated.

### Example

```json
{
  "03a40f20667ed53513075dc51e715ff2046cad64eb68960632269ba7f0210e38": 3,
  "028a36f0e6638ea7466665fe174d958212723019ec08f9ce6898d897f88e68aa5d": 2,
  "02b4ebb0dda3b9ad83b39e2e31024b777cc0ac205a96b9a6cfab3edea2912ed1b3": 1
}
```

With this payout structure, the `03a40f...` pubkey is allocated 3 of the 6 available weight units (3+2+1), and so its owner should receive half of the DLC funding amount. Similarly, `028a36...` receives a third of the funding amount, and `02b4eb...` receives the remaining sixth.

Weights must be positive integers. Negative weights or weights equal to zero are invalid, and render the whole payout structure invalid.

## Timeouts

The timeout timestamp `t` is an unsigned integer describing a unix-epoch offset in seconds.

The payout structure for the timeout condition `Pt` is the same format as other payout structures defined above.

The timeout condition may be omitted to enable DLCs which are indefinitely-locked.

## Locking Ecash to a DLC

[NUT-10] Secret `kind: DLC`

We define a new [NUT-10] well-known `Secret` kind `DLC`.

```json
[
  "DLC",
  {
    "nonce": "da62796403af76c80cd6ce9153ed3746",
    "data": "2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed",
    "tags": [
      [
        "threshold",
        "10000"
      ]
    ]
  }
]
```

The `Secret.data` field is the root hash of a merkle tree which uniquely identifies a particular DLC (see next section for construction).

Anyone can spend a `Proof` locked with the `DLC` secret kind, but can _only_ spend it in the process of _funding a DLC identified by the same root hash._ **A mint which supports this spec MUST NOT allow a `DLC` secret to be spent unless it is used for funding the indicated DLC.**

The `threshold` tag is a required parameter which stipulates a minimum funding value which must be used to fund the DLC. [^3]

[^3]: The `threshold` tag commits a `DLC` secret to funding only a DLC of at least a specific amount. This is a way of enforcing buy-in from all participants.

## DLC Merkle Tree

The particulars of a DLC are represented by a Merkle tree. The leaf hashes of the tree are constructed by hashing each of the blinded locking points `[K1_, K2_, ... Kn_]` with their corresponding payout structures `[P1, P2, ... Pn]`.

```python
Ti = SHA256(Ki_ || Pi)
```

The timeout condition (if applicable) is also added as a leaf.

```python
Tt = SHA256(hash_to_curve(t.to_bytes(4, 'big')) || Pt)
```

The `hash_to_curve` function is defined in [NUT-00]. [^4] `t` is encoded as a 32-bit big-endian integer before hashing.

[^4]: When constructing `Tt`, we hash `t` to a curve point as a convenience, so that all leaf nodes can be represented as `(Point, Map)` data structures.

Note that curve points are encoded in SEC1 compressed binary format, while each payout condition `Pi` is encoded as UTF8 JSON before being hashed. Because JSON maps are not ordered, all participants must agree ahead of time on a specific set of serialized payout structures.

From the set of `leaf_hashes` `[T1, T2, ... Tn, Tt]`, participants compute the DLC root hash:

```python
dlc_root = merkle_root([T1, T2, ... Tn, Tt])
```

...where the `merkle_root()` function is defined in [NUT-SCT].

`dlc_root` may then be used as the `Secret.data` field for secrets of kind `DLC`.

A wallet can prove `Ti` is a leaf of `dlc_root` by providing a list of merkle branch hashes. See [the appendix of NUT-SCT](sct.md#Appendix) for an example of how to build such a proof.

## DLC Funding

This section describes the DLC funding process.

DLC participants who wish to jointly fund a DLC may mint (or swap for) ecash proofs which use the `DLC` well-known secret kind to commit the funds to a specific `dlc_root`. Wallets MUST ensure that the construction of `dlc_root` is fully validated - Even a single hidden leaf node could be used by a malicious participant to immediately sweep the whole DLC funding amount.

Participants elect an untrusted _funder,_ whose is responsible for collecting `DLC`-locked ecash proofs from the participants, and then submitting them all en-masse to the mint. The funder need not be a DLC participant. Indeed, the mint itself may act as a funder, although this compromises privacy of the participants.

### DLC Funding Token

To ensure money is not lost if the funder disappears without submitting the proofs to the mint, participants should create each locked proof using a [Spending Condition Tree (SCT)](sct.md#SCT) which commits to at least two spending condition leaves:

1. The `DLC` secret.
2. A backup secret which only the participant knows and can claim.

The backup secret allows a participant to swap her exposed proof for a fresh one if the funder takes too long to register the DLC.

A DLC Funding Token is structured and encoded in the same format as [NUT-00] tokens, but also specifies the `dlc_root` hash the token is intended to fund.

Example:

```json
{
  "token": [
    {
      "mint": "https://8333.space:3338",
      "proofs": [
        {
          "amount": 4096,
          "id": "009a1f293253e41e",
          "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"d7578cbc3d5d61a61cb46552f66d7d5fe92ea4606c778e14d662bbe3d887c0d1\"}]",
          "C": "02bc9097997d81afb2cc7346b5e4345a9346bd2a506eb7958598a72f0cf85163ea",
          "witness": {
            "leaf_secret": "[\"DLC\",{\"nonce\":\"da62796403af76c80cd6ce9153ed3746\",\"data\":\"2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed\",\"tags\":[[\"threshold\",\"10000\"]]}]",
            "merkle_proof": ["009ea9fae527f7914096da1f1ce2480d2e4cfea62480afb88da9219f1c09767f"]
          }
        },
        ...
      ]
    }
  ],
  "unit": "sat",
  "memo": "Bet",
  "dlc_root": "2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed"
}
```

The funder cannot use this ecash proof for anything _except_ for funding a DLC with root hash `2db63c...`, and doing so requires a minimum funding amount of 10,000 satoshis. The funder would need to find another 5,904 available satoshis in proofs to fund the DLC with this proof as an input.


### Mint Registration

To register and fund a DLC on the mint, the funder issues a `POST /v1/dlc/fund` request to the mint, sending a request body of the following format.

```json
{
  "atomic": <bool|null>,
  "registrations": [
    {
      "dlc_root": "2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed",
      "inputs": [
        {
          "amount": 2,
          "id": "009a1f293253e41e",
          "secret": "[\"DLC\",{\"nonce\":\"da62796403af76c80cd6ce9153ed3746\",\"data\":\"2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed\",\"tags\":[[\"threshold\",\"10000\"]]}]",
          "C": "02bc9097997d81afb2cc7346b5e4345a9346bd2a506eb7958598a72f0cf85163ea"
        },
        ...
      ]
    },
    ...
  ]
}
```

For each new DLC submitted in `registrations`, the mint MUST process and then consume all of the `inputs` in the same way it would for a swap/melt operation, with one additional rule: **Proofs referencing a secret of kind `DLC` are now spendable, but only if `Proof.secret.data == dlc_root`.**

If the optional `atomic` field in the request body is set to `true`, the mint must process _all_ DLCs in the `registrations` array, or else process none of them.

If one or more inputs does NOT pass validation, the mint must return a response with a `400` status code, and a body of the following format:

```json
{
  "processed": [<hash>, ...],
  "errors": [
    {
      "dlc_root": <hash>,
      "bad_inputs": [
        {
          "index": <int>,
          "detail": <str>
        },
        ...
      ]
    },
    ...
  ]
}
```

The `processed` array tells the funder which DLCs have been successfully registered, while the `errors` field tells the funder which DLCs failed to register, and which specific input proofs for that DLC were faulty. This allows participants to resolve funding disputes. [^5]

[^5]: To resolve a funding dispute where some _accused_ participants supply faulty DLC funding proofs, but refuse to acknowledge their mistake, the funder may broadcast the full set of (locked) DLC funding proofs to all _bystander_ participants. The accused participants also broadcast the proofs they supplied to the funder. The bystanders retry the `POST /v1/dlc/fund` request with both possible sets of input proofs to confirm the mint indeed reports the same failure on both. If the mint accepts any of the funding requests, then the dispute is resolved and the DLC has been funded. If the mint reports errors for both sets of input proofs, the bystanders can use the `bad_inputs` field determine who was behaving dishonestly and evict them from the group.

If all the input proofs of a DLC registration object pass validation, the mint stores the `dlc_root` and the total `funding_amount` (i.e. the sum value of all `inputs`). **It is vital for the mint to remember this state,** as the `(dlc_root, funding_amount)` tuple is now the only valid record that exists anywhere of the participants' joint deposit.

If every DLC in the `registrations` array is processed successfully, the mint must return a `200 OK` response with the following response body format:

```json
{
  "processed": [
    {
      "dlc_root": <hash>
    },
    ...
  ]
}
```

Each object in the `processed` array lists the root hash of a successfully registered DLC.

### Settling the DLC

When the DLC Oracle publishes her attestation, this reveals to the participants a scalar `ki`, the discrete log of `Ki` such that `ki * G = Ki`.

Any DLC participant who knows the matching blinding secret `bi` can compute `ki_` - the discrete log of the blinded locking point `Ki_`.

```
ki_ = ki + bi
```
```
ki_ * G = (ki + bi) * G
        = ki * G + bi * G
        = Ki + bi * G
        = Ki_
```

To mark the DLC as settled on the mint, the wallet issues a `POST /v1/dlc/settle` request with the following body format.

```json
{
  "settlements": [
    {
      "dlc_root": "2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed",
      "outcome": {
        "k": "8e935aec5668312be8f960a5ecc3c5dd290e39985970bfd093047df7f05cc9ec",
        "P": "{\"03361cd8bd1329fea797a6add1cf1990ffcf2270ceb9fc81eeee0e8e9c1bd0cdf5\":\"10000\"}"
      },
      "merkle_proof": [
        "5467757c899a46b847825e632cafc5e960a948045d12fc1143d17966c87ae351",
        "a6df41f37b1b21ebc2b3d68fb8598450a07fb279e82e0e57bd04b926234f2f5f",
        "1f8de293adb9301b16cb5bfb446960000602b74a3b7ed89aa8677323a6b39b8a"
      ]
    },
    ...
  ]
}
```

- `Settlement.dlc_root` is the root hash of a funded and active DLC.
- `Settlement.outcome.k` is the blinded attestation secret `ki_`
- `Settlement.outcome.P` is the serialized payout structure `Pi`
- `Settlement.merkle_proof` is a list of hashes, which must prove that `SHA256(ki_ * G || Pi)` is a leaf hash of the `dlc_root` merkle hash.

The mint verifies each settlement object as follows:

1. If `Settlement.outcome.P` fails to parse as a JSON dictionary mapping pubkeys to positive integers, return an error.
1. If `Settlement.dlc_root` does not correspond to any known funded DLC, return an error.
1. If `Settlement.dlc_root` corresponds to a DLC, but that DLC has already been settled, return an error.
1. Verify `Settlement.merkle_proof`:

```python
leaf_hash = SHA256(Settlement.outcome.k * G || Settlement.outcome.P)
assert merkle_verify(dlc_root, Settlement.merkle_proof, leaf_hash)
```

The mint uses the `merkle_verify()` function from [NUT-SCT] to verify the `merkle_proof`.

#### Timeout Settlement

If the mint's clock reaches the DLC timeout time `t`, any participant can settle the timeout branch of the DLC. To mark the DLC as settled on the mint using the timeout clause, the wallet issues a `POST /v1/dlc/settle` request with the following body format.

```json
{
  "atomic": <bool|null>,
  "settlements": [
    {
      "dlc_root": "2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed",
      "outcome": {
        "timeout": 1716777419,
        "P": "{\"03361cd8bd1329fea797a6add1cf1990ffcf2270ceb9fc81eeee0e8e9c1bd0cdf5\":\"10000\"}"
      },
      "merkle_proof": [
        "5467757c899a46b847825e632cafc5e960a948045d12fc1143d17966c87ae351",
        "a0fc3d18e6baea50ce8fe8a12ad083fc37e07a68f083a1aafc377c60be999e5f"
      ]
    },
    ...
  ]
}
```

`Settlement.outcome.timeout` is the timeout timestamp `t`. The steps for the mint to verify the settlement is the same as an outcome settlement (above), with one modification: `Settlement.merkle_proof` is verified differently.

```python
T = hash_to_curve(Settlement.outcome.timeout.to_bytes(4, 'big'))
leaf_hash = SHA256(T || Settlement.outcome.P)
assert merkle_verify(dlc_root, Settlement.merkle_proof, leaf_hash)
```

If the above checks pass for a `Settlement` object, the mint marks the DLC as "settled". The mint can now use the original `funding_amount` to compute exactly how much each pubkey in `Settlement.outcome.P` is owed. This resulting map of pubkeys to amounts is denoted `debts`.

```python
weights = json.loads(Settlement.outcome.P)
weight_sum = sum(weights.values())
debts = dict(((pubkey, funding_amount * weight // weight_sum) for pubkey, weight in weights.items()))
```

The mint can now replace the `funding_amount` in its storage with the `debts` map.

If all `settlements` validated correctly, the mint returns a `200 OK` response with the following body format:

```json
{
  "settled": [
    {
      "dlc_root": <hash>,
    },
    ...
  ]
}
```

The `settled` array indicates the set of DLCs which were successfully marked as settled.

If some `settlements` failed, the mint must return a `400` response with the following body format:

```json
{
  "settled": [
    {
      "dlc_root": <hash>,
    },
    ...
  ],
  "errors": [
    {
      "dlc_root": <hash>,
      "detail": <str>
    },
    ...
  ]
}
```

If the wallet passes the optional `atomic` request parameter as `true`, then the mint must process ALL the requested `settlements` successfully, or else process none of them.

### Claiming Payouts

To claim a DLC payout, a participant issues a `POST /v1/dlc/payout` request to the mint with the following body format.

```json
{
  "atomic": <bool|null>,
  "payouts": [
    {
      "dlc_root": "2db63c93043ab646836b38292ed4fcf209ba68307427a4b2a8621e8b1daeb8ed",
      "pubkey": "03361cd8bd1329fea797a6add1cf1990ffcf2270ceb9fc81eeee0e8e9c1bd0cdf5",
      "signature": "60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383",
      "outputs": <Array[BlindedMessage]>,
    },
    ...
  ]
}
```

- `Payout.dlc_root` is a DLC merkle root hash.
- `Payout.signature` is a [BIP-340] signature made on the `dlc_root` hash, which should verify against `Payout.pubkey`.
- `Payout.outputs` is a set of blinded messages for the mint to sign.

For each `Payout` object, the mint performs the following checks:

1. Validate that `Payout.signature` is a valid [BIP-340] signature made by `Payout.pubkey` on `payout.dlc_root`
1. If `Payout.dlc_root` does not correspond to any known funded DLC, return an error.
1. If `Payout.dlc_root` corresponds to a known DLC, but that DLC has not been settled, return an error.
1. If `Payout.pubkey` is not a key in the `debts` map, return an error.
1. If `sum([out.amount for out in Payout.outputs]) != debts[Payout.pubkey]`, the mint must return an error to the client.

If all `Payout` objects are validated successfully, the mint returns a `200` response with the blinded signatures on `Payout.outputs`:

```json
{
  "paid": [
    {
      "dlc_root": <hash>,
      "signatures": <Array[BlindSignature]>
    },
    ...
  ]
}
```

For each `Payout` object whose outputs the mint signs, the mint must simultaneously delete `Payout.pubkey` from the `debts` map to prevent the wallet from claiming twice. [^6]

[^6]: Network errors may cause the wallet not to safely receive the blinded signatures sent by the mint. To counteract this occurrence, mints are encouraged to set up idempotent request handlers which cache responses, so the wallet can replay its `POST /v1/dlc/payout` request if needed.

If some `Payout` objects fail the validation checks, the mint returns a `400` response with the following format:

```json
{
  "paid": [
    {
      "dlc_root": <hash>,
      "signatures": <Array[BlindSignature]>
    },
    ...
  ],
  "errors": [
    {
      "dlc_root": <hash>,
      "detail": <str>
    },
    ...
  ]
}
```

Wallets MUST collect and save the blinded signatures from each entry in the `paid` array, even though the mint responded with a `400` error.

If a wallet needs payout processing to be atomic, they

If the wallet passes the `atomic` parameter as `true` in their request body, then the mint must ensure that either _all_ payouts are processed, or else _none_ are.

### Checking the DLC Status

The participants need a way to verify:

- if and when the funder has successfully funded the DLC
- if the DLC has been settled
- if the DLC has been paid out, and if so to whom

To this end, a wallet issues a `GET /v1/dlc/status/{dlc_root}` request to the mint.

If the DLC is not found, the mint responds with a `400` error.

If the DLC is found and is active (not settled), the mint responds with:

```json
{
  "settled": false,
  "funding_amount": <int>
}
```

If the DLC is found and is settled, the mint responds with:

```json
{
  "settled": true,
  "debts": {
    "03361cd8bd1329fea797a6add1cf1990ffcf2270ceb9fc81eeee0e8e9c1bd0cdf5": <int>
  }
}
```

To prevent needless polling when waiting for a DLC to be funded, wallets MAY issue a `GET /v1/dlc/status/{dlc_root}?wait=true&timeout=30` request, adding the `?wait=true&timeout=30` query parameters. The mint SHOULD treat this request as a long-poll: If the `dlc_root` exists, return a response immediately. Otherwise, wait for `timeout` number of seconds to see if anyone registers the DLC, before eventually returning a `400` status if the DLC still has not been funded by then.

## Tidying Up

Once all payouts have been issued, the mint may purge the DLC from its storage, or it may retain the DLC and return `"debts": {}` in the `/v1/dlc/status/{dlc_root}` response body to indicate the DLC has been fully settled and paid.

## TODO

- prevent a mint from being DOS'd by using payout structure size limits, DLC lifetime limits
- allow mint to charge fees for DLC processing
- give the funder a non-interactive proof of DLC registration so that participants don't have to poll

## Previous Work

This NUT is inspired by [this original proposal](https://conduition.io/cryptography/ecash-dlc/) for DLC settlement with generic Chaumian Ecash.

[NUT-00]: 00.md
[NUT-10]: 10.md
[NUT-12]: 12.md
[NUT-SCT]: sct.md
[BIP-340]: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
