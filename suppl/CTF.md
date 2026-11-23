# Supplementary: NUT-CTF Design Decisions

## Q&A: Design Decisions

### Why use a cursor in addition to `since`?

A timestamp alone cannot page through more than one page of registrations
created in the same second. The cursor includes the timestamp and stable ID.
`since` remains a registration filter. It cannot discover an attestation added
to an older condition. Individual condition queries reveal interest to the
mint; this protocol does not promise query privacy.

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

## Oracle Communication Notes

### Note on adaptor signatures

This specification does NOT use adaptor signatures. In Cashu's custodial model, the mint directly verifies the oracle's BIP 340 signature — no adaptor encryption/decryption is needed.

### Oracle evidence and mint trust

Oracle-authenticated resolution uses the registered oracle's DLC evidence,
even when the mint operator also acts as the oracle. Clients can fetch and
verify this evidence once, then retain it. It need not appear in every response.
Discretionary refunds are a separate human-operated exception and need no
oracle signature. Signature verification does not prove the real-world result
is true or guarantee payment by the mint.

[00]: ../00.md
[02]: ../02.md
[03]: ../03.md
[06]: ../06.md
[12]: ../12.md
[CTF]: ../CTF.md
[CTF-split-merge]: ../CTF-split-merge.md
