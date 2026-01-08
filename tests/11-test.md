# NUT-11 Test Vectors

### Multisig Test Vectors

The following `Proof`, with locktime in the past, is spendable via either **Locktime Multisig** or **Refund Multisig**.

```json
{
  "amount": 64,
  "C": "02d7cd858d866fca404b5cb1ffd813946e6d19efa1af00d654080fd20266bdc0b1",
  "id": "001b6c716bf42c7e",
  "secret": "[\"P2PK\",{\"nonce\":\"395162bf2d0add3c66aea9f22c45251dbee6e04bd9282addbb366a94cd4fb482\",\"data\":\"03ab50a667926fac858bac540766254c14b2b0334d10e8ec766455310224bbecf4\",\"tags\":[[\"locktime\",\"21\"],[\"pubkeys\",\"0229a91adec8dd9badb228c628a07fc1bf707a9b7d95dd505c490b1766fa7dc541\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"],[\"n_sigs\",\"2\"],[\"refund\",\"03ab50a667926fac858bac540766254c14b2b0334d10e8ec766455310224bbecf4\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"]]}]"
}
```

#### Valid Locktime Multisig

Has **TWO** valid signatures (`n_sigs = 2`) from the set: `data` + `pubkeys`.

```json
{
  "amount": 64,
  "C": "02d7cd858d866fca404b5cb1ffd813946e6d19efa1af00d654080fd20266bdc0b1",
  "id": "001b6c716bf42c7e",
  "secret": "[\"P2PK\",{\"nonce\":\"395162bf2d0add3c66aea9f22c45251dbee6e04bd9282addbb366a94cd4fb482\",\"data\":\"03ab50a667926fac858bac540766254c14b2b0334d10e8ec766455310224bbecf4\",\"tags\":[[\"locktime\",\"21\"],[\"pubkeys\",\"0229a91adec8dd9badb228c628a07fc1bf707a9b7d95dd505c490b1766fa7dc541\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"],[\"n_sigs\",\"2\"],[\"refund\",\"03ab50a667926fac858bac540766254c14b2b0334d10e8ec766455310224bbecf4\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"]]}]",
  "witness": "{\"signatures\":[\"6a4dd46f929b4747efe7380d655be5cfc0ea943c679a409ea16d4e40968ce89de885d995937d5b85f24fa33a25df10990c5e11d5397199d779d5cf87d42f6627\",\"0c266fffe2ea2358fb93b5d30dfbcefe52a5bb53d6c85f37d54723613224a256165d20dd095768f168ab2e97bc5a879f7c2a84eee8963c9bcedcd39552dbe093\"]}"
}
```

#### Valid Refund Multisig

Has **ONE** valid signature (`n_sigs_refund` is omitted, so equals `1`) from the `refund` tag.

```json
{
  "amount": 64,
  "C": "02d7cd858d866fca404b5cb1ffd813946e6d19efa1af00d654080fd20266bdc0b1",
  "id": "001b6c716bf42c7e",
  "secret": "[\"P2PK\",{\"nonce\":\"395162bf2d0add3c66aea9f22c45251dbee6e04bd9282addbb366a94cd4fb482\",\"data\":\"03ab50a667926fac858bac540766254c14b2b0334d10e8ec766455310224bbecf4\",\"tags\":[[\"locktime\",\"21\"],[\"pubkeys\",\"0229a91adec8dd9badb228c628a07fc1bf707a9b7d95dd505c490b1766fa7dc541\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"],[\"n_sigs\",\"2\"],[\"refund\",\"03ab50a667926fac858bac540766254c14b2b0334d10e8ec766455310224bbecf4\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"]]}]",
  "witness": "{\"signatures\":[\"d39631363480adf30433ee25c7cec28237e02b4808d4143469d4f390d4eae6ec97d18ba3cc6494ab1d04372f0838426ea296f25cb4bd8bddb296adc292eeaa96\"]}"
}
```

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
  "secret": "[\"P2PK\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]]}]",
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

The following is a `Proof` with one signature failing the multi-signature spend condition.

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
  "amount": 64,
  "C": "0257353051c02e2d650dede3159915c8be123ba4f47cf33183c7fedd20bd91a79b",
  "id": "001b6c716bf42c7e",
  "secret": "[\"P2PK\",{\"nonce\":\"4bc88ee09d1886c7461d45da205ca3274e1e3d9da2667c4865045cb18265a407\",\"data\":\"03d5edeb839be873df2348785506d36565f3b8f390fb931709a422b5a247ddefb1\",\"tags\":[[\"locktime\",\"21\"],[\"refund\",\"0234ad87e907e117db1590cc20a3942ffdfd5137aa563d36095d5cf5f96bada122\"]]}]",
  "witness": "{\"signatures\":[\"b316c2ff9c15f0c5c3d230e99ad94bc76a11dfccbdc820366a3db7210288f22ef6cedcded1152904ec31056d1d5176d83a2d96df5cd4ff86afdde1c90c63af5e\"]}"
}
```

The following is a `Proof` with a signature from the refund key that is **not** spendable because the locktime is in the future.

```json
{
  "amount": 64,
  "C": "0215865e3b30bdf6f5cdc1ee2c33379d5629bdf2eff2595603d939ff8c65d80586",
  "id": "001b6c716bf42c7e",
  "secret": "[\"P2PK\",{\"nonce\":\"0c3d085898f1abf2b5521035f4d0f4ecf68c6a5109f6bc836833a1188f06be65\",\"data\":\"03206e0d488387a816bbafd957be51b073432c6c7a403ec4c2a0b27647326c5150\",\"tags\":[[\"locktime\",\"99999999999\"],[\"refund\",\"026acbcd0fff3a424499c83ec892d3155c9d1984438659f448d9d0f1af3e92276a\"]]}]",
  "witness": "{\"signatures\":[\"e5b10d7627ab39bd0cefa219c63752a0026aa5ae754b91a0c7ee2596222f87942c442aca2957166a6b468350c09c9968792784d2ae7c42fc91739b55689f4c7a\"]}"
}
```

### SIG_ALL Test Vectors

Example `SwapRequest`:

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"c7f280eb55c1e8564e03db06973e94bc9b666d9e1ca42ad278408fe625950303\",\"data\":\"030d8acedfe072c9fa449a1efe0817157403fbec460d8e79f957966056e5dd76c1\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02c97ee3d1db41cf0a3ddb601724be8711a032950811bf326f8219c50c4808d3cd",
      "witness": "{\"signatures\":[\"ce017ca25b1b97df2f72e4b49f69ac26a240ce14b3690a8fe619d41ccc42d3c1282e073f85acd36dc50011638906f35b56615f24e4d03e8effe8257f6a808538\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is the `msg_to_sign` on the above `SwapRequest`.

```
["P2PK",{"nonce":"c7f280eb55c1e8564e03db06973e94bc9b666d9e1ca42ad278408fe625950303","data":"030d8acedfe072c9fa449a1efe0817157403fbec460d8e79f957966056e5dd76c1","tags":[["sigflag","SIG_ALL"]]}]02c97ee3d1db41cf0a3ddb601724be8711a032950811bf326f8219c50c4808d3cd2038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39
```

The hex representation of sha256sum(msg_to_sign) should look like this: `de7f9e3ca0fcc5ed3258fcf83dbf1be7fa78a5ed6da7bf2aa60d61e9dc6eb09a`

The following is a `SwapRequest` with a valid sig_all signature.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"c7f280eb55c1e8564e03db06973e94bc9b666d9e1ca42ad278408fe625950303\",\"data\":\"030d8acedfe072c9fa449a1efe0817157403fbec460d8e79f957966056e5dd76c1\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02c97ee3d1db41cf0a3ddb601724be8711a032950811bf326f8219c50c4808d3cd",
      "witness": "{\"signatures\":[\"ce017ca25b1b97df2f72e4b49f69ac26a240ce14b3690a8fe619d41ccc42d3c1282e073f85acd36dc50011638906f35b56615f24e4d03e8effe8257f6a808538\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is a `SwapRequest` that is invalid as the spending conditions are not identical across inputs (secret tags are different).

```json
{
  "inputs": [
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"fa6dd3fac9086c153878dec90b9e37163d38ff2ecf8b37db6470e9d185abbbae\",\"data\":\"033b42b04e659fed13b669f8b16cdaffc3ee5738608810cf97a7631d09bd01399d\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "024d232312bab25af2e73f41d56864d378edca9109ae8f76e1030e02e585847786",
      "witness": "{\"signatures\":[\"27b4d260a1186e3b62a26c0d14ffeab3b9f7c3889e78707b8fd3836b473a00601afbd53a2288ad20a624a8bbe3344453215ea075fc0ce479dd8666fd3d9162cc\"]}"
    },
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"4007b21fc5f5b1d4920bc0a08b158d98fd0fb2b0b0262b57ff53c6c5d6c2ae8c\",\"data\":\"033b42b04e659fed13b669f8b16cdaffc3ee5738608810cf97a7631d09bd01399d\",\"tags\":[[\"locktime\",\"122222222222222\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02417400f2af09772219c831501afcbab4efb3b2e75175635d5474069608deb641"
    }
  ],
  "outputs": [
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    },
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "B_": "03afe7c87e32d436f0957f1d70a2bca025822a84a8623e3a33aed0a167016e0ca5"
    },
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "B_": "02c0d4fce02a7a0f09e3f1bca952db910b17e81a7ebcbce62cd8dcfb127d21e37b"
    }
  ]
}
```

The following is a `SwapRequest` where multiple valid signatures are required and provided.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"04bfd885fc982d553711092d037fdceb7320fd8f96b0d4fd6d31a65b83b94272\",\"data\":\"0275e78025b558dbe6cb8fdd032a2e7613ca14fda5c1f4c4e3427f5077a7bd90e4\",\"tags\":[[\"pubkeys\",\"035163650bbd5ed4be7693f40f340346ba548b941074e9138b67ef6c42755f3449\",\"02817d22a8edc44c4141e192995a7976647c335092199f9e076a170c7336e2f5cc\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "03866a09946562482c576ca989d06371e412b221890804c7da8887d321380755be",
      "witness": "{\"signatures\":[\"be1d72c5ca16a93c5a34f25ec63ce632ddc3176787dac363321af3fd0f55d1927e07451bc451ffe5c682d76688ea9925d7977dffbb15bd79763b527f474734b0\",\"669d6d10d7ed35395009f222f6c7bdc28a378a1ebb72ee43117be5754648501da3bedf2fd6ff0c7849ac92683538c60af0af504102e40f2d8daca8e08b1ca16b\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is a `SwapRequest` where the locktime has passed and the refund key signatures are valid.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"9ea35553beb18d553d0a53120d0175a0991ca6109370338406eed007b26eacd1\",\"data\":\"02af21e09300af92e7b48c48afdb12e22933738cfb9bba67b27c00c679aae3ec25\",\"tags\":[[\"locktime\",\"1\"],[\"refund\",\"02637c19143c58b2c58bd378400a7b82bdc91d6dedaeb803b28640ef7d28a887ac\",\"0345c7fdf7ec7c8e746cca264bf27509eb4edb9ac421f8fbfab1dec64945a4d797\"],[\"n_sigs_refund\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "03dd83536fbbcbb74ccb3c87147df26753fd499cc2c095f74367fff0fb459c312e",
      "witness": "{\"signatures\":[\"23b58ef28cd22f3dff421121240ddd621deee83a3bc229fd67019c2e338d91e2c61577e081e1375dbab369307bba265e887857110ca3b4bd949211a0a298805f\",\"7e75948ef1513564fdcecfcbd389deac67c730f7004f8631ba90c0844d3e8c0cf470b656306877df5141f65fd3b7e85445a8452c3323ab273e6d0d44843817ed\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is a valid `SwapRequest` with an HTLC also locked to a public key

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"HTLC\",{\"nonce\":\"d730dd70cd7ec6e687829857de8e70aab2b970712f4dbe288343eca20e63c28c\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0350cda8a1d5257dbd6ba8401a9a27384b9ab699e636e986101172167799469b14\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "03ff6567e2e6c31db5cb7189dab2b5121930086791c93899e4eff3dda61cb57273",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"a4c00a9ad07f9936e404494fda99a9b935c82d7c053173b304b8663124c81d4b00f64a225f5acf41043ca52b06382722bd04ded0fbeb0fcc404eed3b24778b88\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is an invalid `SwapRequest` with an HTLC also locked to a public key, a locktime and a refund key. The locktime has not expired, but the proof is signed with the refund key.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"HTLC\",{\"nonce\":\"512c4045f12fdfd6f55059669c189e040c37c1ce2f8be104ed6aec296acce4e9\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"03ba83defd31c63f8841d188f0d41b5bb3af1bb3c08d0ba46f8f1d26a4d45e8cad\"],[\"locktime\",\"4854185133\"],[\"refund\",\"032f1008a79c722e93a1b4b853f85f38283f9ef74ee4c5c91293eb1cc3c5e46e34\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02207abeff828146f1fc3909c74613d5605bd057f16791994b3c91f045b39a6939",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"7816d57871bde5be2e4281065dbe5b15f641d8f1ed9437a3ae556464d6f9b8a0a2e6660337a915f2c26dce1453a416daf682b8fb593b67a0750fce071e0759b9\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    },
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "B_": "03afe7c87e32d436f0957f1d70a2bca025822a84a8623e3a33aed0a167016e0ca5"
    }
  ]
}
```

The following is a valid `SwapRequest` with a multisig HTLC also locked to locktime and refund keys.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"HTLC\",{\"nonce\":\"c9b0fabb8007c0db4bef64d5d128cdcf3c79e8bb780c3294adf4c88e96c32647\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"039e6ec7e922abb4162235b3a42965eb11510b07b7461f6b1a17478b1c9c64d100\"],[\"locktime\",\"1\"],[\"refund\",\"02ce1bbd2c9a4be8029c9a6435ad601c45677f5cde81f8a7f0ed535e0039d0eb6c\",\"03c43c00ff57f63cfa9e732f0520c342123e21331d0121139f1b636921eeec095f\"],[\"n_sigs_refund\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "0344b6f1471cf18a8cbae0e624018c816be5e3a9b04dcb7689f64173c1ae90a3a5",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"98e21672d409cc782c720f203d8284f0af0c8713f18167499f9f101b7050c3e657fb0e57478ebd8bd561c31aa6c30f4cd20ec38c73f5755b7b4ddee693bca5a5\",\"693f40129dbf905ed9c8008081c694f72a36de354f9f4fa7a61b389cf781f62a0ae0586612fb2eb504faaf897fefb6742309186117f4743bcebcb8e350e975e2\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

Example `MeltRequest`:

```json
{
  "quote": "cF8911fzT88aEi1d-6boZZkq5lYxbUSVs-HbJxK0",
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"bbf9edf441d17097e39f5095a3313ba24d3055ab8a32f758ff41c10d45c4f3de\",\"data\":\"029116d32e7da635c8feeb9f1f4559eb3d9b42d400f9d22a64834d89cde0eb6835\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02a9d461ff36448469dccf828fa143833ae71c689886ac51b62c8d61ddaa10028b",
      "witness": "{\"signatures\":[\"478224fbe715e34f78cb33451db6fcf8ab948afb8bd04ff1a952c92e562ac0f7c1cb5e61809410635be0aa94d0448f7f7959bd5762cc3802b0a00ff58b2da747\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is the valid `msg_to_sign` on the above `MeltRequest`.

```
["P2PK",{"nonce":"bbf9edf441d17097e39f5095a3313ba24d3055ab8a32f758ff41c10d45c4f3de","data":"029116d32e7da635c8feeb9f1f4559eb3d9b42d400f9d22a64834d89cde0eb6835","tags":[["sigflag","SIG_ALL"]]}]02a9d461ff36448469dccf828fa143833ae71c689886ac51b62c8d61ddaa10028b0038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39cF8911fzT88aEi1d-6boZZkq5lYxbUSVs-HbJxK0
```

The hex representation of sha256sum(msg_to_sign) should look like this: `9efa1067cc7dc870f4074f695115829c3cd817a6866c3b84e9814adf3c3cf262`

The following is a valid `SIG_ALL` `MeltRequest`.

```json
{
  "quote": "cF8911fzT88aEi1d-6boZZkq5lYxbUSVs-HbJxK0",
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"bbf9edf441d17097e39f5095a3313ba24d3055ab8a32f758ff41c10d45c4f3de\",\"data\":\"029116d32e7da635c8feeb9f1f4559eb3d9b42d400f9d22a64834d89cde0eb6835\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02a9d461ff36448469dccf828fa143833ae71c689886ac51b62c8d61ddaa10028b",
      "witness": "{\"signatures\":[\"478224fbe715e34f78cb33451db6fcf8ab948afb8bd04ff1a952c92e562ac0f7c1cb5e61809410635be0aa94d0448f7f7959bd5762cc3802b0a00ff58b2da747\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```

The following is a valid multi-sig `SIG_ALL` `MeltRequest`.

```json
{
  "quote": "Db3qEMVwFN2tf_1JxbZp29aL5cVXpSMIwpYfyOVF",
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"68d7822538740e4f9c9ebf5183ef6c4501c7a9bca4e509ce2e41e1d62e7b8a99\",\"data\":\"0394e841bd59aeadce16380df6174cb29c9fea83b0b65b226575e6d73cc5a1bd59\",\"tags\":[[\"pubkeys\",\"033d892d7ad2a7d53708b7a5a2af101cbcef69522bd368eacf55fcb4f1b0494058\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "03a70c42ec9d7192422c7f7a3ad017deda309fb4a2453fcf9357795ea706cc87a9",
      "witness": "{\"signatures\":[\"ed739970d003f703da2f101a51767b63858f4894468cc334be04aa3befab1617a81e3eef093441afb499974152d279e59d9582a31dc68adbc17ffc22a2516086\",\"f9efe1c70eb61e7ad8bd615c50ff850410a4135ea73ba5fd8e12a734743ad045e575e9e76ea5c52c8e7908d3ad5c0eaae93337e5c11109e52848dc328d6757a2\"]}"
    }
  ],
  "outputs": [
    {
      "amount": 0,
      "id": "00bfa73302d12ffd",
      "B_": "038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39"
    }
  ]
}
```
