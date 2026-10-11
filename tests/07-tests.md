# NUT-07 Test Vectors

These vectors cover the v3 [spend commitment](../07.md) on keysets with version byte `02`. `tagged_hash` is [NUT-10](../10.md#nutroot-secrets-v3-keysets)'s construction, and `SHA256("Cashu_SpendCommitment")` = `0883d5edc50a8421e9e5e6a106f355a469ff8c9685a34a9f67ce544c8bb6fd9a`; `Y` contributes its raw compressed 48 bytes; `witness_hash` is SHA-256 over the UTF-8 bytes of the exact witness string value, not its JSON-escaped form. Signatures inside the test vector witnesses are reproducible with zero auxiliary randomness.

## Key-path spend, no disclosure

The [NUT-10 swap vector](10-tests.md#transaction-transcripts)'s proof (`Y` from the [NUT-13 V3 vectors](13-tests.md), counter `0`), spent through its key path. The witness is the exact string the wallet sent:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "input_digest": "eca67b680015d42ffb9339b8c0475a90d162d189bd36a15d8b6910de48927edd",
  "witness": "{\"signatures\":[\"5b4b2cbdb5ea75dd2a6451bf2f348e8b837438375dd5e78ba5cb2f3c549258df8ff274e8de9987e7dab88c221f0de820546e42907cec816e2b290af814030a94\"]}",
  "witness_hash": "c0f68fb4268889b1c731f8b6a58b4f3764ea149afda1e99d25833751772d37e7",
  "commitment": "eb3dce8232201aa69f4344f89e07dbfa6690c10cfb26eff9ef48a8be6efbf522"
}
```

No leaf carries `disclosure`, so the checkstate entry returns the commitment alone:

```json
{
  "Y": "a0acf939f033e3d0ae9b5f784341fada38367eec190edfb34e1f0cce9050c80672dbee77a7512b7243544c85ae290a73",
  "state": "SPENT",
  "witness": null,
  "input_digest": null,
  "commitment": "eb3dce8232201aa69f4344f89e07dbfa6690c10cfb26eff9ef48a8be6efbf522"
}
```

The spender can open the commitment by revealing the `witness` and `input_digest` above: recomputing `tagged_hash("Cashu_SpendCommitment", Y || input_digest || witness_hash)` reproduces the returned commitment, and the witness signature verifies against the secret's x-coordinate over `input_digest`.

## Script-path spend through a disclosure leaf

The [NUT-10 auditable lock vector](10-tests.md#worked-example-auditable-lock-with-disclosure)'s spend. Its exercised leaf carries `disclosure` mode `0x01`, so the mint returns the exact witness string and `input_digest`, which together open the commitment unsolicited:

```json
{
  "Y": "aaba46a463d3d10b59fa1532a32d9a5e8fa8e9962a8c6571917981a6fa4d5fafb08c21bbff94189e24e5c256fc0a7fe7",
  "state": "SPENT",
  "witness": "{\"leaf\":\"00010200010104002102f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f90a000101\",\"control\":{\"K\":\"028edfebd6fdea3e1d89359af20868a2e76315b36cdb1a79de497a1757ca7bd407\",\"path\":[]},\"signatures\":[\"b45249e8b1ae085f56a3b7d773bd92fedc16c2ffa7ebaf22fe2963c64ba1b49aa4f8c247bee55d3ccdb66a75383a81bddc9019ad31f6b00dfaae51a018c837ed\"]}",
  "input_digest": "3b0ac0a9f71ce1fbd51f318e320c88595720cb2fefd2395d4c894e4ba5b216d3",
  "commitment": "a9aa41045103cecebdb9639f223f146a150ca14b538b4ccdf824ee5fba638b1e"
}
```

with `witness_hash` = `d44f5863d5bd9a984f571e575a2c71b2848b98975e53d98d0ae283b8a1ad2c52`. A verifier recomputes the commitment from the returned fields, then verifies the leaf's signature against key `3` over `input_digest` and the control block against the proof's secret.

`UNSPENT` and `PENDING` entries carry `witness`, `input_digest` and `commitment` as `null`.
