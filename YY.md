# NUT-YY: Template leaf

`optional`

`depends on: NUT-10 NUT-XX`

---

The `template` leaf is a [NUT-10](10.md#optional-leaves) condition leaf that is a covenant on where value goes.

| Leaf       | Type   | Fields               | Satisfied by                                                                                             |
| ---------- | ------ | -------------------- | -------------------------------------------------------------------------------------------------------- |
| `template` | `0x05` | `n`, `keys`, `dests` | every output a fixed txout quote locked to a key in `dests`, plus signatures by `n` distinct listed keys |

`dests` (field `0x0c`) **MUST** list at least one valid compressed secp256k1 point, and a repeated key **MUST** be rejected.

## Evaluation

Every output container of the spending transaction **MUST** be a mint quote output (`0x23`, [NUT-XX](XX.md#fixed-txout-quote)) whose lock key is listed in `dests`. Amounts, ids and the number of outputs are the spender's.

On receive, a `template` leaf counts toward [NUT-00](00.md#receive-time-verification)'s check 2 only when the wallet also holds the key of a listed destination.

> [!CAUTION]
> Destinations are fixed when the lock is set, so every spend through the leaf pays the same keys and the mint links them, including repeated issuance from a refillable quote (bolt12, on-chain). A template suits payments that may be linked, such as a standing order or a vault.

## Signaling

A mint implementing the leaf lists `0005` in its NUT-10 [`leaves`](10.md#signaling), and **MUST** then set `fixed_txout_quotes` ([NUT-XX](XX.md#settings)).

**Note:** See the [test vectors][tests].

[tests]: tests/YY-tests.md
