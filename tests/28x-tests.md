# NUT-28 Test Vectors

The test vectors in this section use the following inputs.

```shell
# Sender ephemeral Keypair (E = e·G)
e: "1cedb9df0c6872188b560ace9e35fd55c2532d53e19ae65b46159073886482ca" # hex encoded private key
E: "02a8cda4cf448bfce9a9e46e588c06ea1780fcb94e3bbdf3277f42995d403a8b0c" # hex encoded public key

# Receiver long-lived Keypair (P = p·G)
p: "ad37e8abd800be3e8272b14045873f4353327eedeb702b72ddcc5c5adff5129c" # hex encoded private key
P: "02771fed6cb88aaac38b8b32104a942bf4b8f4696bc361171b3c7d06fa2ebddf06" # hex encoded public key

# Keyset ID
kid: "009a1f293253e41e" # hex keyset ID from Mint
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
  "secret": "[\"P2PK\",{\"nonce\":\"d4a17a88f5d0c09001f7b453c42c1f9d5a87363b1f6637a5a83fc31a6a3b7266\",\"data\":\"03f221b62aa21ee45982d14505de2b582716ae95c265168f586dc547f0ea8f135f\",\"tags\":[]}]",
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
r0: "41b5f15975f787bd5bd8d91753cbbe56d0d7aface851b1063e8011f68551862d" # scalar as hex padded 64
r1: "c4d68c79b8676841f767bcd53437af3f43d51b205f351d5cdfe5cb866ec41494" # scalar as hex padded 64
r2: "04ecf53095882f28965f267e46d2c555f15bcd74c3a84f42cf0de8ebfb712c7c" # scalar as hex padded 64
r3: "4163bc31b3087901b8b28249213b0ecc447cee3ea1f0c04e4dd5934e0c3f78ad" # scalar as hex padded 64
r4: "f5d6d20c399887f29bdda771660f87226e3a0d4ef36a90f40d3f717085957b60" # scalar as hex padded 64
r5: "f275404a115cd720ee099f5d6b7d5dc705d1c95ac6ae01c917031b64f7dccc72" # scalar as hex padded 64
r6: "39dffa9f0160bcda63920305fc12f88d824f5b654970dbd579c08367c12fcd78" # scalar as hex padded 64
r7: "3331338e87608c7f36265c9b52bb5ebeac1bb3e2220d2682370f4b7c09dccd4b" # scalar as hex padded 64
r8: "44947bd36c0200fb5d5d05187861364f6b666aac8ce37b368e27f01cea7cf147" # scalar as hex padded 64
r9: "cf4e69842833e0dab8a7302933d648fee98de80284af2d7ead71b420a8f0ebde" # scalar as hex padded 64
r10 "3638eae8a9889bbd96769637526010b34cd1e121805eaaaaa0602405529ca92f" # scalar as hex padded 64
```

### Blinded Public Keys (P')

The following are valid blinded public keys for receiver pubkey (P), derived by locking slot.

```shell
0: "03f221b62aa21ee45982d14505de2b582716ae95c265168f586dc547f0ea8f135f" # hex encoded public key
1: "0299692178029fe08c49e8123bb0e84d6e960b27f82c8aed43013526489d46c0d5" # hex encoded public key
2: "03ae189850bda004f9723e17372c99ff9df9e29750d2147d40efb45ac8ab2cdd2c" # hex encoded public key
3: "03109838d718fbe02e9458ffa423f25bae0388146542534f8e2a094de6f7b697fa" # hex encoded public key
4: "0339d5ed7ea93292e60a4211b2daf20dff53f050835614643a43edccc35c8313db" # hex encoded public key
5: "0237861efcd52fe959bce07c33b5607aeae0929749b8339f68ba4365f2fb5d2d8d" # hex encoded public key
6: "026d5500988a62cde23096047db61e9fb5ef2fea5c521019e23862108ea4e14d72" # hex encoded public key
7: "039024fd20b26e73143509537d7c18595cfd101da4b18bb86ddd30e944aac6ef1b" # hex encoded public key
8: "03017ec4218ca2ed0fbe050e3f1a91221407bf8c896b803a891c3a52d162867ef8" # hex encoded public key
9: "0380dc0d2c79249e47b5afb61b7d40e37b9b0370ec7c80b50c62111021b886ab31" # hex encoded public key
10: "0261a8a32e718f5f27610a2b7c2069d6bab05d1ead7da21aa9dd2a3c758bdf6479" # hex encoded public key
```

### Derived Secret Keys

The following are valid derived secret keys for the receiver secret key (p), by locking slot.

```shell
# skStd: standard derivation, (p + r0) mod n
0: "eeedda054df845fbde4b8a579952fd9a240a2e9ad3c1dc791c4c6e51654698c9" # hex encoded private key
1: "720e75259068268079da6e1579beee83dc58bd279b5ca893fddfc9547e82e5ef" # hex encoded private key
2: "b224dddc6d88ed6718d1d7be8c5a0499448e4c62af187ab5acda4546db663f18" # hex encoded private key
3: "ee9ba4dd8b0937403b25338966c24e0f97af6d2c8d60ebc12ba1efa8ec348b49" # hex encoded private key
4: "a30ebab8119946311e5058b1ab96c66706bdaf562f921c2b2b396f3e95544cbb" # hex encoded private key
5: "9fad28f5e95d955f707c509db1049d0b9e556b6202d58d0034fd1933079b9dcd" # hex encoded private key
6: "e717e34ad9617b18e604b446419a37d0d581da5334e10748578cdfc2a124e014" # hex encoded private key
7: "e0691c3a5f614abdb8990ddb98429e01ff4e32d00d7d51f514dba7d6e9d1dfe7" # hex encoded private key
8: "f1cc647f4402bf39dfcfb658bde87592be98e99a7853a6a96bf44c77ca7203e3" # hex encoded private key
9: "7c86523000349f193b19e169795d884382118a09c0d6b8b5cb6bb1eeb8afbd39" # hex encoded private key
10: "e370d394818959fc18e9477797e74ff6a004600f6bced61d7e2c80603291bbcb" # hex encoded private key

# skNeg: negated derivation, (-p + r0) mod n
0: "947e08ad9df6c97ed96627d70e447f1238540da5ac2a25cf208614287592b4d2" # hex encoded private key
1: "179ea3cde066aa0374f50b94eeb06ffbf0a29c3273c4f1ea02196f2b8ecf01f8" # hex encoded private key
2: "57b50c84bd8770ea13ec753e014b861158d82b6d8780c40bb113eb1debb25b21" # hex encoded private key
3: "942bd385db07bac3363fd108dbb3cf87abf94c3765c935172fdb957ffc80a752" # hex encoded private key
4: "489ee9606197c9b4196af631208847df1b078e6107fa65812f731515a5a068c4" # hex encoded private key
5: "453d579e395c18e26b96ee1d25f61e83b29f4a6cdb3dd6563936bf0a17e7b9d6" # hex encoded private key
6: "8ca811f3295ffe9be11f51c5b68bb948e9cbb95e0d49509e5bc68599b170fc1d" # hex encoded private key
7: "85f94ae2af5fce40b3b3ab5b0d341f7a139811dae5e59b4b19154dadfa1dfbf0" # hex encoded private key
8: "975c9327940142bcdaea53d832d9f70ad2e2c8a550bbefff702df24edabe1fec" # hex encoded private key
9: "221680d85033229c36347ee8ee4f09bb965b6914993f020bcfa557c5c8fbd942" # hex encoded private key
10: "8901023cd187dd7f1403e4f70cd8d16eb44e3f1a44371f738266263742ddd7d4" # hex encoded private key
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
