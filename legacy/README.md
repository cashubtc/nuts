# Legacy specifications

These documents specify the parts of the Cashu protocol that [pre-v3 keysets](../02.md#keyset-id-v3) still use, unchanged apart from this header and link targets. A NUT with no copy here is unchanged. The [current specifications](../README.md) govern anything that touches a v3 keyset.

| NUT #       | Description                       | Current specification |
| ----------- | --------------------------------- | --------------------- |
| [00](00.md) | Cryptography and Models           | [NUT-00](../00.md)    |
| [01](01.md) | Mint public keys                  | [NUT-01](../01.md)    |
| [02](02.md) | Keysets and fees                  | [NUT-02](../02.md)    |
| [03](03.md) | Swapping tokens                   | [NUT-03](../03.md)    |
| [04](04.md) | Minting tokens                    | [NUT-04](../04.md)    |
| [05](05.md) | Melting tokens                    | [NUT-05](../05.md)    |
| [06](06.md) | Mint info                         | [NUT-06](../06.md)    |
| [07](07.md) | Token state check                 | [NUT-07](../07.md)    |
| [08](08.md) | Overpaid Lightning fees           | [NUT-08](../08.md)    |
| [09](09.md) | Signature restore                 | [NUT-09](../09.md)    |
| [10](10.md) | Spending conditions               | [NUT-10](../10.md)    |
| [11](11.md) | Pay-To-Pubkey (P2PK)              | [NUT-10](../10.md)    |
| [12](12.md) | DLEQ proofs                       | [NUT-00](../00.md)    |
| [13](13.md) | Deterministic secrets             | [NUT-13](../13.md)    |
| [14](14.md) | Hashed Timelock Contracts (HTLCs) | [NUT-10](../10.md)    |
| [17](17.md) | WebSocket subscriptions           | [NUT-17](../17.md)    |
| [18](18.md) | Payment requests                  | [NUT-18](../18.md)    |
| [20](20.md) | Signature on Mint Quote           | [NUT-20](../20.md)    |
| [22](22.md) | Blind authentication              | [NUT-22](../22.md)    |
| [23](23.md) | Payment Method: BOLT11            | [NUT-23](../23.md)    |
| [24](24.md) | HTTP 402 Payment Required         | [NUT-24](../24.md)    |
| [25](25.md) | Payment Method: BOLT12            | [NUT-25](../25.md)    |
| [26](26.md) | Payment Request Bech32m Encoding  | [NUT-26](../26.md)    |
| [27](27.md) | Nostr Mint Backup                 | [NUT-27](../27.md)    |
| [28](28.md) | Pay to Blinded Key (P2BK)         | [NUT-28](../28.md)    |
| [29](29.md) | Batched Mint                      | [NUT-29](../29.md)    |
| [30](30.md) | Payment Method: Onchain           | [NUT-30](../30.md)    |

Test vectors are in [`tests/`](tests).

Maintainers: this folder is a snapshot of `1363de4`, regenerated rather than edited.
