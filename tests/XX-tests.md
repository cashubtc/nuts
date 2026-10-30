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
nonce_bytes is a valid nonzero secp256k1 scalar, so no retry is used.
Secret.nonce = f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a

blinding_message =
  7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|funding|64|blinding|0
blinding_factor = HMAC-SHA256(channel_secret, blinding_message) =
  95066df465e8e73f5d56df3bcf010ed7c8cc473b0e68ada8bb51589f31009618
```

The `blinding_factor` is a valid secp256k1 scalar, so no retry is needed for
this vector.

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
Each `message` is the exact HMAC-SHA256 input.

```text
channel_id = 7af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
prefix = Cashu_Spilman_stage1_key_tweak_v1

sender_stage1:
  original_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
  message = Cashu_Spilman_stage1_key_tweak_v17af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|sender_stage1
  scalar = 08bcce7d4847ab4ed33c737431cfe6f6aeba419edd418cae80e12178221296e9
  blinded_pubkey = 02516479c6dee216722f477dcc5ecddb6a793fa7aaf7d8d2b887f45dc6ff96faee

receiver_stage1:
  original_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
  message = Cashu_Spilman_stage1_key_tweak_v17af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|receiver_stage1
  scalar = 0f1bf68bab1e80af962b49eec1f2dc479c3bff3d093e8d2ad9c4c475713cada9
  blinded_pubkey = 02b37243d00583b225e1f5dc23a48a7568b09eec889bfa45c20fc865de7309b2a9

sender_stage1_refund:
  original_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
  message = Cashu_Spilman_stage1_key_tweak_v17af675f4f1b9843200d23060ebeb5bf5abea67fa511af79aefa4ba6a19b88c2e|sender_stage1_refund
  scalar = 956ac1d4ed35bf4abf97b2177053c50ca66e9e1d614dd3934b2374fa1bda5f2e
  blinded_pubkey = 022055ae1c0cba2f9cb756b4779276c8e061fe9ccd286c43a91b4164d265fcfbe8
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
secret = ["P2PK",{"data":"02516479c6dee216722f477dcc5ecddb6a793fa7aaf7d8d2b887f45dc6ff96faee","nonce":"e9aad80a4e747e570bb68cff4f8a33f8c2d904f424e695f9e2febf92bbd4fb30","tags":[["pubkeys","02b37243d00583b225e1f5dc23a48a7568b09eec889bfa45c20fc865de7309b2a9"],["locktime","1800000000"],["n_sigs","2"],["refund","022055ae1c0cba2f9cb756b4779276c8e061fe9ccd286c43a91b4164d265fcfbe8"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = e9aad80a4e747e570bb68cff4f8a33f8c2d904f424e695f9e2febf92bbd4fb30
blinding_factor = d8d6d77cfe64154981bc10bfbb96987c27353f1854e3b977543e5c92ff91ffef
blinded_message = 036a453cdf46b2abdb52d72c591152199bd386f79dd00c322f2e2d776b0c9ec16a

amount = 32
index = 0
secret = ["P2PK",{"data":"02516479c6dee216722f477dcc5ecddb6a793fa7aaf7d8d2b887f45dc6ff96faee","nonce":"879abe0662d57e86ec39d715103c1c95814780b29752c01aadb0888b92d3c081","tags":[["pubkeys","02b37243d00583b225e1f5dc23a48a7568b09eec889bfa45c20fc865de7309b2a9"],["locktime","1800000000"],["n_sigs","2"],["refund","022055ae1c0cba2f9cb756b4779276c8e061fe9ccd286c43a91b4164d265fcfbe8"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = 879abe0662d57e86ec39d715103c1c95814780b29752c01aadb0888b92d3c081
blinding_factor = 8952cedabe7d95af9d8388373e1bc2d8cb8897a4e59a5b3c0d3c7e93d2059b0f
blinded_message = 02be9df107c01a2e33640bc229b673b71dccdee427c4e417c83c39f585abfb5dc6

amount = 64
index = 0
secret = ["P2PK",{"data":"02516479c6dee216722f477dcc5ecddb6a793fa7aaf7d8d2b887f45dc6ff96faee","nonce":"f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a","tags":[["pubkeys","02b37243d00583b225e1f5dc23a48a7568b09eec889bfa45c20fc865de7309b2a9"],["locktime","1800000000"],["n_sigs","2"],["refund","022055ae1c0cba2f9cb756b4779276c8e061fe9ccd286c43a91b4164d265fcfbe8"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = f934dd4311715f9e9af3d338c2b7235581a779f748839ffbfe584b0c1e21e37a
blinding_factor = 95066df465e8e73f5d56df3bcf010ed7c8cc473b0e68ada8bb51589f31009618
blinded_message = 02529111ff074c0e7503ab7f299c6221702a77c40354ad5f3e38c7cb61a9dc2c83
```

## spilman-test-vector-stage2-p2bk-keysetv2

This vector fixes the NUT-28 derivation for the commitment-output `(amount,
index) = (32, 0)` slot. Both entries use the channel ID and channel secret from
`spilman-test-vector-channel-id-keysetv2`.

```text
amount = 32
index = 0

context = receiver_stage2
recipient_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
ephemeral_secret = 6736788d5e1325a6ad0aec521c673c80db323ae9cb6e756252d190f658a49da4
p2pk_e = 03b95460565471b30d35b7b96cb632391c680806dad65379a3bf93e5a66dcc936f
shared_secret_x = 0b205af6f661eb73197e71666e46f8d7acb03dbe79734d5eb6056b3efa9c5c95
p2bk_scalar = 40f12c7792828472b303dec3ffd759c374b7646fa73182f737eb4c45a3c9cd61
blinded_pubkey = 02270ea899810d2f4064d4df8bfc356b5706ba8e236c93c1963f620c14794ad601

context = sender_stage2
recipient_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
ephemeral_secret = 17809cf637c793619c16f1a26a641ec05cc35237205da5c2c705fe0942e51df5
p2pk_e = 03600d205df80cea1ea916c7a3ea98009a001483aa4a35cfb96ca20ce707f58a74
shared_secret_x = 600d205df80cea1ea916c7a3ea98009a001483aa4a35cfb96ca20ce707f58a74
p2bk_scalar = b0706b1fa1e4c0865243c94e7a114ff6b0f5a16664240d90308b1d04023c9704
blinded_pubkey = 03b5b9b73e75d63ff6a43093ed2604fb056aa932620a80940e25a1d1de4455264f
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
secret = ["P2PK",{"data":"03976217324d65dd310860c16ed0ab60b9bb2a7e6bf9354d1d204899f17d6b1e12","nonce":"008b267f22e9da9672d141c6ca72f069c464e1863909d82e4ccdd0fbca0fe658","tags":[]}]
p2pk_e = 035ccec34674ef9771472cdb1140a30d288a76040b9a402be53638866d3369ab2b
blinding_factor = 42a8442f1f234b0fd8727e653fc69ff73e66ea3c84b7689a76339d9ab3ff07bf
blinded_message = 0225d53d34dfeec3151295621c0094165dd3d94bf4d0f7cf9f4bcd946a94eaaab5

context = receiver
amount = 16
index = 0
secret = ["P2PK",{"data":"0355c22359dc1ab7f5c2f3bc90149f949aaffea848f38d3bba967a48d3776ad537","nonce":"fe4ac5c03c0dca0ef9af528fddb8975558d03ae7a7f73a93e3718d6f52f4c2f0","tags":[]}]
p2pk_e = 02010f9d212bcdece828a68524d97ebe6c4506df314efb7ce0070d04f5084dc2bf
blinding_factor = 3a793efb2d8332e71a04a4f126ebdf7622546583a25f555dbd028a871858c55e
blinded_message = 02686997630f52fd739d62b94cd14358f1d4ba5daf3a6d6c3b10ee4479938ccdea

context = receiver
amount = 32
index = 0
secret = ["P2PK",{"data":"02270ea899810d2f4064d4df8bfc356b5706ba8e236c93c1963f620c14794ad601","nonce":"0c640e9c0e7b5c13d519e6a5dbae6d84fc8b71a2da736689fd950606aa3abd07","tags":[]}]
p2pk_e = 03b95460565471b30d35b7b96cb632391c680806dad65379a3bf93e5a66dcc936f
blinding_factor = acdd0fcfceef385b839d58b70d27dae12d708729e4efefe31f63420c101fae3f
blinded_message = 02160974d3b2928f741ce5833309d8c572faf4ce64aeb620e7163f34fcd82dff55

context = sender
amount = 2
index = 0
secret = ["P2PK",{"data":"02493df89ad25a74a098b302fdd225344189cb2865c6d1edc2fcd730384888d246","nonce":"a5a204390c60cca38988fcedc3f77bef1f32272cef922082f3a8cb8de6fbc73d","tags":[]}]
p2pk_e = 0378728c7baf110d9336a9ed523cf49c94473c30f0909cf5d8edfb5ab42a823add
blinding_factor = 8c525518a63808137e793b3fdd1491b745e737b0cabb42047337825c717cd40a
blinded_message = 032bf5de6d21526305149bc2e08424ed024f74a644409f637902154b28dd2b7278

context = sender
amount = 16
index = 0
secret = ["P2PK",{"data":"02b49021bc36f31cc22f4ee2b70dab41e5900b8d7681e6d415fdf0db2231c55ada","nonce":"fa5eac4d875dbb343a5840d62a9b6fd0b90d1ee08f1a0b627ba7767c0c622881","tags":[]}]
p2pk_e = 030642bc7f978e74851befc286198a5121b909baf11f90c7b2db0b318062b0e5a9
blinding_factor = 5c8fbc6e15ed4b6ecf8ba42485db5cf8b4cd44840c60a12c2de289041163536f
blinded_message = 02a30cde253b234c36193de2b5b91254255ef42250b51628ca856bcebba76f4ecb

context = sender
amount = 32
index = 0
secret = ["P2PK",{"data":"03b5b9b73e75d63ff6a43093ed2604fb056aa932620a80940e25a1d1de4455264f","nonce":"d19c3e67ae5c9aa3d737ccd349cb83c8f384ec5940d166238da8eef54fcd0cfe","tags":[]}]
p2pk_e = 03600d205df80cea1ea916c7a3ea98009a001483aa4a35cfb96ca20ce707f58a74
blinding_factor = 51a394d16ba49c82f05813628ec414ab082198c9c7136b352df13b828244f00c
blinded_message = 03c652d5f40b395d33be28c1547761101cf9f0c65c995b2f701644cb43966d42e0

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
funding_input_0_C = 03324f2f0c4961e71397999bb072623d53e05276faf6e377aff1e04c8fc89757f0
funding_input_1_amount = 32
funding_input_1_C = 0396b23d7ddc18f2f2f0a47c464d0316bd65011d1e96605c2d653272cd5955f04b
funding_input_2_amount = 64
funding_input_2_C = 03ce7ca88ba5cdc6999008b6395feaf372a628587203a974ca1a284f3d019e6484

commitment_outputs_in_order =
  2|0225d53d34dfeec3151295621c0094165dd3d94bf4d0f7cf9f4bcd946a94eaaab5,
  2|032bf5de6d21526305149bc2e08424ed024f74a644409f637902154b28dd2b7278,
  16|02686997630f52fd739d62b94cd14358f1d4ba5daf3a6d6c3b10ee4479938ccdea,
  16|02a30cde253b234c36193de2b5b91254255ef42250b51628ca856bcebba76f4ecb,
  32|02160974d3b2928f741ce5833309d8c572faf4ce64aeb620e7163f34fcd82dff55,
  32|03c652d5f40b395d33be28c1547761101cf9f0c65c995b2f701644cb43966d42e0

sig_all_message_sha256 = 917319d409c84dccb0d21fe31a6129bbd34c5db72c9757d3a2522eadca030189
```

The concatenated message is signed by Alice's stage-1 blinded key for each
balance update. Charlie signs the identical message with his stage-1 blinded
key when submitting the close swap. Schnorr signature bytes are not fixed by
this vector because NUT-11 signatures are nondeterministic.
