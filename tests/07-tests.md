# NUT-07 Test Vectors

These vectors cover the v3 [spend commitment](../07.md) on keysets with version byte `02`. `tagged_hash` is [NUT-10](../10.md#nutroot-secrets-v3-keysets)'s construction, and `SHA256("Cashu_SpendCommitment")` = `0883d5edc50a8421e9e5e6a106f355a469ff8c9685a34a9f67ce544c8bb6fd9a`; `Y` contributes its raw compressed 48 bytes; `witness_hash` is SHA-256 over the UTF-8 bytes of the exact witness string value, not its JSON-escaped form. Signatures inside the test vector witnesses are reproducible with zero auxiliary randomness.

## Key-path spend, no disclosure

The [NUT-10 swap vector](10-tests.md#transaction-transcripts)'s proof (`Y` from the [NUT-13 V3 vectors](13-tests.md), counter `0`), spent through its key path. The witness is the exact string the wallet sent:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "input_digest": "867091ad6dba3069bcff610e29300b5c1e2d89f0e5165f17d155000e77d18f9c",
  "witness": "{\"signatures\":[\"a46a08f9cf25bee38abe8e83a57dae316b64e826f3bd1a7261d3230cb97a70d910ffda84536464853b651cafeb3167affc13d1456d0647cdc685422ba56509a2\"]}",
  "witness_hash": "15b72b9b3158f621dd9c95fecfaa93e9f5292d1df521c4c97a9129722305f7e6",
  "commitment": "80ef4c3484dd76f89eab82d2a24178f89259507cb6d1c5dfc3cb573fa9597f5b"
}
```

No leaf carries `disclosure`, so the checkstate entry returns the commitment alone:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "state": "SPENT",
  "witness": null,
  "input_digest": null,
  "commitment": "80ef4c3484dd76f89eab82d2a24178f89259507cb6d1c5dfc3cb573fa9597f5b"
}
```

The spender can open the commitment by revealing the `witness` and `input_digest` above: recomputing `tagged_hash("Cashu_SpendCommitment", Y || input_digest || witness_hash)` reproduces the returned commitment, and the witness signature verifies against the secret's x-coordinate over `input_digest`.

## Script-path spend through a disclosure leaf

The [NUT-10 auditable lock vector](10-tests.md#worked-example-auditable-lock-with-disclosure)'s spend. Its exercised leaf carries `disclosure` mode `0x01`, so the mint returns the exact witness string and `input_digest`, which together open the commitment unsolicited:

```json
{
  "Y": "aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe7",
  "state": "SPENT",
  "witness": "{\"leaf\":\"00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101\",\"control\":{\"K\":\"028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407\",\"path\":[]},\"signatures\":[\"4cc8e5af02375b2497f5ad1c0241ea2de2b9ead33a6b5abd809bf27f8563967a13a0b484333e90e1d8622d5e884156ea40e1000587c25afe9904e1dbb85d0660\"]}",
  "input_digest": "1732e47d4ce0b6510a51c88ccc41cb7b5fe673987e635738d54d8ca9686336d1",
  "commitment": "c682da9c8601ab9795aaf464ff3ee29f22b4a659ffa8393a00d4ee1e2a361ae4"
}
```

with `witness_hash` = `6bed7b71c323ba221b4941a179c55981115459e065f2ec884b6bb2c73d7d2f03`. A verifier recomputes the commitment from the returned fields, then verifies the leaf's signature against key `3` over `input_digest` and the control block against the proof's secret.

`UNSPENT` and `PENDING` entries carry `witness`, `input_digest` and `commitment` as `null`.
