# Cashu NUTs (Notation, Usage, and Terminology)

These documents each specify parts of the Cashu protocol. Read the specifications for the legacy API [here](https://github.com/cashubtc/nuts/tree/74f26b81b6617db710fa1081eebc0c7203711213).

## Specifications
Wallets and mints `MUST` implement all mandatory specs and `CAN` implement optional specs.

### Mandatory

| NUT #    | Description                       |
|----------|-----------------------------------|
| [00][00] | Cryptography and Models           |
| [01][01] | Mint public keys                  |
| [02][02] | Keysets and keyset IDs            |
| [03][03] | Swapping tokens                   |
| [04][04] | Minting tokens                    |
| [05][05] | Melting tokens                    |
| [06][06] | Mint info                         |

### Optional

| # | Description | Wallets | Mints |
| --- | --- | --- | --- |
| [07][07] | Token state check | [Nutshell][py], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts], [cdk] | [Nutshell][py], [LNbits], [Moksha][moksha], [cashu-rs-mint][cashu-rs-mint] |
| [08][08] | Overpaid Lightning fees | [Nutshell][py], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts], [cdk] | [Nutshell][py], [LNbits], [Moksha][moksha], [cashu-rs-mint][cashu-rs-mint] |
| [09][09] | Signature restore | [Nutshell][py], [cdk], [cashu-ts][ts] | [Nutshell][py], [cashu-rs-mint][cashu-rs-mint]
| [10][10] | Spending conditions | [Nutshell][py], [cdk] | [Nutshell][py], [cashu-rs-mint] |
| [11][11] | Pay-To-Pubkey (P2PK) | [Nutshell][py], [cdk] | [Nutshell][py], [cashu-rs-mint] |
| [12][12] | DLEQ proofs | [Nutshell][py], [cdk] | [Nutshell][py], [cashu-rs-mint] |
| [13][13] | Deterministic secrets | [Nutshell][py], [Moksha][moksha], [cashu-ts][ts], [cdk] | - |
| [14][14] | Hashed Timelock Contracts (HTLCs) | [Nutshell][py], [cdk] | [Nutshell][py], [cashu-rs-mint] |
| [15][15] | Partial multi-path payments (MPP) | [Nutshell][py] | [Nutshell][py] |

#### Wallets:

 - [Nutshell][py]
 - [cdk][cdk]
 - [cashu-ts][ts]
 - [eNuts][enuts]
 - [Moksha][moksha]
 - [Nutstash][ns]
 - [Cashu.me][cashume]
 - [Gonuts][gonuts]

#### Mints:
 
 - [Nutshell][py]
 - [Gonuts][gonuts]
 - [LNbits][lnbits]
 - [Moksha][moksha]
 - [cashu-rs-mint][cashu-rs-mint]
 

[py]: https://github.com/cashubtc/cashu
[lnbits]: https://github.com/lnbits/cashu
[cashume]: https://cashu.me
[ns]: https://nutstash.app/
[ts]: https://github.com/cashubtc/cashu-ts
[enuts]: https://github.com/cashubtc/eNuts
[moksha]: https://github.com/ngutech21/moksha
[cdk]: https://github.com/cashubtc/cdk
[cashu-rs-mint]: https://github.com/thesimplekid/cashu-rs-mint
[gonuts]: https://github.com/elnosh/gonuts

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