# NUT-XX: Deterministic Keypairs

`optional`

---

In this document, we describe how wallets deterministically derive secp256k1 keypairs from their seed for use as locking keys in spending conditions (e.g. [NUT-11][11] P2PK) and as quote locking keys (e.g. [NUT-20][20]). This allows wallets to recover the private keys needed to spend locked ecash and to sign quote-locked mint requests after a restore.

## Derivation

The wallet uses the `seed` derived from a [BIP39][bip39] mnemonic, a domain separation tag `DST`, and a `counter` to derive each private key. A separate `counter` is kept per domain.

The HMAC-SHA256 KDF is built as the following:

1. `message = DST || counter_bytes`, where:
   - `DST` is the UTF-8 encoded domain separation tag (see [Domains](#domains)).
   - `counter_bytes` is the counter encoded as an unsigned 64-bit integer in big-endian format.
2. `hmac_digest = HMAC_SHA256(seed, message)`.
3. `priv_key = OS2IP(hmac_digest) mod N`, where `N` is the secp256k1 group order and `OS2IP` interprets the digest as an unsigned big-endian integer.
4. If `priv_key == 0`, the derivation **MUST** be rejected. The probability is negligible.
5. The wallet derives the compressed secp256k1 public key from `priv_key` and uses it as the locking pubkey for the relevant domain.

## Domains

Each application gets a distinct DST and an independent `counter`. Wallets **MUST NOT** share counters across domains.

| Domain                  | DST                           |
| ----------------------- | ----------------------------- |
| [NUT-11][11] P2PK keys  | `Cashu_KDF_HMAC_SHA256_NUT11` |
| [NUT-20][20] quote keys | `Cashu_KDF_HMAC_SHA256_NUT20` |

Future NUTs that require deterministic wallet keys **SHOULD** register a new domain here with a distinct DST of the form `Cashu_KDF_HMAC_SHA256_NUT<n>`.

## Counter

For each domain, the wallet starts with `counter := 0` and increments it by `1` every time it consumes a derived key. The wallet stores the latest `counter` per domain in its database.

## Restoring keys

To recover keys after a restore, the wallet iterates `counter` from `0` for each domain and derives candidate public keys until it has found all keys that were used. Because locked proofs and quote pubkeys carry the terminal pubkey only (no derivation marker), recovery requires deriving candidate keys and matching them against on-mint state (locked proofs found via [NUT-09][09] restore, mint quotes queried by the wallet).

Wallets **SHOULD** scan in batches and continue until three consecutive batches yield no matches, mirroring the [NUT-13][13] approach.

## Code examples

Python:

```python
import hmac
import hashlib

SECP256K1_N = int(
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16
)

def derive_priv_key(seed: bytes, dst: bytes, counter: int) -> bytes:
    """
    Derive a 32-byte secp256k1 private key from seed for the given domain DST and counter.
    """
    message = dst + counter.to_bytes(8, "big")
    digest = hmac.new(seed, message, hashlib.sha256).digest()
    x = int.from_bytes(digest, "big", signed=False)
    k = x % SECP256K1_N
    if k == 0:
        raise RuntimeError("Derived invalid scalar k == 0")
    return k.to_bytes(32, "big")

# Example domains
DST_NUT11 = b"Cashu_KDF_HMAC_SHA256_NUT11"
DST_NUT20 = b"Cashu_KDF_HMAC_SHA256_NUT20"
```

TypeScript:

```typescript
import * as crypto from "crypto";

const SECP256K1_N = BigInt(
  "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141",
);

function derivePrivKey(seed: Buffer, dst: Buffer, counter: number): Buffer {
  const counterBuffer = Buffer.alloc(8);
  counterBuffer.writeBigUInt64BE(BigInt(counter));
  const message = Buffer.concat([dst, counterBuffer]);

  const digest = crypto.createHmac("sha256", seed).update(message).digest();
  const x = BigInt("0x" + digest.toString("hex"));
  const k = x % SECP256K1_N;

  if (k === 0n) {
    throw new Error("Derived invalid scalar k == 0");
  }

  return Buffer.from(k.toString(16).padStart(64, "0"), "hex");
}

// Example domains
const DST_NUT11 = Buffer.from("Cashu_KDF_HMAC_SHA256_NUT11");
const DST_NUT20 = Buffer.from("Cashu_KDF_HMAC_SHA256_NUT20");
```

The compressed secp256k1 public key derived from the returned private key is the value used as the locking pubkey.

**Note:** See the [test vectors][tests].

[09]: 09.md
[11]: 11.md
[13]: 13.md
[20]: 20.md
[bip39]: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
[tests]: tests/XX-tests.md
