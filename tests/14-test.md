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

### SIG_ALL Test Vector

HTLC shares the [NUT-11][11] SIG_ALL message aggregation. The following `SwapRequest` has a valid preimage and a valid signature over the aggregated message.

```json
{
  "inputs": [
    {
      "amount": 8,
      "id": "009a1f293253e41e",
      "secret": "[\"HTLC\",{\"nonce\":\"da62796403af76c80cd6ce9153ed3746\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"5df34ba9ea8097b5c89c475d24e2feb5dd816c7486ad1a4f2f3afeef808f82a469859bc9075ab1bc1735e47b87f600301172f4ed5ba3feca80e13771d6f6fe6f\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 8,
      "id": "009a1f293253e41e",
      "B_": "035015e6d7ade60ba8426cefaf1832bbd27257636e44a76b922d78e79b47cb689d"
    },
    {
      "amount": 2,
      "id": "009a1f293253e41e",
      "B_": "0288d7649652d0a83fc9c966c969fb217f15904431e61a44b14999fabc1b5d9ac6"
    }
  ]
}
```

The corresponding `msg_to_sign` (386 bytes, hex) and its SHA-256 hash are:

```
msg_to_sign = 43617368755f536967416c6c5369675f763100000000000000ef5b2248544c43222c7b226e6f6e6365223a226461363237393634303361663736633830636436636539313533656433373436222c2264617461223a2265633439313664643238666334633130643738653238376361356439636335316565316165373363626664653038633662333733323463626661616338626335222c2274616773223a5b5b227075626b657973222c22303237396265363637656639646362626163353561303632393563653837306230373032396266636462326463653238643935396632383135623136663831373938225d2c5b22736967666c6167222c225349475f414c4c225d5d7d5d0000002102698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904000000010800000021035015e6d7ade60ba8426cefaf1832bbd27257636e44a76b922d78e79b47cb689d0000000102000000210288d7649652d0a83fc9c966c969fb217f15904431e61a44b14999fabc1b5d9ac6
sha256(msg_to_sign) = cd1a10eadc41f679104b542aee828ba22390fff80ac29747504c51a118792a58
```

[11]: ../11.md
