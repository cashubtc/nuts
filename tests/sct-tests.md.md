# NUT-XX Test Vectors

An SCT tree built with the following leaf secrets:

```json
[
  "[\"P2PK\",{\"nonce\":\"ffd73b9125cc07cdbf2a750222e601200452316bf9a2365a071dd38322a098f0\",\"data\":\"028fab76e686161cc6daf78fea08ba29ce8895e34d20322796f35fec8e689854aa\",\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]]}]",
  "[\"P2PK\",{\"tags\":[[\"sigflag\",\"SIG_ALL\"]],\"nonce\":\"ad4481ae666d97c347e2d737aaae159b30ac6d6fcef93cdca4395bb49d581f0e\",\"data\":\"0276cedb9a3b160db6a158ad4e468d2437f021293204b3cd4bf6247970d8aff54b\"}]",
  "[\"P2PK\",{\"nonce\":\"f7325999fee4aacfcd7e6e8d54f651e4b518724c486178b6587ebce107119596\",\"data\":\"030d3f2ad7a4ca115712ff7f140434f802b19a4c9b2dd1c76f3e8e80c05c6a9310\"}]",
  "[\"HTLC\",{\"nonce\":\"83a2010affde58f99848e6c33906a0fc04b8fb4fd195e1467c5cb4dbfff43438\",\"data\":\"023192200a0cfd3867e48eb63b03ff599c7e46c8f4e41146b2d281173ca6c50c54\",\"tags\":[[\"pubkeys\",\"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904\"],[\"locktime\",\"1689418329\"],[\"refund\",\"033281c37677ea273eb7183b783067f5244933ef78d8c3f15b1a77cb246099c26e\"]]}]",
  "[\"HTLC\",{\"nonce\":\"99fc46253939ba6f057760b8b29b00c6f876050e32bd8ee95b5b223f8aa0ec90\",\"data\":\"02573b68784ceba9617bbcc7c9487836d296aa7c628c3199173a841e7a19798020\",\"tags\":[[\"pubkeys\",\"02fb58522cd662f2f8b042f8161caae6e45de98283f74d4e99f19b0ea85e08a56d\"],[\"locktime\",\"1689418329\"]]}]",
  "9becd3a8ce24b53beaf8ffb20a497b683b55f87ef87e3814be43a5768bcfe69f",
  "3838b0454a81511d33b608984c7f01a082f3a80830168f1f3e7d47d21420e8f9",
]
```

Will result in the following leaf hashes:

```json
[
  "b43b79ed408d4cc0aa75ad0a97ab21e357ff7ee027300fb573833c568431e808",
  "6bad0d7d596cb9048754ee75daf13ee7e204c6e408b83ee67514369e3f8f3f96",
  "8da10ed117cad5e89c6131198ffe271166d68dff9ce961ff117bd84297133b77",
  "7ec5a236d308d2c2bf800d81d3e3df89cc98f4f937d0788c302d2754ba28166a",
  "e19353a94d1aaf56b150b1399b33cd4ef4096b086665945fbe96bd72c22097a7",
  "cc655b7103c8b999b3fc292484bcb5a526e2d0cbf951f17fd7670fc05b1ff947",
  "009ea9fae527f7914096da1f1ce2480d2e4cfea62480afb88da9219f1c09767f"
]
```

Which results in the following SCT merkle root hash:

```
71655cac0c83c6949169bcd6c82b309810138895f83b967089ffd9f64d109306
```

Each leaf hash has the following proofs of inclusion:
```json
[
  [
    "7a56977edf9c299c1cfb14dfbeb2ab28d7b3d44b3c9cc6b7854f8a58acb3407d",
    "7de4c7c75c8082ed9a2124ce8f027ed9a60f2236b6f50c62748a220086ed367b"
  ],
  [
    "8da10ed117cad5e89c6131198ffe271166d68dff9ce961ff117bd84297133b77",
    "b43b79ed408d4cc0aa75ad0a97ab21e357ff7ee027300fb573833c568431e808",
    "7de4c7c75c8082ed9a2124ce8f027ed9a60f2236b6f50c62748a220086ed367b"
  ],
  [
    "6bad0d7d596cb9048754ee75daf13ee7e204c6e408b83ee67514369e3f8f3f96",
    "b43b79ed408d4cc0aa75ad0a97ab21e357ff7ee027300fb573833c568431e808",
    "7de4c7c75c8082ed9a2124ce8f027ed9a60f2236b6f50c62748a220086ed367b"
  ],
  [
    "e19353a94d1aaf56b150b1399b33cd4ef4096b086665945fbe96bd72c22097a7",
    "f583288c32937865b0c5c7d4a9262f65b7275f59c8796eb3e79de9e0b217d5e0",
    "7ea48b9a4ad58f92c4cfa8e006afa98b2b05ac1b4de481e13088d26f672d8edc"
  ],
  [
    "7ec5a236d308d2c2bf800d81d3e3df89cc98f4f937d0788c302d2754ba28166a",
    "f583288c32937865b0c5c7d4a9262f65b7275f59c8796eb3e79de9e0b217d5e0",
    "7ea48b9a4ad58f92c4cfa8e006afa98b2b05ac1b4de481e13088d26f672d8edc"
  ],
  [
    "009ea9fae527f7914096da1f1ce2480d2e4cfea62480afb88da9219f1c09767f",
    "2628c9759f0cecbb43b297b6eb0c268573d265730c2c9f6e194b4948f43d669d",
    "7ea48b9a4ad58f92c4cfa8e006afa98b2b05ac1b4de481e13088d26f672d8edc"
  ],
  [
    "cc655b7103c8b999b3fc292484bcb5a526e2d0cbf951f17fd7670fc05b1ff947",
    "2628c9759f0cecbb43b297b6eb0c268573d265730c2c9f6e194b4948f43d669d",
    "7ea48b9a4ad58f92c4cfa8e006afa98b2b05ac1b4de481e13088d26f672d8edc"
  ]
]
```


## Proofs

The following is a valid `Proof` object spending an `SCT` secret with a bearer leaf secret.

```json
{
  "amount": 1,
  "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"71655cac0c83c6949169bcd6c82b309810138895f83b967089ffd9f64d109306\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": {
    "leaf_secret": "9becd3a8ce24b53beaf8ffb20a497b683b55f87ef87e3814be43a5768bcfe69f",
    "merkle_proof": [
      "009ea9fae527f7914096da1f1ce2480d2e4cfea62480afb88da9219f1c09767f",
      "2628c9759f0cecbb43b297b6eb0c268573d265730c2c9f6e194b4948f43d669d",
      "7ea48b9a4ad58f92c4cfa8e006afa98b2b05ac1b4de481e13088d26f672d8edc"
    ]
  }
}
```

The following is a valid `Proof` object spending an `SCT` secret with a NUT-11 P2PK leaf secret.

```json
{
  "amount": 1,
  "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"71655cac0c83c6949169bcd6c82b309810138895f83b967089ffd9f64d109306\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": {
    "leaf_secret": "[\"P2PK\",{\"nonce\":\"ffd73b9125cc07cdbf2a750222e601200452316bf9a2365a071dd38322a098f0\",\"data\":\"028fab76e686161cc6daf78fea08ba29ce8895e34d20322796f35fec8e689854aa\",\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]]}]",
    "merkle_proof": [
      "7a56977edf9c299c1cfb14dfbeb2ab28d7b3d44b3c9cc6b7854f8a58acb3407d",
      "7de4c7c75c8082ed9a2124ce8f027ed9a60f2236b6f50c62748a220086ed367b"
    ],
    "witness": "{\"signatures\":[\"9ef66b39609fe4b5653ee8cc1d4f7133ca16c6cf1862eca7df626c63d90f19f257241ebae3939baa837e1be25e2996b7062e16ba58877aa8318db20729184ff4\"]}"
  }
}
```

<sub>The secret key for the above pubkey is `8e935aec5668312be8f960a5ecc3c5dd290e39985970bfd093047df7f05cc9ec`</sub>

### Invalid

The following is an *invalid* `Proof` object which attempts to spend an `SCT` secret with a bearer leaf secret. The proof is invalid becase the `merkle_proof`'s first (deepest) hash is incorrect.

```json
{
  "amount": 1,
  "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"71655cac0c83c6949169bcd6c82b309810138895f83b967089ffd9f64d109306\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": {
    "leaf_secret": "9becd3a8ce24b53beaf8ffb20a497b683b55f87ef87e3814be43a5768bcfe69f",
    "merkle_proof": [
      "db7a191c4f3c112d7eb3ae9ee8fa9bd940fc4fed6ada9ba9ab2f102c3e3bbe80",
      "2628c9759f0cecbb43b297b6eb0c268573d265730c2c9f6e194b4948f43d669d",
      "7ea48b9a4ad58f92c4cfa8e006afa98b2b05ac1b4de481e13088d26f672d8edc"
    ]
  }
}
```

The following is an *invalid* `Proof` object spending an `SCT` secret with a NUT-11 P2PK leaf secret. The proof is invalid because the P2PK signature is made on the `leaf_secret` instead of the top-level `Proof.secret`.

```json
{
  "amount": 1,
  "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"71655cac0c83c6949169bcd6c82b309810138895f83b967089ffd9f64d109306\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": {
    "leaf_secret": "[\"P2PK\",{\"nonce\":\"ffd73b9125cc07cdbf2a750222e601200452316bf9a2365a071dd38322a098f0\",\"data\":\"028fab76e686161cc6daf78fea08ba29ce8895e34d20322796f35fec8e689854aa\",\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]]}]",
    "merkle_proof": [
      "7a56977edf9c299c1cfb14dfbeb2ab28d7b3d44b3c9cc6b7854f8a58acb3407d",
      "7de4c7c75c8082ed9a2124ce8f027ed9a60f2236b6f50c62748a220086ed367b"
    ],
    "witness": "{\"signatures\":[\"106b3df8cbe1b9e867ec5717f5018b42e388e8fce7de3b09da1da7c6ab1eaaa19ab7ab95a3bcb8af8d627214f339a594efa8aefa9db7f34de2ca0587f5693e46\"]}"
  }
}
```
