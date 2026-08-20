# NUT-20 (legacy) Test Vectors

## Deterministic quote locking key derivation

Using [NUT-20](../20.md) quote locking key derivation, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The public keys derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "m/129373'/20'/0'/0'/0": "03062837166e56114b59a4d1fd3a5a812bf7aadc1dde758428cf943d80acd41539",
  "m/129373'/20'/0'/0'/1": "02b47d9d41725f5ce6f08c874835cef25376cb1e95f6cb073fef52ca8fd986cf15",
  "m/129373'/20'/0'/0'/2": "029acbd3a46fd75bc05ba0226d0b4d909b2fb6e96c80544a094a1a3567737e44d3",
  "m/129373'/20'/0'/0'/3": "0373e4a42fbe0a4e18aadb57cf500b655f2446b4071ee579121d2ed8905bcc49c2",
  "m/129373'/20'/0'/0'/4": "02b8709bfce17c10f1864f5218844533ae60930d52089669b317d8b5f474eec071"
}
```

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
