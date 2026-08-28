# Offline Spilman Channel Test Vectors

## Reference Implementations

Each named test vector in this file is exercised by two independent test
layers in
[`cashu_spilman_channels`](https://github.com/SatsAndSports/cashu_spilman_channels):

- [`spilman-test-vectors`](https://github.com/SatsAndSports/cashu_spilman_channels/tree/main/crates/spilman-test-vectors)
  contains a clean-room reference derivation used to generate and verify the
  fixed vector values.
- [`cdk-spilman` compatibility tests](https://github.com/SatsAndSports/cashu_spilman_channels/blob/main/crates/cdk-spilman/tests/spilman_test_vectors.rs)
  verify that production code derives the same values.

The test names use the exact vector names from this file.

## spilman-test-vector-channel-secret-hkdf-v1-001

This vector defines the channel-secret derivation in the [Offline Spilman
channel draft](../XX.md). The private keys below are fixed public test inputs
only and MUST NOT be used for funds.

```text
alice_secret_key_hex =
  0000000000000000000000000000000000000000000000000000000000000001

charlie_secret_key_hex =
  0000000000000000000000000000000000000000000000000000000000000002

alice_public_key_compressed_sec1_hex =
  0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798

charlie_public_key_compressed_sec1_hex =
  02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5

shared_point_compressed_sec1_hex =
  02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5

dh = SHA256(compressed_SEC1(alice_secret_key * charlie_public_key)) =
  b1c9938f01121e159887ac2c8d393a22e4476ff8212de13fe1939de2a236f0a7

hkdf_hash = SHA-256
hkdf_salt = empty byte string
hkdf_ikm = dh
hkdf_info_utf8 = Cashu_Spilman_channel_secret_v1
hkdf_length = 32

channel_secret =
  acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
```

Charlie obtains the same `shared_point`, `dh`, and `channel_secret` from
`charlie_secret_key * alice_public_key`.
