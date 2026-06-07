# NUT-CTF-split-merge Test Vectors

These test vectors provide reference data for implementing the Conditional Token Framework (CTF) convert operation (split, merge, recombine, conversion) with per-outcome collection keysets. All values are hex-encoded for reproducibility. Split and merge are the `"*"`-inputs and `"*"`-outputs special cases of `POST /v1/ctf/convert`.

## Condition ID Calculation

The condition ID is computed as `tagged_hash("Cashu_condition_id", sorted_oracle_pubkeys || event_id || outcome_count)` where `tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)`. The condition ID is independent of requested outcome keysets.

### Test 1: Binary condition ID

```shell
# Condition parameters
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event_id:           "btc_price_100k_2025"
event_id_utf8:      6274635f70726963655f3130306b5f32303235
outcome_count:      2
outcome_count_byte: 02

# Tagged hash computation
tag:                "Cashu_condition_id"
tag_utf8:           43617368755f636f6e646974696f6e5f6964
tag_hash:           SHA256(tag_utf8)

# Preimage (message for tagged hash) — no outcome keyset identifiers
msg_hex:            9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce06274635f70726963655f3130306b5f3230323502

# Condition ID = SHA256(tag_hash || tag_hash || msg)
```

### Test 2: Three-outcome condition ID

```shell
# Condition parameters
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event_id:           "election_2024_winner"
event_id_utf8:      656c656374696f6e5f323032345f77696e6e6572
outcome_count:      3
outcome_count_byte: 03

# Condition ID = tagged_hash("Cashu_condition_id", oracle_pubkey || event_id || outcome_count)
# No outcome keyset identifiers — condition_id is keyset-independent
```

### Test 3: Condition ID with special characters in question

```shell
# Condition parameters
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
event_id:           "Will ETH/USD > $5000?"
event_id_utf8:      57696c6c204554482f555344203e2024353030303f
outcome_count:      2
outcome_count_byte: 02

# Condition ID uses tagged_hash (includes space, /, >, $ characters in event_id)
# No outcome keyset identifiers in condition_id
```

## Condition Registration

### Test 4: Register condition with default keysets (binary)

```shell
# Step 1: Register condition (POST /v1/conditions)
register_request:   {
  "threshold": 1,
  "tags": [["description", "Will BTC reach $100k?"]],
  "announcements": ["<hex_encoded_tlv>"],
  "collateral": "sat"
}

register_response:  {
  "condition_id": "<tagged_hash_result>",
  "keysets": {
    "YES": "00abc123def456",
    "NO": "00def789abc012"
  }
}

# These keyset IDs are used in all subsequent split/merge/trade operations
```

### Test 5: Three-outcome condition with one-vs-rest keysets

```shell
# Step 1: Register condition
register_request:   {
  "threshold": 1,
  "tags": [["description", "Election winner"]],
  "announcements": ["<hex_encoded_tlv>"],
  "collateral": "sat"
}

register_response:  {
  "condition_id": "<tagged_hash_result>",
  "keysets": {
    "CANDIDATE_A": "00aa11bb22cc33dd",
    "CANDIDATE_B": "00bb22cc33dd44ee",
    "CANDIDATE_C": "00cc33dd44ee55ff",
    "CANDIDATE_A|CANDIDATE_B": "00dd44ee55ff6600",
    "CANDIDATE_A|CANDIDATE_C": "00ee55ff66007711",
    "CANDIDATE_B|CANDIDATE_C": "00ff660077118822"
  }
}
```

## Convert Operation — Split

A split is a `POST /v1/ctf/convert` whose inputs are collateral under the reserved key `"*"`.

### Test 6: Binary condition split request

```shell
# Condition parameters
condition_id:          <tagged_hash_result>

# Input (100 sats collateral using regular keyset, fee F = 0)
input_amount:       100
input_keyset_id:    009a1f293253e41e  # regular keyset

# Output keyset IDs from condition preparation
yes_keyset_id:      00abc123def456
no_keyset_id:       00def789abc012

# Convert (split) request JSON — POST /v1/ctf/convert
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "*": [
      {"amount": 64, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."},
      {"amount": 32, "id": "009a1f293253e41e", "secret": "secret2", "C": "02..."},
      {"amount": 4, "id": "009a1f293253e41e", "secret": "secret3", "C": "02..."}
    ]
  },
  "outputs": {
    "YES": [
      {"amount": 64, "id": "00abc123def456", "B_": "03..."},
      {"amount": 32, "id": "00abc123def456", "B_": "03..."},
      {"amount": 4, "id": "00abc123def456", "B_": "03..."}
    ],
    "NO": [
      {"amount": 64, "id": "00def789abc012", "B_": "03..."},
      {"amount": 32, "id": "00def789abc012", "B_": "03..."},
      {"amount": 4, "id": "00def789abc012", "B_": "03..."}
    ]
  }
}

# Each outcome collection's BlindedMessages use the outcome collection-specific keyset ID
```

### Test 7: Successful split response

```shell
# Response with signatures for each outcome collection (using conditional keyset IDs)
response_json:      {
  "signatures": {
    "YES": [
      {"amount": 64, "id": "00abc123def456", "C_": "02...sig1..."},
      {"amount": 32, "id": "00abc123def456", "C_": "02...sig2..."},
      {"amount": 4, "id": "00abc123def456", "C_": "02...sig3..."}
    ],
    "NO": [
      {"amount": 64, "id": "00def789abc012", "C_": "02...sig4..."},
      {"amount": 32, "id": "00def789abc012", "C_": "02...sig5..."},
      {"amount": 4, "id": "00def789abc012", "C_": "02...sig6..."}
    ]
  }
}

# Each BlindSignature uses the outcome collection-specific keyset ID
```

## Trading (Same-Keyset Swap)

### Test 8: Trade swap request

```shell
# Bob receives YES tokens from Alice and swaps at mint
# All inputs and outputs use same conditional keyset
swap_json:          {
  "inputs": [
    {"amount": 64, "id": "00abc123def456", "secret": "received_secret_1", "C": "02..."},
    {"amount": 32, "id": "00abc123def456", "secret": "received_secret_2", "C": "02..."}
  ],
  "outputs": [
    {"amount": 64, "id": "00abc123def456", "B_": "03..."},
    {"amount": 32, "id": "00abc123def456", "B_": "03..."}
  ]
}

# Standard NUT-03 swap within same keyset
# No oracle witness required
# Mint verifies proofs and signs outputs with YES conditional keyset keys
result:             PASS
```

## Convert Operation — Merge

A merge is a `POST /v1/ctf/convert` whose outputs are collateral under the reserved key `"*"`.

### Test 9: Binary condition merge request

```shell
# Condition parameters
condition_id:          <tagged_hash_result>

# Inputs (100 sats of each outcome collection using conditional keysets, fee F = 0)
# Outputs are collateral under "*"
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "YES": [
      {"amount": 64, "id": "00abc123def456", "secret": "yes_secret_1", "C": "02..."},
      {"amount": 32, "id": "00abc123def456", "secret": "yes_secret_2", "C": "02..."},
      {"amount": 4, "id": "00abc123def456", "secret": "yes_secret_3", "C": "02..."}
    ],
    "NO": [
      {"amount": 64, "id": "00def789abc012", "secret": "no_secret_1", "C": "02..."},
      {"amount": 32, "id": "00def789abc012", "secret": "no_secret_2", "C": "02..."},
      {"amount": 4, "id": "00def789abc012", "secret": "no_secret_3", "C": "02..."}
    ]
  },
  "outputs": {
    "*": [
      {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
    ]
  }
}

# Input proofs use conditional keysets, output BlindedMessages are collateral ("*")
# No oracle witness required (complete set cancels out)
output_total:       100
```

### Test 10: Successful merge response

```shell
# Response with signatures for collateral outputs under "*" (regular keyset)
response_json:      {
  "signatures": {
    "*": [
      {"amount": 64, "id": "009a1f293253e41e", "C_": "02...sig1..."},
      {"amount": 32, "id": "009a1f293253e41e", "C_": "02...sig2..."},
      {"amount": 4, "id": "009a1f293253e41e", "C_": "02...sig3..."}
    ]
  }
}

# Resulting proofs use regular keyset (not condition-specific)
```

## Redemption (Cross-Keyset Swap)

### Test 11: Winner redemption via POST /v1/redeem_outcome

```shell
# Oracle attests "YES" won
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# YES holder redeems conditional keyset tokens for regular keyset tokens
redeem_json:        {
  "inputs": [
    {
      "amount": 64,
      "id": "00abc123def456",
      "secret": "random_secret_yes_1",
      "C": "02...",
      "witness": "{\"oracle_sigs\":[{\"oracle_pubkey\":\"9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0\",\"oracle_sig\":\"a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890\"}]}"
    }
  ],
  "outputs": [
    {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."}
  ]
}

# Input: YES conditional keyset (00abc123def456) with oracle witness
# Output: regular keyset (009a1f293253e41e)
# Mint verifies oracle signature per NUT-CTF
result:             PASS
```

### Test 12: Loser cannot redeem

```shell
# Oracle attests "YES" won, but user holds NO tokens
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# NO holder attempts to redeem via POST /v1/redeem_outcome
redeem_json:        {
  "inputs": [
    {
      "amount": 64,
      "id": "00def789abc012",
      "secret": "random_secret_no_1",
      "C": "02...",
      "witness": "{\"oracle_sigs\":[{\"oracle_pubkey\":\"9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0\",\"oracle_sig\":\"a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890\"}]}"
    }
  ],
  "outputs": [
    {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."}
  ]
}

# Verification fails: oracle signed "YES" but input keyset is for "NO"
error_code:         13015
error_message:      "Oracle has not attested to this outcome collection"
```

## Error Cases

### Test 13: Convert (split) payoff mismatch

```shell
# Input total != output total for some outcome (out(YES) != in(YES) - F)
input_total:        100
output_yes_total:   90   # Mismatch!
output_no_total:    100

error_code:         13041
error_message:      "Convert payoff/fee violation"
```

### Test 14: Missing outcome collection in outputs

```shell
# Binary condition but only YES outputs provided
# in(NO) = 100, out(NO) = 0  ->  out(NO) != in(NO) - F
outcome_collections:  ["YES", "NO"]
outputs_provided:   ["YES"]  # Missing NO!

error_code:         13041
error_message:      "Convert payoff/fee violation"
```

### Test 15: Invalid condition ID

```shell
# Condition ID too short
condition_id:          3a7f8d2e1b4c5a6f  # Only 16 hex chars (8 bytes)

error_code:         13020
error_message:      "Invalid condition ID"
```

### Test 16: Condition not found

```shell
# Valid format but non-existent condition
condition_id:          ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

error_code:         13021
error_message:      "Condition not found"
```

### Test 17: Unequal outcome collection amounts

```shell
# Different amounts for different outcomes (out(NO) != in(NO) - F)
input_total:        100
output_yes_total:   100
output_no_total:    50   # Different!

error_code:         13041
error_message:      "Convert payoff/fee violation"
```

### Test 18: Convert (merge) payoff mismatch

```shell
# Input amounts don't match across outcomes (in(YES) != in(NO))
input_yes_total:    100
input_no_total:     80   # Mismatch!

error_code:         13041
error_message:      "Convert payoff/fee violation"
```

### Test 19: Missing outcome collection in merge inputs

```shell
# Binary condition but only YES inputs provided
# in(NO) = 0 but out(NO) (from "*") = output_total  ->  violation
outcome_collections:  ["YES", "NO"]
inputs_provided:    ["YES"]  # Missing NO!

error_code:         13041
error_message:      "Convert payoff/fee violation"
```

### Test 20: Output amount mismatch in merge

```shell
# Collateral output total doesn't equal per-outcome input total
input_yes_total:    100
input_no_total:     100
output_total:       50   # Should be 100 (F = 0)!

error_code:         13041
error_message:      "Convert payoff/fee violation"
```

## Multi-Oracle Condition ID

### Test 21: Multi-oracle condition ID calculation

```shell
# Condition parameters (2-of-3 threshold)
oracle_pubkeys:     [
  "9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0",
  "79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
  "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"
]
sorted_pubkeys:     [
  "79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
  "9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0",
  "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"
]
event_id:           "btc_price_100k_2025"
outcome_count:      2

# condition_id = tagged_hash("Cashu_condition_id", sorted_pubkeys || event_id || outcome_count)
# No outcome keyset identifiers — condition_id is keyset-independent
```

## Outcome Collections

### Test 22: Split with outcome collections (3-outcome condition)

```shell
# Condition with 3 outcomes, registered with root outcome collection keysets
outcomes:           ["ALICE", "BOB", "CAROL"]

# Condition registration returned these keysets
keysets:
  "ALICE|BOB":      00aabb11cc22dd33
  "CAROL":          00ccdd44ee55ff66

# Convert (split) request with outcome collections
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "*": [
      {"amount": 100, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."}
    ]
  },
  "outputs": {
    "ALICE|BOB": [
      {"amount": 64, "id": "00aabb11cc22dd33", "B_": "03..."},
      {"amount": 32, "id": "00aabb11cc22dd33", "B_": "03..."},
      {"amount": 4, "id": "00aabb11cc22dd33", "B_": "03..."}
    ],
    "CAROL": [
      {"amount": 64, "id": "00ccdd44ee55ff66", "B_": "03..."},
      {"amount": 32, "id": "00ccdd44ee55ff66", "B_": "03..."},
      {"amount": 4, "id": "00ccdd44ee55ff66", "B_": "03..."}
    ]
  }
}

# Payoff check
payoff_valid:       true (ALICE|BOB and CAROL cover all outcomes, disjoint)
```

### Test 23: Outcome collection redemption (oracle signs covered outcome)

```shell
# Token uses ALICE|BOB conditional keyset
keyset_id:          00aabb11cc22dd33
outcome_collection_outcomes: ["ALICE", "BOB"]

# Oracle signs "ALICE"
oracle_attested:    "ALICE"
attested_in_set:    true

# Redemption succeeds (swap to regular keyset with witness)
can_redeem:         true
```

### Test 24: Outcome collection redemption (oracle signs uncovered outcome)

```shell
# Token uses ALICE|BOB conditional keyset
keyset_id:          00aabb11cc22dd33
outcome_collection_outcomes: ["ALICE", "BOB"]

# Oracle signs "CAROL"
oracle_attested:    "CAROL"
attested_in_set:    false

# Redemption fails
can_redeem:         false
error_code:         13015
error_message:      "Oracle has not attested to this outcome collection"
```

### Test 25: Duplicate canonical outcome collection error

```shell
# Invalid request - duplicate after canonicalization
outcome_collections: ["ALICE|BOB", "BOB|ALICE"]
condition_outcomes:    ["ALICE", "BOB", "CAROL"]

# Validation fails
error_code:         13037
error_message:      "Duplicate canonical outcome collection"
```

### Test 26: Unknown outcome collection member error

```shell
# Invalid request - DAVE is not in the oracle outcome list
outcome_collections: ["ALICE|DAVE"]
condition_outcomes:    ["ALICE", "BOB", "CAROL"]

# Validation fails
error_code:         13038
error_message:      "Unknown outcome in outcome collection"
```

### Test 27: Merge with outcome collections

```shell
# Merge request with outcome collections
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "ALICE|BOB": [
      {"amount": 100, "id": "00aabb11cc22dd33", "secret": "ab_secret_1", "C": "02..."}
    ],
    "CAROL": [
      {"amount": 100, "id": "00ccdd44ee55ff66", "secret": "carol_secret_1", "C": "02..."}
    ]
  },
  "outputs": {
    "*": [
      {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
    ]
  }
}

# Input proofs use outcome collection keysets, outputs are collateral under "*"
# Valid merge - outcome collections form a complete disjoint cover
merge_result:       SUCCESS
```

### Test 28: Escaped pipe character in outcome name

```shell
# Outcome name containing pipe character
outcome_name:       "A|B"
escaped_name:       "A\\|B"

# This is a single outcome, not an outcome collection
parsed_outcome:     ["A|B"]  # Single outcome with literal pipe
```

## Combinatorial Condition Tests

### Test 29: Outcome collection ID computation

```shell
# Outcome collection ID computation (NUT-CTF algorithm)
# outcome_collection_id(parent, condition_id, outcome_collection_string):
#   h = tagged_hash("Cashu_outcome_collection_id", condition_id || outcome_collection_string_bytes)
#   P = hash_to_curve(h)
#   If parent is identity: return x_only(P)
#   Else: return x_only(EC_add(lift_x(parent), P))

# Root condition (parent = identity/zero)
parent_collection_id: 0000000000000000000000000000000000000000000000000000000000000000
condition_id_A:        a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd
outcome_A:        "YES"
outcome_A_utf8:   594553

# Step 1: h = tagged_hash("Cashu_outcome_collection_id", condition_id_A || "YES")
# Step 2: P_A = hash_to_curve(h)
# Step 3: outcome_collection_id_A = x_only(P_A)  (parent is identity)
```

### Test 30: Combinatorial condition commutativity

```shell
# Two conditions
election_condition_id:  a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd
btc_price_condition_id:  b2c3d4e5f67890123456789012345678901234567890123456789012345678ef

# Path 1: Election first, then BTC price
# Step 1a: oc_A = outcome_collection_id(0, election_condition_id, "PARTY_A")
# Step 1b: oc_AB = outcome_collection_id(oc_A, btc_price_condition_id, "UP")

# Path 2: BTC price first, then election
# Step 2a: oc_B = outcome_collection_id(0, btc_price_condition_id, "UP")
# Step 2b: oc_BA = outcome_collection_id(oc_B, election_condition_id, "PARTY_A")

# Commutativity: oc_AB == oc_BA
# This holds because EC point addition is commutative:
#   P_election_A + P_btc_UP = P_btc_UP + P_election_A
```

### Test 31: Nested parent collection rejected

```shell
# Step 1a: Register root election condition (POST /v1/conditions)
root_condition_request: {
  "threshold": 1,
  "tags": [["description", "Election winner"]],
  "announcements": ["<hex_encoded_tlv>"],
  "collateral": "sat"
}

root_condition_response: {
  "condition_id": "<election_condition_id>",
  "keysets": {
    "PARTY_A": "00aa11bb22cc33dd",
    "PARTY_B": "00bb22cc33dd44ee"
  }
}

# Nested/combinatorial construction is out of scope for this version.
convert_request: {
  "condition_id": "<election_condition_id>",
  "parent_collection_id": "<x_only_pubkey_of_PARTY_A>"
}

error_code: 13041
```

### Test 32: Nested condition split rejected

```shell
# Non-zero parent_collection_id is reserved for future nested support.
request_json:       {
  "condition_id": "<btc_price_condition_id>",
  "parent_collection_id": "<x_only_pubkey_of_PARTY_A>",
  "inputs": {"*": [{"amount": 100, "id": "009a1f293253e41e", "secret": "secret", "C": "02..."}]},
  "outputs": {"UP": [{"amount": 99, "id": "00cc33dd44ee55ff", "B_": "03..."}]}
}

error_code:         13041
```

### Test 33: Nested condition merge rejected

```shell
request_json:       {
  "condition_id": "<btc_price_condition_id>",
  "parent_collection_id": "<x_only_pubkey_of_PARTY_A>",
  "inputs": {"UP": [{"amount": 100, "id": "00cc33dd44ee55ff", "secret": "up_secret_1", "C": "02..."}]},
  "outputs": {"*": [{"amount": 99, "id": "009a1f293253e41e", "B_": "03..."}]}
}

error_code:         13041
```

### Test 34: Maximum depth unsupported

```shell
# This version has no max_depth setting; all non-root parent_collection_id values are rejected.
error_code:         13041
error_message:      "Convert payoff/fee violation"
```

## Complete Flow Example

### Test 35: End-to-end condition lifecycle

```shell
# Step 1a: Register condition (POST /v1/conditions)
condition_id:          <tagged_hash_result>

# Step 1b: Keysets returned by condition registration
keysets:
  YES:              00abc123def456
  NO:               00def789abc012

# Step 2: Alice splits 100 sats
alice_input:        100 sats (regular keyset 009a1f293253e41e)
alice_receives:     100 sats YES tokens (keyset 00abc123def456) + 100 sats NO tokens (keyset 00def789abc012)

# Step 3: Alice sells NO tokens to Bob for 40 sats
# Bob swaps at mint: input NO keyset -> output NO keyset (standard NUT-03 swap)

# Step 4: Oracle attests "YES"
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
attested_outcome:   "YES"
oracle_sig:         <valid_signature_on_YES>

# Step 5: Alice redeems YES tokens
# Redeem via POST /v1/redeem_outcome: input YES keyset (00abc123def456) + witness -> output regular keyset (009a1f293253e41e)
alice_redeems:      100 sats YES tokens
alice_receives:     100 sats regular ecash

# Step 6: Bob cannot redeem NO tokens
# Redeem via POST /v1/redeem_outcome: input NO keyset (00def789abc012) + witness -> FAILS
bob_attempts:       100 sats NO tokens
bob_result:         FAIL (oracle signed YES, not NO)

# Net result:
# - Alice: started with 100 sats, now has 100 sats + 40 sats from sale = 140 sats
# - Bob: paid 40 sats for worthless NO tokens = -40 sats
```

## Convert — Recombine and Conversion

### Test 36: Recombine (floor 0, fee paid as collateral)

```shell
# Condition Omega = {A, B, C, D}; registered collections include A, B|C, A|B|C
# Holder of A(1) + B|C(1) recombines into A|B|C(1). Fee F = 1, so the holder
# adds 1 sat of collateral under "*" to satisfy in(o) >= F on every outcome.

request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "*":   [{"amount": 1, "id": "009a1f293253e41e", "secret": "c1", "C": "02..."}],
    "A":   [{"amount": 1, "id": "00a000...",         "secret": "a1", "C": "02..."}],
    "B|C": [{"amount": 1, "id": "00bc00...",         "secret": "bc1", "C": "02..."}]
  },
  "outputs": {
    "A|B|C": [{"amount": 1, "id": "00abc0...", "B_": "03..."}]
  }
}

# Per-outcome: in = (A:2, B:2, C:2, D:1), out = (A:1, B:1, C:1, D:0)
# out(o) == in(o) - 1 for every o. Mint retains 1 on every outcome.
result:             PASS
```

### Test 37: Conversion (negative-risk style, collateral on output)

```shell
# Condition Omega = {A, B, C, D}; registered collections A|B|C, B|C|D, B|C. Fee F = 1.
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "A|B|C": [{"amount": 100, "id": "00abc0...", "secret": "s1", "C": "02..."}],
    "B|C|D": [{"amount": 100, "id": "00bcd0...", "secret": "s2", "C": "02..."}]
  },
  "outputs": {
    "*":   [{"amount": 99,  "id": "009a1f293253e41e", "B_": "03..."}],
    "B|C": [{"amount": 100, "id": "00bc00...",         "B_": "03..."}]
  }
}

# Per-outcome: in = (A:100, B:200, C:200, D:100), out = (A:99, B:199, C:199, D:99)
# out(o) == in(o) - 1 for every o. 99 sats withdrawn as spendable collateral, no witness.
result:             PASS
```

### Test 38: Convert fee not covered on some outcome

```shell
# Pure recombine A(1) + B|C(1) -> A|B|C(1) WITHOUT adding collateral, F = 1.
# in = (A:1, B:1, C:1, D:0); in(D) = 0 < F  ->  rejected.
error_code:         13041
error_message:      "Convert payoff/fee violation"
```

### Test 39: Convert after attestation recorded

```shell
# Oracle attestation already recorded for the condition.
error_code:         13042
error_message:      "Convert not permitted for this condition"
```

### Test 40: Full-set outcome collection rejected at registration

```shell
# Attempt to register an outcome collection that covers all outcomes
outcome_collections: ["ALICE|BOB|CAROL"]
error_code:         13043
error_message:      "Full-set or reserved outcome collection"
```

[NUT-CTF-split-merge]: ../CTF-split-merge.md
[NUT-CTF]: ../CTF.md
