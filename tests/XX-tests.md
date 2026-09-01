# NUT-XX Test Vectors

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

The same `Y` yields a different element for each state, so a wallet computes one candidate per state it wants to detect.

```shell
# All three use Y = 024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725
UNSPENT: 533e37f559ec5fcf8bd7eac154b08d7df4a3970a426380063bdb34edb44b68bb
PENDING: 8baa493d59d4d95de2f2c04cca1eace28bcefbfabc88c1ff4c9f17fe58bf5a7b
SPENT:   dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06
```

### Preimages

The full preimage in hex, for implementations to check their length prefixing. This is the most likely source of an interoperability failure.

```shell
# Test 1: proof_state / Y of hash_to_curve(0x0000...0000) / SPENT
# 43617368755f537461746546696c7465725f7631  "Cashu_StateFilter_v1"
# 0000000b                                  len32("proof_state")
# 70726f6f665f7374617465                    "proof_state"
# 00000021                                  len32(Y), 33 bytes
# 024cce...1a725                            Y
# 00000005                                  len32("SPENT")
# 5350454e54                                "SPENT"
Preimage: 43617368755f537461746546696c7465725f76310000000b70726f6f665f737461746500000021024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725000000055350454e54
E:        dce02b593be7ddd8abe04bcaf19e35094c67429c21ef5c62ab5550841a603f06

# Test 2: mint_quote / quote id / empty state
# Note the trailing 00000000: a mint quote has no state, so the final
# length-prefixed field is present but empty.
Preimage: 43617368755f537461746546696c7465725f76310000000a6d696e745f71756f74650000002430313965366435612d323334372d373030302d386166612d30353161653537316633333400000000
E:        35ed99b8bfd3097979009f605da85c27c11819604b21a78bbed8d8b018d932d8
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

### Filter encoding

A filter over the five `SPENT` elements of the first section, with `P = 28` and therefore `N = 5`. The position of an element depends on `N`, so the same element has a different position in every filter.

```shell
# Positions, in the order the elements are listed above
E: dce02b59...  pos: 1158024587
E: e0393bc4...  pos: 1175577261
E: 7a66c649...  pos: 641736182
E: e813cc13...  pos: 1216753606
E: 01cc4029...  pos: 9425932

# Sorted, then Rice coded with P = 28
Sorted:    9425932, 641736182, 1158024587, 1175577261, 1216753606
data:      047ea0665b049eabb17be54217aa442744d190
N decoded: 5           # 19 bytes = 152 bits, 5 codes of 29 bits, 7 bits padding
```

`N` is not carried alongside the filter. A decoder reads codes while at least `P + 1` bits remain, and the count it ends with is `N`.

A single element filter, useful for checking the bit layout by hand. The delta is `1885186`, whose quotient is `0`, so the code is one `0` bit followed by the 28 bits `0000000111001100010000000010`, padded with three `0` bits to four bytes.

```shell
Y:         02e208f9a78cd523444aadf854a4e91281d20f67a923d345239c37f14e137c7c3d
State:     SPENT
pos:       1885186
data:      00e62010
N decoded: 1           # 32 bits, one 29 bit code, 3 bits padding
```

An epoch in which nothing changed. No bits remain, so nothing is decoded:

```shell
data:      ""
N decoded: 0
```

### Matching

A wallet decodes the filter first, takes `N` from the number of values it read, and only then computes the position of its own candidate. Testing an element that is not in the filter above:

```shell
Y:      024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725
State:  PENDING
E:      8baa493d59d4d95de2f2c04cca1eace28bcefbfabc88c1ff4c9f17fe58bf5a7b
pos:    732247779   # with N = 5
Result: no match    # the filter contains 9425932, 641736182, 1158024587, 1175577261, 1216753606
```

### Paging

Page numbers count from the mint's first epoch, so a full page never changes again. A year of hourly epochs is 8,760 filters, which is 175 full pages and one still filling:

```shell
epoch = 3600, page_size = 50
first_page = 0, current_page = 175, current_page_count = 10
earliest_start = 1698796800, latest_end = 1730332800

page 0    ->  50 filters, 1698796800 .. 1698976800   # full, cacheable forever
page 174  ->  50 filters, ends 1730296800            # full, 175 * 50 = 8750
page 175  ->  10 filters so far, still filling
page 176  ->  error 40002                            # above current_page
```

### Reference implementation

The listings below are not normative. They reproduce every vector above, so that an implementation can be checked against working code as well as against hex.

#### Generating filters (mint)

`BitWriter`, `Filter` and `now` are assumed. `write_bits` writes the low `count` bits of its argument most significant bit first.

```rust
const DOMAIN_SEPARATOR: &[u8] = b"Cashu_StateFilter_v1";

/// `state` is the empty string for mint quotes, which have no state enum.
struct Element {
    kind: String,
    id: Vec<u8>,
    state: String,
}

impl Element {
    fn hash(&self) -> [u8; 32] {
        let mut h = Sha256::new();
        h.update(DOMAIN_SEPARATOR);
        for field in [self.kind.as_bytes(), self.id.as_slice(), self.state.as_bytes()] {
            h.update((field.len() as u32).to_be_bytes());
            h.update(field);
        }
        h.finalize().into()
    }
}

/// Widened to `u128` because `v * n * 2^p` overflows `u64` by construction.
fn position(digest: &[u8; 32], n: u64, p: u8) -> u64 {
    let mut head = [0u8; 8];
    head.copy_from_slice(&digest[..8]);
    let v = u64::from_be_bytes(head) as u128;
    let f = (n as u128) << p;
    ((v * f) >> 64) as u64
}

/// Deduplicates digests rather than positions, so that `n` is recoverable by
/// a wallet that only ever sees the encoded filter.
fn build_filter(changes: &[Element], p: u8) -> Vec<u8> {
    let mut digests: Vec<[u8; 32]> = changes.iter().map(Element::hash).collect();
    digests.sort_unstable();
    digests.dedup();
    let n = digests.len() as u64;

    let mut positions: Vec<u64> = digests.iter().map(|d| position(d, n, p)).collect();
    positions.sort_unstable();

    let mut writer = BitWriter::default();
    let mut previous = 0;
    for pos in positions {
        let delta = pos - previous;
        previous = pos;
        for _ in 0..(delta >> p) {
            writer.write_bit(true);
        }
        writer.write_bit(false);
        writer.write_bits(delta & ((1u64 << p) - 1), p);
    }
    writer.into_bytes()
}
```

The epoch loop. `epoch_start` holds the boundary the open epoch began at and becomes the next epoch's `start` when this one closes, which is what keeps the history contiguous. An epoch in which nothing changed still produces a filter, so the history never has gaps. The pending filter is the same `build_filter` call over the changes accumulated so far in the open epoch.

```rust
fn close_epoch(&mut self, changes: &[Element]) -> Filter {
    let filter = Filter {
        start: self.epoch_start,
        end: now(),
        data: build_filter(changes, self.p),
    };
    self.epoch_start = filter.end;
    filter
}
```

#### Consuming filters (wallet)

`sha256`, `concat`, `fromHex`, `getJson` and `BitReader` are assumed. `BitReader.bit` returns the next bit, `BitReader.bits` reads `count` bits most significant bit first, and `BitReader.remaining` is the number of bits not yet read.

```ts
const DOMAIN_SEPARATOR = new TextEncoder().encode("Cashu_StateFilter_v1");

function element(kind: string, id: Uint8Array, state: string): Uint8Array {
  const enc = new TextEncoder();
  const parts: Uint8Array[] = [DOMAIN_SEPARATOR];
  for (const field of [enc.encode(kind), id, enc.encode(state)]) {
    const length = new Uint8Array(4);
    new DataView(length.buffer).setUint32(0, field.length, false);
    parts.push(length, field);
  }
  return sha256(concat(parts));
}

/** BigInt because the intermediate `v * n * 2^p` does not fit in a double. */
function position(e: Uint8Array, n: number, p: number): bigint {
  const v = new DataView(e.buffer, e.byteOffset, 8).getBigUint64(0, false);
  return (v * (BigInt(n) << BigInt(p))) >> 64n;
}

/** Stops when fewer than `p + 1` bits remain, which is shorter than any code,
 *  so the trailing padding is never mistaken for one. `N` is the length. */
function decodeFilter(data: Uint8Array, p: number): bigint[] {
  const reader = new BitReader(data);
  const positions: bigint[] = [];
  let previous = 0n;
  while (reader.remaining() >= p + 1) {
    let quotient = 0n;
    while (reader.bit() === 1) quotient++;
    previous += (quotient << BigInt(p)) | reader.bits(p);
    positions.push(previous);
  }
  return positions;
}
```

Paging and matching. Pages below `current_page` never change, so a wallet resumes at the page it stopped on and re-reads only the last one. Each filter is decoded before its candidates are placed, because their positions depend on the `N` that decoding yields.

```ts
/** A match may be a false positive, so the caller confirms every hit through
 *  POST /v1/checkstate before acting on it. */
async function scan(
  mintUrl: string,
  ys: Uint8Array[],
  fromPage: number,
  since: number,
) {
  const info = await getJson(`${mintUrl}/v1/filters/info`);
  const hits: { start: number; y: Uint8Array; state: string }[] = [];

  for (
    let page = Math.max(fromPage, info.first_page);
    page <= info.current_page;
    page++
  ) {
    const { filters } = await getJson(`${mintUrl}/v1/filters/${page}`);

    for (const filter of filters) {
      if (filter.end <= since) continue;
      const decoded = decodeFilter(fromHex(filter.data), info.p);
      const positions = new Set(decoded);
      for (const y of ys) {
        for (const state of ["PENDING", "SPENT"]) {
          const e = element("proof_state", y, state);
          if (positions.has(position(e, decoded.length, info.p))) {
            hits.push({ start: filter.start, y, state });
          }
        }
      }
    }
  }
  return { hits, nextPage: info.current_page, since: info.latest_end };
}
```

`fromPage` and `since` are the two bookmarks a wallet stores: the page it stopped on, and the `end` of the newest filter it scanned. The page bookmark skips whole immutable pages; the timestamp skips filters already seen on the page that was still filling. A wallet recovering from a seed passes `0` for both. The pending filter is tested with the same `decodeFilter` and `position` calls, recomputing `N` on every poll.

[NUT-00]: ../00.md
