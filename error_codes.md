# NUT Errors

| Code  | Description                                     | Relevant nuts                            |
| ----- | ----------------------------------------------- | ---------------------------------------- |
| 10002 | Blinded message of output already signed        | [NUT-03][03], [NUT-04][04], [NUT-05][05] |
| 10003 | Token could not be verified                     | [NUT-03][03], [NUT-05][05]               |
| 11001 | Token is already spent                          | [NUT-03][03], [NUT-05][05]               |
| 11002 | Transaction is not balanced (inputs != outputs) | [NUT-02][02], [NUT-03][03], [NUT-05][05] |
| 11005 | Unit in request is not supported                | [NUT-04][04], [NUT-05][05]               |
| 11006 | Amount outside of limit range                   | [NUT-04][04], [NUT-05][05]               |
| 11007 | Duplicate inputs provided                       | [NUT-03][03], [NUT-04][04], [NUT-05][05] |
| 11008 | Duplicate outputs provided                      | [NUT-03][03], [NUT-04][04], [NUT-05][05] |
| 11009 | Inputs/Outputs of multiple units                | [NUT-03][03], [NUT-04][04], [NUT-05][05] |
| 11010 | Inputs and outputs not of same unit             | [NUT-03][03], [NUT-04][04], [NUT-05][05] |
| 11011 | Amountless invoice is not supported             | [NUT-05][05]                             |
| 11012 | Amount in request does not equal invoice        | [NUT-05][05]                             |
| 12001 | Keyset is not known                             | [NUT-02][02], [NUT-04][04]               |
| 12002 | Keyset is inactive, cannot sign messages        | [NUT-02][02], [NUT-03][03], [NUT-04][04] |
| 20001 | Quote request is not paid                       | [NUT-04][04]                             |
| 20002 | Tokens have already been issued for quote       | [NUT-04][04]                             |
| 20003 | Minting is disabled                             | [NUT-04][04]                             |
| 20004 | Lightning payment failed                        | [NUT-05][05]                             |
| 20005 | Quote is pending                                | [NUT-04][04], [NUT-05][05]               |
| 20006 | Invoice already paid                            | [NUT-05][05]                             |
| 20007 | Quote is expired                                | [NUT-04][04], [NUT-05][05]               |
| 20008 | Signature for mint request invalid              | [NUT-20][20]                             |
| 20009 | Pubkey required for mint quote                  | [NUT-20][20]                             |
| 30001 | Endpoint requires clear auth                    | [NUT-21][21]                             |
| 30002 | Clear authentication failed                     | [NUT-21][21]                             |
| 31001 | Endpoint requires blind auth                    | [NUT-22][22]                             |
| 31002 | Blind authentication failed                     | [NUT-22][22]                             |
| 31003 | Maximum BAT mint amount exceeded                | [NUT-22][22]                             |
| 31004 | BAT mint rate limit exceeded                    | [NUT-22][22]                             |

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
[20]: 20.md
[21]: 21.md
[22]: 22.md
