# NUT-07 Test Vectors

These vectors cover the v3 [spend commitment](../07.md) on keysets with version byte `02`. `tagged_hash` is [NUT-10](../10.md#nutroot-secrets-v3-keysets)'s construction, and `SHA256("Cashu_SpendCommitment")` = `0883d5edc50a8421e9e5e6a106f355a469ff8c9685a34a9f67ce544c8bb6fd9a`; `Y` contributes its raw compressed 48 bytes; `witness_hash` is SHA-256 over the UTF-8 bytes of the exact witness string value, not its JSON-escaped form. Signatures inside the test vector witnesses are reproducible with zero auxiliary randomness.

## Key-path spend, no disclosure

The [NUT-10 swap vector](10-tests.md#transaction-transcripts)'s proof (`Y` from the [NUT-13 V3 vectors](13-tests.md), counter `0`), spent through its key path. The witness is the exact string the wallet sent:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "input_digest": "d988bdcfa1d7699324894fc5dba3a70e7bca534e644b257c9700debb424b4ec8",
  "witness": "{\"signatures\":[\"678c1e71b29552ad86069bcc6d1965028b31df1e4dedf69fe5274ffefcad8c77593e474f581e7b43d9e5f8815c0babb607b17f22536ef5f2354889f088da3979\"]}",
  "witness_hash": "16b13901e951752b15d565b2c477e2fcec7450d6f0a7af96d831946be6935146",
  "commitment": "36c3dac6f3d99dc42dc05ddc1eb5d1b619b70e6a4433c0e1a115126aecdbc0cf"
}
```

No leaf carries `disclosure`, so the checkstate entry returns the commitment alone:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "state": "SPENT",
  "witness": null,
  "input_digest": null,
  "commitment": "36c3dac6f3d99dc42dc05ddc1eb5d1b619b70e6a4433c0e1a115126aecdbc0cf"
}
```

The spender can open the commitment by revealing the `witness` and `input_digest` above: recomputing `tagged_hash("Cashu_SpendCommitment", Y || input_digest || witness_hash)` reproduces the returned commitment, and the witness signature verifies against the secret's x-coordinate over `input_digest`.

## Script-path spend through a disclosure leaf

The [NUT-10 auditable lock vector](10-tests.md#worked-example-auditable-lock-with-disclosure)'s spend. Its exercised leaf carries `disclosure` mode `0x01`, so the mint returns the exact witness string and `input_digest`, which together open the commitment unsolicited:

```json
{
  "Y": "aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe7",
  "state": "SPENT",
  "witness": "{\"leaf\":\"00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101\",\"control\":{\"K\":\"028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407\",\"path\":[]},\"signatures\":[\"3b213cc219a97ab9fafbc91386e2996c9bf5d1973699d5647003728fc95cc8cc9a5fe6e06f5d3e920bb82433e31006a82e25116aa6a120eab5a8e20805d593b0\"]}",
  "input_digest": "1f2cc22d83da66466ce82250f41977b59f97ffc97d1cb4a8933654c6413fdf24",
  "commitment": "fd323982ad241242d815f35668d15000cf2d10f890b8a5073add680416f19969"
}
```

with `witness_hash` = `7b085aa3a28fcc33df4feebc995d749f4c11dd85ce248270748376075b6a8856`. A verifier recomputes the commitment from the returned fields, then verifies the leaf's signature against key `3` over `input_digest` and the control block against the proof's secret.

`UNSPENT` and `PENDING` entries carry `witness`, `input_digest` and `commitment` as `null`.
