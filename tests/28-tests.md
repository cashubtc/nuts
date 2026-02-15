# NUT-28 Test Vectors

These test vectors provide reference data for implementing conditional keysets. All values are hex-encoded for reproducibility.

## Conditional Token Structure (Per-Condition Keysets)

### Test 1: YES conditional token with conditional keyset

```shell
# Market registration returned keysets:
# YES -> keyset_id: 00abc123def456
# NO  -> keyset_id: 00def789abc012

# YES token proof (regular random secret, conditional keyset)
amount:             64
keyset_id:          00abc123def456
secret:             d341ee4871f1f889041e63cf0d3823c713eea6aff01e80f1719f08f9e5be98f6
C:                  02<compressed_point>

# The keyset ID identifies this as a YES conditional token
# The secret is a regular random string (no NUT-10 structure)
```

### Test 2: NO conditional token with conditional keyset

```shell
# Same market as Test 1
# NO token proof (regular random secret, conditional keyset)
amount:             64
keyset_id:          00def789abc012
secret:             99fce58439fc37412ab3468b73db0569322588f62fb3a49182d67e23d877824a
C:                  02<compressed_point>

# The keyset ID identifies this as a NO conditional token
```

## Outcome Collection ID Computation

### Test 3: Outcome Collection ID using tagged hash

```shell
# outcome_collection_id = tagged_hash("Cashu_outcome_collection_id", outcome_collection_string || condition_id)
# tagged_hash(tag, msg) = SHA256(SHA256(tag) || SHA256(tag) || msg)

# Tag preimage
tag:                "Cashu_outcome_collection_id"
tag_utf8:           43617368755f6f7574636f6d655f636f6c6c656374696f6e5f6964
tag_hash:           SHA256(tag_utf8)

# Outcome collection: "YES"
outcome_collection_string:   "YES"
outcome_collection_utf8: 594553

# Condition ID (32 bytes)
condition_id:          3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f

# Preimage for tagged hash
msg:                594553 || 3a7f8d2e1b4c5a6f9e0d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f

# outcome_collection_id = SHA256(tag_hash || tag_hash || msg)
# Result is a 32-byte (64 hex char) value
```

### Test 4: Outcome Collection ID for outcome collection

```shell
# Outcome collection: "ALICE|BOB" (outcome collection covering two outcomes)
outcome_collection_string:   "ALICE|BOB"
outcome_collection_utf8: 414c4943457c424f42

# Condition ID (32 bytes)
condition_id:          7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d

# outcome_collection_id = tagged_hash("Cashu_outcome_collection_id", "ALICE|BOB" || condition_id)
# Different outcome collection strings produce different outcome_collection_ids
# Different condition_ids produce different outcome_collection_ids
```

## Witness Validation

### Test 5: Valid oracle redemption witness (enum)

```shell
# Oracle signature on "YES"
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
oracle_sig:         a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890

# Witness JSON (oracle_sigs array format)
witness_json:       {"oracle_sigs":[{"oracle_pubkey":"9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0","oracle_sig":"a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"}]}

# Redemption via POST /v1/redeem_outcome: conditional keyset -> regular keyset
input_keyset_id:    00abc123def456    # YES conditional keyset
output_keyset_id:   009a1f293253e41e  # regular keyset

# Oracle signature verification
outcome:            "YES"
signature_check:    PASS
```

### Test 6: Invalid oracle signature

```shell
# Attempt to redeem with invalid signature
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
oracle_sig:         ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

# Witness JSON (oracle_sigs array format)
witness_json:       {"oracle_sigs":[{"oracle_pubkey":"9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0","oracle_sig":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}]}

# Redemption via POST /v1/redeem_outcome: conditional keyset -> regular keyset
input_keyset_id:    00abc123def456    # YES conditional keyset
output_keyset_id:   009a1f293253e41e  # regular keyset

# Oracle signature verification
outcome:            "YES"
signature_check:    FAIL
error_code:         13010
```

### Test 7: Redemption without witness

```shell
# Attempt to redeem via POST /v1/redeem_outcome without witness
input_keyset_id:    00abc123def456    # YES conditional keyset
output_keyset_id:   009a1f293253e41e  # regular keyset
witness:            null

# POST /v1/redeem_outcome requires oracle witness
error_code:         13014
error_message:      "Conditional keyset requires oracle witness"
```

## Trading (Same-Keyset Swap)

### Test 8: Valid trade swap (no witness needed)

```shell
# Swap within same conditional keyset (trading)
input_keyset_id:    00abc123def456    # YES conditional keyset
output_keyset_id:   00abc123def456    # same YES conditional keyset

# No witness needed - same keyset swap
witness:            null
result:             PASS
```

### Test 9: Three-outcome market keysets

```shell
# Market with three outcomes
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0
event:              "election_2024_winner"
outcomes:           ["CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C"]

# Market registration returns 3 conditional keysets
keysets:
  CANDIDATE_A:      00aa11bb22cc33dd
  CANDIDATE_B:      00bb22cc33dd44ee
  CANDIDATE_C:      00cc33dd44ee55ff

# Oracle signs CANDIDATE_B
signed_outcome:     "CANDIDATE_B"
oracle_sig:         <implementation_specific_signature>

# Only CANDIDATE_B keyset holders can redeem (swap to regular keyset with witness)
# CANDIDATE_A and CANDIDATE_C keyset holders cannot redeem
```

## Multi-Oracle Tests

### Test 10: Two-of-three oracle threshold

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

# Condition ID computation (sorted pubkeys, tagged hash)
sorted_pubkeys:     [oracle_1_pubkey, oracle_2_pubkey, oracle_3_pubkey]  # lexicographic
condition_id:          tagged_hash("Cashu_condition_id", sorted_pubkeys || event_id || outcome_count || sorted_partition_keys)

# Attestations from oracles 1 and 2 (meets threshold)
oracle_1_sig_YES:   <64_byte_signature_from_oracle_1>
oracle_2_sig_YES:   <64_byte_signature_from_oracle_2>

# Verification with 2 signatures
verification:       PASS (threshold met: 2 >= 2)
```

### Test 11: Multi-oracle threshold not met

```shell
# Same setup as Test 10
threshold:          2

# Only 1 attestation provided
oracle_1_sig_YES:   <64_byte_signature_from_oracle_1>

# Verification fails
verification:       FAIL
error_code:         13027  # Oracle threshold not met
```

## Error Validation Tests

### Test 12: Outcome collection not attested by oracle

```shell
# Attempt to claim with outcome collection not matching attestation
outcomes:           ["YES", "NO"]
outcome:            "MAYBE"
error_code:         13015
error_message:      "Oracle has not attested to this outcome collection"
```

### Test 13: Invalid oracle public key format

```shell
# 33-byte compressed key instead of 32-byte x-only
oracle_pubkey:      0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
error:              Invalid oracle public key format
error_code:         13010
```

[NUT-28]: ../28.md
