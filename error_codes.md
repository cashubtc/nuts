# NUT Errors

| Code  | Description                                        | Relevant nuts                                                        |
| ----- | -------------------------------------------------- | -------------------------------------------------------------------- |
| 10001 | Proof verification failed                          | [NUT-03][03], [NUT-05][05], [NUT-28][28], [NUT-29][29]               |
| 11001 | Proofs already spent                               | [NUT-03][03], [NUT-05][05], [NUT-28][28], [NUT-29][29]               |
| 11002 | Proofs are pending                                 | [NUT-03][03], [NUT-05][05], [NUT-28][28], [NUT-29][29]               |
| 11003 | Outputs already signed                             | [NUT-03][03], [NUT-04][04], [NUT-05][05]                             |
| 11004 | Outputs are pending                                | [NUT-03][03], [NUT-04][04], [NUT-05][05]                             |
| 11005 | Transaction is not balanced (inputs != outputs)    | [NUT-02][02], [NUT-03][03], [NUT-05][05], [NUT-29][29]               |
| 11006 | Amount outside of limit range                      | [NUT-04][04], [NUT-05][05]                                           |
| 11007 | Duplicate inputs provided                          | [NUT-03][03], [NUT-04][04], [NUT-05][05], [NUT-28][28], [NUT-29][29] |
| 11008 | Duplicate outputs provided                         | [NUT-03][03], [NUT-04][04], [NUT-05][05], [NUT-29][29]               |
| 11009 | Inputs/Outputs of multiple units                   | [NUT-03][03], [NUT-04][04], [NUT-05][05]                             |
| 11010 | Inputs and outputs not of same unit                | [NUT-03][03], [NUT-04][04], [NUT-05][05]                             |
| 11011 | Amountless invoice is not supported                | [NUT-05][05]                                                         |
| 11012 | Amount in request does not equal invoice           | [NUT-05][05]                                                         |
| 11013 | Unit in request is not supported                   | [NUT-04][04], [NUT-05][05]                                           |
| 11014 | Max inputs exceeded                                | [NUT-03][03], [NUT-05][05]                                           |
| 11015 | Max outputs exceeded                               | [NUT-03][03], [NUT-04][04], [NUT-05][05]                             |
| 12001 | Keyset is not known                                | [NUT-02][02], [NUT-04][04], [NUT-28][28], [NUT-29][29]               |
| 12002 | Keyset is inactive, cannot sign messages           | [NUT-02][02], [NUT-03][03], [NUT-04][04], [NUT-28][28], [NUT-29][29] |
| 20001 | Quote request is not paid                          | [NUT-04][04]                                                         |
| 20002 | Quote has already been issued                      | [NUT-04][04]                                                         |
| 20003 | Minting is disabled                                | [NUT-04][04]                                                         |
| 20004 | Lightning payment failed                           | [NUT-05][05]                                                         |
| 20005 | Quote is pending                                   | [NUT-04][04], [NUT-05][05]                                           |
| 20006 | Invoice already paid                               | [NUT-05][05]                                                         |
| 20007 | Quote is expired                                   | [NUT-04][04], [NUT-05][05]                                           |
| 20008 | Signature for mint request invalid                 | [NUT-20][20]                                                         |
| 20009 | Pubkey required for mint quote                     | [NUT-20][20]                                                         |
| 30001 | Endpoint requires clear auth                       | [NUT-21][21]                                                         |
| 30002 | Clear authentication failed                        | [NUT-21][21]                                                         |
| 31001 | Endpoint requires blind auth                       | [NUT-22][22]                                                         |
| 31002 | Blind authentication failed                        | [NUT-22][22]                                                         |
| 31003 | Maximum BAT mint amount exceeded                   | [NUT-22][22]                                                         |
| 31004 | BAT mint rate limit exceeded                       | [NUT-22][22]                                                         |
| 13010 | Invalid oracle signature                           | [NUT-28][28]                                                         |
| 13011 | Oracle announcement verification failed            | [NUT-28][28]                                                         |
| 13014 | Conditional keyset requires oracle witness         | [NUT-28][28]                                                         |
| 13015 | Oracle has not attested to this outcome collection | [NUT-28][28]                                                         |
| 13016 | Inputs must use the same conditional keyset        | [NUT-28][28]                                                         |
| 13017 | Outputs must use a regular keyset                  | [NUT-28][28]                                                         |
| 13020 | Invalid condition ID                               | [NUT-28][28]                                                         |
| 13021 | Condition not found                                | [NUT-28][28], [NUT-29][29]                                           |
| 13022 | Split amount mismatch                              | [NUT-29][29]                                                         |
| 13024 | Condition not active                               | [NUT-29][29]                                                         |
| 13025 | Merge amount mismatch                              | [NUT-29][29]                                                         |
| 13027 | Oracle threshold not met                           | [NUT-28][28]                                                         |
| 13028 | Condition already exists                           | [NUT-28][28]                                                         |
| 13030 | Invalid numeric range (lo_bound >= hi_bound)       | [NUT-30][30]                                                         |
| 13031 | Digit signature verification failed                | [NUT-30][30]                                                         |
| 13032 | Attested value outside representable range         | [NUT-30][30]                                                         |
| 13033 | Payout calculation overflow                        | [NUT-30][30]                                                         |
| 13037 | Overlapping outcome collections                    | [NUT-28][28], [NUT-29][29]                                           |
| 13038 | Incomplete partition                               | [NUT-28][28], [NUT-29][29]                                           |
| 13040 | Maximum condition depth exceeded                   | [NUT-29][29]                                                         |

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
[28]: 28.md
[29]: 29.md
[30]: 30.md
