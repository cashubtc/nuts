# NUT-03 mint-rerandomized V2 swap vectors

These vectors specify the optional [mint-rerandomized swap](../03.md)
encoding. All hex strings are lowercase; point encodings are compressed
secp256k1 public keys. Signing vectors test transcript bytes and Schnorr
verification only; the illustrative secret `example-input` is **not** a
NUT-10 spending condition, and the examples are not executable swap requests.

## Shared mint tweak and additive points

For `R = 0x42` repeated 32 times, counter zero is accepted:

```text
R             = 4242424242424242424242424242424242424242424242424242424242424242
tag           = Cashu_OutputRerandomization_secp256k1_v1
counter       = 00000000
t             = ea8bfdd0711f5a0cdd1377930ed729ca779722a8a5f97156242fcef09965eeb5

G             = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
2G            = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
G + tG        = 020f78ce253e2f82c3f92f2e2c529f0c2320d628f0456e360f14e7005565f35ee6
2G + tG       = 03b0da7d80f73fdece3947e68b62c6cea972ba798600de31ce7a754d934e7d7c26
-tG           = 037c6797ffee9183650748f55b3e90fcabfa9e0d26b068c86ee72f8c25f15b1146
```

Adding `tG` to `-tG` yields infinity and requires a fresh `R` or a failed
swap without spending inputs. As a signing/unblinding example, take
`Y = G`, original blinding factor `r = 1`, original `B = 2G`, and mint key
`a = 3` (`A = 3G`). This is a point-level algebraic example, not a claim
that a particular secret hashes to `G`. Then:

```text
original B     = 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
derived B'     = 03b0da7d80f73fdece3947e68b62c6cea972ba798600de31ce7a754d934e7d7c26
A = 3G         = 02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9
C' = 3B'       = 033a0b1d9624a63e568496edc17143458e6fd1b73b829792087f6af6f4692cd728
r + t         = ea8bfdd0711f5a0cdd1377930ed729ca779722a8a5f97156242fcef09965eeb6
P = C'-(r+t)A = 02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9
```

The mint's ordinary DLEQ for `(B', C')`, if present, is reusable on the
proof `P` with the effective blinding factor `r + t`; it is not recomputed
using the original point `B`.

## Tagged `SIG_ALL` transcript

Frame each byte string with a four-byte unsigned big-endian byte length. For
an empty input list and one output with amount `1` and original `B_ = G`:

```text
message = 00000000 00000001 01 00000021 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
digest  = 2e96fda9957222af5e1a8e8c581ab12ed8b5180108a554bdb934d661d9bc2c71
```

The digest is `TaggedSHA256("Cashu_SigAllRerandomized_v1", message)`, signed
**directly** as a BIP-340 32-byte message (no extra SHA-256). For a
non-empty example, use one input with secret string `example-input`, input
`C = G`, and two outputs in order: `(amount=1, B_=G)` and
`(amount=2, B_=2G)`. The length-framed message is:

```text
00000000
0000000d 6578616d706c652d696e707574
00000021 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
00000001 01
00000021 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
00000001 02
00000021 02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5
```

The spaces and newlines in this display are not part of the message. The
tagged digest is
`f8f04365e973b5f8c055ed59bd6c472ac9130b796fe6c87d710c6d73ea3382eb`.
Signing that digest with secp256k1 private key `1` and zero BIP-340
auxiliary randomness yields this valid Schnorr signature:

```text
44010d2050afb5865c3073542121ae6d6cc9b1ec967da69f91606e2610b026aecaa152fd4f6034449e3eea5e4338c414cbd0ab34286c7ee23b46b81c0311c50b
```

Reversing the two **output pairs** (amount and original `B_` together)
changes the tagged digest to
`5cde29fc07d63d3ee59fe843d76f65ad3afb6366c49fba340b25463d5f7c3d8c`.
The signature above cannot authorize that reordered request. Neither this
digest nor its signature is interchangeable with ordinary NUT-11 `SIG_ALL`.
