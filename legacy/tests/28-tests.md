# NUT-28 (legacy) Test Vectors

P2BK proofs on P2PK and HTLC secrets for pre-v3 keysets ([legacy NUT-28](../28.md)). The keypairs, shared secret, blinding scalars and blinded keys they use are the [current vectors](../../tests/28-tests.md).

Per NUT-11, there are up to 11 locking 'slots' in the order: `[data, ...pubkeys, ...refund]`.

Slot 0 is the `data` tag. Slots 1-10 can be any combination of `pubkeys` and `refund` keys.

### Example P2BK proof

The following P2BK proof shows the receiver's public key (P) blinded in the `data` tag (slot `0`), and the ephemeral public key (E) in the `p2pk_e` metadata field.

```json
{
  "amount": 64,
  "C": "0381855ddcc434a9a90b3564f29ef78e7271f8544d0056763b418b00e88525c0ff",
  "id": "009a1f293253e41e",
  "secret": "[\"P2PK\",{\"nonce\":\"d4a17a88f5d0c09001f7b453c42c1f9d5a87363b1f6637a5a83fc31a6a3b7266\",\"data\":\"03b7c03eb05a0a539cfc438e81bcf38b65b7bb8685e8790f9b853bfe3d77ad5315\",\"tags\":[]}]",
  "dleq": {
    "s": "6178978456c42eee8eefb50830fc3146be27b05619f04e3490dc596005f0cc78",
    "e": "23f2190b18bfd043d3a526103e15f4a938d646a6bf93b017e2bb7c85e1540b32",
    "r": "d26a55aa39ca50957fdaf54036b01053b0de42048b96a6fb2a167e03f00d0a0f"
  },
  "p2pk_e": "02a8cda4cf448bfce9a9e46e588c06ea1780fcb94e3bbdf3277f42995d403a8b0c"
}
```

### Example P2BK HTLC proof

The following HTLC proof shows the receiver's public key (P) blinded at slot `1` in the `pubkeys` tag, and blinded again at slot `2` in the `refund` tag (for illustration). The `data` tag holds the hash lock, so it occupies slot `0`, but it is **not** blinded, as it is not a key.

The hash lock is the matching pair from the NUT-14 examples (preimage: `0000000000000000000000000000000000000000000000000000000000000001`).

```json
{
  "amount": 64,
  "C": "0270aba098c920adafa1ce75acefb06d8cc541ef80270f70cc7b66375b789ed9be",
  "id": "009a1f293253e41e",
  "secret": "[\"HTLC\",{\"nonce\":\"8b1f18aa85a2787903cfdc776fde0b8555bdb126eea02b05cd84de06a4f4b551\",\"data\":\"ec4916dd28fc4c10d78e287ca5d9cc51ee1ae73cbfde08c6b37324cbfaac8bc5\",\"tags\":[[\"pubkeys\",\"0352fb6d93360b7c2538eedf3c861f32ea5883fceec9f3e573d9d84377420da838\"],[\"locktime\",\"1689418329\"],[\"refund\",\"03667361ca925065dcafea0a705ba49e75bdd7975751fcc933e05953463c79fff1\"]]}]",
  "dleq": {
    "s": "bd6ed079b954151898cadac38c3b8d3371c20d67e8c5f06af3cee4152ac317b4",
    "e": "9ec5b6f2095a8dc7d052a00e0bb050ac95e633e702575630cfd43cb58592d2a1",
    "r": "e8349cf88e5a9f025f0072bf8a2db48d394bad9f7be3d8023f9ee90de1c1924d"
  },
  "p2pk_e": "02a8cda4cf448bfce9a9e46e588c06ea1780fcb94e3bbdf3277f42995d403a8b0c"
}
```

### Example V4 token

The two example proofs above, encoded as a V4 token. Note the `pe` field carrying the ephemeral public key (E) as a 33-byte CBOR bstr.

```
cashuBo2FtdWh0dHA6Ly9sb2NhbGhvc3Q6MzMzOGF1Y3NhdGF0gaJhaUgAmh8pMlPkHmFwgqVhYRhAYXN4q1siUDJQSyIseyJub25jZSI6ImQ0YTE3YTg4ZjVkMGMwOTAwMWY3YjQ1M2M0MmMxZjlkNWE4NzM2M2IxZjY2MzdhNWE4M2ZjMzFhNmEzYjcyNjYiLCJkYXRhIjoiMDNiN2MwM2ViMDVhMGE1MzljZmM0MzhlODFiY2YzOGI2NWI3YmI4Njg1ZTg3OTBmOWI4NTNiZmUzZDc3YWQ1MzE1IiwidGFncyI6W119XWFjWCEDgYVd3MQ0qakLNWTynveOcnH4VE0AVnY7QYsA6IUlwP9hZKNhZVggI_IZCxi_0EPTpSYQPhX0qTjWRqa_k7AX4rt8heFUCzJhc1ggYXiXhFbELu6O77UIMPwxRr4nsFYZ8E40kNxZYAXwzHhhclgg0mpVqjnKUJV_2vVANrAQU7DeQgSLlqb7KhZ-A_ANCg9icGVYIQKozaTPRIv86ankbliMBuoXgPy5Tju98yd_QpldQDqLDKVhYRhAYXN5AWNbIkhUTEMiLHsibm9uY2UiOiI4YjFmMThhYTg1YTI3ODc5MDNjZmRjNzc2ZmRlMGI4NTU1YmRiMTI2ZWVhMDJiMDVjZDg0ZGUwNmE0ZjRiNTUxIiwiZGF0YSI6ImVjNDkxNmRkMjhmYzRjMTBkNzhlMjg3Y2E1ZDljYzUxZWUxYWU3M2NiZmRlMDhjNmIzNzMyNGNiZmFhYzhiYzUiLCJ0YWdzIjpbWyJwdWJrZXlzIiwiMDM1MmZiNmQ5MzM2MGI3YzI1MzhlZWRmM2M4NjFmMzJlYTU4ODNmY2VlYzlmM2U1NzNkOWQ4NDM3NzQyMGRhODM4Il0sWyJsb2NrdGltZSIsIjE2ODk0MTgzMjkiXSxbInJlZnVuZCIsIjAzNjY3MzYxY2E5MjUwNjVkY2FmZWEwYTcwNWJhNDllNzViZGQ3OTc1NzUxZmNjOTMzZTA1OTUzNDYzYzc5ZmZmMSJdXX1dYWNYIQJwq6CYySCtr6HOdazvsG2MxUHvgCcPcMx7ZjdbeJ7ZvmFko2FlWCCexbbyCVqNx9BSoA4LsFCsleYz5wJXVjDP1Dy1hZLSoWFzWCC9btB5uVQVGJjK2sOMO40zccINZ-jF8GrzzuQVKsMXtGFyWCDoNJz4jlqfAl8Acr-KLbSNOUutn3vj2AI_nukN4cGSTWJwZVghAqjNpM9Ei_zpqeRuWIwG6heA_LlOO73zJ39CmV1AOosM
```
