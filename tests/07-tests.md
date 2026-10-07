# NUT-07 Test Vectors

These vectors cover the v3 [spend commitment](../07.md) on keysets with version byte `02`. `tagged_hash` is [NUT-10](../10.md#nutroot-secrets-v3-keysets)'s construction, and `SHA256("Cashu_SpendCommitment")` = `0883d5edc50a8421e9e5e6a106f355a469ff8c9685a34a9f67ce544c8bb6fd9a`; `Y` contributes its raw compressed 48 bytes; `witness_hash` is SHA-256 over the UTF-8 bytes of the exact witness string value, not its JSON-escaped form. Signatures inside the test vector witnesses are reproducible with zero auxiliary randomness.

## Key-path spend, no disclosure

The [NUT-10 swap vector](10-tests.md#transaction-transcripts)'s proof (`Y` from the [NUT-13 V3 vectors](13-tests.md), counter `0`), spent through its key path. The witness is the exact string the wallet sent:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "input_digest": "cb464413d088ae738b9f78141a02d49f51c6ad85029b6e43cb3ac86ef327990e",
  "witness": "{\"signatures\":[\"45fa48240f7793b749aa5a5b7c4a9abaf836a81dfaa690df20a61d6916b812130febdb02e3806be59a1dd01a03bf8ee51252e42cff87a6e065aa1daa2c5e9c0a\"]}",
  "witness_hash": "dae5c969d1eb46151cf3b9d0872802ec3ad7e3c3c6ba9a72edad4426160cd6de",
  "commitment": "90d5e0bdfd9f893c666cb45e397a1e5821659e2cbbac7c9e5306670440f1e415"
}
```

No leaf carries `disclosure`, so the checkstate entry returns the commitment alone:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "state": "SPENT",
  "witness": null,
  "input_digest": null,
  "commitment": "90d5e0bdfd9f893c666cb45e397a1e5821659e2cbbac7c9e5306670440f1e415"
}
```

The spender can open the commitment by revealing the `witness` and `input_digest` above: recomputing `tagged_hash("Cashu_SpendCommitment", Y || input_digest || witness_hash)` reproduces the returned commitment, and the witness signature verifies against the secret's x-coordinate over `input_digest`.

## Script-path spend through a disclosure leaf

The [NUT-10 auditable lock vector](10-tests.md#worked-example-auditable-lock-with-disclosure)'s spend. Its exercised leaf carries `disclosure` mode `0x01`, so the mint returns the exact witness string and `input_digest`, which together open the commitment unsolicited:

```json
{
  "Y": "aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe7",
  "state": "SPENT",
  "witness": "{\"leaf\":\"00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101\",\"control\":{\"K\":\"028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407\",\"path\":[]},\"signatures\":[\"e8dc3839d64485f75555d9b459ab0f0cab46d5a0420bb80f661b253e9431d0e42526f974f4118c52f95b12427f9cfd2ad24fa7d3c2c93560a08063f849026100\"]}",
  "input_digest": "4b7ffce02cb6ea76d04aaafaa40c0b0522cfcd35f01e3ba697b004b6953cead2",
  "commitment": "c16eff5d1be84d29edf8653880995dcf159dc593323b3d5171f8568b90c57891"
}
```

with `witness_hash` = `f3de76772ca0d0f2dff1d0962c6ba8ecf3b836c8fceae72b6173de0b98364cca`. A verifier recomputes the commitment from the returned fields, then verifies the leaf's signature against key `3` over `input_digest` and the control block against the proof's secret.

`UNSPENT` and `PENDING` entries carry `witness`, `input_digest` and `commitment` as `null`.
