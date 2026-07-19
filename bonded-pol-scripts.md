# Bonded PoL Reference Scripts

`experimental` `companion to NUT-XX-B`

---

## 1. Status

This document gives a concrete covenant construction for [Bonded Proof of Liabilities][bonded-pol]. It specifies the Taproot tree, transaction shapes, witness fields, and script predicates needed to implement the state machine.

The scripts are **not valid on Bitcoin today**. They combine draft opcodes with explicitly assumed operations that have no assigned consensus semantics. The pseudocode is intended to be compiled after equivalent covenant and arithmetic primitives are activated.

The construction uses:

- BIP-443 `OP_CHECKCONTRACTVERIFY` (`OP_CCV`) for state-carrying P2TR outputs and amount preservation.
- BIP-347 `OP_CAT` for canonical message construction.
- BIP-348 `OP_CHECKSIGFROMSTACK` (`OP_CSFS`) for arbitrary-message BIP-340 signatures.
- Unsigned 64-bit arithmetic, comparison, and canonical serialization operations.

No trusted signer or adjudicator appears in any spend path.

---

## 2. Concrete Opcode Profile

An implementation of this construction MUST expose operations with exactly the following logical semantics. Opcode numbers are deliberately not assigned here.

### 2.1 Draft Operations

```text
OP_CAT
    (a b -- a||b)
    Fails if the result exceeds the consensus stack-element limit.

OP_CHECKSIGFROMSTACK
    (sig message pubkey -- bool)
    BIP-340 verification as defined by BIP 348.

OP_CHECKCONTRACTVERIFY
    (data index naked_key taptree mode --)
    State and amount verification as defined by BIP 443.
```

The construction uses these `OP_CCV` modes:

```text
CCV_IN       = -1
CCV_OUT_FULL = 0
```

`CCV_OUT_FULL` MUST require the complete residual value of the bond input to be preserved in the checked output. Transaction fees MUST be paid by external inputs.

### 2.2 Assumed Operations

```text
OP_INPUTCOUNT
    (-- count_u32)

OP_OUTPUTCOUNT
    (-- count_u32)

OP_U64FROMBE
    (bytes8 -- value)
    Fails unless the input is exactly 8 bytes.

OP_U64TOBE
    (value -- bytes8)

OP_U64ADD
    (a b -- sum)
    Adds two uint64 values. The protocol assumes the result is below 2^64.

OP_U64SUB
    (a b -- difference)
    Fails on underflow. The protocol assumes valid inputs are below 2^64.

OP_U64LESSTHAN
    (a b -- bool)

OP_U64LESSTHANOREQUAL
    (a b -- bool)

OP_U64EQUAL
    (a b -- bool)

OP_SIZEVERIFY
    (bytes expected_size -- bytes)
    Fails unless the byte-string length equals expected_size.

```

Challenge, response, and wind-down periods use the existing BIP-112 `OP_CHECKSEQUENCEVERIFY`. The keyset aggregate is a Merkle tree, so every covenant hash preimage is fixed-size and fits below the stack-element limit; streaming SHA-256 is not required.

All uint64 operands and intermediate results are assumed to be less than `2^64`. A witness outside this protocol domain is invalid.

### 2.3 Script Notation

The following are compiler macros, not consensus opcodes:

```text
ASSERT(expr)       compile expr, then OP_VERIFY
EQ(a, b)           compile a, b, OP_EQUALVERIFY
HASH256(parts...)  concatenate parts in order, then OP_SHA256
U16BE(n)           canonical two-byte big-endian encoding
U32BE(n)           canonical four-byte big-endian encoding
U64BE(n)           canonical eight-byte big-endian encoding
CCV_INPUT(data)    data -1 0 -1 CCV_IN OP_CCV
CCV_NEXT(data)     data 0 0 -1 CCV_OUT_FULL OP_CCV
```

`0` as the `OP_CCV` naked key selects the BIP-341 NUMS key. `-1` as the taptree selects the current input's Taproot tree. Consequently, `CCV_NEXT` creates a script-path-only recursive output with the same tree and a new state commitment.

All macros MUST expand to bounded, loop-free Tapscript. Iteration over MMR paths and keysets is statically unrolled to the deployment maxima.

---

## 3. Contract Output

The bond is a P2TR output whose naked internal key is the BIP-341 NUMS key. Key-path spending is forbidden by construction.

```text
bond_output_key = TapTweak(
    DataTweak(BIP341_NUMS_KEY, state_hash),
    bonded_pol_taptree_root
)
```

The BIP-443 `data` value is always the 32-byte `state_hash`, not the full state:

```text
state_hash = SHA256(
    "Cashu_Bonded_PoL_State_v1"
    || canonical_state
)
```

The witness supplies the canonical state fields. Every leaf reconstructs `canonical_state`, hashes it, and calls `CCV_INPUT(state_hash)` to prove that the witness state is the state committed by the spent bond.

The complete bond value is preserved by recursive transitions. Fee inputs MAY appear after the bond input. The bond MUST be input index `0`, and the recursive bond MUST be output index `0`.

---

## 4. Compact State Encodings

The covenant uses fixed-width compact states so every reconstructed state remains below the active stack-element limit.

### 4.1 Common Prefix

```text
common =
    contract_version_u16
    || program_hash_32
    || bond_id_32
    || genesis_nonce_32
    || mint_pubkey_32
    || state_tag_u8
    || state_sequence_u64
    || active_epoch_hash_32
    || epoch_history_mmr_root_32
    || epoch_history_mmr_size_u64
```

`active_epoch_hash` commits to the full `EpochCommitment` defined by NUT-XX-B:

```text
active_epoch_hash = SHA256(
    "Cashu_Bonded_PoL_Epoch_v1"
    || canonical_epoch
)
```

### 4.2 State Bodies

```text
ACTIVE body =
    common

PENDING body =
    common
    || proposed_epoch_hash_32

CHALLENGED body =
    common
    || disputed_epoch_hash_32
    || challenge_type_u8
    || challenge_hash_32
    || challenger_xonly_pubkey_32

WIND_DOWN body =
    common
    || mint_withdrawal_xonly_pubkey_32
```

The slash destination is restricted to P2TR key-path output `P2TR(challenger_xonly_pubkey)`. Arbitrary `scriptPubKey` destinations are not supported in version 1.

---

## 5. Taproot Tree

The bond Taproot tree contains these leaves:

```text
L0  publish_epoch
L1  finalize_epoch
L2  open_leaf_challenge
L3  open_consistency_challenge
L4  refute_leaf_challenge
L5  refute_consistency_challenge
L6  slash_timeout
L7  slash_equivocation
L8  slash_append_only
L9  begin_wind_down
L10 cancel_wind_down_with_challenge
L11 withdraw_after_wind_down
```

The tree SHOULD place common cooperative leaves near the root:

```text
                     root
                   /      \
              operations   disputes
              /       \     /      \
        publish/finalize   ...      slash leaves
```

Leaf ordering affects witness size but not covenant semantics.

---

## 6. Shared Script Fragments

### 6.1 Verify Current State

Every leaf begins with:

```text
macro VERIFY_CURRENT_STATE(canonical_old_state):
    old_state_hash = HASH256(
        "Cashu_Bonded_PoL_State_v1",
        canonical_old_state
    )
    CCV_INPUT(old_state_hash)
```

It then checks:

```text
OP_INPUTCOUNT 1 OP_GREATERTHANOREQUAL OP_VERIFY
old_state.contract_version CONTRACT_VERSION OP_EQUALVERIFY
old_state.program_hash PROGRAM_HASH OP_EQUALVERIFY
```

### 6.2 Verify Recursive Successor

```text
macro VERIFY_SUCCESSOR(old, new):
    EQ(new.contract_version, old.contract_version)
    EQ(new.program_hash, old.program_hash)
    EQ(new.bond_id, old.bond_id)
    EQ(new.genesis_nonce, old.genesis_nonce)
    EQ(new.mint_pubkey, old.mint_pubkey)
    ASSERT(new.state_sequence == old.state_sequence + 1)

    new_state_hash = HASH256(
        "Cashu_Bonded_PoL_State_v1",
        canonical(new)
    )

    CCV_NEXT(new_state_hash)
```

Because `CCV_NEXT` uses full-value preservation, the recursive output receives the entire bond input. External inputs pay fees.

### 6.3 Verify Epoch Commitment

`VERIFY_EPOCH` receives every keyset commitment, its manifest signature, and the ordered list required to reconstruct the epoch.

```text
macro VERIFY_EPOCH(epoch, keysets[], signatures[]):
    ASSERT(1 <= len(keysets) <= MAX_KEYSETS)
    ASSERT(len(signatures) == len(keysets))
    ASSERT(keysets are strictly sorted by keyset_id)

    total = 0

    for i in 0 .. MAX_KEYSETS-1:          # statically unrolled
        if i < len(keysets):
            k = keysets[i]
            ASSERT(k.spent_root_sum <= k.issued_root_sum)
            ASSERT(
                k.outstanding_balance
                == k.issued_root_sum - k.spent_root_sum
            )
            total = OP_U64ADD(total, k.outstanding_balance)

            message_hash = SHA256(canonical_nut_xx_manifest_message(k, epoch))
            ASSERT(CSFS(signatures[i], message_hash, mint_pubkey))

            leaf[i] = SHA256(
                "Cashu_PoL_Keyset_Leaf_v1"
                || canonical_nut_xx_keyset_leaf(k)
            )

    ASSERT(total == epoch.total_outstanding_balance)
    ASSERT(MERKLEIZE_DUPLICATE_LAST(leaf[]) == epoch.epoch_keysets_root)
    ASSERT(
        SHA256(
            "Cashu_PoL_Epoch_v1"
            || epoch.previous_global_digest
            || U64BE(epoch.epoch_index)
            || U16BE(len(keysets))
            || epoch.epoch_keysets_root
        ) == epoch.global_digest
    )
    ASSERT(HASH_EPOCH(epoch) == supplied_epoch_hash)
```

An implementation MUST compile `keysets[]` as a length plus `MAX_KEYSETS` fixed witness slots. Disabled slots contribute no leaf and MUST contain empty byte strings.

### 6.4 Verify sum-MMR Inclusion

```text
macro VERIFY_INCLUSION(item, value, proof, committed_tree):
    ASSERT(proof.path_len <= MAX_MMR_HEIGHT)
    ASSERT(proof.peak_count <= MAX_MMR_HEIGHT + 1)

    current_hash = SHA256(item)
    current_sum = value
    local_offset = 0

    for level in 0 .. MAX_MMR_HEIGHT-1:   # statically unrolled
        if level < proof.path_len:
            sibling = proof.path[level]

            if sibling.is_left:
                current_hash = SHA256(
                    sibling.hash || current_hash
                    || U64BE(sibling.sum) || U64BE(current_sum)
                )
                current_sum = OP_U64ADD(sibling.sum, current_sum)
                local_offset = OP_U64ADD(local_offset, 1 << level)
            else:
                current_hash = SHA256(
                    current_hash || sibling.hash
                    || U64BE(current_sum) || U64BE(sibling.sum)
                )
                current_sum = OP_U64ADD(current_sum, sibling.sum)

    ASSERT((current_hash, current_sum) appears exactly once in proof.peaks)
    ASSERT(DERIVE_INDEX(committed_tree.size, proof, local_offset) == proof.leaf_index)

    bagged = BAG_PEAKS_RIGHT_TO_LEFT(proof.peaks)
    ASSERT(bagged.hash == committed_tree.root_hash)
    ASSERT(bagged.sum == committed_tree.root_sum)
```

Every unused path and peak slot MUST be empty. This prevents alternative witness encodings from bypassing the length bounds.

### 6.5 Verify MMR Consistency

```text
macro VERIFY_CONSISTENCY(old_tree, new_tree, proof):
    ASSERT(old_tree.size <= new_tree.size)
    ASSERT(proof.len <= MAX_MMR_HEIGHT + 1)
    old_peaks = DERIVE_OLD_PEAKS(old_tree.size, proof)
    ASSERT(BAG(old_peaks) == (old_tree.root_hash, old_tree.root_sum))
    new_peaks = APPEND_PROOF_SUBTREES(old_peaks, proof, new_tree.size)
    ASSERT(BAG(new_peaks) == (new_tree.root_hash, new_tree.root_sum))
```

`DERIVE_OLD_PEAKS` and `APPEND_PROOF_SUBTREES` MUST use the exact consistency algorithm and test vectors adopted by NUT-XX. Until NUT-XX defines that proof algorithm beyond its abstract response schema, `L5 refute_consistency_challenge` cannot be compiled. This is a blocking dependency, not an implementation choice.

---

## 7. Concrete Leaves

### 7.1 `L0 publish_epoch`

Transaction:

```text
input[0]  ACTIVE bond
input[1+] optional fee inputs
output[0] PENDING bond, full input[0] value
output[1+] fee change or anchors funded only by input[1+]
```

Witness, bottom to top:

```text
old_active_state_fields
old_epoch_fields
proposed_epoch_fields
proposed_keyset_slots[MAX_KEYSETS]
manifest_signatures[MAX_KEYSETS]
mint_transaction_signature
L0_script
control_block
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)
VERIFY_EPOCH(old_epoch, old_keysets, old_signatures)
VERIFY_EPOCH(proposed_epoch, proposed_keysets, proposed_signatures)

ASSERT(proposed_epoch.epoch_index == old_epoch.epoch_index + 1)
ASSERT(proposed_epoch.previous_global_digest == old_epoch.global_digest)
ASSERT(
    APPEND_HISTORY(
        old.epoch_history_mmr_root,
        old.epoch_history_mmr_size,
        old.active_epoch_hash,
        history_append_proof
    ) == (
        new.epoch_history_mmr_root,
        new.epoch_history_mmr_size
    )
)

new.state_tag = PENDING
new.proposed_epoch_hash = HASH_EPOCH(proposed_epoch)

ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))
VERIFY_SUCCESSOR(old, new)
```

`CHECKSIG` above is ordinary BIP-342 transaction-signature verification and authorizes the mint to propose the transition.

### 7.2 `L1 finalize_epoch`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING)

<CHALLENGE_PERIOD>
OP_CHECKSEQUENCEVERIFY
OP_DROP

new.state_tag = ACTIVE
new.active_epoch_hash = old.proposed_epoch_hash

VERIFY_SUCCESSOR(old, new)
```

Anyone may supply this witness. No signature is required.

### 7.3 `L2 open_leaf_challenge`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WIND_DOWN)

challenge_hash = SHA256(
    "Cashu_Bonded_PoL_Challenge_v1"
    || canonical(leaf_challenge)
)

VERIFY_RECEIPT(
    leaf_challenge.receipt_signature,
    leaf_challenge.leaf_type,
    leaf_challenge.item,
    leaf_challenge.value,
    leaf_challenge.receipt_target_epoch,
    keyset_amount_pubkey
)

ASSERT(leaf_challenge.target_epoch >= leaf_challenge.receipt_target_epoch)
ASSERT(keyset commitment is included in disputed_epoch_hash)

new.state_tag = CHALLENGED
new.challenge_type = LEAF_OMISSION_OR_MISMATCH
new.challenge_hash = challenge_hash
new.challenger_xonly_pubkey = witness.challenger_xonly_pubkey

VERIFY_SUCCESSOR(old, new)
```

The challenger key MUST be exactly 32 bytes. If challenge bonds are enabled, their script is a separate input contract and is not checked by the PoL bond leaf.

### 7.4 `L3 open_consistency_challenge`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WIND_DOWN)
ASSERT(epoch_1 is in authenticated bond ancestry)
ASSERT(epoch_2 == old disputed epoch)
ASSERT(epoch_1.index < epoch_2.index)
ASSERT(tree_type == ISSUED || tree_type == SPENT)

new.state_tag = CHALLENGED
new.challenge_type = SUM_MMR_CONSISTENCY_VIOLATION
new.challenge_hash = HASH_CHALLENGE(consistency_challenge)
new.challenger_xonly_pubkey = witness.challenger_xonly_pubkey

VERIFY_SUCCESSOR(old, new)
```

`epoch_1` ancestry is demonstrated by the authenticated epoch-history MMR carried in every state. Publication appends the prior active epoch hash to this MMR. The challenge witness supplies its inclusion proof.

### 7.5 `L4 refute_leaf_challenge`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == CHALLENGED)
ASSERT(old.challenge_type == LEAF_OMISSION_OR_MISMATCH)
ASSERT(HASH_CHALLENGE(leaf_challenge) == old.challenge_hash)

VERIFY_INCLUSION(
    leaf_challenge.item,
    leaf_challenge.value,
    response.inclusion_proof,
    committed_target_tree
)

new.state_tag = ACTIVE
new.active_epoch_hash = old.disputed_epoch_hash
VERIFY_SUCCESSOR(old, new)
```

The successful response needs no mint signature; possession of a valid inclusion proof is sufficient.

### 7.6 `L5 refute_consistency_challenge`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == CHALLENGED)
ASSERT(old.challenge_type == SUM_MMR_CONSISTENCY_VIOLATION)
ASSERT(HASH_CHALLENGE(challenge) == old.challenge_hash)

VERIFY_CONSISTENCY(old_tree, new_tree, response.consistency_proof)

new.state_tag = ACTIVE
new.active_epoch_hash = old.disputed_epoch_hash
VERIFY_SUCCESSOR(old, new)
```

### 7.7 `L6 slash_timeout`

Transaction:

```text
input[0]  CHALLENGED bond
input[1+] optional fee inputs
output[0] P2TR(challenger_xonly_pubkey), full input[0] value
output[1+] fee change funded only by input[1+]
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == CHALLENGED)

<RESPONSE_PERIOD>
OP_CHECKSEQUENCEVERIFY
OP_DROP

OP_OUTPUTCOUNT 1 OP_GREATERTHANOREQUAL OP_VERIFY

<>                         # no embedded data
0                          # output index 0
old.challenger_xonly_pubkey
<>                         # no taptree; key-path P2TR
CCV_OUT_FULL
OP_CHECKCONTRACTVERIFY
```

No recursive output is created. BIP-443 full-value preservation sends the entire bond to output `0`. Fees cannot be taken from the bond.

### 7.8 `L7 slash_equivocation`

This leaf performs an atomic challenge and slash.

Witness:

```text
old_state_fields
manifest_a_fields
signature_a
manifest_b_fields
signature_b
challenger_xonly_pubkey
L7_script
control_block
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WIND_DOWN)

msg_a = SHA256(canonical_nut_xx_manifest_message(manifest_a))
msg_b = SHA256(canonical_nut_xx_manifest_message(manifest_b))

ASSERT(CSFS(signature_a, msg_a, old.mint_pubkey))
ASSERT(CSFS(signature_b, msg_b, old.mint_pubkey))
ASSERT(manifest_a.keyset_id == manifest_b.keyset_id)
ASSERT(manifest_a.epoch_index == manifest_b.epoch_index)
ASSERT(canonical_signed_fields_a != canonical_signed_fields_b)
ASSERT(one manifest is included in authenticated bond history)

PAY_FULL_BOND_TO_P2TR(challenger_xonly_pubkey)
```

`PAY_FULL_BOND_TO_P2TR` expands to the same `OP_CCV` sequence used by `L6`. Because the challenger key and proof are in the same spending witness, a copied transaction cannot redirect the payout without changing the covenant-checked output.

### 7.9 `L8 slash_append_only`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WIND_DOWN)
ASSERT(epoch_1 and epoch_2 are included in authenticated bond history)
ASSERT(epoch_1.index < epoch_2.index)

VERIFY_INCLUSION(item_1, value_1, proof_1, tree_1)
VERIFY_INCLUSION(item_2, value_2, proof_2, tree_2)
ASSERT(proof_1.leaf_index == proof_2.leaf_index)

violation =
    item_1 != item_2
    || value_1 != value_2
    || !PATH_PREFIX(proof_1.path, proof_2.path)

ASSERT(violation)
PAY_FULL_BOND_TO_P2TR(challenger_xonly_pubkey)
```

`PATH_PREFIX` compares hash, sum, and `is_left` for every enabled slot of the earlier path.

### 7.10 `L9 begin_wind_down`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)
ASSERT(active_epoch.total_outstanding_balance == 0)
ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))

new.state_tag = WIND_DOWN
new.mint_withdrawal_xonly_pubkey = witness.mint_withdrawal_xonly_pubkey

VERIFY_SUCCESSOR(old, new)
```

### 7.11 `L10 cancel_wind_down_with_challenge`

This leaf is the wind-down equivalent of `L2` or `L3`. It verifies the selected challenge-opening predicate and creates `CHALLENGED`. After a successful refutation, the state returns to `ACTIVE`; the mint must begin a new full wind-down period.

### 7.12 `L11 withdraw_after_wind_down`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == WIND_DOWN)

<WIND_DOWN_PERIOD>
OP_CHECKSEQUENCEVERIFY
OP_DROP

PAY_FULL_BOND_TO_P2TR(old.mint_withdrawal_xonly_pubkey)
```

No mint signature is required because the withdrawal key was committed when wind-down began and the complete challenge period has elapsed.

---

## 8. Transaction Output Rules

Every transition uses one of two output templates.

### 8.1 Recursive Transition

```text
output[0].value     == bond_input.value
output[0].script    == BondProgram(new_state_hash)
sum(other outputs) <= sum(external inputs)
```

### 8.2 Terminal Payout

```text
output[0].value     == bond_input.value
output[0].script    == P2TR(committed_recipient_key)
sum(other outputs) <= sum(external inputs)
```

These equalities follow from BIP-443 full residual-value preservation. All transaction fees are exogenous.

---

## 9. Remaining Blocking Definitions

This script profile is concrete about covenant transitions, but three dependencies must be completed before bytecode can be produced:

1. **MMR consistency algorithm:** NUT-XX currently gives a response shape but does not define the exact algorithm mapping `proof_hashes` to old and new peak forests.
2. **Keyset expiry:** Base Cashu expiry uses time-oriented semantics. Bonded consensus needs an unambiguous covenant-verifiable rule or must require expired keysets to remain committed indefinitely.
3. **64-bit opcode proposal:** The arithmetic operations in Section 2.2 need consensus encodings, resource limits, and numeric rules.

Until these are fixed, any claimed final Tapscript bytecode would hide protocol choices rather than implement this specification.

---

## 10. Minimum Prototype

An executable prototype SHOULD first implement this reduced tree on a Bitcoin-like covenant test environment:

```text
publish_epoch
finalize_epoch
slash_equivocation
begin_wind_down
withdraw_after_wind_down
```

Manifest equivocation is the best first end-to-end test because it exercises:

- Recursive state with `OP_CCV`.
- Arbitrary-message signatures with `OP_CSFS`.
- Canonical message construction with `OP_CAT`.
- Permissionless terminal payout.
- No unresolved MMR consistency algorithm.

The leaf-omission and consistency paths SHOULD be added only after their bounded proof verifiers have independent test vectors.

[bip-347]: https://bips.dev/347/
[bip-348]: https://bips.dev/348/
[bip-443]: https://bips.dev/443/
[bonded-pol]: bonded-pol.md
