# Cashu NUTs (Notation, Usage, and Terminology)

These documents each specify parts of the Cashu protocol. Read the specifications for the legacy API [here](https://github.com/cashubtc/nuts/tree/74f26b81b6617db710fa1081eebc0c7203711213).

## Specifications

Wallets and mints `MUST` implement all mandatory specs and `CAN` implement optional specs.

### Mandatory

| NUT #    | Description             |
| -------- | ----------------------- |
| [00][00] | Cryptography and Models |
| [01][01] | Mint public keys        |
| [02][02] | Keysets and fees        |
| [03][03] | Swapping tokens         |
| [04][04] | Minting tokens          |
| [05][05] | Melting tokens          |
| [06][06] | Mint info               |

### Optional

| #        | Description                       | Wallets                                                                     | Mints                                                   |
| -------- | --------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------- |
| [07][07] | Token state check                 | [Nutshell][py], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts], [cdk-cli] | [Nutshell][py], [Moksha][moksha], [cdk-mintd], [nutmix] |
| [08][08] | Overpaid Lightning fees           | [Nutshell][py], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts], [cdk-cli] | [Nutshell][py], [Moksha][moksha], [cdk-mintd], [nutmix] |
| [09][09] | Signature restore                 | [Nutshell][py], [cdk-cli], [cashu-ts][ts], [gonuts]                         | [Nutshell][py], [cdk-mintd], [nutmix]                   |
| [10][10] | Spending conditions               | [Nutshell][py], [cdk-cli], [cashu-ts][ts]                                   | [Nutshell][py], [cdk-mintd], [nutmix]                   |
| [11][11] | Pay-To-Pubkey (P2PK)              | [Nutshell][py], [cdk-cli], [cashu-ts][ts]                                   | [Nutshell][py], [cdk-mintd], [nutmix]                   |
| [12][12] | DLEQ proofs                       | [Nutshell][py], [cdk-cli]                                                   | [Nutshell][py], [cdk-mintd], [nutmix]                   |
| [13][13] | Deterministic secrets             | [Nutshell][py], [Moksha][moksha], [cashu-ts][ts], [cdk-cli], [gonuts]       | -                                                       |
| [14][14] | Hashed Timelock Contracts (HTLCs) | [Nutshell][py], [cdk-cli]                                                   | [Nutshell][py], [cdk-mintd], [nutmix]                   |
| [15][15] | Partial multi-path payments (MPP) | [Nutshell][py]                                                              | [Nutshell][py]                                          |
| [16][16] | Animated QR codes                 | [Cashu.me][cashume]                                                         | -                                                       |
| [17][17] | WebSocket subscriptions           | [Nutshell][py]                                                              | [Nutshell][py]                                          |
| [18][18] | Payment requests                  | [Cashu.me][cashume], [Boardwalk][bwc], [cdk-cli]                            | -                                                       |

#### Wallets:

- [Nutshell][py]
- [cdk-cli][cdk-cli]
- [cashu-ts][ts]
- [eNuts][enuts]
- [Minibits][minibits]
- [Moksha][moksha]
- [Nutstash][ns]
- [Cashu.me][cashume]
- [Gonuts][gonuts]
- [Boardwalk][bwc]

#### Mints:

- [Nutshell][py]
- [Gonuts][gonuts]
- [Moksha][moksha]
- [cdk-mintd][cdk-mintd]
- [Nutmix][nutmix]

[py]: https://github.com/cashubtc/nutshell
[lnbits]: https://github.com/lnbits/cashu
[cashume]: https://cashu.me
[ns]: https://nutstash.app/
[ts]: https://github.com/cashubtc/cashu-ts
[enuts]: https://github.com/cashubtc/eNuts
[minibits]: https://github.com/minibits-cash/minibits_wallet
[moksha]: https://github.com/ngutech21/moksha
[cdk]: https://github.com/cashubtc/cdk
[cdk-cli]: https://github.com/cashubtc/cdk/tree/main/crates/cdk-cli
[cdk-mintd]: https://github.com/cashubtc/cdk/tree/main/crates/cdk-mintd
[gonuts]: https://github.com/elnosh/gonuts
[nutmix]: https://github.com/lescuer97/nutmix
[bwc]: https://github.com/MakePrisms/boardwalkcash
[00]: 00.md
[01]: 01.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[07]: 07.md
[08]: 08.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[13]: 13.md
[14]: 14.md
[15]: 15.md
[16]: 16.md
[17]: 17.md
[18]: 18.md
