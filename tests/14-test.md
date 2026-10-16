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
      "id": "01b8afe98cfccddc07e53fe5f081657f729c322266a1fda00937d27bba3cdf6a82",
      "secret": "[\"HTLC\",{\"nonce\":\"e72b0dbe91e3c17f0680b0a2ecf407f5e237d00d311313b33bcd77f957087e56\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026c32214e4c4d286ff26be59ee705de8c5155885155c57d1bc44033713f0f6d1a",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"f1119822def46095e5f673826336e4c2138f0b7ef62fa0d4b3a59b9b43db6113a7e0ac02e96d59bdbbc7bbc8ebeecddcfd46c872fccc359a41392c758442801c\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 8,
      "id": "01b8afe98cfccddc07e53fe5f081657f729c322266a1fda00937d27bba3cdf6a82",
      "B_": "027c9a3f3dae60a2967dfc3aeea06535fff329cbc196842ecc12a5fb66a2eb9087"
    },
    {
      "amount": 2,
      "id": "01b8afe98cfccddc07e53fe5f081657f729c322266a1fda00937d27bba3cdf6a82",
      "B_": "03cd583efc731edcab6935e0a817cec65851ace7ca842396422ff2c0e9db9c49bc"
    }
  ]
}
```

The corresponding `message` (397 bytes, hex) and its tagged hash `message_hash` (see [NUT-11][11]) are:

```
message = 110000010f5b2248544c43222c7b226e6f6e6365223a2265373262306462653931653363313766303638306230613265636634303766356532333764303064333131333133623333626364373766393537303837653536222c2264617461223a2265633439313664643238666334633130643738653238376361356439636335316565316165373363626664653038633662333733323463626661616338626335222c2274616773223a5b5b227075626b657973222c22303237396265363637656639646362626163353561303632393563653837306230373032396266636462326463653238643935396632383135623136663831373938225d2c5b22736967666c6167222c225349475f414c4c225d5d7d5d00000021026c32214e4c4d286ff26be59ee705de8c5155885155c57d1bc44033713f0f6d1a21000000010800000020a290f1d36e44a532a9c40ea2c8cebefd4fa685a12b58fb92180bea38cc78171421000000010200000020dbc0f7aabcc574dfada0d9cdaba4090810af4a8dd73624a87185ff593e43c71d
message_hash = 955548adebe2142b84498625885e2d205208b9983ec7152b75dc72454bf8b4a0
```

[11]: ../11.md
