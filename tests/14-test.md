# NUT-14 Test Vectors

The signing key for these vectors is the well-known test key:

```
privkey = 0000000000000000000000000000000000000000000000000000000000000001
pubkey  = 0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
```

All hashlocks commit to the same preimage:

```
preimage = 0000000000000000000000000000000000000000000000000000000000000001
hashlock = sha256(preimage) = ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5
```

### Preimage and Signature Test Vectors

The following `Proof` has a valid preimage and a valid signature on `secret` by the `pubkeys` key, so it is spendable.

```json
{
  "amount": 8,
  "id": "009a1f293253e41e",
  "secret": "[\"HTLC\",{\"nonce\":\"5d11913ee0f92fefdc82a6764fd2457a1585d418f0265b5575eb14cd3be76d94\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"8d6da34f529edccdb6a5d2122f16293b01b38263e58733acca0ff6595515224f69b80c0933f96a729899249bc7c1a5f34efcb7cf4347f1135625449bae51f86b\"]}"
}
```

The same `Proof` with a witness whose preimage does not hash to `Secret.data` is **NOT** spendable, regardless of the signature:

```json
{
  "amount": 8,
  "id": "009a1f293253e41e",
  "secret": "[\"HTLC\",{\"nonce\":\"5d11913ee0f92fefdc82a6764fd2457a1585d418f0265b5575eb14cd3be76d94\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000002\",\"signatures\":[\"8d6da34f529edccdb6a5d2122f16293b01b38263e58733acca0ff6595515224f69b80c0933f96a729899249bc7c1a5f34efcb7cf4347f1135625449bae51f86b\"]}"
}
```

### Keyless HTLC Test Vector

A hashlock with no `pubkeys` tag requires no signature: the following `Proof` is spendable with the preimage alone.

```json
{
  "amount": 8,
  "id": "009a1f293253e41e",
  "secret": "[\"HTLC\",{\"nonce\":\"09ef07c284bcda9a413723b8bb5d1a4bbee0e9564ba91e0d5e2b2a1071ab5c53\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\"}"
}
```
