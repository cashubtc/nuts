# Bonded PoL Reference Scripts

`experimental` `companion to NUT-XX-B`

---

## 1. Status

This document gives a concrete covenant construction for [Bonded Proof of Liabilities][bonded-pol]. It specifies the Taproot tree, transaction shapes, witness fields, and script predicates needed to implement the state machine.

The scripts are **not valid on Bitcoin today**. They combine draft opcodes with explicitly assumed operations that have no assigned consensus semantics. The pseudocode is intended to be compiled after equivalent covenant and arithmetic primitives are activated.

The notation is a compiler-neutral typed stack-machine language modeled on Bitcoin Tapscript's Forth-like execution model. Named variables, structs, loops, functions, and `if` statements are specification macros. A compiler MUST lower them to bounded stack operations and statically unroll every loop; they are not proposed Bitcoin Script syntax.

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

Epoch cadence, challenge, response, and withdrawal delays use the existing BIP-112 `OP_CHECKSEQUENCEVERIFY`. The keyset aggregate is a Merkle tree, so every covenant hash preimage is fixed-size and fits below the stack-element limit; streaming SHA-256 is not required.

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

### 2.4 Function and Macro Registry

Every callable name used below is defined in this document. Names beginning with `OP_` are consensus operations defined in Sections 2.1 and 2.2 or existing BIP-342 opcodes. The following notation functions are compiler intrinsics:

```text
function SHA256(parts...):
    return HASH256(parts...)

function len(x):
    return x.length

function SUM_VALUES(values):
    total = 0
    for i in 0 .. MAX_TRANSACTION_ITEMS-1:
        if i < len(values):
            total = OP_U64ADD(total, values[i].value)
    return total

function CSFS(sig, message, key):
    return sig message key OP_CHECKSIGFROMSTACK

function CHECKSIG(sig, key):
    return sig key OP_CHECKSIG

function utf8(ascii_literal):
    return ascii_literal.bytes

function hex(bytes):
    out = []
    for i in 0 .. len(bytes)-1:
        APPEND(out, HEX_DIGIT(bytes[i] >> 4))
        APPEND(out, HEX_DIGIT(bytes[i] & 15))
    return out

function HEX_DIGIT(n):
    ASSERT(0 <= n && n < 16)
    if n < 10:
        return 0x30 + n
    return 0x61 + (n - 10)

function decimal(n):
    if n == 0:
        return 0x30
    reversed = []
    while n > 0:
        APPEND(reversed, 0x30 + (n mod 10))
        n = n / 10
    out = []
    for i in len(reversed)-1 .. 0 descending:
        APPEND(out, reversed[i])
    return out
```

```text
function canonical_nut_xx_manifest_message(k, epoch):
    return utf8(hex(k.keyset_id)) || ":"
        || decimal(epoch.epoch_index) || ":"
        || k.timestamp || ":"
        || hex(epoch.previous_global_digest) || ":"
        || decimal(k.issued_tree.size) || ":"
        || hex(k.issued_tree.root_hash) || ":"
        || decimal(k.issued_tree.root_sum) || ":"
        || decimal(k.spent_tree.size) || ":"
        || hex(k.spent_tree.root_hash) || ":"
        || decimal(k.spent_tree.root_sum) || ":"
        || decimal(k.outstanding_balance) || ":"
        || BOOL_TEXT(k.active) || ":"
        || decimal(k.deactivation_epoch)

function canonical_nut_xx_keyset_leaf(k):
    return U16BE(len(k.keyset_id)) || k.keyset_id
        || U64BE(k.issued_tree.size)
        || k.issued_tree.root_hash
        || U64BE(k.issued_tree.root_sum)
        || U64BE(k.spent_tree.size)
        || k.spent_tree.root_hash
        || U64BE(k.spent_tree.root_sum)
        || BOOL_BYTE(k.active)
        || U64BE(k.deactivation_epoch)

function canonical_signed_fields(m):
    return canonical_nut_xx_manifest_message(m.keyset, m.epoch)

function HASH_EPOCH(epoch):
    return SHA256(
        "Cashu_Bonded_PoL_Epoch_v1"
        || CANONICAL_EPOCH(epoch)
    )

function HASH_CHALLENGE(challenge):
    return SHA256(
        "Cashu_Bonded_PoL_Challenge_v1"
        || CANONICAL_CHALLENGE(challenge)
    )

function VERIFY_MANIFEST_SIGNATURE(manifest, mint_pubkey):
    message = canonical_nut_xx_manifest_message(
        manifest.keyset,
        manifest.epoch
    )
    return CSFS(manifest.signature, SHA256(message), mint_pubkey)

function BOOL_BYTE(value):
    if value:
        return 0x01
    return 0x00

function BOOL_TEXT(value):
    if value:
        return utf8("true")
    return utf8("false")

function CANONICAL_EPOCH(e):
    return U64BE(e.epoch_index)
        || e.global_digest
        || e.previous_global_digest
        || e.pol_keysets_root
        || e.bonded_keysets_root
        || U16BE(e.epoch_keysets_count)
        || U64BE(e.total_outstanding_balance)

function CANONICAL_CHALLENGE(c):
    return U16BE(len(c.keyset_id)) || c.keyset_id
        || U64BE(c.target_epoch)
        || U64BE(c.receipt_target_epoch)
        || U16BE(len(c.receipt_signature)) || c.receipt_signature
        || c.leaf_type
        || c.item
        || U64BE(c.value)

function CANONICAL_STATE(s):
    out = U16BE(s.contract_version)
        || s.program_hash || s.bond_id || s.genesis_nonce || s.mint_pubkey
        || s.state_tag || U64BE(s.state_sequence) || s.active_epoch_hash
    if s.closing_epoch == NONE:
        out = out || 0x00
    else:
        out = out || 0x01 || U64BE(s.closing_epoch)
    out = out || s.epoch_history_mmr_root
        || U64BE(s.epoch_history_mmr_size)
    if s.state_tag == PENDING:
        return out || s.proposed_epoch_hash
    if s.state_tag == CHALLENGED:
        return out || s.disputed_epoch_hash || s.challenge_type
            || s.challenge_hash || s.challenger_xonly_pubkey
    if s.state_tag == WITHDRAWAL_DELAY:
        return out || s.mint_withdrawal_xonly_pubkey
    ASSERT(s.state_tag == ACTIVE)
    return out
```

The bounded collection helpers are:

```text
function FIND_BY_ID(keysets, id):
    found = NONE
    for i in 0 .. MAX_KEYSETS-1:
        if i < len(keysets) && keysets[i].keyset_id == id:
            ASSERT(found == NONE)
            found = keysets[i]
    return found

function MERKLEIZE(leaves, node_domain, empty_domain):
    if len(leaves) == 0:
        return SHA256(empty_domain)
    level = leaves
    while len(level) > 1:
        next = []
        for i in 0 .. MAX_KEYSETS-1 step 2:
            if i < len(level):
                left = level[i]
                if i + 1 < len(level):
                    right = level[i + 1]
                else:
                    right = left
                APPEND(next, SHA256(node_domain || left || right))
        level = next
    return level[0]

function MERKLEIZE_POL_KEYSETS(leaves):
    return MERKLEIZE(
        leaves,
        "Cashu_PoL_Keyset_Node_v1",
        "Cashu_PoL_Keyset_Empty_v1"
    )

function MERKLEIZE_BONDED_KEYSETS(leaves):
    return MERKLEIZE(
        leaves,
        "Cashu_Bonded_PoL_Keyset_Node_v1",
        "Cashu_Bonded_PoL_Keyset_Empty_v1"
    )

function SET_BIT_HEIGHTS_DESCENDING(n):
    heights = []
    for h in MAX_MMR_HEIGHT .. 0 descending:
        if ((n >> h) & 1) == 1:
            APPEND(heights, h)
    return heights

function STACK_HEIGHTS(stack):
    heights = []
    for i in 0 .. MAX_MMR_HEIGHT:
        if i < len(stack):
            APPEND(heights, stack[i].height)
    return heights

function DECOMPOSE_ALIGNED_RANGE(n, m):
    heights = []
    cursor = n
    while cursor < m:
        selected = NONE
        for h in MAX_MMR_HEIGHT .. 0 descending:
            if selected == NONE
               && (1 << h) <= m - cursor
               && cursor mod (1 << h) == 0:
                selected = h
        ASSERT(selected != NONE)
        APPEND(heights, selected)
        cursor = cursor + (1 << selected)
    return heights
```

The MMR helpers operate on ordered `(height, hash, sum)` peaks:

```text
function APPEND(list, value):
    ASSERT(len(list) < list.capacity)
    list[len(list)] = value
    list.length = len(list) + 1

function BAG(peaks):
    return BAG_PEAKS_RIGHT_TO_LEFT(peaks)

function BAG_PEAKS_RIGHT_TO_LEFT(peaks):
    ASSERT(len(peaks) > 0)
    acc = rightmost peak
    for peak in peaks from second-rightmost to leftmost:
        acc.hash = SHA256(
            "Cashu_PoL_Bag_v1"
            || peak.hash || acc.hash
            || U64BE(peak.sum) || U64BE(acc.sum)
        )
        acc.sum = OP_U64ADD(peak.sum, acc.sum)
    return (acc.hash, acc.sum)

function DERIVE_INDEX(tree_size, proof, local_offset):
    heights = SET_BIT_HEIGHTS_DESCENDING(tree_size)
    ASSERT(proof.peak_index < len(heights))
    ASSERT(proof.path_len == heights[proof.peak_index])
    preceding = 0
    for i in 0 .. MAX_MMR_HEIGHT:
        if i < proof.peak_index:
            preceding = OP_U64ADD(preceding, 1 << heights[i])
    ASSERT(local_offset < (1 << heights[proof.peak_index]))
    return OP_U64ADD(preceding, local_offset)

function PATH_PREFIX(earlier, later):
    if earlier.path_len > later.path_len:
        return false
    result = true
    for i in 0 .. MAX_MMR_HEIGHT-1:
        if i < earlier.path_len:
            result = result
                && earlier[i].hash == later[i].hash
                && earlier[i].sum == later[i].sum
                && earlier[i].is_left == later[i].is_left
    return result
```

Receipt verification is defined as:

```text
function VERIFY_RECEIPT(
    sig,
    leaf_type,
    item,
    value,
    target_epoch,
    amount_pubkey,
    authenticated_keyset
):
    if leaf_type == ISSUED:
        message = "Cashu_PoL_Receipt_Issued:" || hex(item)
                  || ":" || decimal(target_epoch)
    else if leaf_type == SPENT:
        message = "Cashu_PoL_Receipt_Spent:" || hex(item)
                  || ":" || decimal(target_epoch)
    else:
        FAIL
    ASSERT(authenticated_keyset.amount_keys[value] == amount_pubkey)
    ASSERT(CSFS(sig, SHA256(utf8(message)), amount_pubkey))
```

History and payout helpers are:

```text
function BAG_HISTORY(peaks):
    ASSERT(len(peaks) > 0)
    acc = peaks[len(peaks) - 1].hash
    for i in len(peaks) - 2 .. 0 descending:
        acc = SHA256(
            "Cashu_Bonded_PoL_History_Bag_v1"
            || peaks[i].hash || acc
        )
    return acc

function REMOVE_LAST(list):
    ASSERT(len(list) > 0)
    value = list[len(list) - 1]
    list.length = len(list) - 1
    return value

function APPEND_HISTORY(old_root, old_size, epoch_hash, proof):
    heights = SET_BIT_HEIGHTS_DESCENDING(old_size)
    ASSERT(len(proof.old_peaks) == len(heights))
    for i in 0 .. MAX_MMR_HEIGHT:
        if i < len(proof.old_peaks):
            ASSERT(proof.old_peaks[i].height == heights[i])
    if old_size == 0:
        ASSERT(old_root == SHA256("Cashu_Bonded_PoL_History_Empty_v1"))
    else:
        ASSERT(BAG_HISTORY(proof.old_peaks) == old_root)
    stack = proof.old_peaks
    APPEND(stack, {
        height: 0,
        hash: SHA256("Cashu_Bonded_PoL_History_Leaf_v1" || epoch_hash)
    })
    while len(stack) >= 2
          && stack[len(stack)-2].height == stack[len(stack)-1].height:
        right = REMOVE_LAST(stack)
        left = REMOVE_LAST(stack)
        APPEND(stack, {
            height: left.height + 1,
            hash: SHA256(
                "Cashu_Bonded_PoL_History_Node_v1"
                || left.hash || right.hash
            )
        })
    return (BAG_HISTORY(stack), OP_U64ADD(old_size, 1))

macro PAY_FULL_BOND_TO_P2TR(recipient_xonly_pubkey):
    ASSERT(len(recipient_xonly_pubkey) == 32)
    ASSERT(OP_OUTPUTCOUNT >= 1)
    <> 0 recipient_xonly_pubkey <> CCV_OUT_FULL
    OP_CHECKCONTRACTVERIFY

function P2TR(xonly_pubkey):
    ASSERT(len(xonly_pubkey) == 32)
    return 0x5120 || xonly_pubkey

function BondProgram(state_hash):
    ASSERT(len(state_hash) == 32)
    data_key = DataTweak(BIP341_NUMS_KEY, state_hash)
    output_key = TapTweak(data_key, bonded_pol_taptree_root)
    return 0x5120 || output_key

intrinsic DataTweak(key, data) = BIP443.DataTweak
intrinsic TapTweak(key, taptree_root) = BIP341.TapTweak
```

`hex`, `decimal`, and `utf8` are canonical encoders: lowercase hexadecimal without a prefix, unsigned decimal without leading zeros, and UTF-8 bytes respectively. `NONE` is the unique absent-entry sentinel and cannot be supplied as an enabled keyset.

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
    || has_closing_epoch_u8
    [|| closing_epoch_u64]
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

WITHDRAWAL_DELAY body =
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
L3  refute_leaf_challenge
L4  slash_timeout
L5  slash_equivocation
L6  slash_append_only
L7  slash_rotation_violation
L8  begin_closing
L9  enter_withdrawal_delay
L10 cancel_withdrawal_delay_with_challenge
L11 withdraw_after_delay
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
        CANONICAL_STATE(canonical_old_state)
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
macro VERIFY_SUCCESSOR(old, new, allow_closing_init=false):
    EQ(new.contract_version, old.contract_version)
    EQ(new.program_hash, old.program_hash)
    EQ(new.bond_id, old.bond_id)
    EQ(new.genesis_nonce, old.genesis_nonce)
    EQ(new.mint_pubkey, old.mint_pubkey)
    ASSERT(new.state_sequence == old.state_sequence + 1)

    if allow_closing_init:
        ASSERT(old.closing_epoch == null)
        ASSERT(new.closing_epoch == old.active_epoch.epoch_index)
    else:
        ASSERT(new.closing_epoch == old.closing_epoch)

    new_state_hash = HASH256(
        "Cashu_Bonded_PoL_State_v1",
        CANONICAL_STATE(new)
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

            pol_leaf[i] = SHA256(
                "Cashu_PoL_Keyset_Leaf_v1"
                || canonical_nut_xx_keyset_leaf(k)
            )

            bonded_leaf[i] = SHA256(
                "Cashu_Bonded_PoL_Keyset_v1"
                || pol_leaf[i]
                || U64BE(k.redemption_end_epoch)
            )

    ASSERT(total == epoch.total_outstanding_balance)
    ASSERT(
        MERKLEIZE_POL_KEYSETS(pol_leaf[])
        == epoch.pol_keysets_root
    )
    ASSERT(
        MERKLEIZE_BONDED_KEYSETS(bonded_leaf[])
        == epoch.bonded_keysets_root
    )
    ASSERT(
        SHA256(
            "Cashu_PoL_Epoch_v1"
            || epoch.previous_global_digest
            || U64BE(epoch.epoch_index)
            || U16BE(len(keysets))
            || epoch.pol_keysets_root
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
    n = old_tree.size
    m = new_tree.size
    ASSERT(0 <= n < m < 2^63)

    expected_old_heights = SET_BIT_HEIGHTS_DESCENDING(n)
    ASSERT(proof.old_peaks.len == len(expected_old_heights))

    for i in 0 .. MAX_MMR_HEIGHT-1:       # statically unrolled
        if i < proof.old_peaks.len:
            ASSERT(proof.old_peaks[i].height == expected_old_heights[i])

    if n == 0:
        ASSERT(proof.old_peaks.len == 0)
        ASSERT(old_tree == EMPTY_MMR)
    else:
        ASSERT(
            BAG(proof.old_peaks)
            == (old_tree.root_hash, old_tree.root_sum)
        )

    expected_append_heights = DECOMPOSE_ALIGNED_RANGE(n, m)
    ASSERT(
        proof.appended_subtrees.len
        == len(expected_append_heights)
    )
    ASSERT(
        proof.appended_subtrees.len
        <= 2 * MAX_MMR_HEIGHT + 1
    )

    stack = proof.old_peaks

    for i in 0 .. 2 * MAX_MMR_HEIGHT:      # statically unrolled
        if i < proof.appended_subtrees.len:
            subtree = proof.appended_subtrees[i]
            ASSERT(subtree.height == expected_append_heights[i])
            APPEND(stack, subtree)

            for j in 0 .. MAX_MMR_HEIGHT-1: # statically unrolled
                if stack.len >= 2 && stack[-2].height == stack[-1].height:
                    right = REMOVE_LAST(stack)
                    left = REMOVE_LAST(stack)
                    APPEND(stack, {
                        hash: SHA256(
                            left.hash || right.hash
                            || U64BE(left.sum) || U64BE(right.sum)
                        ),
                        sum: OP_U64ADD(left.sum, right.sum),
                        height: left.height + 1
                    })

    ASSERT(STACK_HEIGHTS(stack) == SET_BIT_HEIGHTS_DESCENDING(m))
    ASSERT(BAG(stack) == (new_tree.root_hash, new_tree.root_sum))
```

`DECOMPOSE_ALIGNED_RANGE(n, m)` starts at `cursor = n`, repeatedly selects the largest height `h` for which `2^h <= m - cursor` and `cursor mod 2^h == 0`, emits `h`, and advances `cursor` by `2^h`. Its output is derived inside the script and MUST NOT be accepted from the witness. The implementation MUST reproduce the vectors in NUT-XX.

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
issued_consistency_proofs[MAX_KEYSETS]
spent_consistency_proofs[MAX_KEYSETS]
mint_transaction_signature
L0_script
control_block
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)

<MIN_EPOCH_BLOCKS>
OP_CHECKSEQUENCEVERIFY
OP_DROP

VERIFY_EPOCH(old_epoch, old_keysets, old_signatures)
VERIFY_EPOCH(proposed_epoch, proposed_keysets, proposed_signatures)

for i in 0 .. MAX_KEYSETS-1:               # statically unrolled
    if i < len(proposed_keysets):
        new_keyset = proposed_keysets[i]
        old_keyset = FIND_BY_ID(old_keysets, new_keyset.keyset_id)

        if old_keyset exists:
            old_issued = old_keyset.issued_tree
            old_spent = old_keyset.spent_tree
        else:
            old_issued = EMPTY_MMR
            old_spent = EMPTY_MMR

        if old_issued.size == new_keyset.issued_tree.size:
            ASSERT(old_issued == new_keyset.issued_tree)
            ASSERT(issued_consistency_proofs[i] is empty)
        else:
            VERIFY_CONSISTENCY(
                old_issued,
                new_keyset.issued_tree,
                issued_consistency_proofs[i]
            )

        if old_spent.size == new_keyset.spent_tree.size:
            ASSERT(old_spent == new_keyset.spent_tree)
            ASSERT(spent_consistency_proofs[i] is empty)
        else:
            VERIFY_CONSISTENCY(
                old_spent,
                new_keyset.spent_tree,
                spent_consistency_proofs[i]
            )

        if old_keyset exists:
            ASSERT(
                new_keyset.deactivation_epoch
                == old_keyset.deactivation_epoch
            )
            ASSERT(old_keyset.active || !new_keyset.active)
            ASSERT(
                new_keyset.redemption_end_epoch
                == old_keyset.redemption_end_epoch
            )

            if !old_keyset.active:
                # Issuance is locked, but spent_tree remains appendable
                # until redemption_end_epoch so outstanding ecash can be redeemed.
                ASSERT(
                    new_keyset.issued_tree
                    == old_keyset.issued_tree
                )

            if proposed_epoch.epoch_index
               >= new_keyset.redemption_end_epoch:
                ASSERT(
                    new_keyset.issued_tree
                    == old_keyset.issued_tree
                )
                ASSERT(
                    new_keyset.spent_tree
                    == old_keyset.spent_tree
                )
        else:
            ASSERT(
                proposed_epoch.epoch_index
                < new_keyset.deactivation_epoch
            )
            ASSERT(
                new_keyset.deactivation_epoch
                < new_keyset.redemption_end_epoch
            )

        if proposed_epoch.epoch_index
           >= new_keyset.deactivation_epoch:
            ASSERT(!new_keyset.active)

        if old.closing_epoch != null:
            ASSERT(old_keyset exists)
            ASSERT(!new_keyset.active)
            ASSERT(
                new_keyset.issued_tree
                == old_keyset.issued_tree
            )

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
new.closing_epoch = old.closing_epoch

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
ASSERT(old.state_tag == PENDING)

challenge_hash = HASH_CHALLENGE(leaf_challenge)

VERIFY_RECEIPT(
    leaf_challenge.receipt_signature,
    leaf_challenge.leaf_type,
    leaf_challenge.item,
    leaf_challenge.value,
    leaf_challenge.receipt_target_epoch,
    keyset_amount_pubkey,
    target_keyset
)

ASSERT(leaf_challenge.target_epoch >= leaf_challenge.receipt_target_epoch)
ASSERT(target_keyset commitment is included in old.proposed_epoch_hash)

new.state_tag = CHALLENGED
new.disputed_epoch_hash = old.proposed_epoch_hash
new.challenge_type = LEAF_OMISSION_OR_MISMATCH
new.challenge_hash = challenge_hash
new.challenger_xonly_pubkey = witness.challenger_xonly_pubkey

VERIFY_SUCCESSOR(old, new)
```

The challenger key MUST be exactly 32 bytes. If challenge bonds are enabled, their script is a separate input contract and is not checked by the PoL bond leaf.

### 7.4 `L3 refute_leaf_challenge`

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

### 7.5 `L4 slash_timeout`

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

### 7.6 `L5 slash_equivocation`

This leaf performs an atomic challenge and slash.

Witness:

```text
old_state_fields
manifest_a_fields
signature_a
manifest_b_fields
signature_b
challenger_xonly_pubkey
L5_script
control_block
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WITHDRAWAL_DELAY)

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

`PAY_FULL_BOND_TO_P2TR` expands to the same `OP_CCV` sequence used by `L4`. Because the challenger key and proof are in the same spending witness, a copied transaction cannot redirect the payout without changing the covenant-checked output.

### 7.7 `L6 slash_append_only`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WITHDRAWAL_DELAY)
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

### 7.8 `L7 slash_rotation_violation`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == WITHDRAWAL_DELAY)

ASSERT(VERIFY_MANIFEST_SIGNATURE(manifest_a, old.mint_pubkey))
ASSERT(manifest_a.keyset_id == baseline.keyset_id)
ASSERT(baseline is included in authenticated bond history)

if violation_kind == REACTIVATION:
    ASSERT(VERIFY_MANIFEST_SIGNATURE(manifest_b, old.mint_pubkey))
    ASSERT(manifest_a.epoch_index < manifest_b.epoch_index)
    ASSERT(!manifest_a.active && manifest_b.active)

else if violation_kind == ISSUANCE_AFTER_LOCK:
    ASSERT(VERIFY_MANIFEST_SIGNATURE(manifest_b, old.mint_pubkey))
    ASSERT(manifest_a.epoch_index < manifest_b.epoch_index)
    ASSERT(!manifest_a.active)
    ASSERT(
        manifest_a.issued_tree != manifest_b.issued_tree
    )

else if violation_kind == DEACTIVATION_OVERRUN:
    ASSERT(manifest_a.active)
    ASSERT(
        manifest_a.epoch_index
        >= manifest_a.deactivation_epoch
    )

else if violation_kind == DECLARATION_DRIFT:
    ASSERT(VERIFY_MANIFEST_SIGNATURE(manifest_b, old.mint_pubkey))
    ASSERT(manifest_a.epoch_index != manifest_b.epoch_index)
    ASSERT(
        manifest_a.deactivation_epoch
        != manifest_b.deactivation_epoch
    )

else:
    FAIL

PAY_FULL_BOND_TO_P2TR(challenger_xonly_pubkey)
```

For two-manifest variants, `manifest_b.keyset_id` MUST equal `manifest_a.keyset_id`. At least one non-violating lifecycle baseline for that keyset MUST be authenticated by bond history; the violating signed manifest need not have passed `publish_epoch`.

### 7.9 `L8 begin_closing`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)
ASSERT(old.closing_epoch == null)
ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))

new.state_tag = ACTIVE
new.closing_epoch = old.active_epoch.epoch_index
VERIFY_SUCCESSOR(old, new, allow_closing_init=true)
```

### 7.10 `L9 enter_withdrawal_delay`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)
ASSERT(old.closing_epoch != null)
ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))

for each keyset in active_epoch:
    ASSERT(!keyset.active)
    ASSERT(
        active_epoch.epoch_index
        >= keyset.redemption_end_epoch
    )
    ASSERT(keyset lifecycle declaration is unchanged since closing)
    ASSERT(keyset issued and spent trees are frozen at redemption end)

new.state_tag = WITHDRAWAL_DELAY
new.mint_withdrawal_xonly_pubkey = witness.mint_withdrawal_xonly_pubkey

VERIFY_SUCCESSOR(old, new)
```

Residual `outstanding_balance` is permitted and remains committed as expired liability.

### 7.11 `L10 cancel_withdrawal_delay_with_challenge`

This leaf is the withdrawal-delay equivalent of `L2`. It verifies the leaf-challenge opening predicate and creates `CHALLENGED`. After a successful refutation, the state returns to closing `ACTIVE`; the mint must enter a new full withdrawal delay.

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == WITHDRAWAL_DELAY)
ASSERT(old.closing_epoch != null)

challenge_hash = HASH_CHALLENGE(leaf_challenge)

VERIFY_RECEIPT(
    leaf_challenge.receipt_signature,
    leaf_challenge.leaf_type,
    leaf_challenge.item,
    leaf_challenge.value,
    leaf_challenge.receipt_target_epoch,
    keyset_amount_pubkey,
    target_keyset
)

ASSERT(leaf_challenge.target_epoch >= leaf_challenge.receipt_target_epoch)
ASSERT(
    target_keyset commitment is included in old.active_epoch_hash
)
ASSERT(len(witness.challenger_xonly_pubkey) == 32)

new.state_tag = CHALLENGED
new.active_epoch_hash = old.active_epoch_hash
new.disputed_epoch_hash = old.active_epoch_hash
new.challenge_type = LEAF_OMISSION_OR_MISMATCH
new.challenge_hash = challenge_hash
new.challenger_xonly_pubkey = witness.challenger_xonly_pubkey

VERIFY_SUCCESSOR(old, new)
```

The transition removes the `WITHDRAWAL_DELAY` body, including its committed withdrawal key. If `L3` refutes the challenge, its successor is closing `ACTIVE`, not `WITHDRAWAL_DELAY`. Consequently `L11` is unavailable until the mint executes `L9` again, commits a withdrawal key again, and the new output ages for the complete `WITHDRAWAL_DELAY_PERIOD`.

### 7.12 `L11 withdraw_after_delay`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == WITHDRAWAL_DELAY)

<WITHDRAWAL_DELAY_PERIOD>
OP_CHECKSEQUENCEVERIFY
OP_DROP

PAY_FULL_BOND_TO_P2TR(old.mint_withdrawal_xonly_pubkey)
```

No mint signature is required because the withdrawal key was committed when the delay began and the complete challenge period has elapsed.

---

## 8. Transaction Output Rules

Every transition uses one of two output templates.

### 8.1 Recursive Transition

```text
output[0].value     == bond_input.value
output[0].script    == BondProgram(new_state_hash)
SUM_VALUES(other_outputs) <= SUM_VALUES(external_inputs)
```

### 8.2 Terminal Payout

```text
output[0].value     == bond_input.value
output[0].script    == P2TR(committed_recipient_key)
SUM_VALUES(other_outputs) <= SUM_VALUES(external_inputs)
```

These equalities follow from BIP-443 full residual-value preservation. All transaction fees are exogenous.

---

## 9. Remaining Blocking Definitions

This script profile is concrete about covenant transitions, but one dependency must be completed before bytecode can be produced:

1. **64-bit opcode proposal:** The arithmetic operations in Section 2.2 need consensus encodings, resource limits, and numeric rules.

Until these are fixed, any claimed final Tapscript bytecode would hide protocol choices rather than implement this specification.

---

## 10. Minimum Prototype

An executable prototype SHOULD first implement this reduced tree on a Bitcoin-like covenant test environment:

```text
publish_epoch
finalize_epoch
slash_equivocation
begin_closing
enter_withdrawal_delay
withdraw_after_delay
```

This reduced tree exercises:

- Recursive state with `OP_CCV`.
- Arbitrary-message signatures with `OP_CSFS`.
- Canonical message construction with `OP_CAT`.
- Permissionless terminal payout.
- Mandatory issued and spent MMR consistency verification during publication.

The leaf-omission challenge path SHOULD be added after its bounded inclusion-proof verifier has independent test vectors.

[bip-347]: https://bips.dev/347/
[bip-348]: https://bips.dev/348/
[bip-443]: https://bips.dev/443/
[bonded-pol]: bonded-pol.md
