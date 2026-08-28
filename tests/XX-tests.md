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

## Shared Deterministic V2 Mint Fixture

The vectors below use this real SAT keyset. It is generated directly with CDK
from the public test-only mnemonic below and MUST NOT be used for funds. This
fixture documents test data only; it does not specify Offline Spilman behavior.

```text
mint_seed_mnemonic = nut nut nut nut nut nut nut nut nut nut nut crunch
keyset_version = v2
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

## spilman-test-vector-channel-id-keysetv2

This vector defines the canonical channel-ID encoding in the [Offline Spilman
channel draft](../XX.md). Its `keyset_id` and `input_fee_ppk` are from the
Shared Deterministic V2 Mint Fixture.

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

## spilman-test-vector-channel-id-keysetv2-mint-trailing-slash

This vector verifies that a trailing slash in the mint URL does not affect the
channel ID. All inputs and the expected output are the same as
`spilman-test-vector-channel-id-keysetv2`, except:

```text
mint_input = https://vector-mint.example/
normalized_mint = https://vector-mint.example
```

The exact UTF-8 SHA-256 preimage and the expected channel ID are therefore the
same as `spilman-test-vector-channel-id-keysetv2`.

## spilman-test-vector-output-nonce-and-blinding-keysetv2

This vector covers one 64-sat output in the 100-sat funding token from
`spilman-test-vector-channel-id-keysetv2`. With zero fees and a maximum output amount
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

## spilman-test-vector-amount-selection-keysetv2

This vector selects funding-output denominations from the Shared Deterministic
V2 Mint Fixture.

```text
target = 100
maximum_amount_for_one_output = 64
selected_amounts_largest_first = 64, 32, 4
```

## spilman-test-vector-amount-selection-keysetv2-max32

This is the same V2-keyset target with a lower per-output maximum.

```text
target = 100
maximum_amount_for_one_output = 32
selected_amounts_largest_first = 32, 32, 32, 4
```

## spilman-test-vector-stage1-key-tweaks-keysetv2

This vector derives the three shared P2PK keys used by every funding proof.
Each `message` is the exact HMAC-SHA256 input. All retry counters are `0`.

```text
channel_id = 7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
prefix = Cashu_Spilman_stage1_key_tweak_v1

sender_stage1:
  original_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
  message = Cashu_Spilman_stage1_key_tweak_v17af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|sender_stage1|0
  scalar = 2c30d26a35b0d093bab0d1d58f6c70572c0c7cd82cb0ecc34d7e26a54a0eae49
  blinded_pubkey = 03da88bac82ac2731d6f4463e2d981824ea2d0e4862215bf8a422b1afe4eea6a8d

receiver_stage1:
  original_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
  message = Cashu_Spilman_stage1_key_tweak_v17af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|receiver_stage1|0
  scalar = ea4bf4110a5c73c232ea288adf577be653d334521a82f71a767fdbe66fb49614
  blinded_pubkey = 03c988d50c11fa634afdd519e2a9ce751adf29f0b17ad6251b7c199fdf9c1f7455

sender_stage1_refund:
  original_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
  message = Cashu_Spilman_stage1_key_tweak_v17af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|sender_stage1_refund|0
  scalar = 45ad552923c0cd0e988c5a929766c7da81e1b6eced096ff745a3f95b30abbc2b
  blinded_pubkey = 02d9194f39e5689e97a4f20614b09e5ec751edc41f63d0bde6fc39d7dfeba74760
```

## spilman-test-vector-funding-outputs-keysetv2

This vector combines the 100-sat amount-selection and stage-1 vectors. Outputs
are in Cashu smallest-first order. Each secret is the NUT-10 P2PK JSON with
the shared `data`, `pubkeys`, `locktime`, `n_sigs`, `refund`,
`n_sigs_refund`, and `sigflag = SIG_ALL` fields defined above; only `nonce`
varies by output.

```text
keyset_id = 01fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d

amount = 4
index = 0
secret = ["P2PK",{"data":"03da88bac82ac2731d6f4463e2d981824ea2d0e4862215bf8a422b1afe4eea6a8d","nonce":"e9aad80a4e747e570bb68cff4f8a33f8c2d904f424e695f9e2febf92bbd4fb30","tags":[["pubkeys","03c988d50c11fa634afdd519e2a9ce751adf29f0b17ad6251b7c199fdf9c1f7455"],["locktime","1800000000"],["n_sigs","2"],["refund","02d9194f39e5689e97a4f20614b09e5ec751edc41f63d0bde6fc39d7dfeba74760"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = e9aad80a4e747e570bb68cff4f8a33f8c2d904f424e695f9e2febf92bbd4fb30
blinding_factor = 89d7fc20c07229e615c9365c83b70938566037c55fe61c102afee78ff44fab66
blinded_message = 027e3b02f160f2d75b276bd411821a2fc66bd3ba4aed5fc23b9a88e472dd641134

amount = 32
index = 0
secret = ["P2PK",{"data":"03da88bac82ac2731d6f4463e2d981824ea2d0e4862215bf8a422b1afe4eea6a8d","nonce":"879abe0662d57e86ec39d715103c1c95814780b29752c01aadb0888b92d3c081","tags":[["pubkeys","03c988d50c11fa634afdd519e2a9ce751adf29f0b17ad6251b7c199fdf9c1f7455"],["locktime","1800000000"],["n_sigs","2"],["refund","02d9194f39e5689e97a4f20614b09e5ec751edc41f63d0bde6fc39d7dfeba74760"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = 879abe0662d57e86ec39d715103c1c95814780b29752c01aadb0888b92d3c081
blinding_factor = 932933b55f73dfc76c8fd04e671360e46fc2be33878e83ebde17a5c48651744c
blinded_message = 034e10f284aceb8d8a316105f2533583c7f4e5ea6b2102f276403d061f1ee9460f

amount = 64
index = 0
secret = ["P2PK",{"data":"03da88bac82ac2731d6f4463e2d981824ea2d0e4862215bf8a422b1afe4eea6a8d","nonce":"f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a","tags":[["pubkeys","03c988d50c11fa634afdd519e2a9ce751adf29f0b17ad6251b7c199fdf9c1f7455"],["locktime","1800000000"],["n_sigs","2"],["refund","02d9194f39e5689e97a4f20614b09e5ec751edc41f63d0bde6fc39d7dfeba74760"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a
blinding_factor = 74285411dc702b0e295f143d026b95bd75cf730647a694e5c5b8147f619d1b35
blinded_message = 03fb84f24c1bb271786a89aaeaff334c36db02bde6e1f9607d69f94db907b48bbf
```

## spilman-test-vector-stage2-p2bk-keysetv2

This vector fixes the NUT-28 derivation for the commitment-output `(amount,
index) = (32, 0)` slot. Both entries use the channel ID and channel secret from
`spilman-test-vector-channel-id-keysetv2`; both scalar retry counters are zero.

```text
amount = 32
index = 0

context = receiver_stage2
recipient_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
ephemeral_secret = dc2029be89e39a26f5a49653a7de750807002f9549f4774ed8c6376d1cf4bc7b
p2pk_e = 02224366f001c35581b8316a62160d4e5733f102757a1a824d8e41a9ad795d5a90
shared_secret_x = e5198d9a589490993b1edd9c5bf76e31bf9610bdca088654fb2d654b62a0085d
p2bk_scalar = 51db52022fe771a7e084346852a2115fbefd204efe4fb6c5e94cd3844c718e75
blinded_pubkey = 0397dfedc39293131c2d4c5f76169001e2b11057284dc9345e8178f3ce035660df

context = sender_stage2
recipient_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
ephemeral_secret = b0a12b2dc14d71c23a27c02d35ebde1eccdc50984fac5b4597099cc653a6d69b
p2pk_e = 02a1be7b930f67d26fd168214a18f5c208cb21cda5f6f08bbf61930cae109d5a39
shared_secret_x = a1be7b930f67d26fd168214a18f5c208cb21cda5f6f08bbf61930cae109d5a39
p2bk_scalar = 891005d4ef10bee9b46144fec3d81f051e8d5db42c6078f60a0fd1ad0c4798db
blinded_pubkey = 023725a2912497df0d49de8269b778e664b917e6c919e122fd099e2e99be03f1af
```

## spilman-test-vector-commitment-outputs-keysetv2

This vector uses the zero-fee 100-sat channel and a 50-sat receiver balance.
Receiver and sender each receive deterministic amounts `2 + 16 + 32`. Each
`secret` is the exact canonical UTF-8 JSON string defined by NUT-XX; every
tagless secret uses `"tags":[]`.

```text
keyset_id = 01fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d
receiver_balance = 50

context = receiver
amount = 2
index = 0
secret = ["P2PK",{"data":"03aae5610f300463773890d489bc8638324b7d9966c6aec461b9afe2859cf2be9f","nonce":"008b267f22e9da9672d141c6ca72f069c464e1863909d82e4ccdd0fbca0fe658","tags":[]}]
p2pk_e = 0254f06f28d614849f7e90c53171b194c358a625864cdf26fec99c78553c6781c5
blinding_factor = 9c9107c949e3bb007439519cad428379702bfac828b33fcad7a5b885ba2a95bf
blinded_message = 033a81f9199fda2d0b6955a4114cd2ddffc52b2ddf89197b5a04bd806c8843399e

context = receiver
amount = 16
index = 0
secret = ["P2PK",{"data":"03f8d7134afdf587bf8d40d79ae4aab8905e3a2bb378493a46de13daadff24a2b4","nonce":"fe4ac5c03c0dca0ef9af528fddb8975558d03ae7a7f73a93e3718d6f52f4c2f0","tags":[]}]
p2pk_e = 029927a0192b8c65ad0e4ddbfcb476b4f9f6c4deb8746a4810eb767cfa81d62195
blinding_factor = 3bc38b19a49bc506cee66eca9a779dcb4fc132aea294713150532fae82152e39
blinded_message = 03dc893fd2f3a9509d2f0ed30459aff829cede98826aea0a6ee7a80948c2d74e32

context = receiver
amount = 32
index = 0
secret = ["P2PK",{"data":"0397dfedc39293131c2d4c5f76169001e2b11057284dc9345e8178f3ce035660df","nonce":"0c640e9c0e7b5c13d519e6a5dbae6d84fc8b71a2da736689fd950606aa3abd07","tags":[]}]
p2pk_e = 02224366f001c35581b8316a62160d4e5733f102757a1a824d8e41a9ad795d5a90
blinding_factor = de8dedd0c3484e02422ee298d7fa97cca44b80d82d7c6b7ab33743aa32d78e3d
blinded_message = 024e661853c27f2e83300b1ad45c85290861a6eb2d8567ae6595eb6e582770ddf1

context = sender
amount = 2
index = 0
secret = ["P2PK",{"data":"02ff4d525e601d93409a27b86704fd4fef883bba75729cf88eb2e8d59de3a55c58","nonce":"a5a204390c60cca38988fcedc3f77bef1f32272cef922082f3a8cb8de6fbc73d","tags":[]}]
p2pk_e = 028db3f60a69b312696ca1e54e49a0ea3b9b1aaaf3c1405b412333ac07771707de
blinding_factor = 2c0d9ab01f983f1610a9f8a9b1a3773923bda5e8938b5a15b89c13f02ea0ccd9
blinded_message = 02cf1e71062b1e7ff01986cd0160174c7b039b4b94cd0ef5e1518fe776a1b3154d

context = sender
amount = 16
index = 0
secret = ["P2PK",{"data":"039da1bb99af72c4e3359961d06a27fcba0b09c6e9ced64682c5c58f8166df06b5","nonce":"fa5eac4d875dbb343a5840d62a9b6fd0b90d1ee08f1a0b627ba7767c0c622881","tags":[]}]
p2pk_e = 02f7895660f690f1d498e2f215a7e6de772407b954d09b75e579ed4a284c3a28f7
blinding_factor = 603d1b5b9c66de9a5144c19bbac91e943feccb8d5d408c7a1ce4092bc5bd4b8f
blinded_message = 02a2f5005d6b714b9c35e9806a9c9f45fd6d7055a112e4f22551c555ccb945d550

context = sender
amount = 32
index = 0
secret = ["P2PK",{"data":"023725a2912497df0d49de8269b778e664b917e6c919e122fd099e2e99be03f1af","nonce":"d19c3e67ae5c9aa3d737ccd349cb83c8f384ec5940d166238da8eef54fcd0cfe","tags":[]}]
p2pk_e = 02a1be7b930f67d26fd168214a18f5c208cb21cda5f6f08bbf61930cae109d5a39
blinding_factor = df1c0c9bb910d9dcbace8fa188e38c72ec9e90474b9c574d789aa45b1c31b530
blinded_message = 035ff45bffcec127d65c52aad3fd866591cfd6cdb24cfc95761c1faed0647e1fb5

stable_swap_output_order =
  receiver:2, sender:2, receiver:16, sender:16, receiver:32, sender:32
```

## spilman-test-vector-sig-all-keysetv2

This vector fixes the NUT-11 `SIG_ALL` message for the 50-sat receiver-balance
commitment swap above. The three funding inputs are ordered `4, 32, 64`; use
their complete `secret` strings from
`spilman-test-vector-funding-outputs-keysetv2` in that order.

The funding-proof `C` values are valid unblinded signatures from the shared
deterministic V2 test mint. DLEQ proofs are not part of this Spilman vector;
their generation and verification are defined by NUT-12.

```text
funding_input_0_amount = 4
funding_input_0_C = 028d2b7d1215b72c2b23d51563fb0d61e3652b87a77ceb3b237df1b9f46b0d044f
funding_input_1_amount = 32
funding_input_1_C = 02de5cb101e677403e4658d615e1a665db787558cccd09ff93a65983fa48fcecfd
funding_input_2_amount = 64
funding_input_2_C = 03bb199086ab2d33ce69cc80a007b48350fb13ce669af96be24f44613e9d0013b7

commitment_outputs_in_order =
  2|033a81f9199fda2d0b6955a4114cd2ddffc52b2ddf89197b5a04bd806c8843399e,
  2|02cf1e71062b1e7ff01986cd0160174c7b039b4b94cd0ef5e1518fe776a1b3154d,
  16|03dc893fd2f3a9509d2f0ed30459aff829cede98826aea0a6ee7a80948c2d74e32,
  16|02a2f5005d6b714b9c35e9806a9c9f45fd6d7055a112e4f22551c555ccb945d550,
  32|024e661853c27f2e83300b1ad45c85290861a6eb2d8567ae6595eb6e582770ddf1,
  32|035ff45bffcec127d65c52aad3fd866591cfd6cdb24cfc95761c1faed0647e1fb5

sig_all_message_sha256 = e070783478edcc7917e26ee2c2b9befc67f5ffc389304519f532d980bc4b5532
```

The concatenated message is signed by Alice's stage-1 blinded key for each
balance update. Charlie signs the identical message with his stage-1 blinded
key when submitting the close swap. Schnorr signature bytes are not fixed by
this vector because NUT-11 signatures are nondeterministic.
