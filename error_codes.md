# NUT Errors

| Code  | Description                                        | Relevant nuts                                          |
| ----- | -------------------------------------------------- | ------------------------------------------------------ |
| 10001 | Proof verification failed                          | [NUT-03][03], [NUT-05][05]                             |
| 11001 | Proofs already spent                               | [NUT-03][03], [NUT-05][05]                             |
| 11002 | Proofs are pending                                 | [NUT-03][03], [NUT-05][05]                             |
| 11003 | Outputs already signed                             | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11004 | Outputs are pending                                | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11005 | Transaction is not balanced (inputs != outputs)    | [NUT-02][02], [NUT-03][03], [NUT-05][05]               |
| 11006 | Amount outside of limit range                      | [NUT-04][04], [NUT-05][05]                             |
| 11007 | Duplicate inputs provided                          | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11008 | Duplicate outputs provided                         | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11009 | Inputs/Outputs of multiple units                   | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11010 | Inputs and outputs not of same unit                | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11011 | Amountless invoice is not supported                | [NUT-05][05]                                           |
| 11012 | Amount in request does not equal invoice           | [NUT-05][05]                                           |
| 11013 | Unit in request is not supported                   | [NUT-04][04], [NUT-05][05]                             |
| 11014 | Max inputs exceeded                                | [NUT-03][03], [NUT-05][05]                             |
| 11015 | Max outputs exceeded                               | [NUT-03][03], [NUT-04][04], [NUT-05][05]               |
| 11016 | Duplicate quote IDs provided                       | [NUT-29][29]                                           |
| 11017 | Max batch size exceeded                            | [NUT-29][29]                                           |
| 12001 | Keyset is not known                                | [NUT-02][02], [NUT-04][04]                             |
| 12002 | Keyset is inactive, cannot sign messages           | [NUT-02][02], [NUT-03][03], [NUT-04][04]               |
| 12003 | Keyset has expired                                 | [NUT-02][02], [NUT-03][03], [NUT-04][04], [NUT-05][05] |
| 20001 | Quote request is not paid                          | [NUT-04][04]                                           |
| 20002 | Quote has already been issued                      | [NUT-04][04]                                           |
| 20003 | Minting is disabled                                | [NUT-04][04]                                           |
| 20004 | Lightning payment failed                           | [NUT-05][05]                                           |
| 20005 | Quote is pending                                   | [NUT-04][04], [NUT-05][05], [NUT-29][29]               |
| 20006 | Invoice already paid                               | [NUT-05][05]                                           |
| 20007 | Quote is expired                                   | [NUT-04][04], [NUT-05][05]                             |
| 20008 | Signature for mint request invalid                 | [NUT-20][20]                                           |
| 20009 | Pubkey required for mint quote                     | [NUT-20][20]                                           |
| 30001 | Endpoint requires clear auth                       | [NUT-21][21]                                           |
| 30002 | Clear authentication failed                        | [NUT-21][21]                                           |
| 31001 | Endpoint requires blind auth                       | [NUT-22][22]                                           |
| 31002 | Blind authentication failed                        | [NUT-22][22]                                           |
| 31003 | Maximum BAT mint amount exceeded                   | [NUT-22][22]                                           |
| 31004 | BAT mint rate limit exceeded                       | [NUT-22][22]                                           |
| 15001 | Unsupported or malformed `PAY_TO_UNLOCK` condition | [NUT-Exchange][exchange]                               |
| 15003 | Receive-output commitment (`H_recv`) mismatch      | [NUT-Exchange][exchange]                               |
| 15004 | Offer/receive keyset relationship violated         | [NUT-Exchange][exchange]                               |
| 15005 | Exchange settlement submitted after `expiry`       | [NUT-Exchange][exchange]                               |
| 15006 | Refund submitted before `expiry`                   | [NUT-Exchange][exchange]                               |
| 15007 | Refund signature missing or invalid                | [NUT-Exchange][exchange]                               |
| 15009 | Exchange request exceeds advertised limits         | [NUT-Exchange][exchange]                               |
| 15010 | Conflicting request or reused input (idempotency)  | [NUT-Exchange][exchange]                               |
| 15011 | Pool manifest hash (`H_manifest`) mismatch         | [NUT-Exchange-partial-fill][partial-fill]              |
| 15012 | Pool selection does not match `outputs`            | [NUT-Exchange-partial-fill][partial-fill]              |
| 15013 | Pool role/keyset or two-class consistency violated | [NUT-Exchange-partial-fill][partial-fill]              |
| 15014 | Pool policy violation (rate/min/max/overflow)      | [NUT-Exchange-partial-fill][partial-fill]              |

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
[29]: 29.md
[exchange]: https://github.com/cashubtc/nuts/pull/410
[partial-fill]: https://github.com/cashubtc/nuts/pull/410
