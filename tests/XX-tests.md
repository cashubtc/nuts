# NUT-XX Test Vectors

`informative`

These vectors help implementers confirm their canonicalization and index derivation logic for [NUT-XX](../XX.md).

- `canonical` is the uppercase NFC form after trimming ASCII whitespace.
- `sha256_first4` is the first four bytes of `SHA256(canonical)` rendered as hex (only relevant for non-reserved units).
- `index` is the final hardened derivation index returned by the algorithm.

| input | canonical | sha256_first4 | index |
| ----- | --------- | ------------- | ----- |
| `sat` | `SAT` | `n/a` | `0` |
| `msat` | `MSAT` | `n/a` | `1` |
| `auth` | `AUTH` | `n/a` | `4` |
| `usd` | `USD` | `n/a` | `2` |
| `eur` | `EUR` | `n/a` | `3` |
| `nuts` | `NUTS` | `598ca193` | `1502388632` |
| `  NUTS  ` | `NUTS` | `598ca193` | `1502388632` |
| `eurc` | `EURC` | `4eca6356` | `1321886555` |
| `cafe\u0301` | `CAFÉ` | `264977a5` | `642348970` |
| `CAFÉ` | `CAFÉ` | `264977a5` | `642348970` |
| `gbp` | `GBP` | `402419e9` | `1076107758` |
| `JPY` | `JPY` | `43d44ae6` | `1137986283` |

Implementations can expand their automated testing to include additional ISO 4217 codes, stablecoin tickers, or application-specific units by following the same procedure.
