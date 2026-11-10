# Legacy specifications

These documents specify the parts of the Cashu protocol that
[pre-v3 keysets](../02.md#keyset-id-v3) still use. v3 keysets follow the
[current specifications](../README.md) only.

| NUT #       | Description                                 | Current specification |
| ----------- | ------------------------------------------- | --------------------- |
| [00](00.md) | secp256k1 BDHKE and V3 tokens               | [NUT-00](../00.md)    |
| [01](01.md) | Mint public key format                      | [NUT-01](../01.md)    |
| [02](02.md) | Keyset IDs V2 and V1                        | [NUT-02](../02.md)    |
| [07](07.md) | Token state check                           | [NUT-07](../07.md)    |
| [10](10.md) | JSON spending conditions                    | [NUT-10](../10.md)    |
| [11](11.md) | Pay to Public Key (P2PK)                    | [NUT-10](../10.md)    |
| [12](12.md) | Offline ecash signature validation          | [NUT-00](../00.md)    |
| [13](13.md) | Deterministic secrets for V2 and V1 keysets | [NUT-13](../13.md)    |
| [14](14.md) | Hashed Timelock Contracts (HTLCs)           | [NUT-10](../10.md)    |
| [18](18.md) | The `nut10` locking option                  | [NUT-18](../18.md)    |
| [20](20.md) | Mint quote signature message                | [NUT-20](../20.md)    |
| [22](22.md) | DLEQ proofs on blind authentication tokens  | [NUT-22](../22.md)    |
| [26](26.md) | The `nut10` sub-TLV                         | [NUT-26](../26.md)    |
| [28](28.md) | P2BK on P2PK and HTLC secrets               | [NUT-28](../28.md)    |
| [29](29.md) | The batch signature message                 | [NUT-29](../29.md)    |

Test vectors are in [`tests/`](tests).
