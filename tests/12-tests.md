# NUT-12 Test vectors

## `hash_e` function

```shell
R1: "020000000000000000000000000000000000000000000000000000000000000001"
R2: "020000000000000000000000000000000000000000000000000000000000000001"
K: "020000000000000000000000000000000000000000000000000000000000000001"
C_: "02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2"
```

```shell
hash(R1, R2, K, C_): "a4dc034b74338c28c6bc3ea49731f2a24440fc7c4affc08b31a93fc9fbe6401e"
```

## DLEQ verification on `BlindSignature`

The following is a `BlindSignature` with a **valid** DLEQ proof.

```shell
A: "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
B_: "02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2"
```

```json
{
  "amount": 8,
  "id": "00882760bfa2eb41",
  "C_": "02a9acc1e48c25eeeb9289b5031cc57da9fe72f3fe2861d264bdc074209b107ba2",
  "dleq": {
    "e": "9818e061ee51d5c8edc3342369a554998ff7b4381c8652d724cdf46429be73d9",
    "s": "9818e061ee51d5c8edc3342369a554998ff7b4381c8652d724cdf46429be73da"
  }
}
```

## DLEQ verification on `Proof`

The following is a `Prood` with a **valid** DLEQ proof.

```shell
A: "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
```

```json
{
  "amount": 1,
  "id": "00882760bfa2eb41",
  "secret": "daf4dd00a2b68a0858a80450f52c8a7d2ccf87d375e43e216e0c571f089f63e9",
  "C": "024369d2d22a80ecf78f3937da9d5f30c1b9f74f0c32684d583cca0fa6a61cdcfc",
  "dleq": {
    "e": "b31e58ac6527f34975ffab13e70a48b6d2b0d35abc4b03f0151f09ee1a9763d4",
    "s": "8fbae004c59e754d71df67e392b6ae4e29293113ddc2ec86592a0431d16306d8",
    "r": "a6d13fcd7a18442e6076f5e1e7c887ad5de40a019824bdfa9fe740d302e8d861"
  }
}
```
