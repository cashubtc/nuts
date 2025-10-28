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
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"15295d2e313321acc65266c95060f99da5825a0ea00ac01142cf57b1fd397ddd\",\"data\":\"02dc2ecca00f924dd7028bc92793d7bb9230bac43ff690148c33e2c010f44f154c\",\"tags\":[[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "0255d4584468bd226fd290ab454ef61ba0f85a7f19c8b55a383cfa9c87bb37c2b3",
      "witness": "{\"signatures\":[\"74a737275b0e0e3b2598242abbe9c791526fd4e30b5b04fd53a02795775613889d1bc7843301cfe1b91b16687698d8e26fa7b2f5ce42c5043d483f0e9d15e061\"]}"
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

The following is the `msg_to_sign` on the above `SwapRequest`.

```
["P2PK",{"nonce":"15295d2e313321acc65266c95060f99da5825a0ea00ac01142cf57b1fd397ddd","data":"02dc2ecca00f924dd7028bc92793d7bb9230bac43ff690148c33e2c010f44f154c","tags":[["sigflag","SIG_ALL"]]}]0255d4584468bd226fd290ab454ef61ba0f85a7f19c8b55a383cfa9c87bb37c2b3100bfa73302d12ffd038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39100bfa73302d12ffd03afe7c87e32d436f0957f1d70a2bca025822a84a8623e3a33aed0a167016e0ca5
```

The following is a `SwapRequest` with a valid sig_all signature.

```json
{
  "inputs": [
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"6507be98667717777e8a7b4f390f0ce3015ae55ab3d704515a58279dd29b0837\",\"data\":\"02340815f0b7e6aab8309359f2ebd23ecc3a77f391ad0f42429dea4a57726aabd5\",\"tags\":[[\"pubkeys\",\"02caa73a36330cd4dd1c35a601fccc5caf9ba0af9aaa32ff6fd997f8016958012e\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "03800d22be5fc78ba23fb2c7a98c04ac4df18d5a347830492f8861123266128594",
      "witness": "{\"signatures\":[\"0517134f98154091ea9e9ff2b89124f7ea9f33808de6533ca4658f0cf71019d461305ee4029c7cd4f23eac8c6b8d19c0717a57250aa55c62a97cb5fecb62492e\",\"c129e6fdc3b90ad5de688551310aa8c8efc74d485ab699477e7dbb9e71d096b19535ae7ed8178e78016dad816fe83213693892e64e94b53caf63a6e1fb7fd90f\"]}"
    },
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"ec17595b7841d3f755a0511904d475406db0b55d87192f1249e8cba9c1af82d7\",\"data\":\"02340815f0b7e6aab8309359f2ebd23ecc3a77f391ad0f42429dea4a57726aabd5\",\"tags\":[[\"pubkeys\",\"02caa73a36330cd4dd1c35a601fccc5caf9ba0af9aaa32ff6fd997f8016958012e\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "025a0739fbff052ea7776ff84667d2f496073366b245bc1ed43ea51babba2ae83e"
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

The following is a `SwapRequest` that is invalid as there are multiple secrets.

```json
{
  "inputs": [
    {
      "amount": 1,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"e2a221fe361f19d95c5c3312ccff3ffa075b4fe37beec99de85a6ee70568385b\",\"data\":\"03dad7f9c588f4cbb55c2e1b7b802fa2bbc63a614d9e9ecdf56a8e7ee8ca65be86\",\"tags\":[[\"pubkeys\",\"025f2af63fd65ca97c3bde4070549683e72769d28def2f1cd3d63576cd9c2ffa6c\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02a79c09b0605f4e7a21976b511cc7be01cdaeac54b29645258c84f2e74bff13f6",
      "witness": "{\"signatures\":[\"b42c7af7e98ca4e3bba8b73702120970286196340b340c21299676dbc7b10cafaa7baeb243affc01afce3218616cf8b3f6b4baaf4414fedb31b0c6653912f769\",\"17781910e2d806cae464f8a692929ee31124c0cd7eaf1e0d94292c6cbc122da09076b649080b8de9201f87d83b99fe04e33d701817eb287d1cdd9c4d0410e625\"]}"
    },
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"973c78b5e84c0986209dc14ba57682baf38fa4c1ea60c4c5f6834779a1a13e6d\",\"data\":\"02685df03c777837bc7155bd2d0d8e98eede7e956a4cd8a9edac84532584e68e0f\",\"tags\":[[\"pubkeys\",\"025f2af63fd65ca97c3bde4070549683e72769d28def2f1cd3d63576cd9c2ffa6c\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02be48c564cf6a7b4d09fbaf3a78a153a79f687ac4623e48ce1788effc3fb1e024"
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

The following is a `SwapRequest` multiple valid signatures are provided and required.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"9f130eaddeacec1e0cf67c4458b376316a566b797c9ab6ef2d90dc22da3244da\",\"data\":\"0258121ea454f256b310025855788a274eebd8e5f32c23db307388c7ac5f17669c\",\"tags\":[[\"pubkeys\",\"0273031aec7105bb1b1bed4320b22d2bfa26bf798a1f04103cc572b9c2ac31d629\",\"033980a7d123e67bd0cada4bb7463c3a1604d56da15f8bea00d93f2fa9fcb4ff03\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02f64662a77beef0df41d5ab3861c6816845b0ddbb535abfaa2d6cf1d67767db43",
      "witness": "{\"signatures\":[\"0a2e7934e3ee997553df0fad0d54c6c24dc398c0f1bd84f83dfafb55a57d60f82f426b4b5aadf12bbe3e729396bdac04260cb88ed720e05a483d7a3cfe5e060a\",\"5267f545d2da679d6e08ce453ab335f90c5cfd34b66f67cd078f6ad757a257e5471342701ec7b3f864c0326223ef4c92fa46efc5d4c94e7802844c51927265f7\"]}"
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

The following is an invalid `SwapRequest` with pubkeys and refund mixed.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"cc93775c74df53d7c97eb37f72018d166a45ce4f4c65f11c4014b19acd02bd2f\",\"data\":\"02f515ab63e973e0dadfc284bf2ef330b01aa99c3ff775d88272f9c17afa25568c\",\"tags\":[[\"pubkeys\",\"026925e5bb547a3ec6b2d9b8934e23b882f54f89b2a9f45300bf81fd1b311d9c97\"],[\"n_sigs\",\"2\"],[\"refund\",\"03c8cd46b7e6592c41df38bc54dce2555586e7adbb15cc80a02d1a05829677286d\"],[\"n_sigs_refund\",\"1\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "03f6d40d0ab11f4082ee7e977534a6fcd151394d647cde4ab122157e6d755410fd",
      "witness": "{\"signatures\":[\"a9f61c2b7161a50839bf7f3e2e1cb9bd7bdacd2ce62c0d458a5969db44646dad409a282241b412e8b191cc7432bcfebf16ad72339a9fb966ca71c8bd971662cc\",\"aa778ec15fe9408e1989c712c823e833f33d45780b9a25555ea76004b05d495e99fd326914484f92e7e91f919ee575e79add26e9d4bbe4349d7333d7e0021af7\"]}"
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

The following is a `SwapRequest` with locktime passed and refund keys signatures are valid

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"3ab4fe4969edd99ee9f3d40d2f382157ae5f382ba280ee5ff2d87360e315951b\",\"data\":\"032d3eecd23c9e50972d2964aaae2d302ffdb8717018469f05b051502191c398b1\",\"tags\":[[\"locktime\",\"1\"],[\"n_sigs\",\"1\"],[\"refund\",\"02d3edfb9e9ffdcd4845ba1d3f4cfc65503937c5c9d653ce49f315e76b608a8683\",\"03068b44ca2edca02b6e0832a9e014e409a5e44501e07d7227877efdf10aedf19d\"],[\"n_sigs_refund\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "0244bb030c94f79092eb66bc84937ab920360fec3c333f424248592113fcc96cd6",
      "witness": "{\"signatures\":[\"83c45281c4a4dbbaab82c795ff435468f8c22506dc75debe34e5e07d1a889693e89ab1d621575039a1470bea1bf9a73dcf57f9902bff32afb52c4c403c852e46\",\"071570a852228cb16368807024fd6d7c53b1c3b1a574f206fd2cb6fd61235ad894be111a49a42133c786c366d0a96bfc108b45f6bcfa5496701e0d5cc2e4d86a\"]}"
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

The following is a valid `SwapRequest` with an HTLC also locked to a public key

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"HTLC\",{\"nonce\":\"247864413ecc86739078f8ab56deb8006f9c304fc270f20eb30340beca173088\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"03f2a205a6468f29af3948f036e8e35e0010832d8d0b43b0903331263a45f93f31\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "0394ffcb2ec2a96fd58c1b935784a7709c62954f7f11f1e684de471f808ccfb0bf",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"fa820534d75faac577eb5b42e9929a9f648baaaf28876cbcb7c10c6047cf97f6197d1cbf4907d94c1e77decf4b1acf0c85816a30524ee1b546181a19b838b535\"]}"
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

The following is an invalid `SwapRequest` with an HTLC also locked to a public key, locktime and refund key. locktime is
not expired but proof is signed with refund key.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"HTLC\",{\"nonce\":\"b6f0c59ea4084369d4196e1318477121c2451d59ae767060e083cb6846e6bbe0\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0329fdfde4becf9ff871129653ff6464bb2c922fbcba442e6166a8b5849599604f\"],[\"locktime\",\"4854185133\"],[\"refund\",\"035fcf4a5393e4bdef0567aa0b8a9555edba36e5fcb283f3bbce52d86a687817d3\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "024fbbee3f3cc306a48841ba327435b64de20b8b172b98296a3e573c673d52562b",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"7526819070a291f731e77acfbe9da71ddc0f748fd2a3e6c2510bc83c61daaa656df345afa3832fe7cb94352c8835a4794ad499760729c0be29417387d1fc3cd1\"]}"
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

The following is a valid `SwapRequest` with a multisig HTLC also locked to locktime and refund keys.

```json
{
  "inputs": [
    {
      "amount": 2,
      "id": "00bfa73302d12ffd",
      "secret": "[\"HTLC\",{\"nonce\":\"d4e089a466a5dd15031a406a3733adecf6f82aa76eee31d6bc8eaff3d78f6daa\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0367ec6c26c688ddd6162907298726c6d5ad669f99cf27b3ac6240c64fa7c5036f\"],[\"locktime\",\"1\"],[\"refund\",\"0302208be01ac255b9845e88a571120d2ce2df3f877414a430e17b5c0d993b66de\",\"0275a814c7a891f3241aca84097253cd173b933d012009b1335a981599bec3cb3f\"],[\"n_sigs_refund\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "0374419050d909ba80122ed5e1e8ae6cc569c269fdff257fc5eae32945ca6076fe",
      "witness": "{\"preimage\":\"0000000000000000000000000000000000000000000000000000000000000001\",\"signatures\":[\"4c7d55d6447c6d950fe2d2629441e8e69368be6e0f576bc4f343e830bcdc1e2296ddce74cb5a64245639464814ca98b129b06461b0897b0d1b94133050f233bd\",\"bb7fd77512ac69a47462e91c5e47e20b5ad1466d28ea71ffbdf5d0ae40d2865b90ffc34fc3202f3b775b9428667c9aa54d778af2055a530946db3a0311a28493\"]}"
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
  "quote": "uHwJ-f6HFAC-lU2dMw0KOu6gd5S571FXQQHioYMD",
  "inputs": [
    {
      "amount": 4,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"f5c26c928fb4433131780105eac330338bb9c0af2b2fd29fad9e4f18c4a96d84\",\"data\":\"03c4840e19277822bfeecf104dcd3f38d95b33249983ac6fed755869f23484fb2a\",\"tags\":[[\"pubkeys\",\"0256dcc53d9330e0bc6e9b3d47c26287695aba9fe55cafdde6f46ef56e09582bfb\"],[\"n_sigs\",\"1\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02174667f98114abeb741f4964bdc88a3b86efde0afa38f791094c1e07e5df3beb",
      "witness": "{\"signatures\":[\"abeeceba92bc7d1c514844ddb354d1e88a9776dfb55d3cdc5c289240386e401c3d983b68371ce5530e86c8fc4ff90195982a262f83fa8a5335b43e75af5f5fc7\"]}"
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
["P2PK",{"nonce":"f5c26c928fb4433131780105eac330338bb9c0af2b2fd29fad9e4f18c4a96d84","data":"03c4840e19277822bfeecf104dcd3f38d95b33249983ac6fed755869f23484fb2a","tags":[["pubkeys","0256dcc53d9330e0bc6e9b3d47c26287695aba9fe55cafdde6f46ef56e09582bfb"],["n_sigs","1"],["sigflag","SIG_ALL"]]}]02174667f98114abeb741f4964bdc88a3b86efde0afa38f791094c1e07e5df3beb000bfa73302d12ffd038ec853d65ae1b79b5cdbc2774150b2cb288d6d26e12958a16fb33c32d9a86c39uHwJ-f6HFAC-lU2dMw0KOu6gd5S571FXQQHioYMD
```

The following is a valid `SIG_ALL` `MeltRequest`.

```json
{
  "quote": "uHwJ-f6HFAC-lU2dMw0KOu6gd5S571FXQQHioYMD",
  "inputs": [
    {
      "amount": 4,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"f5c26c928fb4433131780105eac330338bb9c0af2b2fd29fad9e4f18c4a96d84\",\"data\":\"03c4840e19277822bfeecf104dcd3f38d95b33249983ac6fed755869f23484fb2a\",\"tags\":[[\"pubkeys\",\"0256dcc53d9330e0bc6e9b3d47c26287695aba9fe55cafdde6f46ef56e09582bfb\"],[\"n_sigs\",\"1\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02174667f98114abeb741f4964bdc88a3b86efde0afa38f791094c1e07e5df3beb",
      "witness": "{\"signatures\":[\"abeeceba92bc7d1c514844ddb354d1e88a9776dfb55d3cdc5c289240386e401c3d983b68371ce5530e86c8fc4ff90195982a262f83fa8a5335b43e75af5f5fc7\"]}"
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
  "quote": "wYHbJm5S1GTL28tDHoUAwcvb-31vu5kfDhnLxV9D",
  "inputs": [
    {
      "amount": 4,
      "id": "00bfa73302d12ffd",
      "secret": "[\"P2PK\",{\"nonce\":\"1705e988054354b703bc9103472cc5646ec76ed557517410186fa827c19c444d\",\"data\":\"024c8b5ec0e560f1fc77d7872ab75dd10a00af73a8ba715b81093b800849cb21fb\",\"tags\":[[\"pubkeys\",\"028d32bc906b3724724244812c450f688c548020f5d5a8c1d6cd1075650933d1a3\"],[\"n_sigs\",\"2\"],[\"sigflag\",\"SIG_ALL\"]]}]",
      "C": "02f2a0ff12c4dd95f2476662f1df49e5126f09a5ea1f3ce13b985db57661953072",
      "witness": "{\"signatures\":[\"a98a2616716d7813394a54ddc82234e5c47f0ddbddb98ccd1cad25236758fa235c8ae64d9fccd15efbe0ad5eba52a3df8433e9f1c05bc50defcb9161a5bd4bc4\",\"dd418cbbb23276dab8d72632ee77de730b932a3c6e8e15bc8802cef13db0b346915fe6e04e7fae03c3b5af026e25f71a24dc05b28135f0a9b69bc6c7289b6b8d\"]}"
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
