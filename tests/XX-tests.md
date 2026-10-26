# NUT-XX Test Vectors

These vectors are normative for the element construction, the position derivation, the nesting rule, the fold and the bitmap layout. Every value below is produced by the reference script at the end of this file, so an implementation can regenerate the whole document rather than trust it.

### Element derivation

An element commits to the kind, the identifier and the new state of an object. All three are length-prefixed with a 32-bit big-endian byte count, after the constant domain separator `Cashu_StateFilter_v1`.

The `Y` values below are the outputs of the hash-to-curve function in [NUT-00], so these vectors chain onto the NUT-00 test vectors.

```shell
# Test 1 (proof_state, Y of hash_to_curve(0x0000...0000))
Y:     024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725
E:     dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06 # state SPENT

# Test 2 (proof_state, Y of hash_to_curve(0x0000...0001))
Y:     022e7158e11c9506f1aa4248bf531298daa7febd6194f003edcd9b93ade6253acf
E:     e0393bc41dee7200865edd731ccf50864194606d81780c69c6b063df5810de45 # state SPENT

# Test 3 (proof_state, Y of hash_to_curve(0x0000...0002))
Y:     026cdbe15362df59cd1dd3c9c11de8aedac2106eca69236ecd9fbe117af897be4f
E:     7a66c6493f52021a890e14e9c75d3fdabf6614a56aafdeb794d35a50f948af7e # state SPENT

# Test 4 (proof_state, Y of the NUT-07 example)
Y:     02599b9ea0a1ad4143706c2a5a4a568ce442dd4313e1cf1f7f0b58a317c1a355ee
E:     e813cc139a0a342be273fc1de476e0a2b5bc31fe3f2b465e58d708ef63f23d62 # state SPENT

# Test 5 (proof_state, Y of the NUT-17 example)
Y:     02e208f9a78cd523444aadf854a4e91281d20f67a923d345239c37f14e137c7c3d
E:     01cc40295f336f97a9b46fffeb128d4ec4f70a05b5e89fd5e9179d72767f2c14 # state SPENT
```

### State separation

The same `Y` yields a different element for each state, so a wallet computes one candidate per state it wants to detect. `UNSPENT` is listed because a proof returning to it after `PENDING` is an insertion event; the `UNSPENT` that issuance creates is not.

```shell
# All three use Y = 024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725
UNSPENT: 533e37f559ec5fcf8bd7eac154b08d7df4a3970a426380063bdb34edb44b68bb
PENDING: 8baa493d59d4d95de2f2c04cca1eace28bcefbfabc88c1ff4c9f17fe58bf5a7b
SPENT:   dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06
```

### Quote elements

All of the following use the quote ID `019e6d5a-2347-7000-8afa-051ae571f334`. The first four share that ID and differ only by `kind` and `state`, which is what the length-prefixed preimage has to keep apart. Kinds carry no payment method, so these vectors hold for BOLT11, BOLT12 and onchain alike.

```shell
# Test 1 (mint quote: state is the empty string)
Kind:  mint_quote
State: ""
E:     35ed99b8bfd3097979009f605da85c27c11819604b21a78bbed8d8b018d932d8

# Test 2 (melt quote states)
Kind:  melt_quote
E:     23271db7462d9fa843ae39d6d41fb5afc26a644b64f29b88b39be92945f55944 # state UNPAID
E:     f3648aff04eb3ef749c1024f4b44cc8c40360210aa3ca60b57924d92bef31d10 # state PENDING
E:     8a5b9cecaaf0ecd6edbb1a5aaffd770e43d180080126538f1489575ad9e09122 # state PAID

# Test 3 (the quote id is hashed verbatim: uppercasing it changes the element,
#         so implementations must not normalize case)
Kind:  mint_quote
Quote: 019E6D5A-2347-7000-8AFA-051AE571F334
E:     50800ed2e2532d29409724cedce3ff6d1a33d6a2d0551ffaa8cbf5a52749fce9
```

Because a mint quote's state field is empty, every post-creation transition of one quote inserts the same `E`. Each of those insertions increments `count`.

### Blind signature elements

A `blind_signature` element commits to the kind, the blinded message `B_` and an empty state. The `B_` values below are the outputs of the blinding step in [NUT-00], so these vectors chain onto the NUT-00 test vectors. The derivation from a seed to `B_` is [NUT-13][NUT-13]'s and [NUT-00][NUT-00]'s and is covered by their own vectors; these start from `B_` so that an implementation can check the element construction on its own.

```shell
# Test 1 (B_ of the first NUT-00 blinded message vector)
B_: 033b1a9737a40cc3fd9b6af4b723632b76a67a36782596304612a6c2bfb5197e6d
E:  08bbc296f43f185a10d328a09322635a13fdffa369719205748ac8588a33dd66

# Test 2 (B_ of the second NUT-00 blinded message vector)
B_: 029bdf2d716ee366eddf599ba252786c1033f47e230248a4612a5670ab931f1763
E:  7b6233c71b7e9113139cc36d69fa8cc78d6828ef2c5690cb4d839fd84e5c8910

# Test 3 (B_ of the NUT-00 blinded signature vectors)
B_: 02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2
E:  c2d87b1b167d013cf2f0269bc2aebd212ba66b21020cf4e615adcd47f23224d9
```

### Kind separation

The same 33 bytes yield a different element under a different kind, which is what the length-prefixed `kind` field exists to guarantee. A wallet that confused the two would test for an issuance that never happened.

These both use the bytes `024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725`, which is the `Y` of `hash_to_curve(0x0000...0000)` above, read here once as a `B_` and once as a `Y`.

```shell
Kind:  blind_signature
State: ""
E:     62c10db24e577ec96363ad4ae34adfe6814ac11f0deacfc08139bc7df6093e06

Kind:  proof_state
State: SPENT
E:     dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06
```

## Cases

Seven cases in full, each from its inputs through to the wire form. `words` are the 16 32-bit big-endian words of `SHA256(E || u32be(0)) || SHA256(E || u32be(1))`, in order. `positions` are those words shifted right by `32 - b`.

### Case 1: a `proof_state` element

```shell
kind:      proof_state
input:     Y = hash_to_curve(0x0000...0000), state SPENT
id:        024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725
state:     5350454e54                                   # "SPENT"
preimage:  43617368755f537461746546696c7465725f76310000000b70726f6f665f737461746500000021024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725000000055350454e54
E:         dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06
d0:        35bc6778264f5a0570d3c11653bc97961f31b776b3dcac81132e09be21b88afa
d1:        e8745ba17a260bfe658390ee5c9aa6b51d8ed3b547430af9926b8c97b12859c8
words:     35bc6778 264f5a05 70d3c116 53bc9796 1f31b776 b3dcac81 132e09be 21b88afa
           e8745ba1 7a260bfe 658390ee 5c9aa6b5 1d8ed3b5 47430af9 926b8c97 b12859c8

b:         8
positions: 53, 38, 112, 83, 31, 179, 19, 33, 232, 122, 101, 92, 29, 71, 146, 177
distinct:  16 of 16
popcount:  16 of 256
hex:       0000100542000400010010080400802000002000000050000000000000800000
base64:    AAAQBUIABAABABAIBACAIAAAIAAAAFAAAAAAAACAAAA=      # padded
           AAAQBUIABAABABAIBACAIAAAIAAAAFAAAAAAAACAAAA       # unpadded
```

The preimage in fields, for implementations checking their length prefixing:

```shell
# 43617368755f537461746546696c7465725f7631  "Cashu_StateFilter_v1"
# 0000000b                                  len32("proof_state")
# 70726f6f665f7374617465                    "proof_state"
# 00000021                                  len32(Y), 33 bytes
# 024cce...1a725                            Y
# 00000005                                  len32("SPENT")
# 5350454e54                                "SPENT"
```

### Case 2: a `mint_quote` element with an empty state

The final length-prefixed field is present and zero. An implementation that omits it entirely produces a different `E`.

```shell
kind:      mint_quote
input:     quote id 019e6d5a-2347-7000-8afa-051ae571f334, empty state
id:        30313965366435612d323334372d373030302d386166612d303531616535373166333334
state:                                                  # empty, len32 is 00000000
preimage:  43617368755f537461746546696c7465725f76310000000a6d696e745f71756f74650000002430313965366435612d323334372d373030302d386166612d30353161653537316633333400000000
E:         35ed99b8bfd3097979009f605da85c27c11819604b21a78bbed8d8b018d932d8
d0:        0232b60eaf79aaaf8b8ed3327caeeba82546b34226b2b6ee8f79920a1f326c26
d1:        6872bdcd4bb198298acad4aedaa1d1413158ad550fb90365eeade7c279ee3cb4
words:     0232b60e af79aaaf 8b8ed332 7caeeba8 2546b342 26b2b6ee 8f79920a 1f326c26
           6872bdcd 4bb19829 8acad4ae daa1d141 3158ad55 0fb90365 eeade7c2 79ee3cb4

b:         8
positions: 2, 175, 139, 124, 37, 38, 143, 31, 104, 75, 138, 218, 49, 15, 238, 121
distinct:  16 of 16
popcount:  16 of 256
hex:       2001000106004000001000000080004800310000000100000000002000020000
base64:    IAEAAQYAQAAAEAAAAIAASAAxAAAAAQAAAAAAIAACAAA=      # padded
           IAEAAQYAQAAAEAAAAIAASAAxAAAAAQAAAAAAIAACAAA       # unpadded
```

### Case 3: a `blind_signature` element

```shell
kind:      blind_signature
input:     B_ of the first NUT-00 blinded message vector, empty state
id:        033b1a9737a40cc3fd9b6af4b723632b76a67a36782596304612a6c2bfb5197e6d
state:                                                  # empty, len32 is 00000000
preimage:  43617368755f537461746546696c7465725f76310000000f626c696e645f7369676e617475726500000021033b1a9737a40cc3fd9b6af4b723632b76a67a36782596304612a6c2bfb5197e6d00000000
E:         08bbc296f43f185a10d328a09322635a13fdffa369719205748ac8588a33dd66
d0:        0c9dddd93e3c41fce20f0d8fee745654a78c2e3c706a9f442e3c0d5a96577740
d1:        60d88399c9ed1d5ab06515ba7e5902958cb740ba349fd8034fe67d6538ec93cd
words:     0c9dddd9 3e3c41fc e20f0d8f ee745654 a78c2e3c 706a9f44 2e3c0d5a 96577740
           60d88399 c9ed1d5a b06515ba 7e590295 8cb740ba 349fd803 4fe67d65 38ec93cd

b:         8
positions: 12, 62, 226, 238, 167, 112, 46, 150, 96, 201, 176, 126, 140, 52, 79, 56
distinct:  16 of 16
popcount:  16 of 256
hex:       0008000000020882000100008000800200080200010080000040000020020000
base64:    AAgAAAACCIIAAQAAgACAAgAIAgABAIAAAEAAACACAAA=      # padded
           AAgAAAACCIIAAQAAgACAAgAIAgABAIAAAEAAACACAAA       # unpadded
```

### Case 4: several elements in one bitmap

The five `SPENT` elements of the first section, inserted into one `b = 10` block in the order listed. Position `p` is bit `0x80 >> (p & 7)` of byte `p >> 3`, so position 0 is the most significant bit of byte 0.

Five insertions set 76 of the 1024 bits rather than 80, because some of the 80 positions collide. Collisions need no special handling and `count` is still 5.

```shell
kind:      proof_state
b:         10
count:     5
elements:  dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06
           e0393bc41dee7200865edd731ccf50864194606d81780c69c6b063df5810de45
           7a66c6493f52021a890e14e9c75d3fdabf6614a56aafdeb794d35a50f948af7e
           e813cc139a0a342be273fc1de476e0a2b5bc31fe3f2b465e58d708ef63f23d62
           01cc40295f336f97a9b46fffeb128d4ec4f70a05b5e89fd5e9179d72767f2c14
popcount:  76 of 1024
hex:       00080020400014820048000000000208020000400800100200402200000400200000000400000000000a408000002400000202400000000010800000008001c3000810000480010000c04004001240080800011000080002080100000008000000c0000004000000014400800080000000002004400000000000000085010800
base64:    AAgAIEAAFIIASAAAAAACCAIAAEAIABACAEAiAAAEACAAAAAEAAAAAAAKQIAAACQAAAICQAAAAAAQgAAAAIABwwAIEAAEgAEAAMBABAASQAgIAAEQAAgAAggBAAAACAAAAMAAAAQAAAABRACAAIAAAAAAIARAAAAAAAAAAIUBCAA=
           AAgAIEAAFIIASAAAAAACCAIAAEAIABACAEAiAAAEACAAAAAEAAAAAAAKQIAAACQAAAICQAAAAAAQgAAAAIABwwAIEAAEgAEAAMBABAASQAgIAAEQAAgAAggBAAAACAAAAMAAAAQAAAABRACAAIAAAAAAIARAAAAAAAAAAIUBCAA
```

This is the bitmap in the NUT's own example. `b = 10` holds only 44 insertions, so no real mint would use it; 1024 bits fit on a page.

All five elements match it. The `PENDING` element of the first `Y` does not, and the test ends on its first probe, which is why a wallet stops at the first clear bit rather than reading all 16.

```shell
# Non-member: PENDING element of Y = 024cce99...a725
E:         8baa493d59d4d95de2f2c04cca1eace28bcefbfabc88c1ff4c9f17fe58bf5a7b
positions: 724, 692, 954, 531, 722, 43, 45, 775, 235, 887, 229, 487, 136, 923, 323, 373
p_0:       724          # byte 90, mask 0x08
bit:       0            # clear, so no match after one read
```

### Case 5: two positions of one element colliding

At a small `b` the 16 words of a single element can land on the same position. The insertion then sets fewer than 16 bits, counts once, and needs no special handling. The element is Case 1's.

```shell
E:         dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06

b:         5
positions: 6, 4, 14, 10, 3, 22, 2, 4, 29, 15, 12, 11, 3, 8, 18, 22
distinct:  13 of 16    # w_1 and w_7 both give 4, w_4 and w_12 give 3, w_5 and w_15 give 22
count:     1
popcount:  13 of 32
hex:       3abb2204
base64:    OrsiBA==     # padded
           OrsiBA       # unpadded

# The same element at wider b, for the point at which the collisions disappear
b:         6   distinct: 14 of 16
b:         7   distinct: 16 of 16
```

### Case 6: nesting

Positions taken from fixed 32-bit windows nest: the position at a smaller width is the position at the larger width shifted right by the difference. Positions taken from packed `b`-bit slices of a digest do not, because the field boundaries move when `b` changes. This is the vector that separates the two.

```shell
E:         dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06

# Positions at b = 22
880409, 627670, 1848560, 1371941, 511085, 2946859, 314242, 552482,
3808534, 2001282, 1663204, 1517225, 484276, 1167554, 2398947, 2902550

# Positions at b = 10, derived directly from the same two digests
214, 153, 451, 334, 124, 719, 76, 134,
929, 488, 406, 370, 118, 285, 585, 708

# The b = 22 positions shifted right by 22 - 10 = 12, in the same order
214, 153, 451, 334, 124, 719, 76, 134,
929, 488, 406, 370, 118, 285, 585, 708
```

The first three words fix the byte order: `w_0 = 0x35bc6778`, `w_1 = 0x264f5a05`, `w_2 = 0x70d3c116`, and at `b = 22`, `p_0 = 0x35bc6778 >> 10 = 880409`.

### Case 7: folding a bitmap to a smaller width

The fold of Case 4's `b = 10` bitmap to `b' = 6`. Bit `j` of the result is the OR of the bits it covers, which is what a position shifted right by `b - b'` selects. Folding is what a mint does when it seals an unsaturated block at the smallest width that still holds its `count`.

```shell
from b:    10
to b':     6
popcount:  46 of 64
hex:       f9ff4dcbfffaae63
base64:    -f9Ny__6rmM=     # padded
           -f9Ny__6rmM      # unpadded
```

Two properties an implementation must reproduce:

```shell
# The fold equals inserting the same five elements directly at b' = 6.
fold(insert_all(b=10), 6) == insert_all(b=6)     # true

# All five elements still match the folded bitmap, because positions nest.
# The fold only ever adds false positives; it never removes a member.
all five match at b = 6                          # true
```

A block is served as raw bytes, so the hex above is the wire form. The base64 lines in each case are an alternate rendering, kept because they are convenient to paste and to eyeball.

### Capacity and right-sizing

Capacity is `2^b * ln2 / 16` rounded down, the insertion count at which the expected fill is approximately one half. The NUT carries it as an integer ratio, `floor(2^b * 6931471805599453 / 160000000000000000)`, so that the seal point and the fold land on the same value everywhere. These rows are that expression evaluated.

```shell
b      capacity     bitmap
5      1            4 B
8      11           32 B
10     44           128 B
12     177          512 B
15     1419         4 KiB
18     11356        32 KiB
20     45426        128 KiB
22     181704       512 KiB
25     1453634      4 MiB
26     2907269      8 MiB

# A block sealed on timeout is folded to the smallest b that still holds
# its count.
count      b      bitmap
0          5      4 B
1          5      4 B
10         8      32 B
100        12     512 B
1000       15     4 KiB
10000      18     32 KiB
45426      20     128 KiB
```

Dividing the bitmap by the capacity gives 2.89 bytes an insertion on every row from `b = 12` up, which is the check that the capacity expression has been implemented correctly. The smaller rows come out higher, 4 bytes at `b = 5` and 2.91 at `b = 8`, because rounding the capacity down leaves slack that only matters when the capacity is tiny.

### Sizing each kind

Every kind is sized on its own, to the smallest `b` whose capacity holds a day of that kind. A mint at a million proof state changes a day:

```shell
kind               insertions/day    b     bitmap    rotation
proof_state        1,000,000         25    4 MiB     every 1.5 days
blind_signature    1,000,000         25    4 MiB     every 1.5 days
mint_quote         5,000             18    32 KiB    every 2.3 days
melt_quote         100               12    512 B     every 1.8 days
```

A saturated block costs about 2.89 bytes an insertion whatever its `b`, so the bitmap bytes over these insertions are roughly what a single sequence over the same insertions would publish, about 5.8 MB a day. What changes is a wallet's share: one following only proof states takes about 2.9 MB a day, and one following only melt quotes under 300 bytes. A single sequence would have put those 100 melt quotes in the 4 MiB block. The split is not free beyond the bitmaps: it adds per-sequence metadata, one open block per sequence, and framing per request.

### Saturation

Fill and estimated false-positive probability against `count`, at `b = 20`, assuming every insertion is a distinct element whose positions do not collide. The probability is `f^16` in the observed fill `f`. A block sealed on saturation sits near the capacity row and one sealed on timeout sits above it; the rows past capacity are what a mint that ignored the seal rule would publish.

```shell
count      expected fill    estimated false positive
4542       0.0670           1 in 6.1e18
13628      0.1877           1 in 4.2e11
45426      0.5000           1 in 65536          # capacity, 2^-16
60050      0.6000           1 in 3545
90852      0.7500           1 in 100
```

The fill column is `1 - exp(-16 * count / 2^b)`, the expectation. A wallet does not use it: it takes the popcount of the bitmap it holds, divides by `2^b`, and raises that to the sixteenth. Repeated elements and colliding positions leave the actual fill below the expectation, which lowers the probability rather than raising it.

Two blocks with the same `b` can be merged with a bitwise OR, but sealing near half fill is what makes that useless. The result is a correct filter over the union with a probability that collapses:

```shell
blocks OR'd    fill      estimated false positive
1              0.5000    1 in 65536
2              0.7500    1 in 100
3              0.8750    1 in 8
4              0.9375    1 in 3
8              0.9961    1 in 1
```

### Scanning

A restore tests two elements per candidate against every block: the `blind_signature` element of `B_` to learn whether the mint ever signed it, and the `SPENT` element of `Y` to rank what came back. Both use the matching procedure unchanged.

```shell
# Expected spurious matches while scanning, at a probability of 2^-16
# across a year of blocks at the one-a-day sizing rule (365 blocks).

candidates scanned    expected spurious issuance matches
1,000                 5.6
10,000                55.7
100,000               556.9

# Each costs one extra entry in the restore request, which the mint
# answers with nothing.

live proofs held      expected spurious SPENT matches
50                    0.3
500                   2.8

# These are why a SPENT match MUST NOT delete a proof.
```

### The sequence summary

One request per kind. Two sequences rotating at their own pace, one serving an open block and one not.

`GET /v1/filters/info/proof_state`:

```json
{
  "b": 25,
  "timeout": 604800,
  "open_interval": 60,
  "blocks": [
    { "start": 1737030357, "end": 1737157557 },
    { "start": 1737157557, "end": 1737284757 },
    { "start": 1737284757, "end": 1737412757 },
    { "start": 1737412757, "end": null }
  ]
}
```

`GET /v1/filters/info/melt_quote`:

```json
{
  "b": 12,
  "timeout": 604800,
  "open_interval": null,
  "blocks": [
    { "start": 1736790000, "end": 1736945000 },
    { "start": 1736945000, "end": 1737100000 },
    { "start": 1737100000, "end": 1737255000 },
    { "start": 1737255000, "end": null }
  ]
}
```

```shell
# A block's height is its index, so both sequences run 0 to 3 and block 2 of
# proof_state covers 1737284757 to 1737412757. Each entry's end is the next
# entry's start, and only the last entry of each list has end null.

# melt_quote serves no open block: open_interval is null, so its height 3 is
# listed but not fetchable until it seals.

# A sequence that has never sealed a block has a blocks list of one entry.

# A restore whose seed was created at 1737200000 starts at height 1, the last
# height whose start precedes it.
```

### Heights and the seal boundary

Heights are per sequence. Each kind numbers its blocks from 0 at the mint's first block of that kind, so the same height names a different block in each.

A block response is the bitmap and nothing else, so `b` comes from its length: 4 MiB at `b = 25`, 512 B at `b = 12`. Which heights are sealed comes from the `blocks` list above, not from the response.

```shell
GET /v1/filters/blocks/proof_state/2     -> 200, 4194304 bytes, the newest sealed block
GET /v1/filters/blocks/proof_state/3     -> 200, 4194304 bytes, the block still filling
GET /v1/filters/blocks/proof_state/4     -> 40001, above the last index
GET /v1/filters/blocks/melt_quote/3      -> 40001, open_interval is null
GET /v1/filters/blocks/mint_quote/0      -> 40002, a kind this mint does not cover
GET /v1/filters/info/mint_quote          -> 40002, the same for the info route

# A length that is not 2^b / 8 for a b in 5..26 is rejected.
GET /v1/filters/blocks/proof_state/2     -> 200, 4194300 bytes   # reject
```

The two responses at height 3 below are identical in shape, a second apart across the seal, and the wallet cannot tell them apart from the bytes alone. It does not need to: the list said height 3 was open, so it keeps its bookmark at 3 and re-reads the list, which then shows a fourth entry and moves 3 into the sealed range.

```shell
# Revalidating the block still filling
GET /v1/filters/blocks/proof_state/3
  -> 200, ETag "b3f1c0a2", Cache-Control: max-age=60

GET /v1/filters/blocks/proof_state/3, If-None-Match: "b3f1c0a2"
  -> 304 Not Modified                     # nothing inserted since
  -> 200 with a new ETag                  # something was
```

## Reference implementation

The listings below are not normative. The first reproduces every value in this document; the other two show the two sides in the shape the NUT describes.

### Generating the vectors

```python
import hashlib, base64, struct

DS = b"Cashu_StateFilter_v1"
K = 16

def l32(x):
    return struct.pack(">I", len(x))

def preimage(kind, idb, state):
    kb = kind.encode()
    sb = state.encode() if isinstance(state, str) else state
    return DS + l32(kb) + kb + l32(idb) + idb + l32(sb) + sb

def element(kind, idb, state):
    return hashlib.sha256(preimage(kind, idb, state)).digest()

def words(E):
    W = (hashlib.sha256(E + struct.pack(">I", 0)).digest()
         + hashlib.sha256(E + struct.pack(">I", 1)).digest())
    return [struct.unpack(">I", W[i * 4:i * 4 + 4])[0] for i in range(K)]

def positions(E, b):
    return [w >> (32 - b) for w in words(E)]

def new_bitmap(b):
    return bytearray((1 << b) // 8)

def insert(bm, E, b):
    """One insertion operation. Increments count by one whatever it sets."""
    for p in positions(E, b):
        bm[p >> 3] |= 0x80 >> (p & 7)

def test(bm, E, b):
    return all(bm[p >> 3] & (0x80 >> (p & 7)) for p in positions(E, b))

def fold(bm, b, b2):
    """Bit j of the result is the OR of the bits it covers."""
    out = new_bitmap(b2)
    shift = b - b2
    for p in range(1 << b):
        if bm[p >> 3] & (0x80 >> (p & 7)):
            q = p >> shift
            out[q >> 3] |= 0x80 >> (q & 7)
    return out

def wire(bm):
    s = base64.urlsafe_b64encode(bytes(bm)).decode()
    return s, s.rstrip("=")

def capacity(b):
    return ((1 << b) * 6931471805599453) // 160000000000000000
```

### Generating blocks (mint)

```rust
const K: usize = 16;

/// The capacity table of the NUT, as the arithmetic that generated it.
/// Integer throughout so that the seal point cannot drift between builds.
fn capacity(b: u8) -> u64 {
    ((1u128 << b) * 6_931_471_805_599_453 / (10_000_000_000_000_000 * K as u128)) as u64
}

/// Positions come from fixed 32-bit windows rather than packed `b`-bit slices
/// so that they nest: at any smaller width the position is a right shift away.
fn positions(e: &[u8; 32], b: u8) -> [u32; K] {
    let mut out = [0u32; K];
    for j in 0..2 {
        let mut h = Sha256::new();
        h.update(e);
        h.update((j as u32).to_be_bytes());
        let d = h.finalize();
        for i in 0..8 {
            let w = u32::from_be_bytes(d[i * 4..i * 4 + 4].try_into().unwrap());
            out[j * 8 + i] = w >> (32 - b);
        }
    }
    out
}

/// One kind's block. A mint runs one of these per kind it covers, each with
/// its own height space, its own `b` and its own seal point.
struct Block {
    kind: &'static str,
    height: u32,
    b: u8,
    start: u64,
    count: u64,
    bits: Vec<u8>,
}

impl Block {
    fn open(kind: &'static str, height: u32, b: u8, start: u64) -> Self {
        Self {
            kind,
            height,
            b,
            start,
            count: 0,
            bits: vec![0u8; (1usize << b) / 8],
        }
    }

    /// One insertion operation. `count` counts operations, so a repeat of an
    /// element already inserted still counts, and no exact set is kept.
    fn insert(&mut self, e: [u8; 32]) {
        for p in positions(&e, self.b) {
            self.bits[(p >> 3) as usize] |= 0x80 >> (p & 7);
        }
        self.count += 1;
    }

    fn full(&self) -> bool {
        self.count >= capacity(self.b)
    }

    /// Folds the bitmap down to the smallest width that still holds `count`.
    /// Only `Sealed` carries an `end`; an open `Block` serializes with `end`
    /// set to null.
    fn seal(mut self, end: u64) -> Sealed {
        let mut b = self.b;
        while b > 5 && self.count <= capacity(b - 1) {
            b -= 1;
        }
        if b < self.b {
            let shift = self.b - b;
            let mut folded = vec![0u8; (1usize << b) / 8];
            for p in 0..(1u32 << self.b) {
                if self.bits[(p >> 3) as usize] & (0x80 >> (p & 7)) != 0 {
                    let q = p >> shift;
                    folded[(q >> 3) as usize] |= 0x80 >> (q & 7);
                }
            }
            self.bits = folded;
            self.b = b;
        }
        Sealed { inner: self, end }
    }
}
```

### Following blocks (wallet)

```typescript
const K = 16;

/// The 16 words of a candidate, computed once and reused for every block at
/// any width. Caching the words rather than the positions is what survives a
/// mint folding a block or changing b.
function words(e: Uint8Array): Uint32Array {
  const out = new Uint32Array(K);
  for (let j = 0; j < 2; j++) {
    const d = new DataView(sha256(concat(e, u32be(j))).buffer);
    for (let i = 0; i < 8; i++) out[j * 8 + i] = d.getUint32(i * 4, false);
  }
  return out;
}

/// Stops at the first clear bit, which is after two reads on average against
/// a block near half fill.
function test(bitmap: Uint8Array, w: Uint32Array, b: number): boolean {
  for (let i = 0; i < K; i++) {
    const p = w[i] >>> (32 - b);
    if ((bitmap[p >> 3] & (0x80 >> (p & 7))) === 0) return false;
  }
  return true;
}

/// Walks one sequence. A wallet runs this once per kind it follows, with the
/// bookmark it keeps for that kind.
async function scan(
  mint: string,
  kind: string,
  candidates: Candidate[],
  fromHeight: number,
) {
  // The per-kind form, so following one kind costs only that kind's metadata.
  const seq = await get(`${mint}/v1/filters/info/${kind}`);

  // A response is the bitmap and nothing else, so b is its length.
  const widthOf = (bitmap) => {
    const b = Math.log2(bitmap.length * 8);
    if (!Number.isInteger(b) || b < 5 || b > 26)
      throw new Error("body is not 2^b / 8 bytes for any valid b");
    return b;
  };

  const match = (bitmap) => {
    const b = widthOf(bitmap);
    return candidates.filter((c) => test(bitmap, c.w, b));
  };

  // A block's height is its index, and the last entry is the open block.
  const openHeight = seq.blocks.length - 1;

  const hits = [];
  for (let h = fromHeight; h <= openHeight - 1; h++) {
    const bitmap = await getBytes(`${mint}/v1/filters/blocks/${kind}/${h}`);
    for (const c of match(bitmap)) hits.push({ height: h, candidate: c });
  }

  // The open block is an early signal, not history. The bookmark stops below
  // it, and the wallet tests it again on the next pass.
  const early = [];
  if (seq.open_interval !== null) {
    const bitmap = await getBytes(
      `${mint}/v1/filters/blocks/${kind}/${openHeight}`,
    );
    early.push(...match(bitmap));
  }

  return { hits, early, nextHeight: openHeight };
}
```

A wallet stores one `fromHeight` per sequence it follows. The `blocks` list gives the whole height range up front, so a block the mint will not serve shows up as a failed fetch of a height the list claims rather than as a quiet period. A wallet recovering from a seed passes height `0`, or the height whose interval covers its seed's creation, and accepts that it knows nothing about what came before the sequence began.

`nextHeight` stops at the open block's height whether or not it was tested, so the open block is walked again on the next pass and counted once, when it seals. A hit there is worth acting on immediately, which is the whole reason to fetch it; a miss there means nothing, because the block is still filling.

[NUT-00]: ../00.md
[NUT-07]: ../07.md
[NUT-13]: ../13.md
