# NUT-11 Test Vectors

The following is a `Proof` with a valid signature.

```json
{"amount":1,"id":"009a1f293253e41e","secret":"[\"P2PK\",{\"nonce\":\"7b99e03aeeef568244585c8a4c9cdb855fafdf7809db929e69015a42b142e08b\",\"data\":\"79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\"}]","C":"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904","witness":"{\"signatures\":[\"9a2851824c39fc1743dd0a9ecf4469284798882ebbc783ae11c823daf936a2ba04d63006865fd62c96a7d323a8161828cd606797a3fed47d624453a56be548bf\"]}"}
```

The following is a `Proof` with an invalid signature as it is on a different secret.
```json
{"amount":1,"secret":"[\"P2PK\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\"}]","C":"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904","id":"009a1f293253e41e","witness":"{\"signatures\":[\"3426df9730d365a9d18d79bed2f3e78e9172d7107c55306ac5ddd1b2d065893366cfa24ff3c874ebf1fc22360ba5888ddf6ff5dbcb9e5f2f5a1368f7afc64f15\"]}"}
```

The following is a `Proof` with 2 signatures required to meet the multi-signature spend condition.
```json
{"amount":1,"id":"009a1f293253e41e","secret":"[\"P2PK\",{\"nonce\":\"f809a1f89ecb15846c6366caa56dbb409ddaf7517b1737374331c2ddaa4638bb\",\"data\":\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"]]}]","C":"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904","witness":"{\"signatures\":[\"163f276d92b98cfa3cc2fce66d3e6df50f11318433a7006af613ab7f044f5c96bb536e4d6bcb83511c1163c7762a699283247017568de9062164170faddfc12a\",\"53f7a6362d3f42897b0bc288d0b1b8499569d29f10def2fb5dc0ce030194db4b742999920adad4e7eb802f0a2311707f330a622c4227828018fde75fc8cc7819\"]}"}
```

The following is a `Proof` with only one signature failing the multi-signature spend condition.
```json
{"amount":1,"id":"009a1f293253e41e","secret":"[\"P2PK\",{\"nonce\":\"f809a1f89ecb15846c6366caa56dbb409ddaf7517b1737374331c2ddaa4638bb\",\"data\":\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"n_sigs\",\"2\"]]}]","C":"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904","witness":"{\"signatures\":[\"163f276d92b98cfa3cc2fce66d3e6df50f11318433a7006af613ab7f044f5c96bb536e4d6bcb83511c1163c7762a699283247017568de9062164170faddfc12a\"]}"}
```

The following is a `Proof` with a signature from the refund key that is spendable because the locktime is in the past.
```json
{"amount":1,"id":"009a1f293253e41e","secret":"[\"P2PK\",{\"nonce\":\"e54f03d9805de0ddc1bc75c65fac9f7c3cc605d372b898bee7f23c90ede09d75\",\"data\":\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"locktime\",\"21\"],[\"n_sigs\",\"2\"],[\"refund\",\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\"]]}]","C":"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904","witness":"{\"signatures\":[\"7ac6d7f02de854e5592b407d9f3ff4bc3521c698841faa0f78f8944398cf3cd223b9ca83cc03da807717a317a11774278a505aa95b8e24f48f06152c044c19a8\"]}"}
```

The following is a `Proof` with a signature from the refund key that is **not** spendable because the locktime is in the future.
```json
{"amount":1,"id":"009a1f293253e41e","secret":"[\"P2PK\",{\"nonce\":\"1318018406468abcb35d7be69eea84e8625172fe470efbd76d4cc374bd1fe027\",\"data\":\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"pubkeys\",\"79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798\",\"142715675faf8da1ecc4d51e0b9e539fa0d52fdd96ed60dbe99adb15d6b05ad9\"],[\"locktime\",\"2100000000000\"],[\"n_sigs\",\"2\"],[\"refund\",\"49098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\"]]}]","C":"02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904","witness":"{\"signatures\":[\"e78bbd50240049e2dc6191812ed6a9989e8c997722443e1c1b8ab60ab9202b7a41b34b15298a52ba58ae67f1475ffcb6485a807c384474979fc86db90531c670\"]}"}
```
