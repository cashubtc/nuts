# NUT-XX-B: Bonded Proof of Liabilities

`optional` `experimental`

---

## Abstract

This document extends [NUT-XX: Proof of Liabilities][pol] with Bitcoin-native collateral and permissionless slashing.

A participating mint locks bitcoin in a recursive covenant called the **PoL bond**. The covenant carries the latest Proof of Liabilities epoch commitment and permits the bonded funds to move only through protocol-defined state transitions. A mint can advance the bond by publishing a new PoL epoch, complete a controlled wind-down after its liabilities reach zero, or lose the entire bond to the first challenger who proves a supported PoL violation.

Version 1 intentionally awards the complete bonded amount, less transaction fees, to the first successful challenger. Holder recovery, proportional distribution, and bounded challenger rewards are outside this document.

---

## 1. Scope

This document specifies:

1. The covenant capabilities required by Bonded PoL.
2. The state committed by a PoL bond output.
3. Epoch publication, finalization, challenge, slashing, and withdrawal transitions.
4. On-chain prevention of MMR consistency violations and resolution of the other three fraud challenges defined by [NUT-XX][pol].
5. Canonical commitments and relative delays required for consensus-enforced adjudication.

This document does not specify:

1. A final Bitcoin soft-fork activation or consensus opcode assignment.
2. Distribution of slashed collateral beyond the first-successful-challenger rule.
3. A BTC exchange-rate oracle for non-`sat` units.
4. Proof that the bond fully collateralizes the mint's liabilities.
5. Data publication beyond the response obligations created by a valid challenge.

The base PoL protocol remains usable without a bond. Support for this extension MUST NOT be interpreted as proof of solvency; it proves only that the advertised bond is subject to the rules in this document.

The concrete reference covenant, Taproot leaves, witness layouts, and opcode assumptions are specified in [Bonded PoL Reference Scripts][scripts].

---

## 2. Covenant Execution Model

Bonded PoL assumes a future Bitcoin covenant environment with semantics equivalent to all of the following capabilities:

1. **Recursive state:** A script can require a successor output to execute the same program while committing to dynamically computed state.
2. **Input state access:** A script can read or verify the state committed by the current bond input.
3. **Output introspection:** A script can constrain successor output scripts, committed state, values, and positions.
4. **Value preservation:** A script can require the bond value, less an explicitly bounded fee, to be preserved or paid to a specified output.
5. **Arbitrary-message signatures:** A script can verify the BIP-340 signatures used by manifests and PoL receipts rather than only transaction signatures.
6. **Hash composition:** A script can construct and SHA-256 hash the byte strings required by NUT-XX.
7. **Bounded arithmetic:** A script can safely add, subtract, compare, and serialize unsigned 64-bit sums.
8. **Timelocks:** A script can enforce relative block delays with `OP_CHECKSEQUENCEVERIFY`.
9. **Bounded proof execution:** A script can verify inclusion and consistency proofs whose maximum lengths are fixed by this document.

An implementation MAY realize these semantics using state-carrying covenants, transaction introspection, `OP_CAT`, arbitrary-message signature verification, BitVM-style optimistic computation, or another consensus-enforced construction.

Template-only covenants are conforming only if their precommitted transaction graph implements every state transition and bound defined here. No trusted adjudicator or discretionary signer may decide whether a challenge succeeds.

---

## 3. Terminology

- **Bond:** Bitcoin value controlled by the Bonded PoL covenant.
- **Bond outpoint:** The transaction outpoint containing the current bond state.
- **Bond program:** The immutable covenant program governing the bond.
- **Bond state:** Canonical data committed in the bond output.
- **Active epoch:** The most recently finalized PoL epoch.
- **Pending epoch:** A published epoch still inside its challenge period.
- **Challenger:** The party that initiates a challenge and commits the slash destination.
- **Challenge bond:** Optional anti-spam collateral supplied by a challenger.
- **Slash destination:** The Bitcoin `scriptPubKey` that receives the bond after a successful challenge.
- **Response period:** The relative block delay during which a challenged mint may publish a valid response.
- **Finalization:** Transition of an unchallenged pending epoch into the active state.

`bond_id` is an immutable identifier derived before the initial deposit:

```text
bond_id = SHA256(
    "Cashu_Bonded_PoL_Bond_Id_v1"
    || mint_pubkey
    || genesis_nonce
)
```

`genesis_nonce` is 32 uniformly random bytes committed by the initial bond state. Deriving the identifier from the initial bond's own outpoint is forbidden because doing so would create a transaction-ID hash cycle. `bond_id` remains constant across all recursive successor outputs.

---

## 4. Constants and Bounds

Each deployment MUST commit to the following parameters in `program_hash`:

| Name                  | Type   | Meaning                                                        |
| :-------------------- | :----- | :------------------------------------------------------------- |
| `NETWORK`             | string | Bitcoin network identifier                                     |
| `CHALLENGE_PERIOD`    | uint32 | Blocks between epoch publication and finalization              |
| `RESPONSE_PERIOD`     | uint32 | Blocks allowed for a mint response                             |
| `WIND_DOWN_PERIOD`    | uint32 | Blocks between zero liabilities and withdrawal                 |
| `MAX_KEYSETS`         | uint16 | Maximum keysets committed by one epoch                         |
| `MAX_MMR_HEIGHT`      | uint8  | Maximum accepted inclusion or consistency proof height         |
| `MAX_CHALLENGE_BYTES` | uint32 | Maximum canonical challenge size                               |
| `MAX_RESPONSE_BYTES`  | uint32 | Maximum canonical response size                                |
| `MIN_CHALLENGE_BOND`  | uint64 | Minimum anti-spam input, or zero if challenge bonds are unused |
| `CONTRACT_VERSION`    | uint16 | Bonded PoL program version                                     |

`MAX_MMR_HEIGHT` MUST NOT exceed 63. Therefore a single committed sum-MMR cannot contain more than `2^63 - 1` leaves.

All delays are relative block counts enforced with input `nSequence` and `OP_CHECKSEQUENCEVERIFY`. Timestamps, median-time-past, wall-clock time, and PoL epoch timestamps MUST NOT determine challenge or response expiry.

The protocol assumes that no valid operation causes a sum or intermediate arithmetic result to reach or exceed `2^64`. Values violating this assumption are outside the valid protocol domain.

---

## 5. Canonical Encoding

Consensus-enforced commitments MUST NOT hash JSON. Values MUST use the following binary encoding:

- Unsigned integers: fixed-width big-endian.
- Hashes: 32 raw bytes.
- Compressed curve points: 33 raw bytes.
- `scriptPubKey`: CompactSize length followed by raw script bytes.
- Variable byte strings: CompactSize length followed by the bytes.
- Lists: CompactSize element count followed by canonical elements.
- Enumerations: one byte.
- Optional values: one-byte presence flag followed by the value when present.

Strings MUST be UTF-8 and MUST be preceded by their CompactSize byte length. Text fields used only for display MUST NOT affect covenant decisions.

All domain separators in this document are literal UTF-8 bytes without a terminating zero byte.

### 5.1 Program Commitment

```text
program_hash = SHA256(
    "Cashu_Bonded_PoL_Program_v1"
    || contract_version_u16
    || network
    || challenge_period_u32
    || response_period_u32
    || wind_down_period_u32
    || max_keysets_u16
    || max_mmr_height_u8
    || max_challenge_bytes_u32
    || max_response_bytes_u32
    || min_challenge_bond_u64
    || verifier_program_hash
)
```

`verifier_program_hash` commits to the exact consensus-executed implementation of all predicates in this document.

---

## 6. Bond States

The state tag is one of:

| Value | State        |
| :---- | :----------- |
| `0`   | `ACTIVE`     |
| `1`   | `PENDING`    |
| `2`   | `CHALLENGED` |
| `3`   | `WIND_DOWN`  |

There is no recursive `SLASHED` state. Slashing consumes the bond and pays it to the committed slash destination.

### 6.1 Common State

Every bond state commits to:

```text
BondCommon {
    contract_version: uint16,
    program_hash: bytes32,
    bond_id: bytes32,
    genesis_nonce: bytes32,
    mint_pubkey: bytes32,
    state_tag: uint8,
    state_sequence: uint64,
    active_epoch: EpochCommitment,
    epoch_history_mmr_root: bytes32,
    epoch_history_mmr_size: uint64
}
```

`mint_pubkey` is the x-only NUT-06 master public key used to verify PoL manifests.

`state_sequence` MUST increase by exactly one in every recursive transition. It prevents two semantically different successor states from claiming the same covenant sequence.

`epoch_history_mmr_root` commits to every previously finalized `EpochCommitment` hash in ascending epoch order. Publication appends the prior active epoch before proposing its successor. Challenges that reference an older epoch MUST prove it against this history root. The history MMR uses ordinary SHA-256 nodes without sums and the same post-order peak construction used by NUT-XX.

### 6.2 Epoch Commitment

```text
EpochCommitment {
    epoch_index: uint64,
    global_digest: bytes32,
    previous_global_digest: bytes32,
    epoch_keysets_root: bytes32,
    epoch_keysets_count: uint16,
    total_outstanding_balance: uint64
}
```

`epoch_keysets_root` is the root of a binary Merkle tree whose leaves are sorted lexicographically by lowercase hexadecimal `keyset_id` and encoded as:

```text
KeysetCommitment {
    keyset_id: bytes,
    issued_mmr_size: uint64,
    issued_mmr_root_hash: bytes32,
    issued_mmr_root_sum: uint64,
    spent_mmr_size: uint64,
    spent_mmr_root_hash: bytes32,
    spent_mmr_root_sum: uint64,
    outstanding_balance: uint64
}
```

The keyset leaf hash is the base NUT-XX keyset leaf:

```text
SHA256(
    "Cashu_PoL_Keyset_Leaf_v1"
    || bytes_2(len(utf8(keyset_id)))
    || utf8(keyset_id)
    || bytes_8(issued_mmr_size)
    || issued_mmr_root_hash
    || bytes_8(issued_mmr_root_sum)
    || bytes_8(spent_mmr_size)
    || spent_mmr_root_hash
    || bytes_8(spent_mmr_root_sum)
)
```

Merkle parents are:

```text
SHA256("Cashu_PoL_Keyset_Node_v1" || left || right)
```

When a level has an odd node count, its final node is duplicated. An empty list is forbidden. `epoch_keysets_count` MUST be between 1 and `MAX_KEYSETS`, inclusive.

The covenant MUST verify that:

```text
total_outstanding_balance
    == sum(keyset.outstanding_balance for every committed keyset)
```

and for each keyset:

```text
keyset.outstanding_balance
    == keyset.issued_mmr_root_sum - keyset.spent_mmr_root_sum
```

### 6.3 Pending State

```text
PendingState {
    common: BondCommon,
    proposed_epoch: EpochCommitment
}
```

### 6.4 Challenged State

```text
ChallengedState {
    common: BondCommon,
    disputed_epoch: EpochCommitment,
    challenge_type: uint8,
    challenge_hash: bytes32,
    challenger_script_pubkey: bytes
}
```

The `challenger_script_pubkey` MUST be a standard script under the consensus and relay policy active when the challenge transaction is confirmed. It MUST NOT be changeable by a response or slashing transaction.

### 6.5 Wind-Down State

```text
WindDownState {
    common: BondCommon,
    mint_withdrawal_script_pubkey: bytes
}
```

---

## 7. Bond Output Invariants

Every recursive transition MUST enforce:

1. Exactly one input is the current PoL bond.
2. Exactly one output is the successor PoL bond.
3. The successor executes the same `program_hash` and commits to the required next state.
4. The successor value equals `input_bond_value`.
5. No output other than the successor may receive value from the bond input, except an explicitly constrained fee mechanism.
6. `bond_id`, `genesis_nonce`, `mint_pubkey`, `contract_version`, and `program_hash` are unchanged.
7. `state_sequence` increases by exactly one.
8. The covenant has no unilateral mint key path that bypasses these transitions.

External inputs MAY fund transaction fees. Implementations SHOULD use an exogenous fee input or fee-anchor output so repeated state transitions do not materially reduce the bond.

---

## 8. State Transitions

### 8.1 Deposit: `CREATE_BOND`

The initial deposit creates an `ACTIVE` bond with:

```text
state_sequence = 0
active_epoch = the latest finalized NUT-XX epoch
bond_id = SHA256(
    "Cashu_Bonded_PoL_Bond_Id_v1"
    || mint_pubkey
    || genesis_nonce
)
```

The initial epoch MUST pass the manifest, keyset-root, sum, and signature checks defined in Sections 5 and 6. A zero-history bootstrap epoch MAY use 32 zero bytes for both global digest fields and zero-sized MMRs.

The mint MUST publish the confirmed `bond_id`, bond value, `program_hash`, and full decoded state through `/v1/info`.

### 8.2 Publish: `ACTIVE_TO_PENDING`

Only the mint may authorize publication of a proposed epoch. The transaction MUST create a `PENDING` successor satisfying:

```text
proposed_epoch.epoch_index == active_epoch.epoch_index + 1
proposed_epoch.previous_global_digest == active_epoch.global_digest
```

The covenant MUST verify every proposed keyset manifest signature, reconstruct `global_digest`, and verify the sorted keyset commitment root, every keyset sum, and the total outstanding balance. The proposed keyset list MUST contain every unexpired keyset exactly once, as required by NUT-XX.

For every keyset present in both epochs, the publication witness MUST contain one NUT-XX consistency proof for the issued MMR and one for the spent MMR. The covenant MUST execute the NUT-XX consistency algorithm and require each proof to resolve exactly from the active epoch's size, root, and sum to the proposed epoch's size, root, and sum.

For a keyset that first appears in the proposed epoch, both consistency proofs MUST use the canonical empty MMR as their old state. Consequently, all issuance and spending recorded before the keyset's first bonded epoch is still committed as an append from an empty history.

The transition MUST reject any proposed epoch unless every issued and spent MMR passes consistency verification. The size inequalities below are necessary but not sufficient:

```text
new.issued_mmr_size >= old.issued_mmr_size
new.spent_mmr_size >= old.spent_mmr_size
```

A keyset may disappear only under a deterministic expiry rule fixed by `verifier_program_hash`. A deployment MAY instead require expired keysets to remain committed indefinitely.

### 8.3 Finalize: `PENDING_TO_ACTIVE`

Anyone may finalize a pending epoch after its bond output has aged by at least `CHALLENGE_PERIOD` blocks. The finalization input MUST set `nSequence >= CHALLENGE_PERIOD`, and the finalization leaf MUST enforce `<CHALLENGE_PERIOD> OP_CHECKSEQUENCEVERIFY`.

The successor state MUST be `ACTIVE` and:

```text
successor.active_epoch == pending.proposed_epoch
```

No mint signature is required for finalization. Finalization MUST NOT change the bond value.

### 8.4 Challenge: `PENDING_TO_CHALLENGED`

Anyone may challenge a pending epoch before a finalization transaction confirms by providing a canonical challenge and a slash destination. The challenge path has no relative delay.

The covenant MUST require:

```text
SHA256("Cashu_Bonded_PoL_Challenge_v1" || canonical(challenge))
    == challenge_hash
```

If `MIN_CHALLENGE_BOND > 0`, the transaction MUST include a separate challenger-controlled input of at least that value and lock it under the challenge-resolution rules. The challenge bond is not part of the PoL bond.

The slash destination is committed at this transition. Copying a later challenge witness cannot redirect the payout.

### 8.5 Refute: `CHALLENGED_TO_ACTIVE`

The mint may refute a challenge while its output remains unspent and only with the response specified for that challenge type. The response path has no relative delay.

If the response predicate succeeds:

1. The disputed epoch becomes `ACTIVE`.
2. The PoL bond is preserved.
3. A configured challenge bond MAY be paid to the mint or burned.
4. The original challenger receives no PoL bond value.

An invalid response cannot spend the challenged output.

### 8.6 Slash: `CHALLENGED_TO_CHALLENGER`

A successful slash consumes the PoL bond without a recursive successor and creates exactly one bond-funded payout:

```text
slash_output.script_pubkey == challenger_script_pubkey
slash_output.value == input_bond_value
```

The mint MUST NOT authorize or veto this transaction.

For a response-based challenge, anyone may execute the slash transition after the challenged output has aged by at least `RESPONSE_PERIOD` blocks. The slashing input MUST set `nSequence >= RESPONSE_PERIOD`, and the slash leaf MUST enforce `<RESPONSE_PERIOD> OP_CHECKSEQUENCEVERIFY`. A valid response and a timeout slash race to spend the same output.

For a self-contained challenge, the implementation MAY combine challenge and slash into a single transaction if the entire success predicate is verified atomically and the payout destination is constrained by that transaction.

### 8.7 Begin Wind-Down: `ACTIVE_TO_WIND_DOWN`

The mint may begin wind-down only if:

```text
active_epoch.total_outstanding_balance == 0
```

The withdrawal destination is committed at this transition.

### 8.8 Withdraw: `WIND_DOWN_TO_MINT`

The bond may be paid to `mint_withdrawal_script_pubkey` after the wind-down output has aged by at least `WIND_DOWN_PERIOD` blocks. The withdrawal input MUST set `nSequence >= WIND_DOWN_PERIOD`, and the withdrawal leaf MUST enforce `<WIND_DOWN_PERIOD> OP_CHECKSEQUENCEVERIFY`.

A conforming implementation MUST permit challenges against the final active epoch throughout `WIND_DOWN_PERIOD`. A challenge confirmed during wind-down replaces the wind-down state with `CHALLENGED` and cancels withdrawal unless the challenge is refuted.

---

## 9. Challenge Types

Challenge identifiers are:

| Value | Challenge                   |
| :---- | :-------------------------- |
| `0`   | `leaf_omission_or_mismatch` |
| `1`   | `append_only_violation`     |
| `2`   | `manifest_equivocation`     |

All referenced epoch and keyset commitments MUST be proven against the covenant state or one of its ancestor states. A caller-supplied root that was never committed by the bond is invalid.

### 9.1 Leaf Omission or Value Mismatch

This is a response-based challenge.

The challenge contains:

```text
LeafChallenge {
    keyset_id: bytes,
    target_epoch: uint64,
    receipt_target_epoch: uint64,
    receipt_signature: bytes,
    leaf_type: uint8,             // 0 = issued, 1 = spent
    item: bytes33,
    value: uint64
}
```

The covenant MUST verify:

1. The target epoch is committed by the bond and is not earlier than `receipt_target_epoch`.
2. The receipt signature is valid under the applicable keyset-amount public key.
3. The receipt domain and message exactly match NUT-XX.
4. The referenced keyset exists in the target epoch.

The mint refutes the challenge with an inclusion proof resolving `item` and `value` to the applicable issued or spent MMR root.

If no valid response spends the challenged output during `RESPONSE_PERIOD`, the bond is slashable. An invalid response cannot spend the output.

### 9.2 Append-Only Violation

This is a self-contained challenge.

The challenge contains two bond-committed epochs and two valid inclusion proofs for the same derived `leaf_index`. It succeeds if:

```text
proof_1.item != proof_2.item
|| proof_1.value != proof_2.value
|| later_path_does_not_preserve_earlier_prefix
```

The covenant MUST derive both leaf positions and reject a caller-supplied position that differs from either derivation.

If all predicates succeed, the challenge transaction MAY slash atomically.

### 9.3 Manifest Equivocation

This is a self-contained challenge.

The challenge contains two canonical NUT-XX manifests with signatures. It succeeds if:

```text
VerifyManifestSignature(manifest_a, mint_pubkey)
&& VerifyManifestSignature(manifest_b, mint_pubkey)
&& manifest_a.keyset_id == manifest_b.keyset_id
&& manifest_a.epoch_index == manifest_b.epoch_index
&& canonical(manifest_a.signed_fields)
    != canonical(manifest_b.signed_fields)
```

At least one manifest MUST match a keyset commitment contained in a bond-committed epoch. This prevents unrelated signatures made before the bond existed from being used unless the bond adopted the corresponding history.

If all predicates succeed, the challenge transaction MAY slash atomically.

---

## 10. Race Resolution

Bitcoin transaction ordering resolves competing transitions:

1. The first confirmed valid spend of a bond state determines its successor.
2. A challenge must confirm before the pending epoch's finalization transaction.
3. A mint response must confirm before a timeout-slash transaction.
4. Among multiple successful challengers spending the same bond output, only the first confirmed transaction receives the bond.
5. Reorganizations MAY reverse an apparent winner. Implementations MUST wait for a locally configured confirmation depth before treating a finalization, refutation, slash, or withdrawal as settled.

Wallets and challengers SHOULD use replace-by-fee and fee-anchor mechanisms compatible with the covenant. The bond MUST NOT depend on a fixed fee that could become uneconomic during congestion.

---

## 11. HTTP Discovery

A bonded mint MUST add the following setting to `GET /v1/info`:

```json
{
  "nuts": {
    "XX-B": {
      "supported": true,
      "network": "mainnet",
      "bond_outpoint": "<txid>:<vout>",
      "bond_value": 100000000,
      "program_hash": "<32-byte-lowercase-hex>",
      "contract_version": 1,
      "state": "ACTIVE",
      "state_sequence": 42,
      "active_epoch": 12,
      "challenge_period": 144,
      "response_period": 144,
      "wind_down_period": 2016
    }
  }
}
```

Clients MUST verify these values against the confirmed bond output. The HTTP response is discovery metadata, not an authority.

The mint SHOULD provide:

```text
GET /v1/pol/bond
GET /v1/pol/bond/{state_sequence}
GET /v1/pol/bond/{state_sequence}/transaction
```

These endpoints return decoded state and transaction data for convenience. A client MUST reject any response that does not reproduce the confirmed covenant commitment.

---

## 12. Wallet and Watcher Behavior

A wallet claiming Bonded PoL support MUST:

1. Resolve `bond_outpoint` using its own Bitcoin node or a trust-minimized backend.
2. Verify `program_hash`, value, state, and recursive ancestry.
3. Verify that the active PoL epoch matches the covenant commitment.
4. Display the bond amount separately from outstanding liabilities.
5. Never describe partial collateral as full collateralization.
6. Retain PoL receipts until their target epoch has finalized and the applicable challenge period has expired.

A watcher SHOULD:

1. Monitor every pending epoch throughout its `CHALLENGE_PERIOD`.
2. Retain prior bond states and committed manifests.
3. Test all held receipts against the proposed epoch.
4. Challenge early enough to win the race against finalization.
5. Monitor the mempool for conflicting finalization and withdrawal transactions.
6. Maintain fee-bumping capability.

The protocol requires at least one economically motivated watcher to detect and submit each violation. Consensus enforces a submitted proof; it does not discover fraud by itself.

---

## 13. Security Considerations

### 13.1 First-Challenger Payout

Version 1 awards the full bond to the first confirmed successful challenger. This creates intentional competition and may cause witness copying, fee races, private relay use, and miner extractable value.

Committing `challenger_script_pubkey` when entering `CHALLENGED` prevents later witness copying from changing the payout for response-based challenges. Atomic self-contained challenges remain susceptible to transaction copying unless the challenge proof commits to the payout script or the covenant otherwise binds proof authorization to that script.

These consequences are accepted in version 1.

### 13.2 Bond Is Not Solvency

A bond smaller than outstanding liabilities provides partial economic security only. Wallets MUST present both values:

```text
bond_coverage = bond_value / total_outstanding_balance
```

This ratio is meaningful only when liabilities are denominated in satoshis.

### 13.3 Non-BTC Units

For units other than `sat`, this protocol cannot compare liabilities to the BTC bond without an oracle. Such bonds MAY still be advertised as fixed BTC penalties, but MUST NOT advertise an on-chain collateral ratio.

### 13.4 Data Withholding

The covenant can slash a mint that fails to answer a valid response-based challenge, but it cannot ensure that all off-chain data is continuously available. Watchers must retain receipts, manifests, and proofs needed to form challenges.

### 13.5 Deadline Censorship

Miners may censor challenge or response transactions. Deployments SHOULD choose periods long enough to tolerate congestion and temporary censorship. A relative delay shorter than 144 blocks is NOT RECOMMENDED.

### 13.6 Fee Exhaustion

Transaction fees MUST be paid by exogenous inputs. No transition may reduce the bond to pay fees.

### 13.7 Script and Verifier Bugs

The covenant is the final adjudicator. A defect can make honest collateral unspendable or allow invalid slashing. `verifier_program_hash` and `contract_version` MUST make the executed rules unambiguous. Deployments SHOULD begin with limited bonds and independently audited implementations.

### 13.8 Covenant Upgrade

The mint MUST NOT unilaterally migrate the bond to a new verifier. An upgrade requires a transition explicitly authorized by the current program and MUST provide a full challenge window before the new program becomes active.

---

## 14. Protocol Invariants

A conforming implementation MUST preserve all of the following:

```text
I1. The mint cannot spend the bond outside the covenant state machine.

I2. Every active epoch was either the initial epoch or passed through
    a full pending challenge period.

I3. Every recursive successor preserves the program, identity, and
    bond value except for a bounded fee.

I4. A successful fraud predicate can pay the bond without mint consent.

I5. A response-based challenge can slash after its relative delay when no
    valid response confirmed.

I6. The slash destination cannot change after challenge initiation.

I7. The bond cannot return to the mint until committed liabilities are
    zero and the wind-down challenge period has expired.

I8. For competing valid spends, Bitcoin confirmation order determines
    the unique successor or payout.
```

---

## 15. Rationale

The base PoL protocol makes liability claims auditable. Bonded PoL makes a subset of violations economically enforceable by Bitcoin consensus.

The design is optimistic because honest epochs should require only one publication and one later finalization. Expensive MMR verification occurs only during a dispute. The bond is recursive so the mint cannot withdraw collateral between epochs. Challenge and response delays turn otherwise ambiguous refusal or silence into a condition voluntarily accepted by the bonded mint.

The first-challenger payout is deliberately simple. It keeps version 1 focused on the core mechanism: converting a deterministic PoL violation into a permissionless covenant spend.

[pol]: pol.md
[scripts]: bonded-pol-scripts.md
