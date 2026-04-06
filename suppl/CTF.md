# Supplementary: NUT-CTF Design Decisions

## Q&A: Design Decisions

### Why "download all, then sync" instead of server-side filtering?

Supporting complex query combinations (filter by oracle, by unit, by date range, etc.) increases server complexity and creates a DoS vector — an attacker can craft expensive queries to burden the mint. More importantly, fine-grained server-side filtering leaks information about which conditions a wallet cares about, potentially revealing trading positions to the mint. The "download all, then sync with `since`" pattern keeps the server stateless and simple: every client gets the same data, preserving privacy. Since the total number of conditions on a single mint is expected to remain manageable, full downloads are practical.

### Why `>=` instead of `>` for the `since` parameter?

Unix timestamps have second-level precision. If two conditions are registered within the same second and the client uses `>` (strict greater-than), it could silently skip items that share the boundary timestamp. Using `>=` (greater-than-or-equal) guarantees that no items are missed at the cost of re-delivering boundary items. Clients MUST deduplicate by `condition_id` (or keyset `id` for the keysets endpoint), which is trivial with a local set.

### When should users merge vs. wait for resolution?

Merge is useful when:

- A user holds a complete set and wants to exit their position before oracle attestation
- Market conditions change and the user wants to recover collateral immediately
- Arbitrage opportunities exist between the market price and collateral value

Waiting for resolution is simpler when:

- The user expects one outcome to win and wants to maximize profit
- Transaction fees make merge uneconomical

## Keyset ID Derivation Rationale

Without condition-specific data in the keyset ID, a wallet cannot verify from the keyset ID alone that a keyset is bound to a particular condition and outcome collection. By including `condition_id` and `outcome_collection_id` in the preimage, the wallet can recompute the keyset ID and confirm the mint's claim about which condition and outcome collection a keyset serves.

## Redemption Witness Comparison

The Redemption Witness extends the established Cashu pattern where `Proof.witness` carries condition-specific unlock data:

| NUT                       | Witness Type       | Format                                     | Trigger                             |
| ------------------------- | ------------------ | ------------------------------------------ | ----------------------------------- |
| [NUT-11][11] (P2PK)       | Signature          | `{"signatures": [...]}`                    | Secret is P2PK kind ([NUT-10][10])  |
| [NUT-14][14] (HTLC)       | Preimage + sig     | `{"preimage": "...", "signatures": [...]}` | Secret is HTLC kind ([NUT-10][10])  |
| **NUT-CTF** (Conditional) | Oracle attestation | `{"oracle_sigs": [...]}`                   | Dedicated `redeem_outcome` endpoint |

Key difference: [NUT-11][11] and [NUT-14][14] witnesses are triggered by the **secret structure** ([NUT-10][10] well-known format). NUT-CTF witnesses are triggered by the **endpoint** — the dedicated `POST /v1/redeem_outcome` endpoint requires oracle attestation. Proof secrets remain plain random strings.

## Oracle Communication Notes

### Note on adaptor signatures

This specification does NOT use adaptor signatures. In Cashu's custodial model, the mint directly verifies the oracle's BIP 340 signature — no adaptor encryption/decryption is needed.

### Note on oracle attestation optionality

Oracle attestation is optional in principle. When the mint operator serves as the oracle (e.g., resolving disputes manually), no external attestation is needed. However, oracle attestation is useful for two reasons: (1) It provides a standardized way for mints to verify redemption claims, and (2) When combined with DLEQ Proof ([NUT-12][12]) and [Proof of Liabilities](https://gist.github.com/callebtc/ed5228d1d8cbaade0104db5d1cf63939), it can serve as a fraud proof if the mint fails to honor valid redemptions.

[00]: ../00.md
[02]: ../02.md
[03]: ../03.md
[06]: ../06.md
[10]: ../10.md
[11]: ../11.md
[12]: ../12.md
[14]: ../14.md
[CTF]: ../CTF.md
[CTF-split-merge]: ../CTF-split-merge.md
