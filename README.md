# Cashu NUTs (Notation, Usage, and Terminology)

These documents each specify parts of the Cashu protocol.

## Wallet protocol

A description of the steps of the protocol is given in the Cashu [wallet specs](/wallet/cashu_wallet_spec.md).

## Specifications
Wallets and mints `MUST` implement all mandatory specs and `CAN` implement optional specs.

### Mandatory
| # | Description | Wallets | Mints |
|--- | --- | --- | --- |
| [00][00] | Cryptography and Models | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [01][01] | Mint public keys | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [02][02] | Keysets and keyset IDs | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [03][03] | Request minting | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [04][04] | Minting tokens | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [05][05] | Melting tokens | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [06][06] | Splitting tokens | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]

### Optional
| # | Description | Wallets | Mints
|--- | --- | --- | --- |
| [07][07] | Token state check | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [Feni][feni], [LNbits], [Moksha][moksha]
| [08][08] | Overpaid Lightning fees | [Nutshell][py], [Feni][feni], [Moksha][moksha], [Nutstash][ns], [cashu-ts][ts] | [Nutshell][py], [LNbits], [Moksha][moksha]
| [09][09] | Mint info | [Nutshell][py], [eNuts][enuts] | [Nutshell][py]
| [10][10] | Spending conditions | [Nutshell][py] | [Nutshell][py]
| [11][11] | Pay-To-Pubkey (P2PK) | [Nutshell][py] | [Nutshell][py]
| TBD | DLEQ proofs | - | -



[py]: https://github.com/cashubtc/cashu
[feni]: https://github.com/cashubtc/cashu-feni
[lnbits]: https://github.com/lnbits/cashu
[cashume]: https://cashu.me
[ns]: https://nutstash.app/
[ts]: https://github.com/cashubtc/cashu-ts
[enuts]: https://github.com/cashubtc/eNuts
[moksha]: https://github.com/ngutech21/moksha

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
