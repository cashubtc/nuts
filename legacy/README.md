# Legacy specifications

These documents specify the parts of the Cashu protocol that keysets with version
byte `00` or `01` still use. Keysets with version byte `02` or later follow the
[current specifications](../README.md) only.

| NUT #       | Description                                 | Current specification |
| ----------- | ------------------------------------------- | --------------------- |
| [00](00.md) | secp256k1 BDHKE, V3 tokens                  | [NUT-00](../00.md)    |
| [02](02.md) | Keyset IDs V2 and V1                        | [NUT-02](../02.md)    |
| [10](10.md) | JSON spending conditions                    | [NUT-10](../10.md)    |
| [11](11.md) | Pay-To-Pubkey (P2PK)                        | [NUT-10](../10.md)    |
| [12](12.md) | DLEQ proofs                                 | [NUT-00](../00.md)    |
| [13](13.md) | Deterministic secrets for V2 and V1 keysets | [NUT-13](../13.md)    |
| [14](14.md) | Hashed Timelock Contracts (HTLCs)           | [NUT-10](../10.md)    |
| [20](20.md) | Signature on mint quote                     | [NUT-20](../20.md)    |
| [18](18.md) | The `nut10` payment request locking option  | [NUT-18](../18.md)    |
| [26](26.md) | The `nut10` sub-TLV, tag `0x08`             | [NUT-26](../26.md)    |

Test vectors are in [`tests/`](tests).
