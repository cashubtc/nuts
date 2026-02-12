# NUT-28 Test Vectors

The test vectors in this section use the following inputs.

```shell
# Sender ephemeral Keypair (E = e·G)
e: "1cedb9df0c6872188b560ace9e35fd55c2532d53e19ae65b46159073886482ca" # hex encoded private key
E: "02a8cda4cf448bfce9a9e46e588c06ea1780fcb94e3bbdf3277f42995d403a8b0c" # hex encoded public key

# Receiver long-lived Keypair (P = p·G)
p: "ad37e8abd800be3e8272b14045873f4353327eedeb702b72ddcc5c5adff5129c" # hex encoded private key
P: "02771fed6cb88aaac38b8b32104a942bf4b8f4696bc361171b3c7d06fa2ebddf06" # hex encoded public key

```

Per NUT-11, there are up to 11 locking 'slots' in the order: `[data, ...pubkeys, ...refund]`.

Slot 0 is the `data` tag. Slots 1-10 can be any combination of `pubkeys` and `refund` keys.

### Example P2BK proof

The following P2BK proof shows the receiver's public key (P) blinded in the `data` tag (slot `0`), and the ephemeral public key (E) in the `p2pk_e`metadata field.

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

### Shared Secret (Zx)

The unique shared secret between sender and receiver is: `x(e·p·G) = x(e·P) = x(p·E)`:

```shell
Zx: "40d6ba4430a6dfa915bb441579b0f4dee032307434e9957a092bbca73151df8b" # hex encoded bytes
```

### Deterministic blinding scalar (r)

The following are valid ECDH blinding scalars for receiver pubkey (P), derived by locking slot.

```shell
r0: "f43cfecf4d44e109872ed601156a01211c0d9eba0460d5be254a510782a2d4aa" # scalar as hex padded 64
r1: "4a57e6acb9db19344af5632aa45000cd2c643550bc63c7d5732221171ab0f5b3" # scalar as hex padded 64
r2: "d4a8b84b21f2b0ad31654e96eddbc32bfdedae2d05dc179bdd6cc20236b1104d" # scalar as hex padded 64
r3: "ecebf43123d1da3de611a05f5020085d63ca20829242cdc07f7c780e19594798" # scalar as hex padded 64
r4: "5f42d463ead44cbb20e51843d9eb3b8b0e0021566fd89852d23ae85f57d60858" # scalar as hex padded 64
r5: "a8f1c9d336954997ad571e5a5b59fe340c80902b10b9099d44e17abb3070118c" # scalar as hex padded 64
r6: "c39fa43b707215c163593fb8cadc0eddb4fe2f82c0c79c82a6fc2e3b6b051a7e" # scalar as hex padded 64
r7: "b17d6a51396eb926f4a901e20ff760a852563f90fd4b85e193888f34fd2ee523" # scalar as hex padded 64
r8: "4d4af85ea296457155b7ce328cf9accbe232e8ac23a1dfe901a36ab1b72ea04d" # scalar as hex padded 64
r9: "ce311248ea9f42a73fc874b3ce351d55964652840d695382f0018b36bb089dd1" # scalar as hex padded 64
r10 "9de35112d62e6343d02301d8f58fef87958e99bb68cfdfa855e04fe18b95b114" # scalar as hex padded 64
```

### Blinded Public Keys (P')

The following are valid blinded public keys for receiver pubkey (P), derived by locking slot.

```shell
0: "03b7c03eb05a0a539cfc438e81bcf38b65b7bb8685e8790f9b853bfe3d77ad5315" # hex encoded public key
1: "0352fb6d93360b7c2538eedf3c861f32ea5883fceec9f3e573d9d84377420da838" # hex encoded public key
2: "03667361ca925065dcafea0a705ba49e75bdd7975751fcc933e05953463c79fff1" # hex encoded public key
3: "02aca3ed09382151250b38c85087ae0a1436a057b40f824a5569ba353d40347d08" # hex encoded public key
4: "02cd397bd6e326677128f1b0e5f1d745ad89b933b1b8671e947592778c9fc2301d" # hex encoded public key
5: "0394140369aae01dbaf74977ccbb09b3a9cf2252c274c791ac734a331716f1f7d4" # hex encoded public key
6: "03480f28e8f8775d56a4254c7e0dfdd5a6ecd6318c757fcec9e84c1b48ada0666d" # hex encoded public key
7: "02f8a7be813f7ba2253d09705cc68c703a9fd785a055bf8766057fc6695ec80efc" # hex encoded public key
8: "03aa5446aaf07ca9730b233f5c404fd024ef92e3787cd1c34c81c0778fe23c59e9" # hex encoded public key
9: "037f82d4e0a79b0624a58ef7181344b95afad8acf4275dad49bcd39c189b73ece2" # hex encoded public key
10: "032371fc0eef6885062581a3852494e2eab8f384b7dd196281b85b77f94770fac5" # hex encoded public key
```

### Derived Secret Keys

The following are valid derived secret keys for the receiver secret key (p), by locking slot.

```shell
# skStd: standard derivation, (p + r0) mod n
0: "a174e77b25459f4809a187415af14065b49140c1408860f543444ed59261a605" # hex encoded private key
1: "f78fcf5891dbd772cd68146ae9d740107f96b43ea7d3f34850ee7d71faa6084f" # hex encoded private key
2: "81e0a0f6f9f36eebb3d7ffd733630270967150344203a2d2fb66bfd0466fe1a8" # hex encoded private key
3: "9a23dcdcfbd2987c6884519f95a747a1fc4dc289ce6a58f79d7675dc291818f3" # hex encoded private key
4: "0c7abd0fc2d50af9a357c9841f727acfa683c35dac002389f034e62d6794d9b3" # hex encoded private key
5: "5629b27f0e9607d62fc9cf9aa0e13d78a50432324ce094d462db7889402ee2e7" # hex encoded private key
6: "70d78ce74872d3ffe5cbf0f910634e224d81d189fcef27b9c4f62c097ac3ebd9" # hex encoded private key
7: "5eb552fd116f7765771bb322557e9fecead9e19839731118b1828d030cedb67e" # hex encoded private key
8: "fa82e10a7a9703afd82a7f72d280ec0f3565679a0f120b5bdf6fc70c9723b2e9" # hex encoded private key
9: "7b68faf4c2a000e5c23b25f413bc5c9a2ec9f48b4990deba0dfb8904cac76f2c" # hex encoded private key
10: "4b1b39beae2f21825295b3193b172ecc2e123bc2a4f76adf73da4daf9b54826f" # hex encoded private key

# skNeg: negated derivation, (-p + r0) mod n
0: "47051623754422cb04bc24c0cfe2c1ddc8db1fcc18f0aa4b477df4aca2adc20e" # hex encoded private key
1: "9d1ffe00e1da5af5c882b1ea5ec8c18893e09349803c3c9e552823490af22458" # hex encoded private key
2: "2770cf9f49f1f26eaef29d56a85483e8aabb2f3f1a6bec28ffa065a756bbfdb1" # hex encoded private key
3: "3fb40b854bd11bff639eef1f0a98c91a1097a194a6d2a24da1b01bb3396434fc" # hex encoded private key
4: "b20aebb812d38e7c9e7267039463fc46757c7f4f33b10d1bb440ea91481736fd" # hex encoded private key
5: "fbb9e1275e948b592ae46d1a15d2beef73fcee23d4917e6626e77ced20b14031" # hex encoded private key
6: "1667bb8f98715782e0e68e788554cf9a61cbb094d557710fc92fd1e08b1007e2" # hex encoded private key
7: "044581a5616dfae8723650a1ca702164ff23c0a311db5a6eb5bc32da1d39d287" # hex encoded private key
8: "a0130fb2ca958732d3451cf247726d8749af46a4e77a54b1e3a96ce3a76fcef2" # hex encoded private key
9: "20f9299d129e8468bd55c37388adde124313d39621f9281012352edbdb138b35" # hex encoded private key
10: "f0ab6866fe2da5054db05098b008b042fd0af7b42ca8547137e652137bd6dfb9" # hex encoded private key
```

### Choosing Correct Secret Key Derivation

To decide which derivation to use, receiver calculates their natural Pubkey and compares the parity to their actual pubkey. If the parity matches, use standard derivation, otherwise negated.

```shell
# Natural Pubkey: pG
pG: "03771fed6cb88aaac38b8b32104a942bf4b8f4696bc361171b3c7d06fa2ebddf06" # hex encoded public key

# Actual Pubkey:
P: "02771fed6cb88aaac38b8b32104a942bf4b8f4696bc361171b3c7d06fa2ebddf06" # hex encoded public key

# Parity is mismatched (Schnorr even-Y lifted), so use negated derivation key for slot
```
