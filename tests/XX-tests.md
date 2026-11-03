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
sender_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
receiver_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
setup_timestamp = 1700000000
expiry_timestamp = 1800000000
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
```

The exact canonical TLV records are:

```text
type 0,  length 1:  01
type 2,  length 27: 68747470733a2f2f766563746f722d6d696e742e6578616d706c65
type 4,  length 3:  736174
type 6,  length 1:  64
type 8,  length 1:  64
type 10, length 33: 01fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d
type 12, length 0:  <empty>
type 14, length 1:  40
type 16, length 33: 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
type 18, length 33: 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
type 20, length 4:  6553f100
type 22, length 4:  6b49d200
type 24, length 32: acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
```

The exact TLV stream, including each `bigsize(type)` and `bigsize(length)`, is:

```text
000101021b68747470733a2f2f766563746f722d6d696e742e6578616d706c6504037361740601640801640a2101fd5a9250eb619ce33b33bf6e752634a5a8ca4bb629c6b48a99db9c94d09d310d0c000e014010210279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798122102c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee514046553f10016046b49d2001820acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
```

```text
channel_id = tagged_SHA256("Cashu_Spilman_channel_id", tlv_stream) =
  22d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781
```

## spilman-test-vector-channel-id-keysetv2-mint-trailing-slash

This vector verifies that a trailing slash in the mint URL does not affect the
channel ID. All inputs and the expected output are the same as
`spilman-test-vector-channel-id-keysetv2`, except:

```text
mint_input = https://vector-mint.example/
normalized_mint = https://vector-mint.example
```

The exact TLV stream and the expected channel ID are therefore the
same as `spilman-test-vector-channel-id-keysetv2`.

## spilman-test-vector-output-nonce-and-blinding-keysetv2

This vector covers one 64-sat output in the 100-sat funding token from
`spilman-test-vector-channel-id-keysetv2`. With zero fees and a maximum output amount
of 64, that funding token has outputs of 64, 32, and 4 sats. This vector does
not define the funding output's stage-1 P2PK keys; it only defines its
per-proof NUT-10 nonce and Cashu blind-signature blinding factor.

```text
channel_id = 22d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
output_context = funding
amount = 64
index = 0

nonce_message =
  22d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781|funding|64|nonce|0
nonce_bytes = HMAC-SHA256(channel_secret, nonce_message) =
  872b3ae7294249e7bb7a5351623b3a8a400820f5af294cf7f74888eb55a22273
nonce_bytes is a valid nonzero secp256k1 scalar, so no retry is used.
Secret.nonce = 872b3ae7294249e7bb7a5351623b3a8a400820f5af294cf7f74888eb55a22273

blinding_message =
  22d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781|funding|64|blinding|0
blinding_factor = HMAC-SHA256(channel_secret, blinding_message) =
  9f395ca331cf075dd3a651037a088b99a76c60a3e49ecda22905e5eff7f92f18
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
channel_id = 22d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781
channel_secret = acfc96a584e645524b017b75cfe0770c3b8dc2ba4f9cef6d99f2cb7bcee691cf
prefix = Cashu_Spilman_stage1_key_tweak_v1

sender_stage1:
  original_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
  message = Cashu_Spilman_stage1_key_tweak_v122d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781|sender_stage1
  scalar = c91d056874abe1711778d9674158b43b42ac6754e58072431627ef8dce944218
  blinded_pubkey = 025032d5e99037ddabf57564ebd03e79994bd86d77f47302ca81eca7e8555dd80b

receiver_stage1:
  original_pubkey = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
  message = Cashu_Spilman_stage1_key_tweak_v122d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781|receiver_stage1
  scalar = 983b646d09e66356f4a1fd6d5f8189c0a59a4412db772e5a13dca08804d01ff6
  blinded_pubkey = 035ab3f5c8bfd229dfddf3d6bd0f4c6a7470c43f3c864f8e4121d6ac86a16e43e4

sender_stage1_refund:
  original_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
  message = Cashu_Spilman_stage1_key_tweak_v122d8063ac8592223c0cb20d9da883787382db861569c0aa84f664ae75c641781|sender_stage1_refund
  scalar = 67def3cde1286293b89db06d5797741c4cbb89a7dd5deb43aca30dfb2c1f6f11
  blinded_pubkey = 0262059f95d1ac59f34a29f9e9d5c26b414e1921b0b76d5f162b54d67d0540a72d
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
secret = ["P2PK",{"data":"025032d5e99037ddabf57564ebd03e79994bd86d77f47302ca81eca7e8555dd80b","nonce":"cd4bfbda7d1d630ba93d4027eb37fcde4cdcf886809b4a1d38af6b26dc5fdf67","tags":[["pubkeys","035ab3f5c8bfd229dfddf3d6bd0f4c6a7470c43f3c864f8e4121d6ac86a16e43e4"],["locktime","1800000000"],["n_sigs","2"],["refund","0262059f95d1ac59f34a29f9e9d5c26b414e1921b0b76d5f162b54d67d0540a72d"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = cd4bfbda7d1d630ba93d4027eb37fcde4cdcf886809b4a1d38af6b26dc5fdf67
blinding_factor = 08333c12d6cacac3bb9b53ac724d9cc53ee2bead9b8380353335916a7094f9a0
blinded_message = 03d3c8c76a78f1cdb3cdb4a392f77afe1d9a4f19e1681afcffe7cc013ac20d8873

amount = 32
index = 0
secret = ["P2PK",{"data":"025032d5e99037ddabf57564ebd03e79994bd86d77f47302ca81eca7e8555dd80b","nonce":"7f3dd5bc167eb0a52c0a8fc3a02aacd79520ae5d825974dfb25cc913d21a0955","tags":[["pubkeys","035ab3f5c8bfd229dfddf3d6bd0f4c6a7470c43f3c864f8e4121d6ac86a16e43e4"],["locktime","1800000000"],["n_sigs","2"],["refund","0262059f95d1ac59f34a29f9e9d5c26b414e1921b0b76d5f162b54d67d0540a72d"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = 7f3dd5bc167eb0a52c0a8fc3a02aacd79520ae5d825974dfb25cc913d21a0955
blinding_factor = 47f8a37dba6dd9962f324aa46071f75ee290bae336ef341fc9e10ab7b7ac4a2d
blinded_message = 02b852b64fd1fcdd6c8e8aa0bd4609ab2925d9dc588b2a883123c7ab27d1a54503

amount = 64
index = 0
secret = ["P2PK",{"data":"025032d5e99037ddabf57564ebd03e79994bd86d77f47302ca81eca7e8555dd80b","nonce":"872b3ae7294249e7bb7a5351623b3a8a400820f5af294cf7f74888eb55a22273","tags":[["pubkeys","035ab3f5c8bfd229dfddf3d6bd0f4c6a7470c43f3c864f8e4121d6ac86a16e43e4"],["locktime","1800000000"],["n_sigs","2"],["refund","0262059f95d1ac59f34a29f9e9d5c26b414e1921b0b76d5f162b54d67d0540a72d"],["n_sigs_refund","1"],["sigflag","SIG_ALL"]]}]
nonce = 872b3ae7294249e7bb7a5351623b3a8a400820f5af294cf7f74888eb55a22273
blinding_factor = 9f395ca331cf075dd3a651037a088b99a76c60a3e49ecda22905e5eff7f92f18
blinded_message = 02ecc9ac363e78600d4b4dc84908d899e7c7eba9f5b93aa5c5d3bf5d7548319b50
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
ephemeral_secret = d79f3c31c57af70666f5027c50a9937b62f0473fdb7ca9af9ae9f5a37d61d44c
p2pk_e = 0340c8ee89ad2f338ea2d6500527e1c9ffd97557567d3a4748ffa6961ec2d77e20
shared_secret_x = eb9412b52bcc6054eb9390f8ddb674bd8e9a1cc77c596f7b99c16a6e8c796d37
p2bk_scalar = 951b4a015a54c64120953f11d2084b3bbd505db9b7e3c0f1e07516ab7115cc77
blinded_pubkey = 027d9a5bc962b7c0dbb6032556d6575707e02e5133e9fc6cb8c4c79a9163e02219

context = sender_stage2
recipient_pubkey = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
ephemeral_secret = bce31ccf7f2e3ccd4f3d56101dccf0b9f66bb8802f0d9771a6eeeec9ccad6903
p2pk_e = 0227f12894d245777fbc258e8a1fc36a8af80d1bca020b3effdd3ed9b4edf9175f
shared_secret_x = 27f12894d245777fbc258e8a1fc36a8af80d1bca020b3effdd3ed9b4edf9175f
p2bk_scalar = 612685c011c734555acc7632212d783178aadb09f5a169ffb4df1dd6ec2f2910
blinded_pubkey = 02f04dbe714c4e574b656448843c816516674ed63ff4bda3970e8df7a203892abf
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
secret = ["P2PK",{"data":"0395499a0b6977b755bd762b394dfea023e6829449989209b852e2baef3d5acc04","nonce":"e7cd816bb2de9369901c3d058915cb08e64141df5fed1e7f816591463680ca29","tags":[]}]
p2pk_e = 03f83f09c1b594b8c959865ac9187bc84794867cf1f1f6d5f23e9fe39b5cc62823
blinding_factor = 997f96b9970fbbdfb5ad707a0678aca7f852234019a4ebfce78b03a5d5534005
blinded_message = 02edb30c85ffdf26a839211cb8fdb6e66a2683b63d3a219c18cda91a06ec6a8bf2

context = receiver
amount = 16
index = 0
secret = ["P2PK",{"data":"03968acd8b22c3da2f7dfd82418ae566dd4f832d96992f9ccbd9f698c1bf07c0ba","nonce":"82a7afe482d3bacc1f8cc2c6d05445ee2ecec26499698c2934b3685beb363080","tags":[]}]
p2pk_e = 033fcbf07fdeeafc79176cfa5b3084775c55d7a4244413b13519b53b7ebcc87983
blinding_factor = 8db1bc3dbd5b32a51d99d6ba0e91aaf9df2449aa27b70e12b3a8b065db409c44
blinded_message = 03a19de7bde70cd3da6da9c0249c8a4cd4240a20717e7144852c861b8290e9e4c7

context = receiver
amount = 32
index = 0
secret = ["P2PK",{"data":"027d9a5bc962b7c0dbb6032556d6575707e02e5133e9fc6cb8c4c79a9163e02219","nonce":"3de4b352b152e9f42a0bf1a80a2074c808022b85423839ceb962fc163ab5ccb1","tags":[]}]
p2pk_e = 0340c8ee89ad2f338ea2d6500527e1c9ffd97557567d3a4748ffa6961ec2d77e20
blinding_factor = 645c826ab04b1d7270f10d7c403c3ba8eea43252484ce9f0342720de35d75674
blinded_message = 03f0aad58d35ce66a5079fe9d24ff8862a04d7ffdcd6683773e80a67f6f2e461e0

context = sender
amount = 2
index = 0
secret = ["P2PK",{"data":"030b30774438c74441f23c2ac465d417bcd8ea843540e4e2966347b314d6a426dc","nonce":"1c2ea5c4c211ca037ccd134f0fa4feeb52751c73f4cfcbe25fd04a9a12881436","tags":[]}]
p2pk_e = 03060bb9b3f46ec85a8c3e2c6b9eb4aa4d342fb77f12a4bbf5f20d601630faf9eb
blinding_factor = 4cce8c264871220521a6ca7fa0e61e4af38348629d205e984228d378ae5fdc6a
blinded_message = 02432306a375dabf1d699278ad5ed5e7a0659c6b1ec7dd2fb924c86534a6cb534b

context = sender
amount = 16
index = 0
secret = ["P2PK",{"data":"03f9c0f1e4a8c06d8210786dcbcb2f476953d523406eed124bb6c64d2654e81c4e","nonce":"20790520e7ff1e36a0150443664111fee2496cc07632464387ae3ff6735ea80c","tags":[]}]
p2pk_e = 026b9a9bfd5f6f1720eb96a808d7937bf49ada33fc067cb751ab8bbe400ea37e3b
blinding_factor = 749bf464cf293c7d9fc181894e946498587251d6a39c6e4242bac03c715ec237
blinded_message = 02f8b5fc29575571508b6d0e503da0c4f298dc71098fb8d28c0f27fe82ae8e8a5a

context = sender
amount = 32
index = 0
secret = ["P2PK",{"data":"02f04dbe714c4e574b656448843c816516674ed63ff4bda3970e8df7a203892abf","nonce":"097a16413a89691abc4c196437b6d174a5b737d9e59d9e53d19e35e1e934e7d3","tags":[]}]
p2pk_e = 0227f12894d245777fbc258e8a1fc36a8af80d1bca020b3effdd3ed9b4edf9175f
blinding_factor = c68c1540afdd821f401c6163965ce3e45f7275c1485f6351529466b2bec19179
blinded_message = 0259f0b01c35e6331d95d25c0e45845fb03189964dc20a35bc6a90023a8c8aa71b

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
funding_input_0_C = 0320e3aaf985b86ecee63a5e758c09fdea742467794e76a546e5115b08671e678e
funding_input_1_amount = 32
funding_input_1_C = 03e89934e5d9246f259e4acea8deb61ac9788849857d1c92cba5f5c68b4599209e
funding_input_2_amount = 64
funding_input_2_C = 0389162c83564dde12f6296de5cc586eb31cf2ce57b77f57e5a278330158508833

commitment_outputs_in_order =
  2|02edb30c85ffdf26a839211cb8fdb6e66a2683b63d3a219c18cda91a06ec6a8bf2,
  2|02432306a375dabf1d699278ad5ed5e7a0659c6b1ec7dd2fb924c86534a6cb534b,
  16|03a19de7bde70cd3da6da9c0249c8a4cd4240a20717e7144852c861b8290e9e4c7,
  16|02f8b5fc29575571508b6d0e503da0c4f298dc71098fb8d28c0f27fe82ae8e8a5a,
  32|03f0aad58d35ce66a5079fe9d24ff8862a04d7ffdcd6683773e80a67f6f2e461e0,
  32|0259f0b01c35e6331d95d25c0e45845fb03189964dc20a35bc6a90023a8c8aa71b

sig_all_message_sha256 = 92cc83021c6a89d461afce624895f38023f99dd82162c0e92acd28407175064d
```

The concatenated message is signed by Alice's stage-1 blinded key for each
balance update. Charlie signs the identical message with his stage-1 blinded
key when submitting the close swap. Schnorr signature bytes are not fixed by
this vector because NUT-11 signatures are nondeterministic.
