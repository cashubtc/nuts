# NUT-XX: Deterministic Currency Unit Indices

`optional`

`depends on: NUT-01`

---

This NUT standardizes how mints and wallets derive a deterministic BIP32 index for every currency unit string they support. The index becomes the second hardened component of the derivation path the mint uses when generating key material for a keyset unit (see [NUT-01][nut01]). Wallets that implement deterministic secrets ([NUT-13][nut13]) use the same index so that both sides converge on the identical derivation path for a given unit.

The goal is to guarantee that every implementation maps a currency unit label to the same hardened index, independent of platform, locale, or Unicode representation.

## Canonical Unit Parsing

Implementations **MUST** accept currency unit labels case-insensitively and ignore leading or trailing ASCII whitespace. When serializing a unit into JSON (e.g., as part of a keyset description in NUT-01 responses), implementations **SHOULD** emit the uppercase representation of the unit so that mints and wallets display consistent labels.

Before deriving an index, the input label **MUST** be transformed as follows:

1. Remove leading and trailing ASCII whitespace characters (space, tab, carriage return, line feed).
2. Apply Unicode Normalization Form C (NFC).
3. Convert the normalized string to uppercase using Unicode-aware semantics.

All further processing uses this uppercase canonical string.

## Reserved Indices

The following currency units occupy the reserved band `[0, 4]` to maintain compatibility with earlier releases. Implementations **MUST** return these indices without hashing:

| Unit | Index |
| ---- | ----- |
| `SAT` | `0` |
| `MSAT` | `1` |
| `USD` | `2` |
| `EUR` | `3` |
| `AUTH` | `4` |

## Custom Unit Index Derivation

For every other unit, implement the following deterministic procedure. The result is always a hardened child index in the inclusive range `[5, 2^31 - 1]`.

```text
RESERVED = 5
HARDENED_MAX = 2^31 - 1
INTERVAL_SIZE = HARDENED_MAX - RESERVED + 1

canon = canonicalize(unit)                # per Canonical Unit Parsing
hash  = SHA256(canon UTF-8 bytes)
X     = first 4 bytes of hash interpreted as big-endian u32
R     = X mod INTERVAL_SIZE
index = RESERVED + R
```

Implementations **MUST** use SHA-256 for hashing and **MUST** operate on UTF-8 encoded bytes. The modulus step folds the 32-bit space uniformly into the available hardened interval, ensuring deterministic results and avoiding collisions with the reserved indices.

If a unit string hashes to a value already in `[0, RESERVED - 1]`, the final addition shifts it out of the reserved band, so collisions cannot occur.

## Examples

The table below illustrates a few unit labels and their resulting indices. Different capitalizations, redundant whitespace, or canonically equivalent Unicode sequences always produce the same value.

| Input unit | Canonical form | Index |
| ---------- | -------------- | ----- |
| `nuts` | `NUTS` | `1502388632` |
| `USD` | `USD` | `2` *(reserved)* |
| ` usD ` | `USD` | `2` *(reserved)* |
| `café` | `CAFÉ` | `642348970` |
| `cafe\u0301` | `CAFÉ` | `642348970` |
| `eurc` | `EURC` | `1321886555` |

> [!NOTE]
> Reserved units continue to return their fixed indices after canonicalization. The example rows for `USD` illustrate that even when presented with mixed case or padded whitespace, the implementation must fall back to the reserved index table, not the hash-based path.

Additional sample values are provided in the [test vectors][tests] accompanying this NUT.

## Usage with Deterministic Secrets

Mints that derive keysets deterministically place the unit index as the second hardened element in their derivation path:

```
Keyset derivation path: m / 0' / <unit_index>' / <keyset_counter>'
```

Wallets that implement [NUT-13][nut13] **MUST** reuse the same `unit_index` when constructing their secret derivation paths to guarantee compatibility with mints advertising this NUT. Without that alignment, a wallet could derive secrets with a different index than the mint, making recovery impossible.

[nut01]: https://cashubtc.github.io/nuts/01/
[nut13]: https://cashubtc.github.io/nuts/13/
[tests]: tests/XX-tests.md
