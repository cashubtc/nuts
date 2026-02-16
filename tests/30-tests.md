# NUT-30 Test Vectors

These test vectors provide reference data for implementing numeric outcome markets. All values are hex-encoded for reproducibility.

## Numeric Market Registration

### Test 1: Register numeric market (HI/LO)

```shell
# Register a numeric market via POST /v1/conditions
request_json:       {
  "collateral": "sat",
  "threshold": 1,
  "description": "BTC/USD price on 2025-07-01",
  "announcements": ["<hex-encoded TLV with digit_decomposition_event_descriptor>"],
  "market_type": "numeric",
  "lo_bound": 0,
  "hi_bound": 100000,
  "precision": 0
}

response_json:      {
  "condition_id": "<tagged_hash_result>",
  "keysets": {
    "HI": "00hi11keyset22",
    "LO": "00lo33keyset44"
  }
}

# Partition is always ["HI", "LO"] for numeric markets
# condition_id = tagged_hash("Cashu_condition_id",
#   oracle_pubkey || event_id || 0x02 || "HI" + 0x00 + "LO"
#   || 0x01 || lo_bound_i64be || hi_bound_i64be || precision_i32be)
# where lo_bound_i64be = 0x0000000000000000 (0 as i64 big-endian)
#       hi_bound_i64be = 0x00000000000186a0 (100000 as i64 big-endian)
#       precision_i32be = 0x00000000 (0 as i32 big-endian)
```

### Test 2: Invalid numeric range

```shell
# lo_bound >= hi_bound
request_json:       {
  "collateral": "sat",
  "threshold": 1,
  "description": "Invalid range market",
  "announcements": ["<hex_encoded_tlv>"],
  "market_type": "numeric",
  "lo_bound": 100000,
  "hi_bound": 100000,
  "precision": 0
}

error_code:         13030
error_message:      "Invalid numeric range (lo_bound >= hi_bound)"
```

## Payout Calculation

### Test 3: Value in middle of range

```shell
# Range [0, 100000], attested value V = 20000
lo_bound:           0
hi_bound:           100000
attested_value:     20000

# Payout calculation
clamped_V:          20000  # clamp(20000, 0, 100000) = 20000
hi_payout_ratio:    0.2    # (20000 - 0) / (100000 - 0)
lo_payout_ratio:    0.8    # 1 - 0.2

# For 100 sats face value
amount:             100
hi_payout:          20     # floor(100 * 0.2)
lo_payout:          80     # 100 - 20
total:              100    # 20 + 80 = 100 (conservation)
```

### Test 4: Value at lo_bound (LO gets 100%)

```shell
# Range [0, 100000], attested value V = 0
lo_bound:           0
hi_bound:           100000
attested_value:     0

# Payout calculation
clamped_V:          0
hi_payout_ratio:    0.0    # (0 - 0) / (100000 - 0)
lo_payout_ratio:    1.0    # 1 - 0

# For 100 sats face value
amount:             100
hi_payout:          0      # floor(100 * 0.0)
lo_payout:          100    # 100 - 0
```

### Test 5: Value at hi_bound (HI gets 100%)

```shell
# Range [0, 100000], attested value V = 100000
lo_bound:           0
hi_bound:           100000
attested_value:     100000

# Payout calculation
clamped_V:          100000
hi_payout_ratio:    1.0    # (100000 - 0) / (100000 - 0)
lo_payout_ratio:    0.0    # 1 - 1

# For 100 sats face value
amount:             100
hi_payout:          100    # floor(100 * 1.0)
lo_payout:          0      # 100 - 100
```

### Test 6: Value below lo_bound (clamped, LO gets 100%)

```shell
# Range [10000, 100000], attested value V = 5000 (below lo_bound)
lo_bound:           10000
hi_bound:           100000
attested_value:     5000

# Payout calculation
clamped_V:          10000  # clamp(5000, 10000, 100000) = 10000
hi_payout_ratio:    0.0    # (10000 - 10000) / (100000 - 10000)
lo_payout_ratio:    1.0    # 1 - 0

# For 100 sats face value
amount:             100
hi_payout:          0
lo_payout:          100
```

### Test 7: Value above hi_bound (clamped, HI gets 100%)

```shell
# Range [10000, 100000], attested value V = 150000 (above hi_bound)
lo_bound:           10000
hi_bound:           100000
attested_value:     150000

# Payout calculation
clamped_V:          100000  # clamp(150000, 10000, 100000) = 100000
hi_payout_ratio:    1.0     # (100000 - 10000) / (100000 - 10000)
lo_payout_ratio:    0.0     # 1 - 1

# For 100 sats face value
amount:             100
hi_payout:          100
lo_payout:          0
```

### Test 8: Rounding behavior (conservation check)

```shell
# Range [0, 3], attested value V = 1
# This creates a ratio that doesn't divide evenly
lo_bound:           0
hi_bound:           3
attested_value:     1

# Payout calculation
clamped_V:          1
hi_payout_ratio:    0.3333...  # 1/3
lo_payout_ratio:    0.6666...  # 2/3

# For 100 sats face value
amount:             100
hi_payout:          33     # floor(100 * 1/3) = floor(33.33) = 33
lo_payout:          67     # 100 - 33 = 67 (NOT floor(100 * 2/3) = 66)
total:              100    # 33 + 67 = 100 (conservation guaranteed)

# Note: LO uses amount - floor(amount * hi_ratio), not floor(amount * lo_ratio)
# This ensures total HI + LO = amount exactly
```

## Digit-Decomposition Witness

### Test 9: Valid digit-decomposition witness

```shell
# Oracle attests to value 20000 using digit decomposition
# 5-digit number: digits are [2, 0, 0, 0, 0]
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0

# Each digit gets its own Schnorr signature using the corresponding R-value
digit_0_value:      "2"    # Most significant digit
digit_0_sig:        <64_byte_schnorr_sig_on_"2"_with_R0>
digit_1_value:      "0"
digit_1_sig:        <64_byte_schnorr_sig_on_"0"_with_R1>
digit_2_value:      "0"
digit_2_sig:        <64_byte_schnorr_sig_on_"0"_with_R2>
digit_3_value:      "0"
digit_3_sig:        <64_byte_schnorr_sig_on_"0"_with_R3>
digit_4_value:      "0"
digit_4_sig:        <64_byte_schnorr_sig_on_"0"_with_R4>

# Reconstructed value: 2*10000 + 0*1000 + 0*100 + 0*10 + 0*1 = 20000

# Witness JSON (digit_sigs format)
witness_json:       {
  "oracle_sigs": [
    {
      "oracle_pubkey": "9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0",
      "digit_sigs": [
        "<128_hex_sig_on_2>",
        "<128_hex_sig_on_0>",
        "<128_hex_sig_on_0>",
        "<128_hex_sig_on_0>",
        "<128_hex_sig_on_0>"
      ]
    }
  ]
}
```

### Test 10: Invalid digit signature

```shell
# One of the digit signatures is invalid
oracle_pubkey:      9be6fa256a022aafc98f24a71f0e37ab2ac6fe5b208a77a3d429b4b5c59f7ce0

# Digit 0 signature is invalid
digit_0_sig:        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

error_code:         13031
error_message:      "Digit signature verification failed"
```

## Redemption

### Test 11: HI holder proportional redemption

```shell
# Range [0, 100000], attested value V = 20000
# HI holder redeems 100 sats
input_keyset:       "00hi11keyset22"  # HI conditional keyset
input_amount:       100
attested_value:     20000

# HI payout = floor(100 * (20000 - 0) / (100000 - 0)) = floor(20) = 20
output_amount:      20
output_keyset:      "009a1f293253e41e"  # regular keyset

# POST /v1/redeem_outcome with digit_sigs witness
result:             PASS
```

### Test 12: LO holder proportional redemption

```shell
# Same attestation as Test 11
# LO holder redeems 100 sats
input_keyset:       "00lo33keyset44"  # LO conditional keyset
input_amount:       100
attested_value:     20000

# LO payout = 100 - floor(100 * (20000 - 0) / (100000 - 0)) = 100 - 20 = 80
output_amount:      80
output_keyset:      "009a1f293253e41e"  # regular keyset

# POST /v1/redeem_outcome with digit_sigs witness
result:             PASS
```

### Test 13: Conservation across HI and LO redemptions

```shell
# For the same attestation:
hi_input:           100 sats
lo_input:           100 sats
hi_output:          20 sats
lo_output:          80 sats

# Total collateral in:  100 sats (from original split)
# Total redeemed out:   20 + 80 = 100 sats
# Conservation:         PASS
```

## Split and Merge

### Test 14: Numeric market split

```shell
# Split 100 sats into HI and LO tokens
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": [
    {"amount": 64, "id": "009a1f293253e41e", "secret": "secret1", "C": "02..."},
    {"amount": 32, "id": "009a1f293253e41e", "secret": "secret2", "C": "02..."},
    {"amount": 4, "id": "009a1f293253e41e", "secret": "secret3", "C": "02..."}
  ],
  "outputs": {
    "HI": [
      {"amount": 64, "id": "00hi11keyset22", "B_": "03..."},
      {"amount": 32, "id": "00hi11keyset22", "B_": "03..."},
      {"amount": 4, "id": "00hi11keyset22", "B_": "03..."}
    ],
    "LO": [
      {"amount": 64, "id": "00lo33keyset44", "B_": "03..."},
      {"amount": 32, "id": "00lo33keyset44", "B_": "03..."},
      {"amount": 4, "id": "00lo33keyset44", "B_": "03..."}
    ]
  }
}

result:             PASS
```

### Test 15: Numeric market merge

```shell
# Merge HI and LO tokens back to collateral
request_json:       {
  "condition_id": "<tagged_hash_result>",
  "inputs": {
    "HI": [
      {"amount": 100, "id": "00hi11keyset22", "secret": "hi_secret_1", "C": "02..."}
    ],
    "LO": [
      {"amount": 100, "id": "00lo33keyset44", "secret": "lo_secret_1", "C": "02..."}
    ]
  },
  "outputs": [
    {"amount": 64, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 32, "id": "009a1f293253e41e", "B_": "03..."},
    {"amount": 4, "id": "009a1f293253e41e", "B_": "03..."}
  ]
}

# Standard NUT-29 merge - no oracle witness needed
result:             PASS
```

## Error Cases

### Test 16: Payout calculation overflow

```shell
# Extremely large range that could cause overflow
lo_bound:           0
hi_bound:           9999999999999999999
attested_value:     5000000000000000000

error_code:         13033
error_message:      "Payout calculation overflow"
```

[NUT-30]: ../30.md
[NUT-28]: ../28.md
[NUT-29]: ../29.md
