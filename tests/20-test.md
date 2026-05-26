# NUT-20 Test Vectors

The following is a `PostMintBolt11Request` with a valid signature, where the `pubkey` in the `PostMintQuoteBolt11Response` is `0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798` (secret key `0x01`).

```json
{
  "quote": "0192d3c0-7e8a-7c3d-8e9f-1a2b3c4d5e6f",
  "outputs": [
    {
      "amount": 1,
      "id": "009a1f293253e41e",
      "B_": "036d6caac248af96f6afa7f904f550253a0f3ef3f5aa2fe6838a95b216691468e2"
    },
    {
      "amount": 1,
      "id": "009a1f293253e41e",
      "B_": "021f8a566c205633d029094747d2e18f44e05993dda7a5f88f496078205f656e59"
    }
  ],
  "signature": "4881093a332ff7c79f3e598ce5b249d64978b47165a0b19c18adf0ced0246228e61e702f0abaf1bf27b92be4336bdbabacfbe4c914076386b3c66fdcd0b3480e"
}
```

The corresponding `msg_to_sign` (hex) and its SHA-256 hash are:

```
msg_to_sign = 43617368755f4d696e7451756f74655369675f76310000002430313932643363302d376538612d376333642d386539662d316132623363346435653666000000010100000021036d6caac248af96f6afa7f904f550253a0f3ef3f5aa2fe6838a95b216691468e2000000010100000021021f8a566c205633d029094747d2e18f44e05993dda7a5f88f496078205f656e59
sha256(msg_to_sign) = c164fd384879f74ab6ea2e7cf13d90ed42e6df9d5de607eeb5c9cc7d36fb1c21
```
