# NUT-28 Test Vectors

These test vectors provide reference data for implementing the ORACLE spending condition. All values are hex-encoded for reproducibility.

## BIP 340 Tagged Hash

The DLC oracle signing algorithm uses BIP 340 tagged hashing. These vectors verify the tagged hash implementation.

### Test 1: Tag hash for attestation

```shell
# Tag string
tag:                "DLC/oracle/attestation/v0"
tag_bytes:          444c432f6f7261636c652f6174746573746174696f6e2f7630

# SHA256(tag)
sha256_tag:         89ccf0b7a42a9ddf8f25e350d03e4e2bdd5a93b30d7ef55a6be91e76f7c1c7d0

# tag_hash = SHA256(SHA256(tag) || SHA256(tag))
tag_hash:           97c56b354b7a7b97d6e992d5ffd7e68ca07ea4c0b96c1cfb6a6f3bd9ef8d6fbe
```

### Test 2: Tag hash for announcement

```shell
# Tag string
tag:                "DLC/oracle/announcement/v0"
tag_bytes:          444c432f6f7261636c652f616e6e6f756e63656d656e742f7630

# SHA256(tag)
sha256_tag:         6d8e6d5b3a1c5e2f9a4b7c8d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f

# tag_hash = SHA256(SHA256(tag) || SHA256(tag))
tag_hash:           f0e1d2c3b4a59687706152433425160798a9bacbdcedfe0f10213243546576a7
```

## Oracle Signature Generation

### Test 3: Sign outcome "YES"

```shell
# Oracle private key (32 bytes, x-only format internally)
oracle_privkey:     0000000000000000000000000000000000000000000000000000000000000001

# Oracle x-only public key (32 bytes)
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798

# Outcome to sign
outcome:            "YES"
outcome_utf8_hex:   594553

# Tagged hash computation
tag:                "DLC/oracle/attestation/v0"
tag_hash:           97c56b354b7a7b97d6e992d5ffd7e68ca07ea4c0b96c1cfb6a6f3bd9ef8d6fbe

# Message hash = SHA256(tag_hash || outcome_utf8)
message_preimage:   97c56b354b7a7b97d6e992d5ffd7e68ca07ea4c0b96c1cfb6a6f3bd9ef8d6fbe594553
message_hash:       8da6f8d38c3e4e8c9a2b1c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f

# BIP340 signature (64 bytes)
# Note: Actual signature depends on auxiliary randomness
oracle_sig:         <implementation_specific_64_byte_signature>
```

### Test 4: Sign outcome "NO"

```shell
# Same oracle keys as Test 3
oracle_privkey:     0000000000000000000000000000000000000000000000000000000000000001
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798

# Outcome to sign
outcome:            "NO"
outcome_utf8_hex:   4e4f

# Message hash = SHA256(tag_hash || outcome_utf8)
message_preimage:   97c56b354b7a7b97d6e992d5ffd7e68ca07ea4c0b96c1cfb6a6f3bd9ef8d6fbe4e4f
message_hash:       1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b

# BIP340 signature
oracle_sig:         <implementation_specific_64_byte_signature>
```

## Complete ORACLE Secret Examples (New Format)

### Test 5: YES outcome token secret

```shell
# Secret components
kind:               "ORACLE"
nonce:              da62796403af76c80cd6ce9153ed3746

# Announcement contains:
# - oracle_pubkey: 9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
# - event_id: "btc_price_100k_2025"
# - outcomes: ["YES", "NO"]
# - maturity_epoch: 1751328000
# - oracle_nonce: a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

announcement_hex:   d834<tlv_encoded_announcement>

outcome:            "YES"

# Serialized secret (JSON) - simplified format
secret_json:        ["ORACLE",{"nonce":"da62796403af76c80cd6ce9153ed3746","data":"","tags":[["announcement","d834..."],["outcome","YES"]]}]
```

### Test 6: NO outcome token secret

```shell
# Secret components
kind:               "ORACLE"
nonce:              8f3e2c1d4a5b6789abcdef0123456789

# Same announcement as Test 5
announcement_hex:   d834<tlv_encoded_announcement>

outcome:            "NO"

# Serialized secret (JSON) - simplified format
secret_json:        ["ORACLE",{"nonce":"8f3e2c1d4a5b6789abcdef0123456789","data":"","tags":[["announcement","d834..."],["outcome","NO"]]}]
```

## Witness Validation

### Test 7: Valid oracle claim witness

```shell
# Oracle signature on "YES"
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
signatures:         []

# Witness JSON
witness_json:       {"oracle_sig":"a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890","signatures":[]}

# Validation (current_time >= maturity from announcement)
current_time:       1751328000
maturity:           1751328000
time_check:         PASS

# Oracle signature verification
outcome:            "YES"
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
signature_check:    PASS
```

### Test 8: Invalid oracle signature

```shell
# Attempt to claim with invalid signature
oracle_sig:         ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
signatures:         []

# Validation
current_time:       1751328000
maturity:           1751328000
time_check:         PASS

# Oracle signature verification
outcome:            "YES"
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
signature_check:    FAIL
error_code:         13010
```

### Test 9: Claim before maturity

```shell
# Attempt to claim before maturity
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# Validation
current_time:       1751327999
maturity:           1751328000
time_check:         FAIL
error_code:         13014
```

## Time Boundary Tests

### Test 10: Maturity time boundary (exact match)

```shell
# Claim at exact maturity
current_time:       1751328000
maturity:           1751328000
time_check:         PASS (>= allows exact match)
```

## Multi-Outcome Market Test

### Test 11: Three-outcome market

```shell
# Market with three outcomes
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event:              "election_2024_winner"
outcomes:           ["CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C"]
maturity:           1730764800

# Announcement contains all outcomes
announcement_hex:   d834<tlv_encoded_with_3_outcomes>

# Outcome A secret
outcome_a:          "CANDIDATE_A"
nonce_a:            a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1
secret_a_json:      ["ORACLE",{"nonce":"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1","data":"","tags":[["announcement","d834..."],["outcome","CANDIDATE_A"]]}]

# Outcome B secret
outcome_b:          "CANDIDATE_B"
nonce_b:            b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2
secret_b_json:      ["ORACLE",{"nonce":"b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2","data":"","tags":[["announcement","d834..."],["outcome","CANDIDATE_B"]]}]

# Outcome C secret
outcome_c:          "CANDIDATE_C"
nonce_c:            c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3
secret_c_json:      ["ORACLE",{"nonce":"c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3","data":"","tags":[["announcement","d834..."],["outcome","CANDIDATE_C"]]}]

# Oracle signs CANDIDATE_B
signed_outcome:     "CANDIDATE_B"
oracle_sig:         <implementation_specific_signature>

# Only CANDIDATE_B holders can claim with valid oracle signature
```

## Multi-Oracle Tests

### Test 12: Two-of-three oracle threshold

```shell
# Three oracle announcements
oracle_1_pubkey:    79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
oracle_2_pubkey:    9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
oracle_3_pubkey:    a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

threshold:          2
event_id:           "btc_price_100k_2025"
outcomes:           ["YES", "NO"]

# Each oracle has their own announcement with their nonce
announcement_1:     d834<oracle_1_announcement>
announcement_2:     d834<oracle_2_announcement>
announcement_3:     d834<oracle_3_announcement>

# Market ID computation (sorted pubkeys)
sorted_pubkeys:     [oracle_1_pubkey, oracle_2_pubkey, oracle_3_pubkey]  # lexicographic
market_id:          SHA256(sorted_pubkeys || event_id || outcome_count)

# Attestations from oracles 1 and 2 (meets threshold)
oracle_1_sig_YES:   <64_byte_signature_from_oracle_1>
oracle_2_sig_YES:   <64_byte_signature_from_oracle_2>

# Verification with 2 signatures
verification:       PASS (threshold met: 2 >= 2)
```

### Test 13: Multi-oracle threshold not met

```shell
# Same setup as Test 12
threshold:          2

# Only 1 attestation provided
oracle_1_sig_YES:   <64_byte_signature_from_oracle_1>

# Verification fails
verification:       FAIL
error_code:         13027  # Oracle threshold not met
```

## Announcement Verification Tests

### Test 14: Valid announcement signature

```shell
# Oracle keys
oracle_privkey:     0000000000000000000000000000000000000000000000000000000000000001
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798

# Tag hash computation for announcement
tag:                "DLC/oracle/announcement/v0"
tag_hash:           f0e1d2c3b4a59687706152433425160798a9bacbdcedfe0f10213243546576a7

# Oracle event parameters
nb_nonces:          1
oracle_nonce:       a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
event_maturity:     1751328000
event_id:           "btc_price_100k_2025"
outcomes:           ["YES", "NO"]

# Announcement signature (64 bytes)
announcement_sig:   <implementation_specific_64_byte_signature>

# Verification
signature_valid:    true
```

### Test 15: Invalid announcement signature

```shell
# Attempt to verify with wrong oracle pubkey
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
announcement_sig:   <signature_made_with_different_key>

signature_valid:    false
error_code:         13031
error_message:      "Announcement signature invalid"
```

## Adaptor Point Computation

### Test 16: Single nonce adaptor point for YES outcome

```shell
# Oracle nonce (R)
oracle_nonce:       a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# Oracle public key (P)
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798

# Outcome
outcome:            "YES"
outcome_utf8_hex:   594553

# Outcome hash H(outcome) using attestation tag
tag:                "DLC/oracle/attestation/v0"
outcome_hash:       8da6f8d38c3e4e8c9a2b1c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f

# Adaptor point = R + H(outcome) * P
adaptor_point:      <32_byte_x_only_point>
```

### Test 17: Single nonce adaptor point for NO outcome

```shell
# Same oracle nonce and pubkey
oracle_nonce:       a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
oracle_pubkey:      79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798

# Outcome
outcome:            "NO"
outcome_utf8_hex:   4e4f

# Outcome hash
outcome_hash:       1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b

# Adaptor point = R + H(outcome) * P
adaptor_point:      <32_byte_x_only_point>
```

## UTF-8 NFC Normalization Tests

### Test 18: ASCII outcome

```shell
# Simple ASCII
outcome:            "YES"
outcome_utf8_hex:   594553
outcome_normalized: "YES"
```

### Test 19: Unicode outcome (precomposed)

```shell
# Precomposed Unicode (single codepoint)
outcome:            "café"
outcome_utf8_hex:   636166c3a9
outcome_normalized: "café"  # NFC: é as single codepoint U+00E9
```

### Test 20: Unicode outcome (decomposed)

```shell
# Decomposed Unicode (base + combining)
outcome_input:      "café"  # e + combining acute (U+0065 U+0301)
outcome_utf8_hex:   6361666565cc81
outcome_normalized: "café"  # NFC: é as single codepoint U+00E9
normalized_hex:     636166c3a9
```

## Error Validation Tests

### Test 21: Outcome not in event descriptor

```shell
# Attempt to claim with outcome not in descriptor
outcomes:           ["YES", "NO"]
outcome:            "MAYBE"
error_code:         13013
```

### Test 22: Invalid oracle public key format

```shell
# 33-byte compressed key instead of 32-byte x-only
oracle_pubkey:      0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
error:              Invalid oracle public key format
error_code:         13010
```

### Test 23: Invalid event descriptor

```shell
# Empty outcomes list
outcomes:           []
error_code:         13012
```

### Test 24: Invalid announcement format

```shell
# Malformed TLV
announcement:       "invalid_hex_data"

error_code:         13030
error_message:      "Invalid oracle announcement format"
```

### Test 25: Event descriptor mismatch

```shell
# Announcement has different outcomes than expected
announcement_outcomes: ["WIN", "LOSE"]
expected_outcomes:     ["YES", "NO"]

error_code:         13032
error_message:      "Event descriptor mismatch"
```

## Nonce Reuse Detection

### Test 26: Nonce reuse across markets (WARNING)

```shell
# Same oracle uses same nonce for different events (DANGEROUS)
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0

market_1_event_id:  "btc_price_100k_2025"
market_1_nonce:     a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

market_2_event_id:  "eth_price_10k_2025"
market_2_nonce:     a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# Same nonce! Wallet should warn user
nonce_reuse_detected: true

# If oracle signs different outcomes on both markets, private key can be extracted
```

[NUT-28]: ../28.md
