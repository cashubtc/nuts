# NUT-XX: Prime proofs

`optional`

`depends on: NUT-XX (Keyset extension that allows the mint to signal the keyset type via a new field keyset_type)`

---

This NUT proposes a proof selection scheme that enables more compact tokens. With it, a token can represent any even amount with at most 2 proofs and any odd amount with at most 3 proofs.

---

Goldbach's conjecture states that every even natural number greater than 2 is the sum of two primes. Though unproven, it was shown to hold at least up to `4 * 10^19`[^1]. This NUT is for mints and wallets dealing with maximum amounts below this value.

Based on this, a token can be decomposed in proofs as follows:

| Token amount |            Proof amounts |
|-------------:|-------------------------:|
|            1 |                        1 |
|          `p` |                      `p` |
|         `2n` |                `p1 + p2` |
|     `2n + 1` | `p + 2` or `p1 + p2 + 1` |

where `p`, `p1` and `p2` are primes.

In other words, any amount can be built from at most 3 proofs, but sometimes from only 1 or 2.

To allow wallets to use this scheme, a keyset has to include signatures for `1` and primes up to `P`.


### Client algorithm

There are multiple possible decompositions[^2] for each token amount. When building a token, the wallet only has to find one.

For very low-powered devices, the app can include a table with precomputed decompositions for `1..M`.

Otherwise, the wallet could decompose an amount as follows:

```
// Inputs:
// - keyset_amounts[]: 1 and the first primes until P
// - token_amount: amount for which to construct a token, token_amount <= mint maximum M
function find_proof_amounts(keyset_amounts[], token_amount):
    // Special cases: if token_amount is 1 or a prime
    if keyset_amounts[] contains token_amount
        return [token_amount]
    
    proof_amounts = []
    
    target =
        if token_amount % 2 == 0
            token_amount
        else
            append 1 to proof_amounts[]
            token_amount - 1
        
    for p1 in keyset_amounts
        if p1 > target / 2
            break
            
        p2 = target - p1
        
        if keyset_amounts[] not contains p2
            continue
        
        append p1 to proof_amounts[]
        append p2 to proof_amounts[]
        return proof_amounts[]
        
    return Error("No matching primes found")
```


### Mint Considerations

When choosing how many primes to include, the mint has 2 limiting factors:

  - the maximum token amount the mint allows to be minted or melted `M = max(MAX_mint, MAX_melt)`
  - the payload size for the `GET /v1/keys/:keyset_id` endpoint


#### Range

A naive, but simple approach is for the keyset to include all primes up to `P <= M`.


#### Payload size

Here are a few sample keysets that contain signatures for `1` and primes up to `P`, which allow all token amounts `1..=M` to be represented as a sum of up to 3 keyset amounts:

| Number of primes | Max prime `P` | Max token amount `M` |        Decomposition of `M` | Keyset size | 4G (ms) |
|-----------------:|--------------:|---------------------:|----------------------------:|------------:|--------:|
|            `100` |         `541` |                `967` |             `479 + 487 + 1` |        9 KB |     3.6 |
|          `1_000` |       `7_919` |             `15_523` |         `7_699 + 7_823 + 1` |       86 KB |    34.4 |
|         `10_000` |     `104_729` |            `208_927` |     `104_399 + 104_527 + 1` |      869 KB |   347.6 |
|        `100_000` |   `1_299_709` |          `2_598_333` | `1_298_779 + 1_299_553 + 1` |      8.8 MB |  3604.5 |

Mints which mint or melt amounts of up to `~200_000` can use a keyset containing signatures for `1` and the first `10_000` primes. The `GET /v1/keys/:keyset_id` uncompressed payload would be ~870 KB. With HTTP compression, that can be halved[^3]. The uncompressed payload can be downloaded over 4G in about 350 ms, assuming an average speed of 20 Mbps.

Since the keyset signatures are not fetched that often[^4] by the wallets, even a 3.6s download time (or 1.8s with HTTP compression) could be acceptable for mints that wish to support max amounts of `~2_500_000`.


### Summary

This NUT brings consistently small tokens (up to 3 proofs for any token amount) in exchange for a larger keyset. The keyset size can be reduced by the mint choosing a lower maximum mint or melt amount `M`. Furthermore, the keyset size can be halved if the mint and the wallets support HTTP compression.

In contrast, keysets that use amounts that are powers of two often result in larger tokens (i.e. more proofs needed):

| Token amount | Proof amounts (powers of two) | Proof amounts (this NUT) |
|-------------:|:------------------------------|:-------------------------|
|            6 | 2, 4                          | 3, 3                     |
|            7 | 1, 2, 4                       | 2, 5                     |
|           10 | 2, 8                          | 5, 5                     |
|           30 | 2, 4, 8, 16                   | 7, 23                    |
|           31 | 1, 2, 4, 8, 16                | 1, 7, 23                 |
|           63 | 1, 2, 4, 8, 16, 32            | 1, 3, 59                 |
|          127 | 1, 2, 4, 8, 16, 32, 64        | 127                      |
|          255 | 1, 2, 4, 8, 16, 32, 64, 128   | 1, 3, 251                |
|          700 | 4, 8, 16, 32, 128, 512        | 17, 683                  |
|         1000 | 8, 32, 64, 128, 256, 512      | 3, 997                   |


[^1]: This is 1 order of magnitude away from what a 64 bit unsigned integer can hold (`~1.8 * 10^20`).

[^2]: https://en.wikipedia.org/wiki/Goldbach%27s_comet

[^3]: https://github.com/cashubtc/nuts/pull/176

[^4]: As per NUT-02: https://cashubtc.github.io/nuts/02/#wallet-implementation-notes