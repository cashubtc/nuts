# NUT-XX: Signing packages

`optional`

`depends on: NUT-10`

---

A signing package carries one or more [script-path](10.md#script-path) spends awaiting signatures between wallets, eg to the co-signers of a multisig leaf. It is a JSON object encoded as base64url (no padding) prefixed with `nutspA`:

```json
{
  "version": "nutspA",
  "transcript": <hex_str>,
  "spends": [
    {
      "input": <int>,
      "secret": <hex_str>,
      "leaf": <hex_str>,
      "control": { "K": <hex_str>, "path": [<hex_str>, ...] },
      "E": <hex_str>, // (optional)
      "slots": [<int>, ...], // (optional)
      "signatures": [<hex_str>, ...]
    },
    ...
  ]
}
```

- `transcript` is the transaction's [TLV transcript](00.md#the-transaction-transcript); `SHA256(transcript)` is its transaction digest.
- `spends` holds one entry per input to sign:
  - `input`: the index of the input's container in the transcript, each index at most once;
  - `secret`: the point the input spends, a v3 proof's secret or a mint quote's lock key;
  - `leaf` and `control`: the serialized leaf and its control block, `K` and the merkle `path`;
  - `E`: the ephemeral of a receiver-keyed input ([NUT-28][28]);
  - `slots`: each leaf key's [NUT-28][28] slot, a hint; a signer that matches no slot scans;
  - `signatures`: the signatures collected so far.

A signer decodes the transcript to review the transaction, and **MUST** check each spend before signing: the leaf commits to `secret` through `control`, and `secret` belongs to the named input, its `hash_to_curve` equal to a proof input's `Y` or itself equal to a mint quote input's lock key. It then derives the [input digest](00.md#the-transaction-transcript) and appends BIP-340 signatures by the leaf keys it holds.

The wallet that built the package holds any hashlock preimage, and assembles each witness at merge after checking the package's transcript against its transaction.

See the [test vectors][tests].

[28]: 28.md
[tests]: tests/XX-tests.md
