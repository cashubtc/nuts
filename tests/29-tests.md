# NUT-29 Test Vectors

These test vectors provide reference data for implementing the Conditional Token Framework (CTF). All values are hex-encoded for reproducibility.

## Market ID Calculation

The market ID is computed as `SHA256(oracle_pubkey || question_id || outcome_count)`.

### Test 1: Binary market ID

```shell
# Market parameters
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
question_id:        "btc_price_100k_2025"
question_id_utf8:   6274635f70726963655f3130306b5f32303235
outcome_count:      2
outcome_count_byte: 02

# Preimage
preimage_hex:       9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce06274635f70726963655f3130306b5f3230323502

# Market ID
market_id:          3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f
```

### Test 2: Three-outcome market ID

```shell
# Market parameters
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
question_id:        "election_2024_winner"
question_id_utf8:   656c656374696f6e5f323032345f77696e6e6572
outcome_count:      3
outcome_count_byte: 03

# Preimage
preimage_hex:       9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0656c656374696f6e5f323032345f77696e6e657203

# Market ID
market_id:          7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d
```

### Test 3: Market ID with special characters in question

```shell
# Market parameters
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
question_id:        "Will ETH/USD > $5000?"
question_id_utf8:   57696c6c204554482f555344203e2024353030303f
outcome_count:      2
outcome_count_byte: 02

# Market ID (includes space, /, >, $ characters)
market_id:          1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890
```

## Split Operation

### Test 4: Binary market split request

```shell
# Market parameters
market_id:          3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f

# Input (100 sats collateral)
input_amount:       100
input_proofs:       [
  {"amount": 64, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."},
  {"amount": 32, "id": "009a1f293253e41e", "secret": "secret2", "C": "02..."},
  {"amount": 4, "id": "009a1f293253e41e", "secret": "secret3", "C": "02..."}
]
input_total:        100

# Output requirements per outcome
output_yes_total:   100
output_no_total:    100

# Split request JSON
request_json:       {
  "market_id": "3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f",
  "inputs": [
    {"amount": 64, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."},
    {"amount": 32, "id": "009a1f293253e41e", "secret": "secret2", "C": "02..."},
    {"amount": 4, "id": "009a1f293253e41e", "secret": "secret3", "C": "02..."}
  ],
  "outputs": {
    "YES": [
      {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
    ],
    "NO": [
      {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
      {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
    ]
  }
}
```

### Test 5: Three-outcome market split

```shell
# Market with 3 outcomes
market_id:          7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d
outcomes:           ["CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C"]

# Input (50 sats collateral)
input_amount:       50

# Output requirements per outcome
output_a_total:     50
output_b_total:     50
output_c_total:     50

# Each outcome gets equal share of collateral equivalent
```

## Resulting Token Structure

### Test 6: YES outcome token after split

```shell
# Token parameters derived from split
market_id:          3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event:              "btc_price_100k_2025"
outcomes:           ["YES", "NO"]
outcome:            "YES"
maturity:           1751328000

# Announcement (TLV-encoded) contains oracle pubkey, event_id, outcomes, maturity
announcement_hex:   d834<tlv_encoded_announcement>

# Resulting secret (NUT-28 ORACLE format - simplified)
nonce:              a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1
secret_json:        ["ORACLE",{"nonce":"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1","data":"","tags":[["announcement","d834..."],["outcome","YES"]]}]
```

### Test 7: NO outcome token after split

```shell
# Same market, different outcome
nonce:              b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2
secret_json:        ["ORACLE",{"nonce":"b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2","data":"","tags":[["announcement","d834..."],["outcome","NO"]]}]
```

## Market Info

### Test 8: Market info response

```shell
# Market info structure
market_info_json:   {
  "market_id": "3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f",
  "oracle_pubkeys": ["9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0"],
  "threshold": 1,
  "question_id": "btc_price_100k_2025",
  "outcomes": ["YES", "NO"],
  "maturity": 1751328000,
  "unit": "sat",
  "description": "Will BTC reach $100k by June 2025?",
  "announcements": ["d834..."],
  "announcements_verified": true
}
```

## Error Cases

### Test 9: Split amount mismatch

```shell
# Input total != output total for each outcome
input_total:        100
output_yes_total:   90   # Mismatch!
output_no_total:    100

error_code:         13022
error_message:      "Split amount mismatch"
```

### Test 10: Missing outcome in outputs

```shell
# Binary market but only YES outputs provided
market_outcomes:    ["YES", "NO"]
outputs_provided:   ["YES"]  # Missing NO!

error_code:         13023
error_message:      "Missing outcome in outputs"
```

### Test 11: Invalid market ID

```shell
# Market ID too short
market_id:          3a7f8d2e1b4c5a6f  # Only 16 hex chars (8 bytes)

error_code:         13020
error_message:      "Invalid market ID"
```

### Test 12: Market not found

```shell
# Valid format but non-existent market
market_id:          ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

error_code:         13021
error_message:      "Market not found"
```

### Test 13: Unequal outcome amounts

```shell
# Different amounts for different outcomes
input_total:        100
output_yes_total:   100
output_no_total:    50   # Different!

error_code:         13022
error_message:      "Split amount mismatch"
```

## Split Response

### Test 14: Successful split response

```shell
# Response with signatures for each outcome
response_json:      {
  "signatures": {
    "YES": [
      {"amount": 64, "id": "009a1f293253e41e", "C_": "02...sig1..."},
      {"amount": 32, "id": "009a1f293253e41e", "C_": "02...sig2..."},
      {"amount": 4, "id": "009a1f293253e41e", "C_": "02...sig3..."}
    ],
    "NO": [
      {"amount": 64, "id": "009a1f293253e41e", "C_": "02...sig4..."},
      {"amount": 32, "id": "009a1f293253e41e", "C_": "02...sig5..."},
      {"amount": 4, "id": "009a1f293253e41e", "C_": "02...sig6..."}
    ]
  }
}

# Each BlindSignature corresponds to a BlindedMessage in the request
```

## Merge Operation

### Test 15: Binary market merge request

```shell
# Market parameters
market_id:          3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f

# Inputs (100 sats of each outcome token)
input_yes_total:    100
input_no_total:     100

# Merge request JSON
request_json:       {
  "market_id": "3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f",
  "inputs": {
    "YES": [
      {"amount": 64, "id": "009a1f293253e41e", "secret": "[\"ORACLE\",{...\"outcome\":\"YES\"...}]", "C": "02..."},
      {"amount": 32, "id": "009a1f293253e41e", "secret": "[\"ORACLE\",{...\"outcome\":\"YES\"...}]", "C": "02..."},
      {"amount": 4, "id": "009a1f293253e41e", "secret": "[\"ORACLE\",{...\"outcome\":\"YES\"...}]", "C": "02..."}
    ],
    "NO": [
      {"amount": 64, "id": "009a1f293253e41e", "secret": "[\"ORACLE\",{...\"outcome\":\"NO\"...}]", "C": "02..."},
      {"amount": 32, "id": "009a1f293253e41e", "secret": "[\"ORACLE\",{...\"outcome\":\"NO\"...}]", "C": "02..."},
      {"amount": 4, "id": "009a1f293253e41e", "secret": "[\"ORACLE\",{...\"outcome\":\"NO\"...}]", "C": "02..."}
    ]
  },
  "outputs": [
    {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
  ]
}

# Output: 100 sats collateral (regular proofs, not ORACLE-locked)
output_total:       100
```

### Test 16: Successful merge response

```shell
# Response with signatures for collateral outputs
response_json:      {
  "signatures": [
    {"amount": 64, "id": "009a1f293253e41e", "C_": "02...sig1..."},
    {"amount": 32, "id": "009a1f293253e41e", "C_": "02...sig2..."},
    {"amount": 4, "id": "009a1f293253e41e", "C_": "02...sig3..."}
  ]
}

# Each BlindSignature corresponds to a BlindedMessage in the request
# Resulting proofs are regular (not ORACLE-locked)
```

### Test 17: Merge amount mismatch error

```shell
# Input amounts don't match
input_yes_total:    100
input_no_total:     80   # Mismatch!

error_code:         13025
error_message:      "Merge amount mismatch"
```

### Test 18: Missing outcome in merge inputs error

```shell
# Binary market but only YES inputs provided
market_outcomes:    ["YES", "NO"]
inputs_provided:    ["YES"]  # Missing NO!

error_code:         13026
error_message:      "Missing outcome in merge inputs"
```

### Test 19: Output amount mismatch error

```shell
# Output total doesn't equal per-outcome input total
input_yes_total:    100
input_no_total:     100
output_total:       50   # Should be 100!

error_code:         13025
error_message:      "Merge amount mismatch"
```

## Multi-Oracle Market ID

### Test 20: Multi-oracle market ID calculation

```shell
# Market parameters (2-of-3 threshold)
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
question_id:        "btc_price_100k_2025"
outcome_count:      2

# market_id = SHA256(sorted_pubkeys || question_id || outcome_count)
```

### Test 21: Combinatorial market ID calculation

```shell
# Multiple conditions
conditions:         ["election_winner", "btc_price"]
sorted_conditions:  ["btc_price", "election_winner"]  # sorted lexicographically
sorted_question_id: "btc_price\x00election_winner"    # joined with null byte

oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
outcome_count:      4  # 2 x 2 = 4 combinatorial outcomes

# market_id = SHA256(oracle_pubkey || sorted_question_id || outcome_count)
```

## Redemption via Swap

### Test 22: Winner redemption (via NUT-28 swap)

```shell
# Oracle attests "YES" won
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# YES holder swaps their ORACLE proofs (simplified format)
swap_inputs:        [
  {
    "amount": 64,
    "id": "009a1f293253e41e",
    "secret": "[\"ORACLE\",{\"nonce\":\"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1\",\"data\":\"\",\"tags\":[[\"announcement\",\"d834...\"], [\"outcome\",\"YES\"]]}]",
    "C": "02...",
    "witness": "{\"oracle_sig\":\"a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890\",\"signatures\":[]}"
  }
]

# Outputs are regular BlindedMessages (not ORACLE-locked)
swap_outputs:       [
  {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."}
]

# Mint verifies oracle signature per NUT-28
# Returns regular proofs (not outcome-locked)
```

### Test 23: Loser cannot redeem

```shell
# Oracle attests "YES" won, but user holds NO tokens
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# NO holder attempts to swap their ORACLE proofs
swap_inputs:        [
  {
    "amount": 64,
    "secret": "[\"ORACLE\",{...\"outcome\":\"NO\"...}]",
    "witness": "{\"oracle_sig\":\"a1b2c3...\",\"signatures\":[]}"
  }
]

# Verification fails: oracle signed "YES" but proof is for "NO"
error_code:         13010
error_message:      "Invalid oracle signature"
```

## Complete Flow Example

### Test 24: End-to-end market lifecycle

```shell
# Step 1: Market exists with ID
market_id:          3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f

# Step 2: Alice splits 100 sats
alice_input:        100 sats
alice_receives:     100 sats YES tokens + 100 sats NO tokens

# Step 3: Alice sells NO tokens to Bob for 40 sats
# (normal Cashu transfer, outside this spec)

# Step 4: Oracle attests "YES"
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
attested_outcome:   "YES"
oracle_sig:         <valid_signature_on_YES>

# Step 5: Alice redeems YES tokens
alice_redeems:      100 sats YES tokens
alice_receives:     100 sats regular ecash

# Step 6: Bob cannot redeem NO tokens
bob_attempts:       100 sats NO tokens
bob_result:         FAIL (oracle signed YES, not NO)

# Net result:
# - Alice: started with 100 sats, now has 100 sats + 40 sats from sale = 140 sats
# - Bob: paid 40 sats for worthless NO tokens = -40 sats
```

[NUT-29]: ../29.md
[NUT-28]: ../28.md
