NUT-SCT: Spending Condition Trees (SCT)
==========================

`optional`, `depends on: NUT-10`

---

This NUT describes a [NUT-10] spending condition called a Spending Condition Tree (SCT). An ecash token locked with an SCT is spendable under a set of conditions, but at spend-time only a single condition must be revealed to the mint.

# Definitions

The following section describes some functions which wallets and mints need to compose and verify Spending Condition Trees. Reference code in python is included for clarity.

### `SHA256(data: bytes) -> bytes`

The SHA256 hash function.

```python
import hashlib

def SHA256(data: bytes) -> bytes:
  h = hashlib.sha256()
  h.update(data)
  return h.digest()
```

### `sorted_merkle_hash(left: bytes, right: bytes) -> bytes`

Hashes two internal merkle node hashes, sorting them lexicographically so that left/right position in the tree is irrelevant.

```python
def sorted_merkle_hash(left: bytes, right: bytes) -> bytes:
  if right < left:
    left, right = right, left
  return SHA256(left + right)
```

### `merkle_root(leaf_hashes: List[bytes]) -> bytes`

Compute the merkle root of a set of leaf hashes. Each branch hash is derived using `sorted_merkle_hash()`, so that left/right position in the tree is irrelevant.

```python
def merkle_root(leaf_hashes: List[bytes]) -> bytes:
  if len(leaf_hashes) == 0:
    return b""
  elif len(leaf_hashes) == 1:
    return leaf_hashes[0]
  else:
    split = len(leaf_hashes) // 2
    left = merkle_root(leaf_hashes[:split])
    right = merkle_root(leaf_hashes[split:])
    return sorted_merkle_hash(left, right)
```

### `merkle_verify(root: bytes, leaf_hash: bytes, proof: List[bytes]) -> bool`

Verify a proof of membership in the given merkle root hash. Membership proofs are represented as a list of internal node hashes, in order from deepest to shallowest in the tree.

To match the behavior of `merkle_root()`, each branch hash is derived using `sorted_merkle_hash()`, so that left/right position in the tree is irrelevant.

```python
def merkle_verify(root: bytes, leaf_hash: bytes, proof: List[bytes]) -> bool:
  h = leaf_hash
  for branch_hash in proof:
    h = sorted_merkle_hash(h, branch_hash)
  return h == root
```

# Spending Condition Trees

In its _expanded_ form, a Spending Condition Tree (SCT) is an ordered list of [NUT-00] secrets, `[x1, x2, ... xn]`.

Each secret in the SCT is a UTF8-encoded string. Each may be a serialized JSON [NUT-10] secret, or a plain [NUT-00] bearer secret. Example:

```json
[
  "[\"P2PK\",{\"tags\":[[\"sigflag\",\"SIG_INPUTS\"]],\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\"}]",
  "[\"P2PK\",{\"tags\":[[\"sigflag\",\"SIG_ALL\"]],\"nonce\":\"ad4481ae666d97c347e2d737aaae159b30ac6d6fcef93cdca4395bb49d581f0e\",\"data\":\"0276cedb9a3b160db6a158ad4e468d2437f021293204b3cd4bf6247970d8aff54b\"}]",
  "[\"P2PK\",{\"nonce\":\"f7325999fee4aacfcd7e6e8d54f651e4b518724c486178b6587ebce107119596\",\"data\":\"030d3f2ad7a4ca115712ff7f140434f802b19a4c9b2dd1c76f3e8e80c05c6a9310\"}]",
  "9becd3a8ce24b53beaf8ffb20a497b683b55f87ef87e3814be43a5768bcfe69f"
]
```

Each secret in the SCT is one possible spending condition for an ecash token. Fulfilling _any_ of the spending conditions in the SCT is deemed sufficient to spend the token.

However, only the wallet which creates the SCT will ever see this expanded form of the SCT. To avoid exposing the whole SCT structure to the mint, a wallet must compute the SCT root hash.

```python
secrets: List[str] = [x1, x2, ... xn]
leaf_hashes = [SHA256(x.encode('utf8')) for x in secrets]
sct_root = merkle_root(leaf_hashes)
```

The `sct_root` is then used as a commitment to the list of secrets.

## SCT

[NUT-10] Secret `kind: SCT`

If for a `Proof`, `Proof.secret` is a `Secret` of kind `SCT`. The hex-encoded merkle root hash of a Spending Condition Tree is in `Proof.secret.data`.

The proof is unlocked by fulfilling ALL of the following conditions:

1. `Proof.witness.leaf_secret` must be a UTF8 string, treated as a secret (possibly a [NUT-10] well-known secret).
1. `Proof.witness.merkle_proof` must be a valid proof (i.e. a list of hashes) demonstrating that `SHA256(Proof.witness.leaf_secret)` is a leaf hash of the SCT root (specified in `Proof.secret.data`).
1. (optional) if `Proof.witness.leaf_secret` encodes a [NUT-10] spending condition which requires a witness, then `Proof.witness.witness` must provide witness data which satisfies those conditions.[^1]

[^1]: Note that the `SCT` well-known secret rules allow for nested SCTs, where a leaf node is itself another SCT. In this case, the `Proof.witness.witness` will itself be another `SCT` witness object. Recursion and self-referencing inside an SCT is not permitted.

Example of a [NUT-10] `SCT` secret object:

```json
[
  "SCT",
  {
    "nonce": "d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615",
    "data": "18065b939dbbb648749bd5532c740078bb757c3b9f81e0309350a1277fa9a39c"
  }
]
```

We serialize this object to a JSON string, and get a blind signature on it, by the mint which is stored in `Proof.C` (see [NUT-03](03.md)). This commits the token created with this secret to knowing and (if applicable) passing [NUT-10] checks for at least one of the SCT's leaf secrets.

### Spending

To spend this ecash, the wallet must know a `leaf_secret` and a `merkle_proof` of inclusion in the SCT root hash. Here is an example `Proof` which spends a token locked with a well-known secret of kind `SCT`. The `leaf_secret` is a simple [NUT-00] bearer secret with no spending conditions.

```json
{
  "amount": 1,
  "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"18065b939dbbb648749bd5532c740078bb757c3b9f81e0309350a1277fa9a39c\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"leaf_secret\":\"9becd3a8ce24b53beaf8ffb20a497b683b55f87ef87e3814be43a5768bcfe69f\",\"merkle_proof\":[\"8da10ed117cad5e89c6131198ffe271166d68dff9ce961ff117bd84297133b77\",\"2397636f1aff968e9f8177b8deaaf9514415126e45aa7755841f966f4eb2279f\"]}"
}
```

Here is a different input, which references the same SCT root hash but uses a different leaf secret - this time a [NUT-10] `P2PK` secret. As `P2PK` requires signature validation, we must provide a `P2PKWitness` stored in `Proof.witness.witness` (See [NUT-11] for details).

```json
{
  "amount": 1,
  "secret": "[\"SCT\",{\"nonce\":\"d426a2750847d5775f06560d973b484a5b6315e17efffecb1d8d518876c01615\",\"data\":\"18065b939dbbb648749bd5532c740078bb757c3b9f81e0309350a1277fa9a39c\"}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"leaf_secret\":\"[\\\"P2PK\\\",{\\\"tags\\\":[[\\\"sigflag\\\",\\\"SIG_INPUTS\\\"]],\\\"nonce\\\":\\\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\\\",\\\"data\\\":\\\"0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\\\"}]\",\"merkle_proof\":[\"6bad0d7d596cb9048754ee75daf13ee7e204c6e408b83ee67514369e3f8f3f96\",\"4ac38d0dffb307a4d704c5c7cc28324fd3c151cfaaeddeaa695b890f1a24050b\"],\"witness\":\"{\\\"signatures\\\":[\\\"9ef66b39609fe4b5653ee8cc1d4f7133ca16c6cf1862eca7df626c63d90f19f257241ebae3939baa837e1be25e2996b7062e16ba58877aa8318db20729184ff4\\\"]}\"}"
}
```

Note that for the purpose of [NUT-11] input signature verification, the signature must be made over the **top-level secret**, which is of kind `SCT`.

## Previous Work

The design of SCTs was inspired by the Bitcoin TapRoot upgrade, specifically [BIP-0341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki). Much like TapScript Trees, Cashu SCTs use merkle trees to prove that a spending condition was committed to when an ecash token was first created.

# Appendix

## Merkle Proof Generation

Below is an example of a function which generates a proof that a specific leaf hash at the given position in the tree is a member of the SCT's merkle root hash. It requires knowledge of the full set of leaf hashes.

This is only an example of a merkle-proof generation algorithm. Wallet implementations are free to implement proof construction in any way which passes the `merkle_verify` function.

```python
def merkle_prove(leaf_hashes: List[bytes], position: int) -> List[bytes]:
  if len(leaf_hashes) <= 1:
    return []
  split = len(leaf_hashes) // 2
  if position < split:
    proof = merkle_prove(leaf_hashes[:split], position)
    proof.append(merkle_root(leaf_hashes[split:]))
    return proof
  else:
    proof = merkle_prove(leaf_hashes[split:], position - split)
    proof.append(merkle_root(leaf_hashes[:split]))
    return proof
```

[NUT-00]: 00.md
[NUT-10]: 10.md
[NUT-11]: 11.md
