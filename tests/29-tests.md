# NUT-29 Test Vectors

These test vectors provide reference data for implementing the Conditional Token Framework (CTF) with per-outcome collection keysets. All values are hex-encoded for reproducibility.

## Condition ID Calculation

The condition ID is computed as `tagged_hash("Cashu_condition_id", sorted_oracle_pubkeys || sorted_event_id || outcome_count || sorted_partition_keys)` where `tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)`.

### Test 1: Binary condition ID (default partition)

```shell
# Condition parameters
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event_id:           "btc_price_100k_2025"
event_id_utf8:      6274635f70726963655f3130306b5f32303235
outcome_count:      2
outcome_count_byte: 02

# Default partition (individual outcomes, sorted)
partition_keys:     ["NO", "YES"]  # sorted lexicographically
partition_utf8:     4e4f00594553  # "NO" + 0x00 + "YES"

# Tagged hash computation
tag:                "Cashu_condition_id"
tag_utf8:           43617368755f636f6e646974696f6e5f6964
tag_hash:           SHA256(tag_utf8)

# Preimage (message for tagged hash)
msg_hex:            9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce06274635f70726963655f3130306b5f32303235024e4f00594553

# Condition ID = SHA256(tag_hash || tag_hash || msg)
```

### Test 2: Three-outcome condition ID (default partition)

```shell
# Condition parameters
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event_id:           "election_2024_winner"
event_id_utf8:      656c656374696f6e5f323032345f77696e6e6572
outcome_count:      3
outcome_count_byte: 03

# Default partition (individual outcomes, sorted)
partition_keys:     ["CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C"]  # sorted
partition_utf8:     43414e4449444154455f410043414e4449444154455f420043414e4449444154455f43
#                   "CANDIDATE_A" + 0x00 + "CANDIDATE_B" + 0x00 + "CANDIDATE_C"

# Condition ID = tagged_hash("Cashu_condition_id", oracle_pubkey || event_id || outcome_count || partition)
```

### Test 3: Condition ID with special characters in question

```shell
# Condition parameters
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
event_id:           "Will ETH/USD > $5000?"
event_id_utf8:      57696c6c204554482f555344203e2024353030303f
outcome_count:      2
outcome_count_byte: 02

# Default partition (individual outcomes, sorted)
partition_keys:     ["NO", "YES"]
partition_utf8:     4e4f00594553  # "NO" + 0x00 + "YES"

# Condition ID uses tagged_hash (includes space, /, >, $ characters in event_id)
```

## Condition Preparation

### Test 4: Prepare condition response with keysets

```shell
# Prepare condition request (POST /v1/conditions)
# Response includes per-outcome collection keyset IDs
request_json:       {
  "collateral": "sat",
  "threshold": 1,
  "description": "Will BTC reach $100k?",
  "announcements": ["<hex_encoded_tlv>"]
}

response_json:      {
  "condition_id": "<tagged_hash_result>",
  "keysets": {
    "YES": "00abc123def456",
    "NO": "00def789abc012"
  }
}

# These keyset IDs are used in all subsequent split/merge/trade operations
```

### Test 5: Three-outcome condition preparation

```shell
# Condition with 3 outcomes
request_json:       {
  "collateral": "sat",
  "threshold": 1,
  "description": "Election winner",
  "announcements": ["<hex_encoded_tlv>"],
  "partition": ["CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C"]
}

response_json:      {
  "condition_id": "<tagged_hash_result>",
  "keysets": {
    "CANDIDATE_A": "00aa11bb22cc33dd",
    "CANDIDATE_B": "00bb22cc33dd44ee",
    "CANDIDATE_C": "00cc33dd44ee55ff"
  }
}
```

## Split Operation

### Test 6: Binary condition split request

```shell
# Condition parameters
condition_id:          <tagged_hash_result>

# Input (100 sats collateral using regular keyset)
input_amount:       100
input_keyset_id:    009a1f293253e41e  # regular keyset

# Output keyset IDs from condition preparation
yes_keyset_id:      00abc123def456
no_keyset_id:       00def789abc012

# Split request JSON
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": [
    {"amount": 64, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."},
    {"amount": 32, "id": "009a1f293253e41e", "secret": "secret2", "C": "02..."},
    {"amount": 4, "id": "009a1f293253e41e", "secret": "secret3", "C": "02..."}
  ],
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

## Merge Operation

### Test 9: Binary condition merge request

```shell
# Condition parameters
condition_id:          <tagged_hash_result>

# Inputs (100 sats of each outcome collection using conditional keysets)
# Outputs use regular keyset
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
  "outputs": [
    {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
  ]
}

# Input proofs use conditional keysets, output BlindedMessages use regular keyset
# No oracle witness required (complete set cancels out)
output_total:       100
```

### Test 10: Successful merge response

```shell
# Response with signatures for collateral outputs (regular keyset)
response_json:      {
  "signatures": [
    {"amount": 64, "id": "009a1f293253e41e", "C_": "02...sig1..."},
    {"amount": 32, "id": "009a1f293253e41e", "C_": "02...sig2..."},
    {"amount": 4, "id": "009a1f293253e41e", "C_": "02...sig3..."}
  ]
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
# Mint verifies oracle signature per NUT-28
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

### Test 13: Split amount mismatch

```shell
# Input total != output total for each outcome collection
input_total:        100
output_yes_total:   90   # Mismatch!
output_no_total:    100

error_code:         13022
error_message:      "Split amount mismatch"
```

### Test 14: Missing outcome collection in outputs

```shell
# Binary condition but only YES outputs provided
outcome_collections:  ["YES", "NO"]
outputs_provided:   ["YES"]  # Missing NO!

error_code:         13038
error_message:      "Incomplete partition"
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
# Different amounts for different outcome collections
input_total:        100
output_yes_total:   100
output_no_total:    50   # Different!

error_code:         13022
error_message:      "Split amount mismatch"
```

### Test 18: Merge amount mismatch

```shell
# Input amounts don't match
input_yes_total:    100
input_no_total:     80   # Mismatch!

error_code:         13025
error_message:      "Merge amount mismatch"
```

### Test 19: Missing outcome collection in merge inputs

```shell
# Binary condition but only YES inputs provided
outcome_collections:  ["YES", "NO"]
inputs_provided:    ["YES"]  # Missing NO!

error_code:         13038
error_message:      "Incomplete partition"
```

### Test 20: Output amount mismatch in merge

```shell
# Output total doesn't equal per-outcome collection input total
input_yes_total:    100
input_no_total:     100
output_total:       50   # Should be 100!

error_code:         13025
error_message:      "Merge amount mismatch"
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

# Default partition (individual outcomes, sorted)
partition_keys:     ["NO", "YES"]
partition_utf8:     4e4f00594553  # "NO" + 0x00 + "YES"

# condition_id = tagged_hash("Cashu_condition_id", sorted_pubkeys || event_id || outcome_count || sorted_partition_keys)
```

## Outcome Collections

### Test 22: Split with outcome collections (3-outcome condition)

```shell
# Condition with 3 outcomes, prepared with outcome collection partition
outcomes:           ["ALICE", "BOB", "CAROL"]

# Condition preparation returned keysets for this partition
keysets:
  "ALICE|BOB":      00aabb11cc22dd33
  "CAROL":          00ccdd44ee55ff66

# Split request with outcome collections
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": [
    {"amount": 100, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."}
  ],
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

# Partition check
partition_valid:    true (ALICE|BOB and CAROL cover all outcomes, disjoint)
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

### Test 25: Overlapping outcome collections error

```shell
# Invalid partition - BOB appears in both sets
outputs_keys:       ["ALICE|BOB", "BOB|CAROL"]
condition_outcomes:    ["ALICE", "BOB", "CAROL"]

# Validation fails
error_code:         13037
error_message:      "Overlapping outcome collections"
```

### Test 26: Incomplete partition error

```shell
# Invalid partition - CAROL is missing
outputs_keys:       ["ALICE|BOB"]
condition_outcomes:    ["ALICE", "BOB", "CAROL"]

# Validation fails
error_code:         13038
error_message:      "Incomplete partition"
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
  "outputs": [
    {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
  ]
}

# Input proofs use outcome collection keysets, outputs use regular keyset
# Valid merge - outcome collections form complete partition
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

### Test 29: Collection ID computation

```shell
# Collection ID computation
# collection_id(parent, condition_id, outcome_collection_string):
#   h = tagged_hash("Cashu_collection_id", condition_id || outcome_collection_string_bytes)
#   P = hash_to_curve(h)
#   If parent is identity: return x_only(P)
#   Else: return x_only(EC_add(lift_x(parent), P))

# Root condition (parent = identity/zero)
parent_collection_id: 0000000000000000000000000000000000000000000000000000000000000000
condition_id_A:        a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd
outcome_A:        "YES"
outcome_A_utf8:   594553

# Step 1: h = tagged_hash("Cashu_collection_id", condition_id_A || "YES")
# Step 2: P_A = hash_to_curve(h)
# Step 3: collection_id_A = x_only(P_A)  (parent is identity)
```

### Test 30: Combinatorial condition commutativity

```shell
# Two conditions
election_condition_id:  a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd
btc_price_condition_id:  b2c3d4e5f67890123456789012345678901234567890123456789012345678ef

# Path 1: Election first, then BTC price
# Step 1a: coll_A = collection_id(0, election_condition_id, "PARTY_A")
# Step 1b: coll_AB = collection_id(coll_A, btc_price_condition_id, "UP")

# Path 2: BTC price first, then election
# Step 2a: coll_B = collection_id(0, btc_price_condition_id, "UP")
# Step 2b: coll_BA = collection_id(coll_B, election_condition_id, "PARTY_A")

# Commutativity: coll_AB == coll_BA
# This holds because EC point addition is commutative:
#   P_election_A + P_btc_UP = P_btc_UP + P_election_A
```

### Test 31: Nested condition preparation

```shell
# Step 1: Prepare root election condition
root_request:       {
  "collateral": "sat",
  "threshold": 1,
  "description": "Election winner",
  "announcements": ["<hex_encoded_tlv>"],
  "partition": ["PARTY_A", "PARTY_B"]
}

root_response:      {
  "condition_id": "<election_condition_id>",
  "keysets": {
    "PARTY_A": "00aa11bb22cc33dd",
    "PARTY_B": "00bb22cc33dd44ee"
  }
}

# Step 2: Prepare nested BTC price condition under PARTY_A
# parent_collection_id = collection_id(0, election_condition_id, "PARTY_A")
# collateral = outcome_collection_id of PARTY_A in election condition

nested_request:     {
  "collateral": "<outcome_collection_id_of_PARTY_A>",
  "threshold": 1,
  "description": "BTC price conditional on Party A win",
  "announcements": ["<hex_encoded_btc_price_tlv>"],
  "partition": ["UP", "DOWN"],
  "parent_collection_id": "<outcome_collection_id_of_PARTY_A>"
}

nested_response:    {
  "condition_id": "<btc_price_condition_id>",
  "keysets": {
    "UP": "00cc33dd44ee55ff",
    "DOWN": "00dd44ee55ff6600"
  }
}
```

### Test 32: Nested condition split

```shell
# Split PARTY_A tokens into PARTY_A&UP and PARTY_A&DOWN
# Inputs use PARTY_A conditional keyset (from root condition)
# Outputs use nested condition conditional keysets
request_json:       {
  "condition_id": "<btc_price_condition_id>",
  "inputs": [
    {"amount": 100, "id": "00aa11bb22cc33dd", "secret": "party_a_secret_1", "C": "02..."}
  ],
  "outputs": {
    "UP": [
      {"amount": 64, "id": "00cc33dd44ee55ff", "B_": "03..."},
      {"amount": 32, "id": "00cc33dd44ee55ff", "B_": "03..."},
      {"amount": 4, "id": "00cc33dd44ee55ff", "B_": "03..."}
    ],
    "DOWN": [
      {"amount": 64, "id": "00dd44ee55ff6600", "B_": "03..."},
      {"amount": 32, "id": "00dd44ee55ff6600", "B_": "03..."},
      {"amount": 4, "id": "00dd44ee55ff6600", "B_": "03..."}
    ]
  }
}

# Input uses PARTY_A keyset (parent outcome collection)
# Outputs use UP/DOWN keysets (nested outcome collections)
result:             PASS
```

### Test 33: Nested condition merge

```shell
# Merge PARTY_A&UP and PARTY_A&DOWN back to PARTY_A tokens
request_json:       {
  "condition_id": "<btc_price_condition_id>",
  "inputs": {
    "UP": [
      {"amount": 100, "id": "00cc33dd44ee55ff", "secret": "up_secret_1", "C": "02..."}
    ],
    "DOWN": [
      {"amount": 100, "id": "00dd44ee55ff6600", "secret": "down_secret_1", "C": "02..."}
    ]
  },
  "outputs": [
    {"amount": 64, "id": "00aa11bb22cc33dd", "B_": "03..."},
    {"amount": 32, "id": "00aa11bb22cc33dd", "B_": "03..."},
    {"amount": 4, "id": "00aa11bb22cc33dd", "B_": "03..."}
  ]
}

# Outputs use PARTY_A keyset (parent outcome collection), not regular keyset
result:             PASS
```

### Test 34: Maximum depth exceeded

```shell
# Attempt to prepare condition at depth exceeding max_depth
# Mint's max_depth = 2
# Attempting depth 3 preparation
error_code:         13040
error_message:      "Maximum condition depth exceeded"
```

## Complete Flow Example

### Test 35: End-to-end condition lifecycle

```shell
# Step 1: Prepare condition (POST /v1/conditions)
# Response:
condition_id:          <tagged_hash_result>
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

[NUT-29]: ../29.md
[NUT-28]: ../28.md
