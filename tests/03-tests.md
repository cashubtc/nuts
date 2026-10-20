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

Frame the context, each input field, and each output amount with a four-byte
unsigned big-endian byte length. Append each **unframed** 32-byte
`SHA256(original B_)` immediately after its framed amount. Here `B_` is
the original 33-byte compressed point, not the hex text or tweaked `B'`:

```text
SHA256(G)  = 0f715baf5d4c2ed329785cef29e562f73488c8a2bb9dbc5700b361d54b9b0554
SHA256(2G) = b1c9938f01121e159887ac2c8d393a22e4476ff8212de13fe1939de2a236f0a7
```

For an empty input list and one output with amount `1` and original `B_ = G`:

```text
message = 00000000 00000001 01 0f715baf5d4c2ed329785cef29e562f73488c8a2bb9dbc5700b361d54b9b0554
digest  = 12ba73147194f4528cf2e06b4a557daff57a1f2153938106af49d51c399bbe2a
```

Incorrectly prefixing the 32-byte hash with `00000020` would instead produce
`407b56261c9d046da7e2e5617bf07cacc64413894b2ccb81e3324c41a9cd8359`;
the mint **MUST NOT** accept a signature on that alternate digest.

The digest is `TaggedSHA256("Cashu_SigAllRerandomized_v1", message)`, signed
**directly** as a BIP-340 32-byte message (no extra SHA-256). For a
non-empty **transcript-only** example, use one input with secret string
`example-input`, input `C = G`, and two outputs in order:
`(amount=1, B_=G)` and `(amount=2, B_=2G)`. The message is:

```text
00000000
0000000d 6578616d706c652d696e707574
00000021 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
00000001 01
0f715baf5d4c2ed329785cef29e562f73488c8a2bb9dbc5700b361d54b9b0554
00000001 02
b1c9938f01121e159887ac2c8d393a22e4476ff8212de13fe1939de2a236f0a7
```

The spaces and newlines in this display are not part of the message. The
tagged digest is
`1cf1d9ebb188c3bef26728eb68650d00bef181e24c4e6dcd5f102808183ec9fc`.
Signing that digest with secp256k1 private key `1` and zero BIP-340
auxiliary randomness yields this valid Schnorr signature:

```text
d4d6e5d561a3e6430dfea89f9f786312c29aa88db0456f3828663c15d468aa7d71650eaa4718eca7e0db0b4217e728471ecd3d2b9e23feba50a57ee68b9bfe4e
```

Reversing the two **output pairs** (amount and original `B_` together)
changes the tagged digest to
`c89da53d5da23ea64167e0dc3ff0d8c7b824fa8d6ad5727dddd35076d47417c2`.
The signature above cannot authorize that reordered request or an ordinary
NUT-11 `SIG_ALL` swap. Incorrectly framing the raw compressed point instead
of hashing it would produce
`2e96fda9957222af5e1a8e8c581ab12ed8b5180108a554bdb934d661d9bc2c71`
for the one-output example; that digest is not valid for this mode.

## Two-input P2PK and HTLC authorization vectors

These vectors pin the existing `SIG_ALL` spending-condition behavior using
two inputs and two original outputs. They exercise the authorization digest
and witness rules, **not** mint issuance: `C = G` and `C = 2G` below are
illustrative valid points, not signatures issued on these proof secrets.
For both vectors use keyset `009a1f293253e41e`, two input proofs in order
`(amount=1, C=G)` and `(amount=2, C=2G)`, and two original outputs in order
`(amount=1, B_=G)` and `(amount=2, B_=2G)`. Use the point encodings above.
The mint's derived outputs `B'_i` are **not** part of the signing transcript.

For **P2PK 2-of-2**, use the following exact UTF-8 string as the first
input's `Proof.secret` (all spaces inside this code block are significant):

```text
["P2PK", {"data": "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798", "nonce": "00000000000000000000000000000000", "tags": [["sigflag", "SIG_ALL"], ["pubkeys", "02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"], ["n_sigs", "2"]]}]
```

The second input's secret is identical except its 32-character nonce is
`11111111111111111111111111111111`. **Do not** normalize or reserialize
these strings before framing them. Each secret is 267 UTF-8 bytes, so each
input-secret frame starts with `0000010b`; each input-`C` frame starts with
`00000021`. The exact tail after the input frames is:

```text
00000001 01 0f715baf5d4c2ed329785cef29e562f73488c8a2bb9dbc5700b361d54b9b0554
00000001 02 b1c9938f01121e159887ac2c8d393a22e4476ff8212de13fe1939de2a236f0a7
```

Prefix the first input with the empty context frame `00000000` and frame
the two input secrets and compressed `C` values in request order. With the
tag `Cashu_SigAllRerandomized_v1`, the resulting digest is
`fd3ade51140ee7316f1f95b3f2e55c61ddb82a8ce8b645be6ae6d221a88b3c9f`.
Schnorr signatures with private keys `1` (`G`) and `2` (`2G`), each using
32 zero BIP-340 auxiliary bytes, are:

```text
b13d0056645a8eda768a397979e6763540e0749b15b7acb2d2e73ba60e68aa86d9704f080103c62d09b842bb689f0ce6537aecc26cd429825ae3af3b3da0f8c9
ef0977a09c4df9b3af8f34e2374f53e9f359ba4238d787b1ddba0f35d0aaf48b3a60f9db1f1ec74d6a272a5ff5238edfbafab0dd635aa3fda4abc841d679825f
```

Put both hex signatures in a `P2PKWitness.signatures` array on the first
input; the second input requires no witness. Reordering the two **output
pairs** changes the digest to
`88c0190df9997b266fd4290cc507eb6ae9712661f6fff76af10bdbf194f606e1`.
Replacing the second original `B_` with `3G` instead produces
`5377787396552d37556800f60a8b1e90803dc14b92876a6a51b70694d2fb9a70`;
changing its amount from `2` to `3` produces
`4e486157d56c88cedfae5ddb346b2d10a1b4b5fc039abb1463e2af2306b21cab`.
All these changes invalidate the signatures. Framing the raw compressed
points instead of appending their 32-byte hashes produces the obsolete
digest `c1c3ae247a01b3e2c83646e4f9f12d3c16da5d6198145ee6bed831fb84d478f8`;
it **MUST NOT** authorize the updated mode.

For **HTLC receiver and refund**, use this exact string as the first
input's `Proof.secret`:

```text
["HTLC", {"data": "425ed4e4a36b30ea21b90e21c712c649e8214c29b7eaf68089d1039c6e55384c", "nonce": "00000000000000000000000000000000", "tags": [["sigflag", "SIG_ALL"], ["pubkeys", "02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"], ["refund", "02f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9"], ["locktime", "1"]]}]
```

As for P2PK, the second secret changes only its nonce to 32 `1` characters.
Each secret is 349 UTF-8 bytes, with frame length `0000015d`; use the same
input points, original outputs and output hashes as above. The `data` field
is the SHA-256 hash of 32 bytes of `0x42`; its preimage is
`4242424242424242424242424242424242424242424242424242424242`.
The digest is
`be691a010c111bd4689c18241cfe5a79893b443558db806d3000ec4268ec2670`.
With a matching `HTLCWitness.preimage`, a receiver using key `2` signs:

```text
e14f243196f4857b290589a0326a1433107ccff557372d9f398b5bdf3bbb045193b8a1f9271b26603068f000140dc702a9cbf7c765e50812f1e4ce3e86a93a46
```

After locktime `1` expires, an empty preimage and refund-key `3` signature
provide the alternative spending pathway:

```text
c6a2b4c82137bac2118b37d0d086c18aa893893aa674b41304039dd2359cb503512d360b963970b4480a90b10f3846a1995d5d5f6ce9bda26ea1bb82323090e9
```

Both signatures were produced with 32 zero BIP-340 auxiliary bytes and go
in the first input's HTLC witness. Reordering the outputs changes the digest
to `f1392f8a4083843c1875a43593675b97524a462469526d78462f1d8c321f0289`;
framing the raw compressed points instead of hashing them would yield
`67003e2d948944565c26d5a31de6874da42bab8c2558dcb980fa97b75c162de5`.
Neither alternate digest authorizes the original request in the current mode.
