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

## spilman-test-vector-channel-secret-hkdf

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

## Shared Deterministic Mint Fixture

The vectors below use this real SAT keyset. It is generated directly with CDK
from the public test-only mnemonic below and MUST NOT be used for funds. This
fixture documents test data only; it does not specify Offline Spilman behavior.

```text
mint_seed_mnemonic = nut nut nut nut nut nut nut nut nut nut nut crunch
unit = sat
input_fee_ppk = 0
denominations = 1, 2, 4, ..., 2147483648
keyset_id = 01fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d
```

The complete public SAT keyset is:

```text
1=025940fded404beb21b53e2bdf8126c988b98389c7356e0b18102231999580a36c
2=02fd58fdb8a8939ab38e9ba3352167cdee914c71a3e20bdaa7df127ded477703ff
4=02a9bb3e42b765ce432a1e02bd3e5189b069416a4dd17b92a60b42335854269f60
8=02c5135a0793aebc1dde718788916fd2f763e8fa95ead4d211eacb965baeca6ae3
16=0356f90096d7bc3b34a002e5b057ddb7a44be6d6a21b1863aeb152ed248b6a03c4
32=02cfd62a904934c12c9418c0a1c729b57552ced0f2d3402064e1b3ecd60f76d912
64=03500bfa755ca5b8e97b88719de7bdd5cea3bb0fd25ce0f50e9dc7b47e19a297c6
128=0324a535f92e82a5a04b014d742e95a16b85fcf4318e5f792a6a01a87d29c7b048
256=02fd6baf9d791d5683c6801d5a9898dbed87c87f13520f5296a2e32a511f905296
512=039a25cccd5849f121ea38abd4252a78175223f91985399c7979a9c1169cf0c403
1024=03a35bd4f4bb07a470230a981960f9fb33acaa5523b6d28217d3d7cf4a14250cc8
2048=03ed874ebb9708b6d35d1f06864f19ce319efaf45543e1e8a7ab1cc27e4abab0c5
4096=032775aa538bb6252ec759b2ca6916ce400bc1f0bc2d24728cdcb7ca90fc08b946
8192=03a493c8d8c653c7bb12e0e7812b463086581537c52901b4eeb4b140470da1b323
16384=02b1aa5a46658beead8c75ffaad088f6f6b4f01525ad08eaa88d64091e3ef3878a
32768=023dc4f1fb0c22e85c10c53dbed19e8487b66b30d1b1abdf055df918f958afb096
65536=032ae7371305dcc9ad5b8749874ab8417d5d1685d91cf2f3dd38fe08f88ee34bd1
131072=030344a937f02e50dbd41a460ed65e44aa3ea94749f82d7217e26c124470749792
262144=02e902875fb29e9cef027c5f27de895b86a967684f5ad84d321fb6ad68df6087ae
524288=02adc12a3ab59b4dd077a1e7c2ddabb2c157315bd992d7bbc8d17eabdf5e351c52
1048576=035305b99c4861dc967f084d728b32c28418a52d2b731a96e958ae6079f09b5083
2097152=029d4ce4c99ca0c40f8e3086343b08df07b58f301b4695b5ab8cea7e16de36be94
4194304=03271e1cf5b9aa0d246ecc402bab0017e8bf55bd6e99045b85c0ed684bec119c3b
8388608=02d1567e5866e88bf846aee7cfb7f0219f201dd30656ed89b484d956eaa280e4e9
16777216=03edbbcea0f37e3c11113fcb1d1da120c1bc771fa1e98b8477639f5d7baad8daee
33554432=031bc3a038bb294887340ba8c7dbf520069ac1a7fc60fd67e32d248634f9b477ed
67108864=0209b736cd34ccb545bc2a9a7cb79e47fe575e2409ee9f8571dc2e776411893c70
134217728=024cd0e494ee09931b6fb860571b8dedf456c2c6928bd91b88fbd0d02105efea32
268435456=03a636f035481eb006825fed06c597d23a63db42e9068ad809d793f7ed2ab3ad8c
536870912=03e69698e1242cb31e26e447a56c19a0abfcaabc96e8e31138099d0e754cb06108
1073741824=021f8dbe172cc14b48654ce9a3b26c8945ce78e3071a3e472111267de7a674cf46
2147483648=022d410dc2dd4a4e14e4deda462afd1dd7a61a0a2a9f2d3b92b8c7b091bfd45598
```

## spilman-test-vector-channel-id

This vector defines the canonical channel-ID encoding in the [Offline Spilman
channel draft](../XX.md). Its `keyset_id` and `input_fee_ppk` are from the
Shared Deterministic Mint Fixture.

```text
mint = https://vector-mint.example
unit = sat
capacity = 100
funding_token_amount = 100
keyset_id = 01fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d
input_fee_ppk = 0
maximum_amount = 64
setup_timestamp = 1700000000
sender_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
receiver_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
expiry_timestamp = 1800000000
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
```

The exact UTF-8 SHA-256 preimage is:

```text
https://vector-mint.example|sat|100|100|01fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d|0|64|1700000000|0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798|02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5|1800000000|acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
```

```text
channel_id = SHA256(preimage) =
  7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e
```

## spilman-test-vector-channel-id-mint-trailing-slash

This vector verifies that a trailing slash in the mint URL does not affect the
channel ID. All inputs and the expected output are the same as
`spilman-test-vector-channel-id`, except:

```text
mint_input = https://vector-mint.example/
normalized_mint = https://vector-mint.example
```

The exact UTF-8 SHA-256 preimage and the expected channel ID are therefore the
same as `spilman-test-vector-channel-id`.

## spilman-test-vector-output-nonce-and-blinding

This vector covers one 64-sat output in the 100-sat funding token from
`spilman-test-vector-channel-id`. With zero fees and a maximum output amount
of 64, that funding token has outputs of 64, 32, and 4 sats. This vector does
not define the funding output's stage-1 P2PK keys; it only defines its
per-proof NUT-10 nonce and Cashu blind-signature blinding factor.

```text
channel_id = 7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
output_context = funding
amount = 64
index = 0

nonce_message =
  7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|funding|64|nonce|0
nonce_bytes = HMAC-SHA256(channel_secret, nonce_message) =
  f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a
Secret.nonce = f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a

retry_counter = 0
blinding_message =
  7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|funding|64|blinding|0|0
blinding_factor = HMAC-SHA256(channel_secret, blinding_message) =
  74285411dc702b0e295f143d026b95bd75cf730647a694e5c5b8147f619d1b35
```

The `blinding_factor` is a valid secp256k1 scalar. It is the first valid
candidate, so no retry is needed for this vector.
