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
| #        | Description                       | Wallets                                                                            | Mints                                            |
| -------- | --------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------ |
| [07][07] | Token state check                 | [Nutshell][py], [Nutstash][ns], [cashu-ts][ts], [cdk-cli], [Minibits], [macadamia] | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [08][08] | Overpaid Lightning fees           | [Nutshell][py], [Nutstash][ns], [cashu-ts][ts], [cdk-cli], [Minibits], [macadamia] | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [09][09] | Signature restore                 | [Nutshell][py], [cdk-cli], [Cashu.me][cashume], [Minibits], [macadamia]            | [Nutshell][py], [cdk-mintd]                      |
| [10][10] | Spending conditions               | [Nutshell][py], [cdk-cli], [cashu-ts][ts], [Minibits]                              | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [11][11] | Pay-To-Pubkey (P2PK)              | [Nutshell][py], [cdk-cli], [Cashu.me][cashume], [Minibits]                         | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [12][12] | DLEQ proofs                       | [Nutshell][py], [cdk-cli], [cashu-ts][ts]                                          | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [13][13] | Deterministic secrets             | [Nutshell][py], [cashu-ts][ts], [cdk-cli], [macadamia], [Minibits]                 | -                                                |
| [14][14] | Hashed Timelock Contracts (HTLCs) | [Nutshell][py], [cdk-cli]                                                          | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [15][15] | Partial multi-path payments (MPP) | [Nutshell][py], [cdk-cli]                                                          | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [16][16] | Animated QR codes                 | [Cashu.me][cashume], [macadamia], [Minibits]                                       | -                                                |
| [17][17] | WebSocket subscriptions           | [Nutshell][py], [cdk-cli][cdk-cli], [Cashu.me][cashume], [Minibits]                | [Nutshell][py], [cdk-mintd][cdk-mintd], [nutmix] |
| [18][18] | Payment requests                  | [Cashu.me][cashume], [Boardwalk][bwc], [cdk-cli], [Minibits]                       | -                                                |
| [19][19] | Cached Responses                  | -                                                                                  | [Nutshell][py], [cdk-mintd]                      |
| [20][20] | Signature on Mint Quote           | [cdk-cli], [Nutshell][py]                                                          | [cdk-mintd], [Nutshell][py]                      |
| [21][21] | Clear authentication              | [Nutshell][py], [cdk-cli]                                                          | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [22][22] | Blind authentication              | [Nutshell][py], [cdk-cli]                                                          | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [23][23] | Payment Method: BOLT11            | [Nutshell][py], [cdk-cli]                                                          | [Nutshell][py], [cdk-mintd], [nutmix]            |
| [24][24] | HTTP 402 Payment Required         | -                                                                                  | -                                                |
| [25][25] | Payment Method: BOLT12            | [cdk-cli], [cashu-ts][ts]                                                          | [cdk-mintd]                                      |
| [26][26] | Pay-to-Blinded-Key (P2BK)         | [cashu-ts][ts]                                                                     | -                                                |

#### Wallets:

- [Nutshell][py]
- [CDK-cli][cdk-cli]
- [cashu-ts][ts]
- [Macadamia][macadamia]
- [Minibits][minibits]
- [Nutstash][ns]
- [Cashu.me][cashume]
- [Boardwalk][bwc]

#### Mints:

- [Nutshell][py]
- [cdk-mintd][cdk-mintd]
- [Nutmix][nutmix]

[py]: https://github.com/cashubtc/nutshell
[lnbits]: https://github.com/lnbits/cashu
[cashume]: https://cashu.me
[ns]: https://nutstash.app/
[ts]: https://github.com/cashubtc/cashu-ts
[enuts]: https://github.com/cashubtc/eNuts
[macadamia]: https://github.com/zeugmaster/macadamia
[minibits]: https://github.com/minibits-cash/minibits_wallet
[moksha]: https://github.com/ngutech21/moksha
[cdk]: https://github.com/cashubtc/cdk
[cdk-cli]: https://github.com/cashubtc/cdk/tree/main/crates/cdk-cli
[cdk-mintd]: https://github.com/cashubtc/cdk/tree/main/crates/cdk-mintd
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
[19]: 19.md
[20]: 20.md
[21]: 21.md
[22]: 22.md
[23]: 23.md
[24]: 24.md
[25]: 25.md
