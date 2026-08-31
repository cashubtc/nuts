# NUT-07 Test Vectors

These vectors cover the v3 [spend commitment](../07.md) on keysets with version byte `02`. `tagged_hash` is [NUT-10](../10.md#nutroot-secrets-v3-keysets)'s construction; `Y` contributes its raw compressed 48 bytes; `witness_hash` is SHA-256 over the UTF-8 bytes of the exact witness string value, not its JSON-escaped form. Signatures inside the test vector witnesses are reproducible with zero auxiliary randomness.

## Key-path spend, no disclosure

The [NUT-10 swap vector](10-tests.md#transaction-transcripts)'s proof (`Y` from the [NUT-13 V3 vectors](13-tests.md), counter `0`), spent through its key path. The witness is the exact string the wallet sent:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "input_digest": "0f9483a25c859d5156dccc3c141a26d987618ec365bfa12f8c107db0ebd02ae7",
  "witness": "{\"signatures\":[\"ff3be61493fba8bcb2eb8256a1976699f5d439f1ad9f1e82f724b1565091239fb4e0dcc5f99e83a995176fcb5a750dca017c76c4caac9862e416bfd86f3b8b71\"]}",
  "witness_hash": "c9fe4f8ebf4b357b3149adea8d310969fb12e484d2ac77dc0d4e9e8f1da9006c",
  "commitment": "844f7fb08c7ed859e74f0b70ace741a2d1b75e56eccdac6b0a7ae449a7598ac1"
}
```

No leaf carries `disclosure`, so the checkstate entry returns the commitment alone:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "state": "SPENT",
  "witness": null,
  "input_digest": null,
  "commitment": "844f7fb08c7ed859e74f0b70ace741a2d1b75e56eccdac6b0a7ae449a7598ac1"
}
```

The spender can open the commitment by revealing the `witness` and `input_digest` above: recomputing `tagged_hash("Cashu_SpendCommitment", Y || input_digest || witness_hash)` reproduces the returned commitment, and the witness signature verifies against the secret's x-coordinate over `input_digest`.

## Script-path spend through a disclosure leaf

The [NUT-10 auditable lock vector](10-tests.md#worked-example-auditable-lock-with-disclosure)'s spend. Its exercised leaf carries `disclosure` mode `0x01`, so the mint returns the exact witness string and `input_digest`, which together open the commitment unsolicited:

```json
{
  "Y": "aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe7",
  "state": "SPENT",
  "witness": "{\"leaf\":\"00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101\",\"control\":{\"K\":\"028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407\",\"path\":[]},\"signatures\":[\"e0d832c9de4d75f3dec43205b55e814fef15b186e7309f275107e1aa566b5ab6b8422628e0b8e5ae303e8812f355c83953af8155d1b8310d78e2acb883f48861\"]}",
  "input_digest": "db64ca493b62de0a5d6e66d25a5f9544e0af97aebfb050059a731ea739d3675d",
  "commitment": "7782dda61b6686d0cf1b752c6a096c5765af29e030bbeaa6fa9a0eae36def2d9"
}
```

with `witness_hash` = `e7319c89f247a8cea8b5e29f7ab36bb2aa416b8f863183e95730ad604de0c2c1`. A verifier recomputes the commitment from the returned fields, then verifies the leaf's signature against key `3` over `input_digest` and the control block against the proof's secret.

`UNSPENT` and `PENDING` entries carry `witness`, `input_digest` and `commitment` as `null`.
