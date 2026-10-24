# NUT-388-B: Bonded Proof of Liabilities

`optional` `experimental`

> **Draft identifier:** `388` is the base proposal's pull-request number and MUST be replaced with the NUT number assigned when that proposal is merged.

---

## Abstract

This document extends [NUT-388: Proof of Liabilities][pol] with Bitcoin-native collateral and permissionless slashing.

A participating mint locks bitcoin in a recursive covenant called the **PoL bond**. The covenant carries the latest Proof of Liabilities epoch commitment and permits the bonded funds to move only through protocol-defined state transitions. A mint can advance the bond by publishing a new PoL epoch, close after every committed redemption window ends, or have the bond burned after a supported PoL violation, with only a bounded bounty paid to the successful challenger.

Version 1 pays a fixed, bounded challenger bounty and sends the remainder to a canonical provably unspendable output. This prevents a mint from recovering its collateral by manufacturing its own slash. A later version may replace burning with a deterministic holder-recovery contract.

---

## 1. Scope

This document specifies:

1. The covenant capabilities required by Bonded PoL.
2. The state committed by a PoL bond output.
3. Epoch publication, finalization, challenge, slashing, and withdrawal transitions.
4. On-chain prevention of MMR consistency and lifecycle violations, plus resolution of the other fraud challenges defined by [NUT-388][pol].
5. Canonical commitments and relative delays required for consensus-enforced adjudication.

This document does not specify:

1. A final Bitcoin soft-fork activation or consensus opcode assignment.
2. Distribution of slashed collateral through a holder-recovery mechanism.
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
4. **Exact value and output introspection:** A script can inspect every output, require exact values, and prove the unique successor or terminal-output set; external inputs pay fees. BIP-443's minimum-amount semantics alone are insufficient.
5. **Arbitrary-message signatures:** A script can verify the BIP-340 signatures used by manifests and PoL receipts rather than only transaction signatures.
6. **Hash composition:** A script can construct and SHA-256 hash the byte strings required by NUT-388.
7. **Bounded arithmetic:** A script can safely add, subtract, compare, and serialize unsigned 64-bit sums.
8. **Timelocks:** A script can enforce relative block delays with `OP_CHECKSEQUENCEVERIFY`.
9. **Bounded proof execution:** A script can verify inclusion and consistency proofs whose maximum lengths are fixed by this document.

An implementation MAY realize these semantics using state-carrying covenants, transaction introspection, `OP_CAT`, and arbitrary-message signature verification.

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

| Name                      | Type   | Meaning                                                        |
| :------------------------ | :----- | :------------------------------------------------------------- |
| `NETWORK`                 | string | Bitcoin network identifier                                     |
| `CHALLENGE_PERIOD`        | uint32 | Blocks between epoch publication and finalization              |
| `RESPONSE_PERIOD`         | uint32 | Blocks allowed for a mint response                             |
| `MIN_EPOCH_BLOCKS`        | uint32 | Minimum blocks between finalized epochs                        |
| `WITHDRAWAL_DELAY_PERIOD` | uint32 | Blocks between completed closing and bond withdrawal           |
| `MAX_KEYSETS`             | uint16 | Maximum keysets committed by one epoch                         |
| `MAX_AMOUNT_KEYS`         | uint16 | Maximum denomination keys committed by one keyset              |
| `MAX_UNIT_BYTES`          | uint16 | Maximum UTF-8 byte length of the immutable bond unit           |
| `MAX_TRANSACTION_ITEMS`   | uint16 | Maximum inputs or outputs accepted by a covenant transition    |
| `MAX_MMR_HEIGHT`          | uint8  | Maximum accepted inclusion or consistency proof height         |
| `MAX_CHALLENGE_BYTES`     | uint32 | Maximum canonical challenge size                               |
| `MAX_RESPONSE_BYTES`      | uint32 | Maximum canonical response size                                |
| `MIN_CHALLENGE_BOND`      | uint64 | Positive anti-spam collateral atomically bound to a challenge  |
| `CHALLENGER_BOUNTY`       | uint64 | Fixed maximum amount paid to a successful challenger           |
| `CONTRACT_VERSION`        | uint16 | Bonded PoL program version                                     |

`MAX_MMR_HEIGHT` MUST NOT exceed 63. Therefore a single committed sum-MMR cannot contain more than `2^63 - 1` leaves. `MAX_AMOUNT_KEY_HEIGHT` is the compile-time constant `ceil(log2(MAX_AMOUNT_KEYS))` and bounds every amount-key proof.

Both constants MUST be positive and `CHALLENGER_BOUNTY` MUST be less than the minimum permitted bond value. The challenge-bond input MUST be atomically bound to the challenged bond and paid to the mint (or burned) on refutation; an unrelated extra input is insufficient.

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
    || bytes_2(len(network)) || network
    || bytes_2(len(unit)) || unit
    || challenge_period_u32
    || response_period_u32
    || min_epoch_blocks_u32
    || withdrawal_delay_period_u32
    || max_keysets_u16
    || max_amount_keys_u16
    || max_unit_bytes_u16
    || max_transaction_items_u16
    || max_mmr_height_u8
    || max_challenge_bytes_u32
    || max_response_bytes_u32
    || min_challenge_bond_u64
    || challenger_bounty_u64
    || bytes_1(receipt_signature_scheme)
    || opcode_profile_hash
    || verifier_program_hash
)
```

`opcode_profile_hash` commits to the activated opcode numbers and exact consensus semantics used by the compiler. `verifier_program_hash` commits to the compiled Tapleaf templates with the `PROGRAM_HASH` literal replaced by a distinguished 32-byte placeholder, plus their leaf versions and canonical tree layout. The final scripts instantiate that placeholder with `program_hash`; this normalization avoids a circular hash definition. Both hashes are 32 bytes. Version 1 fixes `receipt_signature_scheme = 0`. Implementations MUST reproduce this preimage byte-for-byte and reject a state whose `program_hash` differs.

### 5.2 Canonical Proof and Witness Types

All lists use a committed logical length plus fixed deployment-sized slots. Every disabled slot MUST be the empty byte string.

```text
MerkleOpening {
    leaf_index: uint16,
    leaf_count: uint16,
    path_len: uint8,
    siblings[MAX_KEYSET_HEIGHT]: bytes32
}

HistoryOpening {
    leaf_index: uint64,
    peak_index: uint8,
    path_len: uint8,
    siblings[MAX_HISTORY_HEIGHT]: {
        hash: bytes32,
        is_left: bool
    },
    peaks[MAX_HISTORY_HEIGHT + 1]: {
        height: uint8,
        hash: bytes32
    }
}

EpochReference {
    kind: uint8, // 0 = active, 1 = proposed, 2 = history
    history_proof: optional<HistoryOpening>
}

AmountKeyEntry {
    amount: uint64,
    pubkey_compressed: bytes33
}

EpochKeysetSlot {
    commitment: KeysetCommitment,
    timestamp: bytes20
}

SignedManifest {
    epoch: EpochCommitment,
    keyset: KeysetCommitment,
    timestamp: bytes20,
    signature: bytes64
}
```

In array pseudocode, an `EpochKeysetSlot` exposes its `commitment` fields directly (for example `slot.unit`) while `slot.timestamp` remains witness metadata excluded from the keyset leaf.

`MAX_KEYSET_HEIGHT = ceil(log2(MAX_KEYSETS))`, `MAX_AMOUNT_KEY_HEIGHT = ceil(log2(MAX_AMOUNT_KEYS))`, and `MAX_HISTORY_HEIGHT = MAX_MMR_HEIGHT`. An active or proposed `EpochReference` MUST have no history proof. A historical reference MUST pass the history-MMR inclusion algorithm and cannot be supplied with a caller-chosen root.

### 5.3 Leaf Witness Schemas

Every leaf begins with the complete canonical old state and ends with its script and control block. Between them, the logical witnesses are:

```text
L0  = old_epoch, old_keysets[MAX_KEYSETS], old_signatures[MAX_KEYSETS],
      proposed_epoch, proposed_keysets[MAX_KEYSETS],
      proposed_signatures[MAX_KEYSETS],
      new_amount_key_sets[MAX_KEYSETS][MAX_AMOUNT_KEYS],
      issued_consistency_proofs[MAX_KEYSETS],
      spent_consistency_proofs[MAX_KEYSETS], history_append_proof,
      mint_transaction_signature

L1  = new_active_state

L2  = challenge_bond_input, target_epoch, target_keyset, target_keyset_opening,
      leaf_challenge, amount_key_proof, challenger_xonly_pubkey,
      challenger_transaction_signature, new_challenged_state

L3  = leaf_challenge, target_epoch, target_keyset,
      target_keyset_opening, inclusion_response, new_origin_state

L4  = timeout payout transaction fields

L5  = equivocation_kind, signed_object_a, signed_object_b,
      committed_selector, committed_epoch_reference,
      optional_committed_keyset_opening,
      challenger_xonly_pubkey, challenger_transaction_signature

L6  = epoch_1, epoch_1_reference, keyset_1, keyset_1_opening,
      epoch_2, epoch_2_reference, keyset_2, keyset_2_opening,
      tree_kind, inclusion_proof_1, inclusion_proof_2,
      challenger_xonly_pubkey, challenger_transaction_signature

L7  = baseline_epoch, baseline_reference, baseline_keyset,
      baseline_keyset_opening, violation_kind, manifest_a,
      optional_manifest_b, challenger_xonly_pubkey,
      challenger_transaction_signature

L8  = active_epoch, mint_transaction_signature, new_active_state

L9  = active_epoch, active_keysets[MAX_KEYSETS],
      active_signatures[MAX_KEYSETS], mint_withdrawal_xonly_pubkey,
      mint_transaction_signature, new_withdrawal_delay_state

L10 = challenge_bond_input, target_epoch, target_keyset, target_keyset_opening,
      leaf_challenge, amount_key_proof, challenger_xonly_pubkey,
      challenger_transaction_signature, new_challenged_state

L11 = withdrawal payout transaction fields

L12 = initial_epoch, initial_keysets[MAX_KEYSETS],
      initial_signatures[MAX_KEYSETS],
      initial_amount_key_sets[MAX_KEYSETS][MAX_AMOUNT_KEYS],
      mint_transaction_signature, new_active_state
```

Each logical list has an explicit length. Signatures and proofs at index `i` apply only to keyset slot `i`. Optional values use the canonical presence byte. A leaf MUST reject extra data in disabled slots, incorrect list lengths, or a witness exceeding its committed byte bound.

---

## 6. Bond States

The state tag is one of:

| Value | State              |
| :---- | :----------------- |
| `0`   | `ACTIVE`           |
| `1`   | `PENDING`          |
| `2`   | `CHALLENGED`       |
| `3`   | `WITHDRAWAL_DELAY` |
| `4`   | `UNINITIALIZED`    |

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
    unit: bytes,
    state_tag: uint8,
    state_sequence: uint64,
    active_epoch: EpochCommitment,
    closing_epoch: optional<uint64>,
    epoch_history_mmr_root: bytes32,
    epoch_history_mmr_size: uint64
}
```

`mint_pubkey` is the x-only NUT-06 master public key used to verify PoL manifests.

`unit` is a non-empty canonical lowercase UTF-8 NUT-02 unit identifier no longer than `MAX_UNIT_BYTES`. It is immutable for the bond's lifetime. A mint creates a separate bond for every unit.

`state_sequence` MUST increase by exactly one in every recursive transition. It prevents two semantically different successor states from claiming the same covenant sequence.

`epoch_history_mmr_root` commits to every previously finalized `EpochCommitment` hash in ascending epoch order. Publication appends the prior active epoch before proposing its successor. Challenges that reference an older epoch MUST prove it against this history root. The history MMR is sum-free and uses:

```text
empty = SHA256("Cashu_Bonded_PoL_History_Empty_v1")
leaf  = SHA256("Cashu_Bonded_PoL_History_Leaf_v1" || epoch_hash)
node  = SHA256("Cashu_Bonded_PoL_History_Node_v1" || left || right)
bag   = SHA256("Cashu_Bonded_PoL_History_Bag_v1" || left_peak || bagged_right)
```

Peaks use the same descending-height and right-to-left bagging order as NUT-388. Historical references MUST execute the bounded inclusion algorithm in the companion scripts.

### 6.2 Epoch Commitment

```text
EpochCommitment {
    epoch_index: uint64,
    global_digest: bytes32,
    previous_global_digest: bytes32,
    pol_keysets_root: bytes32,
    bonded_keysets_root: bytes32,
    pol_keysets_count: uint16,
    bonded_keysets_count: uint16,
    total_outstanding_balance: uint64,
    global_epoch_signature: bytes64
}
```

`global_epoch_signature` is a BIP-340 signature by `mint_pubkey` over `SHA256("Cashu_Bonded_PoL_Global_Epoch_v1" || NETWORK || mint_pubkey || bond_id || program_hash || epoch_index || previous_global_digest || pol_keysets_count || pol_keysets_root)`. It authenticates the complete current all-unit set as one object. Two different valid global objects for the same bond and epoch are atomic equivocation evidence.

`pol_keysets_root` is the complete all-unit NUT-388 `keyset_merkle_root`. `bonded_keysets_root` filters that authenticated ordered list to entries whose signed `unit` equals `BondCommon.unit`, then commits to those keysets plus their Bonded-PoL-only metadata and expiry schedule. Its leaves encode:

```text
KeysetCommitment {
    keyset_id: bytes,
    unit: bytes,
    input_fee_ppk: uint64,
    final_expiry: optional<uint64>,
    receipt_signature_scheme: uint8,
    issued_mmr_size: uint64,
    issued_mmr_root_hash: bytes32,
    issued_mmr_root_sum: uint64,
    spent_mmr_size: uint64,
    spent_mmr_root_hash: bytes32,
    spent_mmr_root_sum: uint64,
    active: bool,
    birth_epoch: uint64,
    deactivation_epoch: uint64,
    amount_keys_root: bytes32,
    redemption_end_epoch: uint64,
    outstanding_balance: uint64
}
```

The bonded keyset leaf hash wraps the base NUT-388 leaf hash:

```text
SHA256(
    "Cashu_Bonded_PoL_Keyset_v1"
    || nut_388_keyset_leaf_hash
    || bytes_8(input_fee_ppk)
    || bytes_1(has_final_expiry) [|| bytes_8(final_expiry)]
    || bytes_1(receipt_signature_scheme)
    || amount_keys_root
    || bytes_8(birth_epoch)
    || bytes_8(redemption_end_epoch)
)
```

Version 1 defines `receipt_signature_scheme = 0` as BIP-340 and rejects every other value. This intentionally excludes BLS receipt keys.

`amount_keys_root` commits to the compressed secp256k1 public key authorized to sign PoL receipts for every denomination in the keyset. Construct its leaves in strictly increasing numeric `amount` order:

```text
SHA256(
    "Cashu_Bonded_PoL_Amount_Key_v1"
    || bytes_2(len(unit)) || unit
    || bytes_8(amount)
    || amount_pubkey_compressed
)
```

`amount_pubkey_compressed` is exactly 33 bytes and starts with `0x02` or `0x03`; BIP-340 verification uses its final 32 bytes as the x-only key. Amount-key Merkle parents are `SHA256("Cashu_Bonded_PoL_Amount_Key_Node_v1" || left || right)`. Odd final nodes are duplicated at every level. A keyset MUST commit at least one and at most `MAX_AMOUNT_KEYS` unique denominations. `unit`, metadata, signature scheme, and `amount_keys_root` are fixed at keyset birth and MUST remain unchanged in every later epoch.

Merkle parents are:

```text
SHA256("Cashu_Bonded_PoL_Keyset_Node_v1" || left || right)
```

When a level has an odd node count, its final node is duplicated. `pol_keysets_count` covers the complete NUT-388 epoch across all units and MUST be between 1 and `MAX_KEYSETS`. `bonded_keysets_count` counts exactly those entries whose signed `unit` equals the bond unit and MUST also be nonzero. `bonded_keysets_root` contains that complete same-unit subsequence in global order. Other-unit keysets remain authenticated by `pol_keysets_root` but do not contribute to bonded liabilities or lifecycle enforcement.

The covenant MUST verify that:

```text
total_outstanding_balance
    == sum(keyset.outstanding_balance for every same-unit bonded keyset)
```

and for each keyset in the full NUT-388 epoch:

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
    challenger_xonly_pubkey: bytes32,
    challenge_origin: uint8
}
```

The terminal payout is the key-path P2TR output `OP_1 <challenger_xonly_pubkey>`. The key MUST NOT be changeable by a response or slashing transaction.

### 6.5 Withdrawal-Delay State

```text
WithdrawalDelayState {
    common: BondCommon,
    mint_withdrawal_xonly_pubkey: bytes32
}
```

---

## 7. Bond Output Invariants

Every recursive transition MUST enforce:

1. Exactly one input is the current PoL bond.
2. Exactly one transaction output matches the successor program and state; all outputs are inspected so a duplicate successor is invalid.
3. The successor executes the same `program_hash` and commits to the required next state.
4. The successor value equals `input_bond_value`; this requires exact-value introspection and does not follow from BIP-443 alone.
5. No output other than the successor may receive value from the bond input, except an explicitly constrained fee mechanism.
6. `bond_id`, `genesis_nonce`, `mint_pubkey`, `unit`, `contract_version`, and `program_hash` are unchanged.
7. `state_sequence` increases by exactly one.
8. The covenant has no unilateral mint key path that bypasses these transitions.
9. Every common field not named as mutable by the selected transition is byte-for-byte unchanged. `PUBLISH` alone may append exactly one history leaf; `FINALIZE` and `REFUTE` alone may replace `active_epoch`; `BEGIN_CLOSING` alone may initialize `closing_epoch`.

External inputs MAY fund transaction fees. Implementations SHOULD use an exogenous fee input or fee-anchor output so repeated state transitions do not materially reduce the bond.

---

## 8. State Transitions

### 8.1 Deposit: `CREATE_BOND`

Because an output script does not execute when the output is created, the funding transaction MUST create an `UNINITIALIZED` bond with:

```text
state_sequence = 0
active_epoch_hash = 32 zero bytes
closing_epoch = null
epoch_history_mmr_root = SHA256("Cashu_Bonded_PoL_History_Empty_v1")
epoch_history_mmr_size = 0
bond_id = SHA256(
    "Cashu_Bonded_PoL_Bond_Id_v1"
    || mint_pubkey
    || genesis_nonce
)
```

`INITIALIZE_BOND` is the only leaf available to `UNINITIALIZED`. It verifies the mint transaction signature, immutable unit, complete initial epoch, every manifest signature, every bonded keyset leaf, and every full amount-key list before producing `ACTIVE` with `state_sequence = 1`. The history remains canonically empty; the first later publication appends the initial active epoch. No wallet may recognize an uninitialized output as a live bond.

Existing keysets may be adopted with nonempty liability MMRs at initialization and are treated as born into this bond at that epoch. Any keyset first admitted later MUST have canonical empty issued and spent MMRs; wallets MUST reject issuance from it until that admission epoch has finalized.

The mint MUST publish the confirmed `bond_id`, bond value, `program_hash`, and full decoded state through `/v1/info`.

### 8.2 Publish: `ACTIVE_TO_PENDING`

Only the mint may authorize publication of a proposed epoch. The transaction MUST create a `PENDING` successor satisfying:

```text
proposed_epoch.epoch_index == active_epoch.epoch_index + 1
proposed_epoch.previous_global_digest == active_epoch.global_digest
```

The active bond output MUST have aged by at least `MIN_EPOCH_BLOCKS`. The publication input MUST set `nSequence >= MIN_EPOCH_BLOCKS`, and the publication leaf MUST enforce `<MIN_EPOCH_BLOCKS> OP_CHECKSEQUENCEVERIFY`. This prevents the mint from accelerating epoch-based lifecycle deadlines.

The covenant MUST verify every proposed keyset manifest signature, reconstruct `global_digest`, and verify the sorted keyset commitment root, every keyset sum, and the total outstanding balance. The proposed keyset list MUST contain every unexpired keyset exactly once, as required by NUT-388.

For every keyset present in both epochs, the publication witness MUST contain one NUT-388 consistency proof for the issued MMR and one for the spent MMR. The covenant MUST execute the NUT-388 consistency algorithm and require each proof to resolve exactly from the active epoch's size, root, and sum to the proposed epoch's size, root, and sum.

For a keyset that first appears after initialization, both its old and proposed issued and spent MMRs MUST be the canonical empty MMR. It becomes eligible for issuance only after this admission epoch finalizes; its first nonempty history may appear in the following epoch.

The transition MUST reject any proposed epoch unless every issued and spent MMR passes consistency verification. The size inequalities below are necessary but not sufficient:

```text
new.issued_mmr_size >= old.issued_mmr_size
new.spent_mmr_size >= old.spent_mmr_size
```

For every keyset, the transition MUST additionally enforce:

1. A newly appearing keyset has `deactivation_epoch > proposed_epoch.epoch_index`.
2. Every keyset has `unit == bond.unit` and `receipt_signature_scheme == 0`.
3. An existing keyset's `unit`, `input_fee_ppk`, `final_expiry`, `receipt_signature_scheme`, `birth_epoch`, `deactivation_epoch`, and `amount_keys_root` are unchanged. A newly admitted keyset has `birth_epoch == proposed_epoch.epoch_index`; an initialized legacy keyset has `birth_epoch == initial_epoch.epoch_index`.
4. A newly appearing keyset supplies its complete, strictly amount-sorted compressed public-key list so the covenant can reconstruct and verify the committed root.
5. `active` cannot change from false to true.
6. If the old keyset is inactive, the new issued MMR is exactly equal to the old issued MMR.
7. If `proposed_epoch.epoch_index >= deactivation_epoch`, the new keyset is inactive.

A bonded keyset inherits the required base-PoL `deactivation_epoch` and MUST commit at birth to:

```text
birth_epoch < deactivation_epoch < redemption_end_epoch
```

`redemption_end_epoch` is immutable. The mint MUST accept redemption through the epoch immediately preceding it. In every epoch at or after `redemption_end_epoch`, both the issued and spent MMRs MUST equal their state at `redemption_end_epoch`; any residual outstanding balance is an expired liability and does not prevent bond withdrawal. `final_expiry` is committed NUT-02 metadata but is not interpreted by Bitcoin Script; wallets MUST reject a bonded lifecycle whose epoch-based redemption window is inconsistent with their policy for the advertised wall-clock expiry.

If `closing_epoch` is set, the proposed epoch MUST contain exactly the same keyset IDs as the active epoch, every keyset MUST be inactive, and no issued MMR may change. Spent MMRs continue through each keyset's redemption window.

Inactivity prohibits issuance but does not prohibit redemption. The spent MMR of an inactive, unexpired keyset MAY grow and MUST pass the same mandatory consistency proof as every other MMR transition. These checks make lifecycle consistency a validity condition of the epoch transition rather than an optimistic challenge.

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

The challenger MUST provide a BIP-342 transaction signature under the x-only payout key. The signature proves control of that key and commits to the `CHALLENGED` successor output. It prevents mutation of that exact transaction but does not stop an observer from constructing a distinct valid transaction from copied public evidence and a different key; confirmation order implements the intentional first-challenger rule.

The same transaction MUST spend a challenge-bond contract of at least `MIN_CHALLENGE_BOND` that is cryptographically bound to this bond outpoint and challenger key. Refutation pays that collateral to the mint or burns it; timeout returns it with the bounded bounty. The PoL bond leaf MUST verify this linkage atomically.

`CHALLENGED` commits whether it originated from `PENDING` or `WITHDRAWAL_DELAY`. Atomic equivocation, append-only, rotation, and global-epoch equivocation leaves remain available from `CHALLENGED`; a receipt challenge cannot monopolize the fraud-proof slot.

### 8.5 Refute: `CHALLENGED_TO_ORIGIN`

The mint may refute a challenge while its output remains unspent and only with the response specified for that challenge type. The response path has no relative delay.

If the response predicate succeeds:

1. A challenge opened from `PENDING` returns to `PENDING`, preserving the disputed proposal and starting a fresh full `CHALLENGE_PERIOD` on the new output. A withdrawal challenge returns to closing `ACTIVE`, requiring a fresh withdrawal-delay transition.
2. The PoL bond is preserved.
3. A configured challenge bond MAY be paid to the mint or burned.
4. The original challenger receives no PoL bond value.

An invalid response cannot spend the challenged output.

### 8.6 Slash: `CHALLENGED_TO_BURN_AND_BOUNTY`

A successful slash consumes the PoL bond without a recursive successor and creates exactly two bond-funded outputs:

```text
bounty_output.script_pubkey == P2TR(challenger_xonly_pubkey)
bounty_output.value == CHALLENGER_BOUNTY
burn_output.script_pubkey == canonical_unspendable_script
burn_output.value == input_bond_value - CHALLENGER_BOUNTY
```

The covenant MUST inspect the complete output vector and reject any other bond-funded output. The burn script is committed by `program_hash`. Thus even a mint-controlled challenger key cannot recover more than the bounded bounty.

The mint MUST NOT authorize or veto this transaction.

For a response-based challenge, anyone may execute the slash transition after the challenged output has aged by at least `RESPONSE_PERIOD` blocks. The slashing input MUST set `nSequence >= RESPONSE_PERIOD`, and the slash leaf MUST enforce `<RESPONSE_PERIOD> OP_CHECKSEQUENCEVERIFY`. A valid response and a timeout slash race to spend the same output.

For a self-contained challenge, the implementation MAY combine challenge and slash into a single transaction if the entire success predicate is verified atomically and the payout destination is constrained by that transaction.

### 8.7 Begin Closing: `ACTIVE_TO_ACTIVE`

The mint may announce closing from `ACTIVE`. The recursive successor remains `ACTIVE` and sets:

```text
closing_epoch = active_epoch.epoch_index
```

Before closing, `closing_epoch` MUST be null. Once set, it is immutable. Closing forbids new keysets and requires all keysets to become issuance-inactive in the next published epoch. Epoch publication continues so redemptions extend the spent MMRs.

### 8.8 Enter Withdrawal Delay: `ACTIVE_TO_WITHDRAWAL_DELAY`

The mint may enter `WITHDRAWAL_DELAY` only if:

```text
closing_epoch != null
active_epoch.epoch_index >= max(redemption_end_epoch)
all keysets are inactive
all keyset IDs and lifecycle declarations are unchanged since closing_epoch
```

The covenant MUST verify that both MMRs are frozen for every keyset whose redemption window ended. `total_outstanding_balance` MAY remain nonzero; it records expired, unredeemed ecash. The withdrawal destination is committed at this transition.

### 8.9 Withdraw: `WITHDRAWAL_DELAY_TO_MINT`

The bond may be paid to `P2TR(mint_withdrawal_xonly_pubkey)` after the withdrawal-delay output has aged by at least `WITHDRAWAL_DELAY_PERIOD` blocks. The withdrawal input MUST set `nSequence >= WITHDRAWAL_DELAY_PERIOD`, and the withdrawal leaf MUST enforce `<WITHDRAWAL_DELAY_PERIOD> OP_CHECKSEQUENCEVERIFY`.

A conforming implementation MUST permit challenges against the final active epoch throughout `WITHDRAWAL_DELAY_PERIOD`. A challenge confirmed during this delay replaces the state with `CHALLENGED` and cancels withdrawal unless the challenge is refuted. After refutation, the mint must enter a new full withdrawal delay.

---

## 9. Challenge Types

Challenge identifiers are:

| Value | Challenge                   |
| :---- | :-------------------------- |
| `0`   | `leaf_omission_or_mismatch` |
| `1`   | `append_only_violation`     |
| `2`   | `manifest_equivocation`     |
| `3`   | `rotation_violation`        |

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
    amount_pubkey_compressed: bytes33,
    leaf_type: uint8,             // 0 = issued, 1 = spent
    item: bytes33,
    value: uint64
}
```

The opening witness additionally contains:

```text
AmountKeyProof {
    leaf_index: uint16,
    leaf_count: uint16,
    path_len: uint8,
    siblings[MAX_AMOUNT_KEY_HEIGHT]: bytes32
}
```

`leaf_index` is the index of `value` in the strictly increasing denomination order. For an odd final node at any level, the proof supplies the current hash itself as the duplicated sibling. The covenant derives the required path length from `leaf_count`, rejects non-canonical disabled slots, and reconstructs `amount_keys_root` before checking the receipt signature.

The covenant MUST verify:

1. The target epoch is committed by the bond and is not earlier than `receipt_target_epoch`.
2. The supplied amount public key and denomination have a valid Merkle inclusion proof against the referenced keyset's committed `amount_keys_root`.
3. The receipt signature is valid under that authenticated amount public key.
4. The receipt domain and message exactly match NUT-388.
5. The referenced keyset exists in the target epoch.

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

### 9.3 Manifest or Global-Epoch Equivocation

This is a self-contained challenge. It accepts either two per-keyset manifests as below or two distinct `global_epoch_signature` objects with identical (`NETWORK`, `bond_id`, `program_hash`, `epoch_index`) domains. At least one object MUST be opened from an authenticated epoch of this bond. The global variant succeeds when both signatures verify and the signed `previous_global_digest`, `pol_keysets_count`, or `pol_keysets_root` differs.

The challenge contains two canonical NUT-388 manifests with signatures. It succeeds if:

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

### 9.4 Keyset Rotation Violation

This is a self-contained challenge. The challenger supplies a lifecycle baseline manifest committed by the bond plus one or two signed manifests satisfying a NUT-388 `rotation_violation` predicate.

The covenant MUST:

1. Verify every supplied manifest under `mint_pubkey`.
2. Prove the baseline keyset commitment against authenticated bond history.
3. Require all manifests to identify the same keyset.
4. Evaluate exactly one of `reactivation`, `issuance_after_lock`, `deactivation_overrun`, or `declaration_drift` as defined by NUT-388, including unit drift.

Every violating statement MUST carry the bonded global-epoch domain (`NETWORK`, `bond_id`, and `program_hash`) and have `epoch_index >= baseline.birth_epoch`. Pre-bond, cross-network, and replacement-bond statements are invalid evidence. If the selected predicate succeeds, the challenge transaction MAY slash atomically.

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
    "388-B": {
      "supported": true,
      "bonds": [
        {
          "network": "mainnet",
          "unit": "sat",
          "bond_outpoint": "<txid>:<vout>",
          "bond_value": 100000000,
          "program_hash": "<32-byte-lowercase-hex>",
          "contract_version": 1,
          "state": "ACTIVE",
          "state_sequence": 42,
          "active_epoch": 12,
          "challenge_period": 144,
          "response_period": 144,
          "min_epoch_blocks": 6,
          "withdrawal_delay_period": 2016
        }
      ]
    }
  }
}
```

Each array entry represents exactly one immutable unit. Clients MUST verify these values against the confirmed bond output. The HTTP response is discovery metadata, not an authority.

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

### 13.1 Bounded Challenger Bounty

Version 1 awards only `CHALLENGER_BOUNTY` to the first confirmed successful challenger and burns the remainder. Competition, fee races, private relay use, and miner extractable value remain possible, but a mint cannot recover the bond by challenging itself.

Every challenge transaction requires a BIP-342 signature under its payout key. For response-based challenges, the signature commits to the successor containing that key. For atomic challenges, it commits directly to the covenant-checked terminal payout. A third party cannot mutate that signed transaction, but may copy public evidence into a distinct competing transaction paying another key. This is a deliberate consequence of the version-1 first-confirmed-challenger policy, not an authorization bypass.

The bounded reward is the only slash value that may reach a caller-controlled key.

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

### 13.9 Consensus and Resource Gate

This proposal does not assign opcode numbers or claim deployability under current Bitcoin limits. Before deployment, the compiler MUST bind the precise opcode semantics in `opcode_profile_hash`, statically unroll all loops, and prove for every Tapleaf that script bytes, witness bytes, stack items, stack-element bytes, validation cost, and signature checks remain within the activated consensus limits. The resulting leaf scripts, tree, compiler version, and resource report are committed by `verifier_program_hash`. A parameter set that exceeds any limit is invalid, even if its logical pseudocode is correct.

---

## 14. Protocol Invariants

A conforming implementation MUST preserve all of the following:

```text
I1. The mint cannot spend the bond outside the covenant state machine.

I2. Every active epoch was either validated by INITIALIZE_BOND or passed
    through a full pending challenge period.

I3. Every recursive successor preserves the program, identity, immutable
    unit, and exact bond value, and is the unique matching output. Fees are
    exogenous.

I4. A successful fraud predicate can pay the bond without mint consent.

I5. A response-based challenge can slash after its relative delay when no
    valid response confirmed.

I6. The bounded bounty destination cannot change after challenge initiation;
    all remaining collateral is provably unspendable.

I7. The bond cannot return to the mint until every committed redemption
    window and the final withdrawal challenge period have expired.

I8. For competing valid spends, Bitcoin confirmation order determines
    the unique successor or payout.

I9. Every receipt key is proven against the immutable amount-key root of
    a keyset opened from an authenticated epoch of the same bond unit.

I10. Every field not explicitly mutable in a transition is unchanged.

I11. Every atomic or response-based challenge payout is authorized by a
     transaction signature under the covenant-checked challenger key.
```

---

## 15. Rationale

The base PoL protocol makes liability claims auditable. Bonded PoL makes a subset of violations economically enforceable by Bitcoin consensus.

The design is optimistic because honest epochs should require only one publication and one later finalization. Expensive MMR verification occurs only during a dispute. The bond is recursive so the mint cannot withdraw collateral between epochs. Challenge and response delays turn otherwise ambiguous refusal or silence into a condition voluntarily accepted by the bonded mint.

The bounded bounty retains permissionless enforcement without turning self-slashing into an early-withdrawal path. Burning is intentionally simple and may later be replaced by a separately specified recovery covenant.

[pol]: pol.md
[scripts]: bonded-pol-scripts.md
