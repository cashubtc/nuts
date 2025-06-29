# NUT-11 Test Vectors

### SIG_INPUTS Test Vectors

The following is a `Proof` with a valid signature.

```json
{
  "amount": 1,
  "secret": "[\"P2PK\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"signatures\":[\"60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383\"]}"
}
```

The following is a `Proof` with an invalid signature as it is on a different secret.

```json
{
  "amount": 1,
  "secret": "[\"P2PK\",{\"nonce\":\"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"02142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"signatures\":[\"83564aca48c668f50d022a426ce0ed19d3a9bdcffeeaee0dc1e7ea7e98e9eff1840fcc821724f623468c94f72a8b0a7280fa9ef5a54a1b130ef3055217f467b3\"]}"
}
```

The following is a `Proof` with 2 signatures required to meet the multi-signature spend condition.

```json
{
  "amount": 1,
  "secret": "[\"P2PK\",{\"nonce\":\"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"02142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"signatures\":[\"83564aca48c668f50d022a426ce0ed19d3a9bdcffeeaee0dc1e7ea7e98e9eff1840fcc821724f623468c94f72a8b0a7280fa9ef5a54a1b130ef3055217f467b3\",\"9a72ca2d4d5075be5b511ee48dbc5e45f259bcf4a4e8bf18587f433098a9cd61ff9737dc6e8022de57c76560214c4568377792d4c2c6432886cc7050487a1f22\"]}"
}
```

The following is a `Proof` with one one signature failing the multi-signature spend condition.

```json
{
  "amount": 1,
  "secret": "[\"P2PK\",{\"nonce\":\"0ed3fcb22c649dd7bbbdcca36e0c52d4f0187dd3b6a19efcc2bfbebb5f85b2a1\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"02142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"signatures\":[\"83564aca48c668f50d022a426ce0ed19d3a9bdcffeeaee0dc1e7ea7e98e9eff1840fcc821724f623468c94f72a8b0a7280fa9ef5a54a1b130ef3055217f467b3\"]}"
}
```

The following is a `Proof` with a signature from the refund key that is spendable because the locktime is in the past.

```json
{
  "amount": 1,
  "id": "009a1f293253e41e",
  "secret": "[\"P2PK\",{\"nonce\":\"902685f492ef3bb2ca35a47ddbba484a3365d143b9776d453947dcbf1ddf9689\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"locktime\",\"21\"],[\"n_sigs\",\"2\"],[\"refund\",\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "witness": "{\"signatures\":[\"710507b4bc202355c91ea3c147c0d0189c75e179d995e566336afd759cb342bcad9a593345f559d9b9e108ac2c9b5bd9f0b4b6a295028a98606a0a2e95eb54f7\"]}"
}
```

The following is a `Proof` with a signature from the refund key that is **not** spendable because the locktime is in the future.

```json
{
  "amount": 1,
  "id": "009a1f293253e41e",
  "secret": "[\"P2PK\",{\"nonce\":\"64c46e5d30df27286166814b71b5d69801704f23a7ad626b05688fbdb48dcc98\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"locktime\",\"21\"],[\"n_sigs\",\"2\"],[\"refund\",\"0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\"],[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "witness": "{\"signatures\":[\"f661d3dc046d636d47cb3d06586da42c498f0300373d1c2a4f417a44252cdf3809bce207c8888f934dba0d2b1671f1b8622d526840f2d5883e571b462630c1ff\"]}"
}
```

### SIG_ALL Test Vectors

Example `SwapRequest`:

```json
{
  "inputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "secret": "[\"P2PK\",{\"nonce\":\"c537ea76c1ac9cfa44d15dac91a63315903a3b4afa8e4e20f868f87f65ff2d16\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a",
      "witness": "{\"signatures\":[\"c38cf7943f59206dc22734d39c17e342674a4025e6d3b424eb79d445a57257d57b45dd94fcd1b8dd8013e9240a4133bdef6523f64cd7288d890f3bbb8e3c6453\",\"f766dbb80e5c27de9a4770486e11e1bac0b1c4f782bf807a5189ea9c3e294559a3de4e217d3dfceafd4d9e8dcbfe4e9a188052d6dab9df07df7844224292de36\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "B_": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a"
    }
  ]
}
```

The following is the `msg_to_sign` on the above `SwapRequest`.

```
["P2PK",{"nonce":"c537ea76c1ac9cfa44d15dac91a63315903a3b4afa8e4e20f868f87f65ff2d16","data":"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a","tags":[["pubkeys","03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9"],["n_sigs","2"],["sigflag","SIG_ALL"]]}]026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a
```

The following is a `SwapRequest` with a valid sig_all signature.

```json
{
  "inputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "secret": "[\"P2PK\",{\"nonce\":\"fc14ca312b7442d05231239d0e3cdcb6b2335250defcb8bec7d2efe9e26c90a6\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a",
      "witness": "{\"signatures\":[\"aa6f3b3f112ec3e834aded446ea67a90cdb26b43e08cfed259e0bbd953395c4af11117c58ec0ec3de404f31076692426cde40d2c1602d9dd067a872cb11ac3c0\"]}"
    },
    {
      "amount": 0,
      "id": "009a1f293253e41f",
      "secret": "[\"P2PK\",{\"nonce\":\"fc14ca312b7442d05231239d0e3cdcb6b2335250defcb8bec7d2efe9e26c90a6\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "B_": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a"
    }
  ]
}
```

The following is a `SwapRequest` that is invalid as there are multiple secrets.

```json
{
  "inputs": [
    {
      "amount": 1,
      "secret": "[\"P2PK\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
      "id": "009a1f293253e41e",
      "witness": "{\"signatures\":[\"60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383\"]}"
    },
    {
      "amount": 1,
      "secret": "[\"P2PK\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"02a60c27104cf6023581e790970fc33994a320abe36e7ceed16771b0f8d76f0666\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
      "id": "009a1f293253e41f",
      "witness": "{\"signatures\":[\"60f3c9b766770b46caac1d27e1ae6b77c8866ebaeba0b9489fe6a15a837eaa6fcd6eaa825499c72ac342983983fd3ba3a8a41f56677cc99ffd73da68b59e1383\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "B_": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
      "id": "009a1f293253e41e"
    }
  ]
}
```

The following is a `SwapRequest` multiple valid signatures are provided and required.

```json
{
  "inputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "secret": "[\"P2PK\",{\"nonce\":\"c537ea76c1ac9cfa44d15dac91a63315903a3b4afa8e4e20f868f87f65ff2d16\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a",
      "witness": "{\"signatures\":[\"c38cf7943f59206dc22734d39c17e342674a4025e6d3b424eb79d445a57257d57b45dd94fcd1b8dd8013e9240a4133bdef6523f64cd7288d890f3bbb8e3c6453\",\"f766dbb80e5c27de9a4770486e11e1bac0b1c4f782bf807a5189ea9c3e294559a3de4e217d3dfceafd4d9e8dcbfe4e9a188052d6dab9df07df7844224292de36\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "B_": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a"
    }
  ]
}
```

Example `MeltRequest`:

```json
{
  "quote": "2fc40ad3-2f6a-4a7e-91fb-b8c2b5dc2bf7",
  "inputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "secret": "[\"P2PK\",{\"nonce\":\"1d0db9cbd2aa7370a3d6e0e3ce5714758ed7a085e2f8da9814924100e1fc622e\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a",
      "witness": "{\"signatures\":[\"b2077717cfe43086582679ce3fbe1802f9b8652f93828c2e1a75b9e553c0ab66cd14b9c5f6c45a098375fe6583e106c7ccdb1421636daf893576e15815f3483f\",\"179f687c2236c3d0767f3b2af88478cad312e7f76183fb5781754494709334c578c7232dc57017d06b9130a406f8e3ece18245064cda4ef66808ed3ff68c933e\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "B_": "028b708cfd03b38bdc0a561008119594106f0c563061ae3fbfc8981b5595fd4e2b"
    }
  ]
}
```

The following is the valid `msg_to_sign` on the above `MeltRequest`.

```
["P2PK",{"nonce":"1d0db9cbd2aa7370a3d6e0e3ce5714758ed7a085e2f8da9814924100e1fc622e","data":"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a","tags":[["pubkeys","026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a","03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9"],["n_sigs","2"],["sigflag","SIG_ALL"]]}]028b708cfd03b38bdc0a561008119594106f0c563061ae3fbfc8981b5595fd4e2b2fc40ad3-2f6a-4a7e-91fb-b8c2b5dc2bf7
```

The following is a valid `SIG_ALL` `MeltRequest`.

```json
{
  "quote": "0f983814-de91-46b8-8875-1b358a35298a",
  "inputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "secret": "[\"P2PK\",{\"nonce\":\"600050bd36cccdc71dec82e97679fa3e7712c22ea33cf4fe69d4d78223757e57\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a",
      "witness": "{\"signatures\":[\"b66c342654ccc95a62100f8f4a76afe1aea612c9c63383be3c7feb5110bb8eabe7ccaa9f117abd524be8c9a2e331e7d70248aeae337b9ce405625b3c49fc627d\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "B_": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a"
    }
  ]
}
```

The following is a valid multi-sig `SIG_ALL` `MeltRequest`.

```json
{
  "quote": "2fc40ad3-2f6a-4a7e-91fb-b8c2b5dc2bf7",
  "inputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "secret": "[\"P2PK\",{\"nonce\":\"1d0db9cbd2aa7370a3d6e0e3ce5714758ed7a085e2f8da9814924100e1fc622e\",\"data\":\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"tags\":[[\"pubkeys\",\"026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a\",\"03142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "026f6a2b1d709dbca78124a9f30a742985f7eddd894e72f637f7085bf69b997b9a",
      "witness": "{\"signatures\":[\"b2077717cfe43086582679ce3fbe1802f9b8652f93828c2e1a75b9e553c0ab66cd14b9c5f6c45a098375fe6583e106c7ccdb1421636daf893576e15815f3483f\",\"179f687c2236c3d0767f3b2af88478cad312e7f76183fb5781754494709334c578c7232dc57017d06b9130a406f8e3ece18245064cda4ef66808ed3ff68c933e\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "009a1f293253e41e",
      "B_": "028b708cfd03b38bdc0a561008119594106f0c563061ae3fbfc8981b5595fd4e2b"
    }
  ]
}
```
