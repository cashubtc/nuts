# Bonded PoL Reference Scripts

`experimental` `companion to NUT-388-B`

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

OP_GREATERTHANOREQUAL
    (a b -- bool)
    Integer comparison used only for bounded transaction counts.

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

OP_U64DIVMOD
    (dividend divisor -- quotient remainder)
    Fails when divisor is zero. Both outputs are canonical uint64 values.

OP_U64AND
    (a b -- result)

OP_U64SHR
    (value shift -- result)
    Fails when shift is greater than 63.

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

```text
ZERO32                    = 32 zero bytes
EMPTY_MMR                 = { size: 0, root_hash: SHA256(empty bytes), root_sum: 0 }
EMPTY_HISTORY_ROOT        = SHA256("Cashu_Bonded_PoL_History_Empty_v1")
BIP340_SCHEME             = 0
ACTIVE                    = 0
PENDING                   = 1
CHALLENGED                = 2
WITHDRAWAL_DELAY          = 3
ACTIVE_REFERENCE          = 0
PROPOSED_REFERENCE        = 1
HISTORY_REFERENCE         = 2
ISSUED                    = 0
SPENT                     = 1
UNINITIALIZED             = 4
PUBLISH_TRANSITION        = 0
FINALIZE_TRANSITION       = 1
OPEN_CHALLENGE_TRANSITION = 2
REFUTE_TRANSITION         = 3
BEGIN_CLOSING_TRANSITION  = 4
ENTER_DELAY_TRANSITION    = 5
INITIALIZE_TRANSITION     = 6
A                         = 0
B                         = 1
LEAF_OMISSION_OR_MISMATCH = 0
REACTIVATION              = 0
ISSUANCE_AFTER_LOCK       = 1
DEACTIVATION_OVERRUN      = 2
DECLARATION_DRIFT         = 3
NONE                      = the unique disabled-slot sentinel
```

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

function IS_EMPTY(x):
    return len(x) == 0

function STRICTLY_SORTED_POL_KEYSETS(keysets):
    result = true
    for i in 1 .. MAX_KEYSETS-1:
        if i < len(keysets):
            result = result && (
                keysets[i-1].unit < keysets[i].unit
                || (
                    keysets[i-1].unit == keysets[i].unit
                    && keysets[i-1].keyset_id < keysets[i].keyset_id
                )
            )
    return result

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
function canonical_nut_388_manifest_message(k, epoch, timestamp):
    # keyset_id is canonical lowercase hexadecimal UTF-8, as in NUT-388.
    return k.keyset_id || ":" || k.unit || ":"
        || decimal(epoch.epoch_index) || ":"
        || timestamp || ":"
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

function canonical_nut_388_keyset_leaf(k):
    return U16BE(len(k.keyset_id)) || k.keyset_id
        || U16BE(len(k.unit)) || k.unit
        || U64BE(k.issued_tree.size)
        || k.issued_tree.root_hash
        || U64BE(k.issued_tree.root_sum)
        || U64BE(k.spent_tree.size)
        || k.spent_tree.root_hash
        || U64BE(k.spent_tree.root_sum)
        || BOOL_BYTE(k.active)
        || U64BE(k.deactivation_epoch)

function canonical_signed_fields(m):
    return canonical_nut_388_manifest_message(
        m.keyset,
        m.epoch,
        m.timestamp
    )

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
    message = canonical_nut_388_manifest_message(
        manifest.keyset,
        manifest.epoch,
        manifest.timestamp
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

function OPTIONAL_U64(value):
    if value == NONE:
        return 0x00
    return 0x01 || U64BE(value)

function VALID_UNIT(unit):
    if len(unit) == 0 || len(unit) > MAX_UNIT_BYTES:
        return false
    for i in 0 .. MAX_UNIT_BYTES-1:
        if i < len(unit):
            if !((0x61 <= unit[i] && unit[i] <= 0x7a)
                 || (0x30 <= unit[i] && unit[i] <= 0x39)
                 || unit[i] == 0x2d):
                return false
    return true

function COMPUTE_PROGRAM_HASH(p):
    return SHA256(
        "Cashu_Bonded_PoL_Program_v1"
        || U16BE(p.contract_version)
        || U16BE(len(p.network)) || p.network
        || U16BE(len(p.unit)) || p.unit
        || U32BE(p.challenge_period)
        || U32BE(p.response_period)
        || U32BE(p.min_epoch_blocks)
        || U32BE(p.withdrawal_delay_period)
        || U16BE(p.max_keysets)
        || U16BE(p.max_amount_keys)
        || U16BE(p.max_unit_bytes)
        || U16BE(p.max_transaction_items)
        || p.max_mmr_height
        || U32BE(p.max_challenge_bytes)
        || U32BE(p.max_response_bytes)
        || U64BE(p.min_challenge_bond)
        || U64BE(p.challenger_bounty)
        || p.receipt_signature_scheme
        || p.opcode_profile_hash
        || p.verifier_program_hash
    )

function CANONICAL_EPOCH(e):
    return U64BE(e.epoch_index)
        || e.global_digest
        || e.previous_global_digest
        || e.pol_keysets_root
        || e.bonded_keysets_root
        || U16BE(e.pol_keysets_count)
        || U16BE(e.bonded_keysets_count)
        || U64BE(e.total_outstanding_balance)
        || e.global_epoch_signature

function CANONICAL_CHALLENGE(c):
    return U16BE(len(c.keyset_id)) || c.keyset_id
        || U64BE(c.target_epoch)
        || U64BE(c.receipt_target_epoch)
        || U16BE(len(c.receipt_signature)) || c.receipt_signature
        || c.amount_pubkey_compressed
        || c.leaf_type
        || c.item
        || U64BE(c.value)

function CANONICAL_STATE(s):
    out = U16BE(s.contract_version)
        || s.program_hash || s.bond_id || s.genesis_nonce || s.mint_pubkey
        || U16BE(len(s.unit)) || s.unit
        || s.state_tag || U64BE(s.state_sequence) || s.active_epoch_hash
    if s.closing_epoch == NONE:
        out = out || 0x00
    else:
        out = out || 0x01 || U64BE(s.closing_epoch)
    out = out || s.epoch_history_mmr_root
        || U64BE(s.epoch_history_mmr_size)
    if s.state_tag == UNINITIALIZED:
        ASSERT(s.active_epoch_hash == ZERO32)
        ASSERT(s.closing_epoch == NONE)
        ASSERT(s.epoch_history_mmr_root == EMPTY_HISTORY_ROOT)
        ASSERT(s.epoch_history_mmr_size == 0)
        return out
    if s.state_tag == PENDING:
        return out || s.proposed_epoch_hash
    if s.state_tag == CHALLENGED:
        return out || s.disputed_epoch_hash || s.challenge_type
            || s.challenge_hash || s.challenger_xonly_pubkey
            || s.challenge_origin
    if s.state_tag == WITHDRAWAL_DELAY:
        return out || s.mint_withdrawal_xonly_pubkey
    ASSERT(s.state_tag == ACTIVE)
    return out
```

The bounded collection helpers are:

```text
function FIND_KEYSET(keysets, unit, id):
    found = NONE
    for i in 0 .. MAX_KEYSETS-1:
        if i < len(keysets)
           && keysets[i].unit == unit
           && keysets[i].keyset_id == id:
            ASSERT(found == NONE)
            found = keysets[i]
    return found

function MERKLEIZE(leaves, node_domain, empty_domain, max_items):
    if len(leaves) == 0:
        return SHA256(empty_domain)
    level = leaves
    while len(level) > 1:
        next = []
        for i in 0 .. max_items-1 step 2:
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
        "Cashu_PoL_Keyset_Empty_v1",
        MAX_KEYSETS
    )

function MERKLEIZE_BONDED_KEYSETS(leaves):
    return MERKLEIZE(
        leaves,
        "Cashu_Bonded_PoL_Keyset_Node_v1",
        "Cashu_Bonded_PoL_Keyset_Empty_v1",
        MAX_KEYSETS
    )

function HASH_BONDED_KEYSET(k):
    pol_leaf = SHA256(
        "Cashu_PoL_Keyset_Leaf_v1"
        || canonical_nut_388_keyset_leaf(k)
    )
    return SHA256(
        "Cashu_Bonded_PoL_Keyset_v1"
        || pol_leaf
        || U64BE(k.input_fee_ppk)
        || OPTIONAL_U64(k.final_expiry)
        || k.receipt_signature_scheme
        || k.amount_keys_root
        || U64BE(k.redemption_end_epoch)
    )

function VERIFY_MERKLE_OPENING(
    leaf,
    proof,
    committed_root,
    node_domain,
    max_leaves,
    max_height
):
    ASSERT(1 <= proof.leaf_count && proof.leaf_count <= max_leaves)
    ASSERT(proof.leaf_index < proof.leaf_count)
    ASSERT(proof.path_len == CEIL_LOG2_BOUNDED(proof.leaf_count, max_leaves))
    current = leaf
    width = proof.leaf_count
    index = proof.leaf_index
    for level in 0 .. max_height-1:
        if level < proof.path_len:
            sibling = proof.siblings[level]
            if index == width - 1 && width mod 2 == 1:
                ASSERT(sibling == current)
            if index mod 2 == 0:
                current = SHA256(node_domain || current || sibling)
            else:
                current = SHA256(node_domain || sibling || current)
            index = index / 2
            width = (width + 1) / 2
        else:
            ASSERT(IS_EMPTY(proof.siblings[level]))
    return width == 1 && index == 0 && current == committed_root

function VERIFY_KEYSET_OPENING(epoch, keyset, proof, expected_epoch_hash):
    ASSERT(HASH_EPOCH(epoch) == expected_epoch_hash)
    ASSERT(proof.leaf_count == epoch.bonded_keysets_count)
    return VERIFY_MERKLE_OPENING(
        HASH_BONDED_KEYSET(keyset),
        proof,
        epoch.bonded_keysets_root,
        "Cashu_Bonded_PoL_Keyset_Node_v1",
        MAX_KEYSETS,
        MAX_KEYSET_HEIGHT
    )

function VERIFY_AMOUNT_KEYS_ROOT(unit, keys, committed_root):
    ASSERT(1 <= len(keys) && len(keys) <= MAX_AMOUNT_KEYS)
    leaves = []
    for i in 0 .. MAX_AMOUNT_KEYS-1:
        if i < len(keys):
            if i > 0:
                ASSERT(keys[i-1].amount < keys[i].amount)
            ASSERT(VALID_COMPRESSED_KEY(keys[i].pubkey_compressed))
            APPEND(leaves, SHA256(
                "Cashu_Bonded_PoL_Amount_Key_v1"
                || U16BE(len(unit)) || unit
                || U64BE(keys[i].amount)
                || keys[i].pubkey_compressed
            ))
    root = MERKLEIZE(
        leaves,
        "Cashu_Bonded_PoL_Amount_Key_Node_v1",
        "Cashu_Bonded_PoL_Amount_Key_Empty_v1",
        MAX_AMOUNT_KEYS
    )
    return root == committed_root

function VERIFY_AMOUNT_KEY(unit, amount, pubkey, proof, committed_root):
    ASSERT(VALID_COMPRESSED_KEY(pubkey))
    ASSERT(1 <= proof.leaf_count && proof.leaf_count <= MAX_AMOUNT_KEYS)
    ASSERT(proof.leaf_index < proof.leaf_count)
    ASSERT(proof.path_len == CEIL_LOG2(proof.leaf_count))
    current = SHA256(
        "Cashu_Bonded_PoL_Amount_Key_v1"
        || U16BE(len(unit)) || unit
        || U64BE(amount)
        || pubkey
    )
    width = proof.leaf_count
    index = proof.leaf_index
    for level in 0 .. MAX_AMOUNT_KEY_HEIGHT-1:
        if level < proof.path_len:
            sibling = proof.siblings[level]
            if index == width - 1 && width mod 2 == 1:
                ASSERT(sibling == current)
            if index mod 2 == 0:
                current = SHA256(
                    "Cashu_Bonded_PoL_Amount_Key_Node_v1"
                    || current || sibling
                )
            else:
                current = SHA256(
                    "Cashu_Bonded_PoL_Amount_Key_Node_v1"
                    || sibling || current
                )
            index = index / 2
            width = (width + 1) / 2
    ASSERT(width == 1 && index == 0)
    return current == committed_root

function VALID_COMPRESSED_KEY(pubkey):
    return len(pubkey) == 33
        && (pubkey[0] == 0x02 || pubkey[0] == 0x03)

function XONLY_FROM_COMPRESSED(pubkey):
    ASSERT(VALID_COMPRESSED_KEY(pubkey))
    return pubkey[1:33]

function CEIL_LOG2_BOUNDED(n, maximum):
    ASSERT(1 <= n && n <= maximum)
    result = 0
    width = 1
    while width < n:
        width = width << 1
        result = result + 1
    return result

function CEIL_LOG2(n):
    return CEIL_LOG2_BOUNDED(n, MAX_AMOUNT_KEYS)

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
        # NUT-388 bags peaks with the ordinary parent function.
        acc.hash = SHA256(
            peak.hash || acc.hash
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

function PATH_PREFIX(earlier_path, earlier_len, later_path, later_len):
    if earlier_len > later_len:
        return false
    result = true
    for i in 0 .. MAX_MMR_HEIGHT-1:
        if i < earlier_len:
            result = result
                && earlier_path[i].hash == later_path[i].hash
                && earlier_path[i].sum == later_path[i].sum
                && earlier_path[i].is_left == later_path[i].is_left
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
    amount_pubkey
):
    if leaf_type == ISSUED:
        message = "Cashu_PoL_Receipt_Issued:" || hex(item)
                  || ":" || decimal(target_epoch)
    else if leaf_type == SPENT:
        message = "Cashu_PoL_Receipt_Spent:" || hex(item)
                  || ":" || decimal(target_epoch)
    else:
        FAIL
    ASSERT(CSFS(sig, SHA256(utf8(message)), amount_pubkey))

function SELECT_TARGET_TREE(keyset, leaf_type):
    if leaf_type == ISSUED:
        return keyset.issued_tree
    ASSERT(leaf_type == SPENT)
    return keyset.spent_tree
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

function VERIFY_HISTORY_EPOCH_OPENING(epoch, proof, history_root, history_size):
    heights = SET_BIT_HEIGHTS_DESCENDING(history_size)
    ASSERT(len(proof.peaks) == len(heights))
    ASSERT(proof.peak_index < len(proof.peaks))
    ASSERT(proof.path_len == heights[proof.peak_index])
    current = SHA256(
        "Cashu_Bonded_PoL_History_Leaf_v1"
        || HASH_EPOCH(epoch)
    )
    local_index = 0
    for level in 0 .. MAX_HISTORY_HEIGHT-1:
        if level < proof.path_len:
            sibling = proof.siblings[level]
            if sibling.is_left:
                current = SHA256(
                    "Cashu_Bonded_PoL_History_Node_v1"
                    || sibling.hash || current
                )
                local_index = local_index + (1 << level)
            else:
                current = SHA256(
                    "Cashu_Bonded_PoL_History_Node_v1"
                    || current || sibling.hash
                )
        else:
            ASSERT(IS_EMPTY(proof.siblings[level]))
    ASSERT(current == proof.peaks[proof.peak_index].hash)
    preceding = 0
    for i in 0 .. MAX_HISTORY_HEIGHT:
        if i < len(proof.peaks):
            ASSERT(proof.peaks[i].height == heights[i])
            if i < proof.peak_index:
                preceding = preceding + (1 << heights[i])
    ASSERT(proof.leaf_index == preceding + local_index)
    return BAG_HISTORY(proof.peaks) == history_root

function VERIFY_EPOCH_REFERENCE(epoch, reference, state):
    if reference.kind == ACTIVE_REFERENCE:
        return HASH_EPOCH(epoch) == state.active_epoch_hash
    if reference.kind == PROPOSED_REFERENCE:
        if state.state_tag == PENDING:
            return HASH_EPOCH(epoch) == state.proposed_epoch_hash
        return state.state_tag == CHALLENGED
            && state.challenge_origin == PENDING
            && HASH_EPOCH(epoch) == state.disputed_epoch_hash
    if reference.kind == HISTORY_REFERENCE:
        return VERIFY_HISTORY_EPOCH_OPENING(
            epoch,
            reference.history_proof,
            state.epoch_history_mmr_root,
            state.epoch_history_mmr_size
        )
    return false

macro PAY_FULL_BOND_TO_P2TR(recipient_xonly_pubkey):
    ASSERT(len(recipient_xonly_pubkey) == 32)
    ASSERT(OP_OUTPUTCOUNT >= 1)
    <> 0 recipient_xonly_pubkey <> CCV_OUT_FULL
    OP_CHECKCONTRACTVERIFY

macro PAY_SLASH_BOUNTY_AND_BURN(recipient_xonly_pubkey):
    ASSERT(len(recipient_xonly_pubkey) == 32)
    ASSERT(OP_OUTPUTCOUNT >= 2)
    ASSERT(output[0].script == P2TR(recipient_xonly_pubkey))
    ASSERT(output[0].value == CHALLENGER_BOUNTY)
    ASSERT(output[1].script == CANONICAL_UNSPENDABLE_SCRIPT)
    ASSERT(output[1].value == BOND_INPUT_VALUE - CHALLENGER_BOUNTY)
    ASSERT(EXACTLY_ONE_MATCHING_OUTPUT(output[0]))
    ASSERT(EXACTLY_ONE_MATCHING_OUTPUT(output[1]))
    ASSERT(SUM_VALUES(output[2:]) <= SUM_VALUES(external_inputs))

macro VERIFY_CHALLENGE_BOND(challenge_bond_input, challenged_bond_outpoint):
    ASSERT(challenge_bond_input.value >= MIN_CHALLENGE_BOND)
    ASSERT(challenge_bond_input.contract.challenge_id == challenged_bond_outpoint)
    ASSERT(challenge_bond_input.contract.refutation_destination
           == P2TR(old.mint_pubkey))
    ASSERT(challenge_bond_input.contract.timeout_destination
           == P2TR(witness.challenger_xonly_pubkey))

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
    || unit_len_u16 || unit
    || state_tag_u8
    || state_sequence_u64
    || active_epoch_hash_32
    || has_closing_epoch_u8
    [|| closing_epoch_u64]
    || epoch_history_mmr_root_32
    || epoch_history_mmr_size_u64
```

`active_epoch_hash` commits to the full `EpochCommitment` defined by NUT-388-B:

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

UNINITIALIZED body =
    common with active_epoch_hash = ZERO32,
    closing_epoch absent, and canonical empty history
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
L12 initialize_bond
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
old_state.unit PROGRAM_UNIT OP_EQUALVERIFY
```

### 6.2 Verify Recursive Successor

```text
macro VERIFY_SUCCESSOR(old, new, transition_kind):
    EQ(new.contract_version, old.contract_version)
    EQ(new.program_hash, old.program_hash)
    EQ(new.bond_id, old.bond_id)
    EQ(new.genesis_nonce, old.genesis_nonce)
    EQ(new.mint_pubkey, old.mint_pubkey)
    EQ(new.unit, old.unit)
    ASSERT(new.state_sequence == old.state_sequence + 1)

    if transition_kind == PUBLISH_TRANSITION:
        EQ(new.active_epoch_hash, old.active_epoch_hash)
        EQ(new.closing_epoch, old.closing_epoch)
        # L0 separately proves the one-leaf history append.
    else if transition_kind == FINALIZE_TRANSITION:
        EQ(new.active_epoch_hash, old.proposed_epoch_hash)
        EQ(new.closing_epoch, old.closing_epoch)
        EQ(new.epoch_history_mmr_root, old.epoch_history_mmr_root)
        EQ(new.epoch_history_mmr_size, old.epoch_history_mmr_size)
    else if transition_kind == OPEN_CHALLENGE_TRANSITION:
        EQ(new.active_epoch_hash, old.active_epoch_hash)
        EQ(new.closing_epoch, old.closing_epoch)
        EQ(new.epoch_history_mmr_root, old.epoch_history_mmr_root)
        EQ(new.epoch_history_mmr_size, old.epoch_history_mmr_size)
    else if transition_kind == REFUTE_TRANSITION:
        if old.challenge_origin == PENDING:
            ASSERT(new.state_tag == PENDING)
            EQ(new.active_epoch_hash, old.active_epoch_hash)
            EQ(new.proposed_epoch_hash, old.disputed_epoch_hash)
        else:
            ASSERT(old.challenge_origin == WITHDRAWAL_DELAY)
            ASSERT(new.state_tag == ACTIVE)
            EQ(new.active_epoch_hash, old.active_epoch_hash)
        EQ(new.closing_epoch, old.closing_epoch)
        EQ(new.epoch_history_mmr_root, old.epoch_history_mmr_root)
        EQ(new.epoch_history_mmr_size, old.epoch_history_mmr_size)
    else if transition_kind == BEGIN_CLOSING_TRANSITION:
        EQ(new.active_epoch_hash, old.active_epoch_hash)
        ASSERT(old.closing_epoch == null)
        ASSERT(new.closing_epoch != null)
        EQ(new.epoch_history_mmr_root, old.epoch_history_mmr_root)
        EQ(new.epoch_history_mmr_size, old.epoch_history_mmr_size)
    else if transition_kind == ENTER_DELAY_TRANSITION:
        EQ(new.active_epoch_hash, old.active_epoch_hash)
        ASSERT(new.closing_epoch == old.closing_epoch)
        EQ(new.epoch_history_mmr_root, old.epoch_history_mmr_root)
        EQ(new.epoch_history_mmr_size, old.epoch_history_mmr_size)
    else if transition_kind == INITIALIZE_TRANSITION:
        ASSERT(old.state_tag == UNINITIALIZED)
        ASSERT(old.state_sequence == 0)
        ASSERT(old.active_epoch_hash == ZERO32)
        ASSERT(old.closing_epoch == null)
        ASSERT(old.epoch_history_mmr_root == EMPTY_HISTORY_ROOT)
        ASSERT(old.epoch_history_mmr_size == 0)
        ASSERT(new.state_tag == ACTIVE)
        ASSERT(new.closing_epoch == null)
        EQ(new.epoch_history_mmr_root, old.epoch_history_mmr_root)
        EQ(new.epoch_history_mmr_size, old.epoch_history_mmr_size)
    else:
        FAIL

    new_state_hash = HASH256(
        "Cashu_Bonded_PoL_State_v1",
        CANONICAL_STATE(new)
    )

    CCV_NEXT(new_state_hash)
```

`CCV_NEXT` establishes the BIP-443 residual minimum. The committed exact-value and complete-output introspection profile additionally proves equality and uniqueness. External inputs pay fees.

### 6.3 Verify Epoch Commitment

`VERIFY_EPOCH` receives every keyset commitment, its manifest signature, and the ordered list required to reconstruct the epoch.

```text
macro VERIFY_EPOCH(
    epoch, keysets[], signatures[], mint_pubkey, bond_unit,
    network, bond_id, program_hash
):
    ASSERT(1 <= len(keysets) <= MAX_KEYSETS)
    ASSERT(len(signatures) == len(keysets))
    ASSERT(STRICTLY_SORTED_POL_KEYSETS(keysets))

    total = 0
    pol_leaf = []
    bonded_leaf = []

    for i in 0 .. MAX_KEYSETS-1:          # statically unrolled
        if i < len(keysets):
            k = keysets[i]
            ASSERT(k.spent_tree.root_sum <= k.issued_tree.root_sum)
            ASSERT(
                k.outstanding_balance
                == k.issued_tree.root_sum - k.spent_tree.root_sum
            )
            message_hash = SHA256(canonical_nut_388_manifest_message(
                k,
                epoch,
                k.timestamp
            ))
            ASSERT(CSFS(signatures[i], message_hash, mint_pubkey))

            current_pol_leaf = SHA256(
                "Cashu_PoL_Keyset_Leaf_v1"
                || canonical_nut_388_keyset_leaf(k)
            )
            APPEND(pol_leaf, current_pol_leaf)

            if k.unit == bond_unit:
                total = OP_U64ADD(total, k.outstanding_balance)
                APPEND(bonded_leaf, SHA256(
                    "Cashu_Bonded_PoL_Keyset_v1"
                    || current_pol_leaf
                    || U64BE(k.input_fee_ppk)
                    || OPTIONAL_U64(k.final_expiry)
                    || k.receipt_signature_scheme
                    || k.amount_keys_root
                    || U64BE(k.birth_epoch)
                    || U64BE(k.redemption_end_epoch)
                ))

    ASSERT(total == epoch.total_outstanding_balance)
    ASSERT(len(pol_leaf) == epoch.pol_keysets_count)
    ASSERT(len(bonded_leaf) == epoch.bonded_keysets_count)
    ASSERT(len(bonded_leaf) > 0)
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
            || U16BE(epoch.pol_keysets_count)
            || epoch.pol_keysets_root
        ) == epoch.global_digest
    )
    global_message = SHA256(
        "Cashu_Bonded_PoL_Global_Epoch_v1"
        || network || mint_pubkey || bond_id || program_hash
        || U64BE(epoch.epoch_index)
        || epoch.previous_global_digest
        || U16BE(epoch.pol_keysets_count)
        || epoch.pol_keysets_root
    )
    ASSERT(CSFS(epoch.global_epoch_signature, global_message, mint_pubkey))
```

An implementation MUST compile `keysets[]` as a length plus `MAX_KEYSETS` fixed witness slots. Disabled slots contribute no leaf and MUST contain empty byte strings.

### 6.4 Verify sum-MMR Inclusion

```text
macro VERIFY_INCLUSION(item, value, proof, committed_tree):
    ASSERT(proof.path_len <= MAX_MMR_HEIGHT)
    expected_heights = SET_BIT_HEIGHTS_DESCENDING(committed_tree.size)
    ASSERT(proof.peak_count == len(expected_heights))
    ASSERT(proof.peak_index < proof.peak_count)
    ASSERT(proof.path_len == expected_heights[proof.peak_index])

    for i in 0 .. MAX_MMR_HEIGHT:         # statically unrolled
        if i < proof.peak_count:
            ASSERT(proof.peaks[i].height == expected_heights[i])

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

    ASSERT(proof.peaks[proof.peak_index].hash == current_hash)
    ASSERT(proof.peaks[proof.peak_index].sum == current_sum)
    ASSERT(DERIVE_INDEX(committed_tree.size, proof, local_offset) == proof.leaf_index)

    bagged = BAG_PEAKS_RIGHT_TO_LEFT(proof.peaks)
    ASSERT(bagged.hash == committed_tree.root_hash)
    ASSERT(bagged.sum == committed_tree.root_sum)
```

Every unused path and peak slot MUST be empty. This prevents alternative witness encodings from bypassing the length bounds.

Conformance tests MUST reject omitted, extra, reordered, and pre-bagged peaks; a computed peak placed at the wrong index; a wrong `peak_index`; nonempty disabled slots; and equal hashes paired with different sums. They MUST also include the seven-leaf adversarial case with canonical heights `[2, 1, 0]`: a path that reaches `P1` and then folds `P0` into it MUST NOT be accepted as a leaf under `P2`.

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

`DECOMPOSE_ALIGNED_RANGE(n, m)` starts at `cursor = n`, repeatedly selects the largest height `h` for which `2^h <= m - cursor` and `cursor mod 2^h == 0`, emits `h`, and advances `cursor` by `2^h`. Its output is derived inside the script and MUST NOT be accepted from the witness. The implementation MUST reproduce the vectors in NUT-388.

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
new_amount_key_sets[MAX_KEYSETS][MAX_AMOUNT_KEYS]
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

VERIFY_EPOCH(
    old_epoch,
    old_keysets,
    old_signatures,
    old.mint_pubkey,
    old.unit, NETWORK, old.bond_id, old.program_hash
)
VERIFY_EPOCH(
    proposed_epoch,
    proposed_keysets,
    proposed_signatures,
    old.mint_pubkey,
    old.unit, NETWORK, old.bond_id, old.program_hash
)
ASSERT(HASH_EPOCH(old_epoch) == old.active_epoch_hash)

for i in 0 .. MAX_KEYSETS-1:               # statically unrolled
    if i < len(proposed_keysets):
        new_keyset = proposed_keysets[i]
        if new_keyset.unit != old.unit:
            ASSERT(IS_EMPTY(new_amount_key_sets[i]))
            ASSERT(IS_EMPTY(issued_consistency_proofs[i]))
            ASSERT(IS_EMPTY(spent_consistency_proofs[i]))
            continue

        old_keyset = FIND_KEYSET(
            old_keysets,
            old.unit,
            new_keyset.keyset_id
        )
        ASSERT(new_keyset.receipt_signature_scheme == BIP340_SCHEME)

        if old_keyset != NONE:
            old_issued = old_keyset.issued_tree
            old_spent = old_keyset.spent_tree
        else:
            old_issued = EMPTY_MMR
            old_spent = EMPTY_MMR
            ASSERT(new_keyset.birth_epoch == proposed_epoch.epoch_index)
            ASSERT(new_keyset.issued_tree == EMPTY_MMR)
            ASSERT(new_keyset.spent_tree == EMPTY_MMR)

        if old_issued.size == new_keyset.issued_tree.size:
            ASSERT(old_issued == new_keyset.issued_tree)
            ASSERT(IS_EMPTY(issued_consistency_proofs[i]))
        else:
            VERIFY_CONSISTENCY(
                old_issued,
                new_keyset.issued_tree,
                issued_consistency_proofs[i]
            )

        if old_spent.size == new_keyset.spent_tree.size:
            ASSERT(old_spent == new_keyset.spent_tree)
            ASSERT(IS_EMPTY(spent_consistency_proofs[i]))
        else:
            VERIFY_CONSISTENCY(
                old_spent,
                new_keyset.spent_tree,
                spent_consistency_proofs[i]
            )

        if old_keyset != NONE:
            ASSERT(IS_EMPTY(new_amount_key_sets[i]))
            ASSERT(
                new_keyset.deactivation_epoch
                == old_keyset.deactivation_epoch
            )
            ASSERT(old_keyset.active || !new_keyset.active)
            ASSERT(
                new_keyset.redemption_end_epoch
                == old_keyset.redemption_end_epoch
            )
            ASSERT(
                new_keyset.amount_keys_root
                == old_keyset.amount_keys_root
            )
            ASSERT(new_keyset.unit == old_keyset.unit)
            ASSERT(new_keyset.birth_epoch == old_keyset.birth_epoch)
            ASSERT(new_keyset.input_fee_ppk == old_keyset.input_fee_ppk)
            ASSERT(new_keyset.final_expiry == old_keyset.final_expiry)
            ASSERT(
                new_keyset.receipt_signature_scheme
                == old_keyset.receipt_signature_scheme
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
            ASSERT(VERIFY_AMOUNT_KEYS_ROOT(
                old.unit,
                new_amount_key_sets[i],
                new_keyset.amount_keys_root
            ))
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
            ASSERT(old_keyset != NONE)
            ASSERT(!new_keyset.active)
            ASSERT(
                new_keyset.issued_tree
                == old_keyset.issued_tree
            )

for i in 0 .. MAX_KEYSETS-1:
    if i < len(old_keysets) && old_keysets[i].unit == old.unit:
        old_keyset = old_keysets[i]
        successor = FIND_KEYSET(
            proposed_keysets,
            old.unit,
            old_keyset.keyset_id
        )
        if successor == NONE:
            ASSERT(old.closing_epoch == null)
            ASSERT(!old_keyset.active)
            ASSERT(
                proposed_epoch.epoch_index
                >= old_keyset.redemption_end_epoch
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
VERIFY_SUCCESSOR(old, new, PUBLISH_TRANSITION)
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

VERIFY_SUCCESSOR(old, new, FINALIZE_TRANSITION)
```

Anyone may supply this witness. No signature is required.

### 7.3 `L2 open_leaf_challenge`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING)
VERIFY_CHALLENGE_BOND(challenge_bond_input, CURRENT_BOND_OUTPOINT)

challenge_hash = HASH_CHALLENGE(leaf_challenge)
ASSERT(target_epoch.epoch_index == leaf_challenge.target_epoch)
ASSERT(VERIFY_KEYSET_OPENING(
    target_epoch,
    target_keyset,
    target_keyset_opening,
    old.proposed_epoch_hash
))
ASSERT(target_keyset.keyset_id == leaf_challenge.keyset_id)

ASSERT(VERIFY_AMOUNT_KEY(
    old.unit,
    leaf_challenge.value,
    leaf_challenge.amount_pubkey_compressed,
    amount_key_proof,
    target_keyset.amount_keys_root
))

VERIFY_RECEIPT(
    leaf_challenge.receipt_signature,
    leaf_challenge.leaf_type,
    leaf_challenge.item,
    leaf_challenge.value,
    leaf_challenge.receipt_target_epoch,
    XONLY_FROM_COMPRESSED(leaf_challenge.amount_pubkey_compressed)
)

ASSERT(leaf_challenge.target_epoch >= leaf_challenge.receipt_target_epoch)
ASSERT(CHECKSIG(
    challenger_transaction_signature,
    witness.challenger_xonly_pubkey
))

new.state_tag = CHALLENGED
new.disputed_epoch_hash = old.proposed_epoch_hash
new.challenge_type = LEAF_OMISSION_OR_MISMATCH
new.challenge_hash = challenge_hash
new.challenger_xonly_pubkey = witness.challenger_xonly_pubkey
new.challenge_origin = PENDING

VERIFY_SUCCESSOR(old, new, OPEN_CHALLENGE_TRANSITION)
```

The challenger key MUST be exactly 32 bytes. The challenge bond is a separate input contract, but the PoL bond leaf verifies its value, outpoint binding, challenger destination, and refutation destination atomically.

### 7.4 `L3 refute_leaf_challenge`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == CHALLENGED)
ASSERT(old.challenge_type == LEAF_OMISSION_OR_MISMATCH)
ASSERT(HASH_CHALLENGE(leaf_challenge) == old.challenge_hash)

ASSERT(target_epoch.epoch_index == leaf_challenge.target_epoch)
ASSERT(VERIFY_KEYSET_OPENING(
    target_epoch,
    target_keyset,
    target_keyset_opening,
    old.disputed_epoch_hash
))
ASSERT(target_keyset.keyset_id == leaf_challenge.keyset_id)

VERIFY_INCLUSION(
    leaf_challenge.item,
    leaf_challenge.value,
    response.inclusion_proof,
    SELECT_TARGET_TREE(target_keyset, leaf_challenge.leaf_type)
)

if old.challenge_origin == PENDING:
    new.state_tag = PENDING
    new.active_epoch_hash = old.active_epoch_hash
    new.proposed_epoch_hash = old.disputed_epoch_hash
else:
    ASSERT(old.challenge_origin == WITHDRAWAL_DELAY)
    new.state_tag = ACTIVE
    new.active_epoch_hash = old.active_epoch_hash
VERIFY_SUCCESSOR(old, new, REFUTE_TRANSITION)
```

The successful response needs no mint signature; possession of a valid inclusion proof is sufficient.

### 7.5 `L4 slash_timeout`

Transaction (all outputs are inspected):

```text
input[0]  CHALLENGED bond
input[1+] optional fee inputs
output[0] P2TR(challenger_xonly_pubkey), CHALLENGER_BOUNTY
output[1] canonical unspendable script,
          input[0] value - CHALLENGER_BOUNTY
output[2+] fee change funded only by input[1+]
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == CHALLENGED)

<RESPONSE_PERIOD>
OP_CHECKSEQUENCEVERIFY
OP_DROP

PAY_SLASH_BOUNTY_AND_BURN(old.challenger_xonly_pubkey)
```

No recursive output is created. `PAY_SLASH_BOUNTY_AND_BURN` uses exact value and complete-output introspection: it requires one `CHALLENGER_BOUNTY` P2TR output, burns the exact remainder, rejects every duplicate/matching terminal output, and proves that any other outputs are funded exclusively by external inputs. BIP-443 minimum-amount semantics alone do not implement this macro.

### 7.6 `L5 slash_equivocation`

This leaf performs an atomic challenge and slash.

Witness:

```text
old_state_fields
equivocation_kind
signed_object_a
signed_object_b
committed_selector
committed_epoch_reference
optional_committed_keyset_opening
challenger_xonly_pubkey
challenger_transaction_signature
L5_script
control_block
```

Script:

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == CHALLENGED
       || old.state_tag == WITHDRAWAL_DELAY)

if equivocation_kind == KEYSET_MANIFEST:
    manifest_a = signed_object_a
    manifest_b = signed_object_b
    ASSERT(VERIFY_MANIFEST_SIGNATURE(manifest_a, old.mint_pubkey))
    ASSERT(VERIFY_MANIFEST_SIGNATURE(manifest_b, old.mint_pubkey))
    ASSERT(manifest_a.keyset.keyset_id == manifest_b.keyset.keyset_id)
    ASSERT(manifest_a.epoch.epoch_index == manifest_b.epoch.epoch_index)
    ASSERT(canonical_signed_fields(manifest_a)
           != canonical_signed_fields(manifest_b))
else:
    ASSERT(equivocation_kind == GLOBAL_EPOCH)
    global_a = signed_object_a
    global_b = signed_object_b
    ASSERT(global_a.network == NETWORK && global_b.network == NETWORK)
    ASSERT(global_a.bond_id == old.bond_id && global_b.bond_id == old.bond_id)
    ASSERT(global_a.program_hash == old.program_hash
           && global_b.program_hash == old.program_hash)
    ASSERT(global_a.epoch_index == global_b.epoch_index)
    ASSERT(VERIFY_GLOBAL_EPOCH_SIGNATURE(global_a, old.mint_pubkey))
    ASSERT(VERIFY_GLOBAL_EPOCH_SIGNATURE(global_b, old.mint_pubkey))
    ASSERT(CANONICAL_GLOBAL_EPOCH(global_a)
           != CANONICAL_GLOBAL_EPOCH(global_b))

if committed_selector == A:
    committed_object = signed_object_a
else:
    ASSERT(committed_selector == B)
    committed_object = signed_object_b

if equivocation_kind == KEYSET_MANIFEST:
    ASSERT(VERIFY_EPOCH_REFERENCE(
        committed_object.epoch, committed_epoch_reference, old
    ))
    ASSERT(VERIFY_KEYSET_OPENING(
        committed_object.epoch,
        committed_object.keyset,
        committed_keyset_opening,
        HASH_EPOCH(committed_object.epoch)
    ))
else:
    ASSERT(VERIFY_EPOCH_REFERENCE(
        committed_object.epoch_commitment,
        committed_epoch_reference,
        old
    ))

ASSERT(CHECKSIG(challenger_transaction_signature, challenger_xonly_pubkey))
PAY_SLASH_BOUNTY_AND_BURN(challenger_xonly_pubkey)
```

The BIP-342 challenger signature commits to the complete transaction and proves control of its bounded bounty key. Public evidence remains copyable into a distinct competing transaction, but the remainder is burned regardless of who wins.

### 7.7 `L6 slash_append_only`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == CHALLENGED
       || old.state_tag == WITHDRAWAL_DELAY)
ASSERT(VERIFY_EPOCH_REFERENCE(epoch_1, epoch_1_reference, old))
ASSERT(VERIFY_EPOCH_REFERENCE(epoch_2, epoch_2_reference, old))
ASSERT(epoch_1.epoch_index < epoch_2.epoch_index)
ASSERT(VERIFY_KEYSET_OPENING(
    epoch_1,
    keyset_1,
    keyset_1_opening,
    HASH_EPOCH(epoch_1)
))
ASSERT(VERIFY_KEYSET_OPENING(
    epoch_2,
    keyset_2,
    keyset_2_opening,
    HASH_EPOCH(epoch_2)
))
ASSERT(keyset_1.keyset_id == keyset_2.keyset_id)
ASSERT(tree_kind == ISSUED || tree_kind == SPENT)

tree_1 = SELECT_TARGET_TREE(keyset_1, tree_kind)
tree_2 = SELECT_TARGET_TREE(keyset_2, tree_kind)

VERIFY_INCLUSION(item_1, value_1, proof_1, tree_1)
VERIFY_INCLUSION(item_2, value_2, proof_2, tree_2)
ASSERT(proof_1.leaf_index == proof_2.leaf_index)

violation =
    item_1 != item_2
    || value_1 != value_2
    || !PATH_PREFIX(
        proof_1.path, proof_1.path_len,
        proof_2.path, proof_2.path_len
    )

ASSERT(violation)
ASSERT(CHECKSIG(challenger_transaction_signature, challenger_xonly_pubkey))
PAY_SLASH_BOUNTY_AND_BURN(challenger_xonly_pubkey)
```

`PATH_PREFIX` compares hash, sum, and `is_left` for every enabled slot of the earlier path.

### 7.8 `L7 slash_rotation_violation`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == PENDING || old.state_tag == CHALLENGED
       || old.state_tag == WITHDRAWAL_DELAY)

ASSERT(VERIFY_BONDED_LIFECYCLE_STATEMENT(
    manifest_a, NETWORK, old.bond_id, old.program_hash, old.mint_pubkey
))
ASSERT(manifest_a.keyset.keyset_id == baseline.keyset_id)
ASSERT(manifest_a.epoch.epoch_index >= baseline.birth_epoch)
ASSERT(VERIFY_EPOCH_REFERENCE(baseline_epoch, baseline_reference, old))
ASSERT(VERIFY_KEYSET_OPENING(
    baseline_epoch,
    baseline,
    baseline_keyset_opening,
    HASH_EPOCH(baseline_epoch)
))

if violation_kind == REACTIVATION:
    ASSERT(VERIFY_BONDED_LIFECYCLE_STATEMENT(
        manifest_b, NETWORK, old.bond_id, old.program_hash, old.mint_pubkey
    ))
    ASSERT(manifest_b.epoch.epoch_index >= baseline.birth_epoch)
    ASSERT(manifest_a.epoch.epoch_index < manifest_b.epoch.epoch_index)
    ASSERT(!manifest_a.keyset.active && manifest_b.keyset.active)

else if violation_kind == ISSUANCE_AFTER_LOCK:
    ASSERT(VERIFY_BONDED_LIFECYCLE_STATEMENT(
        manifest_b, NETWORK, old.bond_id, old.program_hash, old.mint_pubkey
    ))
    ASSERT(manifest_a.epoch.epoch_index < manifest_b.epoch.epoch_index)
    ASSERT(!manifest_a.keyset.active)
    ASSERT(
        manifest_a.keyset.issued_tree != manifest_b.keyset.issued_tree
    )

else if violation_kind == DEACTIVATION_OVERRUN:
    ASSERT(manifest_a.keyset.active)
    ASSERT(
        manifest_a.epoch.epoch_index
        >= manifest_a.keyset.deactivation_epoch
    )

else if violation_kind == DECLARATION_DRIFT:
    ASSERT(VERIFY_BONDED_LIFECYCLE_STATEMENT(
        manifest_b, NETWORK, old.bond_id, old.program_hash, old.mint_pubkey
    ))
    ASSERT(manifest_a.epoch.epoch_index != manifest_b.epoch.epoch_index)
    ASSERT(
        manifest_a.keyset.unit != manifest_b.keyset.unit
        || manifest_a.keyset.deactivation_epoch
           != manifest_b.keyset.deactivation_epoch
    )

else:
    FAIL

ASSERT(manifest_a.epoch.epoch_index >= baseline.birth_epoch)
if manifest_b != NONE:
    ASSERT(manifest_b.keyset.keyset_id == manifest_a.keyset.keyset_id)
    ASSERT(manifest_b.epoch.epoch_index >= baseline.birth_epoch)

ASSERT(CHECKSIG(challenger_transaction_signature, challenger_xonly_pubkey))
PAY_SLASH_BOUNTY_AND_BURN(challenger_xonly_pubkey)
```

`VERIFY_BONDED_LIFECYCLE_STATEMENT` verifies a master signature over the canonical NUT-388 manifest plus `NETWORK`, `bond_id`, `program_hash`, `keyset_id`, and the authenticated `birth_epoch`. For two-statement variants, `manifest_b.keyset.keyset_id` MUST equal `manifest_a.keyset.keyset_id`. Both epoch indices MUST be at least the baseline birth epoch. At least one non-violating lifecycle baseline for that keyset MUST be authenticated by bond history; the violating signed statement need not have passed `publish_epoch`.

### 7.9 `L8 begin_closing`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)
ASSERT(old.closing_epoch == null)
ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))
ASSERT(HASH_EPOCH(active_epoch) == old.active_epoch_hash)

new.state_tag = ACTIVE
new.closing_epoch = active_epoch.epoch_index
VERIFY_SUCCESSOR(old, new, BEGIN_CLOSING_TRANSITION)
```

### 7.10 `L9 enter_withdrawal_delay`

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == ACTIVE)
ASSERT(old.closing_epoch != null)
ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))
ASSERT(HASH_EPOCH(active_epoch) == old.active_epoch_hash)
VERIFY_EPOCH(
    active_epoch,
    active_keysets,
    active_signatures,
    old.mint_pubkey,
    old.unit, NETWORK, old.bond_id, old.program_hash
)

for i in 0 .. MAX_KEYSETS-1:
    if i < len(active_keysets):
        keyset = active_keysets[i]
        if keyset.unit != old.unit:
            continue
        ASSERT(!keyset.active)
        ASSERT(
            active_epoch.epoch_index
            >= keyset.redemption_end_epoch
        )

new.state_tag = WITHDRAWAL_DELAY
new.mint_withdrawal_xonly_pubkey = witness.mint_withdrawal_xonly_pubkey

VERIFY_SUCCESSOR(old, new, ENTER_DELAY_TRANSITION)
```

Residual `outstanding_balance` is permitted and remains committed as expired liability.

### 7.11 `L10 cancel_withdrawal_delay_with_challenge`

This leaf is the withdrawal-delay equivalent of `L2`. It verifies the leaf-challenge opening predicate and creates `CHALLENGED`. After a successful refutation, the state returns to closing `ACTIVE`; the mint must enter a new full withdrawal delay.

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == WITHDRAWAL_DELAY)
VERIFY_CHALLENGE_BOND(challenge_bond_input, CURRENT_BOND_OUTPOINT)
ASSERT(old.closing_epoch != null)

challenge_hash = HASH_CHALLENGE(leaf_challenge)
ASSERT(target_epoch.epoch_index == leaf_challenge.target_epoch)
ASSERT(VERIFY_KEYSET_OPENING(
    target_epoch,
    target_keyset,
    target_keyset_opening,
    old.active_epoch_hash
))
ASSERT(target_keyset.keyset_id == leaf_challenge.keyset_id)

ASSERT(VERIFY_AMOUNT_KEY(
    old.unit,
    leaf_challenge.value,
    leaf_challenge.amount_pubkey_compressed,
    amount_key_proof,
    target_keyset.amount_keys_root
))

VERIFY_RECEIPT(
    leaf_challenge.receipt_signature,
    leaf_challenge.leaf_type,
    leaf_challenge.item,
    leaf_challenge.value,
    leaf_challenge.receipt_target_epoch,
    XONLY_FROM_COMPRESSED(leaf_challenge.amount_pubkey_compressed)
)

ASSERT(leaf_challenge.target_epoch >= leaf_challenge.receipt_target_epoch)
ASSERT(len(witness.challenger_xonly_pubkey) == 32)
ASSERT(CHECKSIG(
    challenger_transaction_signature,
    witness.challenger_xonly_pubkey
))

new.state_tag = CHALLENGED
new.active_epoch_hash = old.active_epoch_hash
new.disputed_epoch_hash = old.active_epoch_hash
new.challenge_type = LEAF_OMISSION_OR_MISMATCH
new.challenge_hash = challenge_hash
new.challenger_xonly_pubkey = witness.challenger_xonly_pubkey
new.challenge_origin = WITHDRAWAL_DELAY

VERIFY_SUCCESSOR(old, new, OPEN_CHALLENGE_TRANSITION)
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

### 7.13 `L12 initialize_bond`

The funding transaction creates an `UNINITIALIZED` covenant output. This is its only valid spend path.

```text
VERIFY_CURRENT_STATE(old)
ASSERT(old.state_tag == UNINITIALIZED)
ASSERT(VALID_UNIT(old.unit))
ASSERT(CHECKSIG(mint_transaction_signature, old.mint_pubkey))
ASSERT(old.bond_id == SHA256(
    "Cashu_Bonded_PoL_Bond_Id_v1"
    || old.mint_pubkey || old.genesis_nonce
))

VERIFY_EPOCH(
    initial_epoch,
    initial_keysets,
    initial_signatures,
    old.mint_pubkey,
    old.unit, NETWORK, old.bond_id, old.program_hash
)

for i in 0 .. MAX_KEYSETS-1:
    if i < len(initial_keysets):
        keyset = initial_keysets[i]
        if keyset.unit != old.unit:
            ASSERT(IS_EMPTY(initial_amount_key_sets[i]))
            continue
        ASSERT(keyset.receipt_signature_scheme == BIP340_SCHEME)
        ASSERT(keyset.birth_epoch == initial_epoch.epoch_index)
        ASSERT(VERIFY_AMOUNT_KEYS_ROOT(
            old.unit,
            initial_amount_key_sets[i],
            keyset.amount_keys_root
        ))
        ASSERT(initial_epoch.epoch_index < keyset.deactivation_epoch)
        ASSERT(
            keyset.deactivation_epoch
            < keyset.redemption_end_epoch
        )

new.state_tag = ACTIVE
new.active_epoch_hash = HASH_EPOCH(initial_epoch)
new.closing_epoch = null
new.epoch_history_mmr_root = EMPTY_HISTORY_ROOT
new.epoch_history_mmr_size = 0

VERIFY_SUCCESSOR(old, new, INITIALIZE_TRANSITION)
```

Existing off-chain keysets are treated as born into the bond at `initial_epoch`. Wallets and watchers MUST verify their pre-bond histories before recognizing the bond.

---

## 8. Transaction Output Rules

Every transition uses one of two output templates.

### 8.1 Recursive Transition

```text
output[0].value     == bond_input.value
output[0].script    == BondProgram(new_state_hash)
SUM_VALUES(other_outputs) <= SUM_VALUES(external_inputs)
```

The implementation MUST inspect every output and require that exactly one output has `BondProgram(new_state_hash)`. Exact equality and uniqueness require the committed introspection profile; they do not follow from BIP-443's residual minimum.

### 8.2 Terminal Slash

```text
output[0].value     == CHALLENGER_BOUNTY
output[0].script    == P2TR(committed_recipient_key)
output[1].value     == bond_input.value - CHALLENGER_BOUNTY
output[1].script    == CANONICAL_UNSPENDABLE_SCRIPT
SUM_VALUES(outputs[2:]) <= SUM_VALUES(external_inputs)
```

Every equality and the absence of another matching successor or terminal output is checked with exact complete-output introspection. All transaction fees are exogenous.

---

## 9. Deployment and Resource Gate

No deployment is conforming until its activated consensus profile assigns exact semantics and encodings to every operation in Sections 2.1 and 2.2, including uint64 division/modulo and bit operations. The compiler MUST statically unroll every bounded loop and emit a machine-verifiable report containing, for every Tapleaf:

```text
ResourceReport {
    script_bytes: uint64,
    maximum_witness_bytes: uint64,
    maximum_stack_items: uint64,
    maximum_stack_element_bytes: uint64,
    maximum_validation_cost: uint64,
    maximum_sigchecks: uint64
}
```

The deployment is invalid if any maximum exceeds the limits of its committed `opcode_profile_hash`. The compiler MUST hash the Tapleaf templates with the `PROGRAM_HASH` literal replaced by the canonical placeholder, together with leaf versions, tree layout, resource report, and compiler version, into `verifier_program_hash`. It then instantiates the resulting `program_hash` in every template. Consequently changing `MAX_KEYSETS`, `MAX_AMOUNT_KEYS`, a proof height, or an opcode implementation creates a different program without a circular hash definition.

The current document specifies logical scripts, not deployable Bitcoin bytecode. It does not claim that useful parameter values fit existing Bitcoin resource limits.

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
