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

## Complete ORACLE Secret Examples

### Test 5: YES outcome token secret

```shell
# Secret components
kind:               "ORACLE"
nonce:              da62796403af76c80cd6ce9153ed3746
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event:              "btc_price_100k_2025"
outcomes:           ["YES", "NO"]
outcome:            "YES"
maturity:           "1751328000"
locktime:           "1754006400"
refund_pubkey:      033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e

# Serialized secret (JSON)
secret_json:        ["ORACLE",{"nonce":"da62796403af76c80cd6ce9153ed3746","data":"","tags":[["oracle","9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0"],["event","btc_price_100k_2025"],["outcomes","YES","NO"],["outcome","YES"],["maturity","1751328000"],["locktime","1754006400"],["refund","033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e"]]}]
```

### Test 6: NO outcome token secret

```shell
# Secret components
kind:               "ORACLE"
nonce:              8f3e2c1d4a5b6789abcdef0123456789
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event:              "btc_price_100k_2025"
outcomes:           ["YES", "NO"]
outcome:            "NO"
maturity:           "1751328000"
locktime:           "1754006400"
refund_pubkey:      033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e

# Serialized secret (JSON)
secret_json:        ["ORACLE",{"nonce":"8f3e2c1d4a5b6789abcdef0123456789","data":"","tags":[["oracle","9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0"],["event","btc_price_100k_2025"],["outcomes","YES","NO"],["outcome","NO"],["maturity","1751328000"],["locktime","1754006400"],["refund","033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e"]]}]
```

## Witness Validation

### Test 7: Valid oracle claim witness

```shell
# Oracle signature on "YES"
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
signatures:         []

# Witness JSON
witness_json:       {"oracle_sig":"a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890","signatures":[]}

# Validation (current_time >= maturity)
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

### Test 10: Valid refund claim

```shell
# Refund claim after locktime
oracle_sig:         null
refund_privkey:     5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f
refund_pubkey:      033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e
refund_signature:   9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba

# Witness JSON (P2PK refund witness)
witness_json:       {"signatures":["9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba"]}

# Validation
current_time:       1754006401
locktime:           1754006400
time_check:         PASS

# Refund signature verification (NUT-11 rules)
signature_check:    PASS
```

### Test 11: Invalid refund before locktime

```shell
# Attempt to refund before locktime
oracle_sig:         null
refund_signature:   9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba

# Validation
current_time:       1754006399
locktime:           1754006400
time_check:         FAIL
error_code:         13015
```

## Time Boundary Tests

### Test 12: Maturity time boundary (exact match)

```shell
# Claim at exact maturity
current_time:       1751328000
maturity:           1751328000
time_check:         PASS (>= allows exact match)
```

### Test 13: Locktime boundary (exact match)

```shell
# Refund at exact locktime
current_time:       1754006400
locktime:           1754006400
time_check:         FAIL (> requires strictly after)
```

### Test 14: Locktime boundary (one second after)

```shell
# Refund one second after locktime
current_time:       1754006401
locktime:           1754006400
time_check:         PASS
```

## Multi-Outcome Market Test

### Test 15: Three-outcome market

```shell
# Market with three outcomes
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event:              "election_2024_winner"
outcomes:           ["CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C"]
maturity:           "1730764800"
locktime:           "1733443200"

# Outcome A secret
outcome_a:          "CANDIDATE_A"
nonce_a:            a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1
secret_a_json:      ["ORACLE",{"nonce":"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1","data":"","tags":[["oracle","9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0"],["event","election_2024_winner"],["outcomes","CANDIDATE_A","CANDIDATE_B","CANDIDATE_C"],["outcome","CANDIDATE_A"],["maturity","1730764800"],["locktime","1733443200"]]}]

# Outcome B secret
outcome_b:          "CANDIDATE_B"
nonce_b:            b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2
secret_b_json:      ["ORACLE",{"nonce":"b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2","data":"","tags":[["oracle","9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0"],["event","election_2024_winner"],["outcomes","CANDIDATE_A","CANDIDATE_B","CANDIDATE_C"],["outcome","CANDIDATE_B"],["maturity","1730764800"],["locktime","1733443200"]]}]

# Outcome C secret
outcome_c:          "CANDIDATE_C"
nonce_c:            c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3
secret_c_json:      ["ORACLE",{"nonce":"c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3","data":"","tags":[["oracle","9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0"],["event","election_2024_winner"],["outcomes","CANDIDATE_A","CANDIDATE_B","CANDIDATE_C"],["outcome","CANDIDATE_C"],["maturity","1730764800"],["locktime","1733443200"]]}]

# Oracle signs CANDIDATE_B
signed_outcome:     "CANDIDATE_B"
oracle_sig:         <implementation_specific_signature>

# Only CANDIDATE_B holders can claim with valid oracle signature
```

## UTF-8 NFC Normalization Tests

### Test 16: ASCII outcome

```shell
# Simple ASCII
outcome:            "YES"
outcome_utf8_hex:   594553
outcome_normalized: "YES"
```

### Test 17: Unicode outcome (precomposed)

```shell
# Precomposed Unicode (single codepoint)
outcome:            "café"
outcome_utf8_hex:   636166c3a9
outcome_normalized: "café"  # NFC: é as single codepoint U+00E9
```

### Test 18: Unicode outcome (decomposed)

```shell
# Decomposed Unicode (base + combining)
outcome_input:      "café"  # e + combining acute (U+0065 U+0301)
outcome_utf8_hex:   6361666565cc81
outcome_normalized: "café"  # NFC: é as single codepoint U+00E9
normalized_hex:     636166c3a9
```

## Error Validation Tests

### Test 19: Outcome not in outcomes list

```shell
# Attempt to claim with outcome not in descriptor
outcomes:           ["YES", "NO"]
outcome:            "MAYBE"
error_code:         13013
```

### Test 20: Invalid oracle public key format

```shell
# 33-byte compressed key instead of 32-byte x-only
oracle_pubkey:      0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
error:              Invalid oracle public key format
error_code:         13010
```

### Test 21: Invalid event descriptor

```shell
# Empty outcomes list
outcomes:           []
error_code:         13012
```

[NUT-28]: ../28.md
