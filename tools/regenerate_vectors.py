#!/usr/bin/env python3
"""
Regenerate (and sanity-check) spec test vectors that depend on Keyset ID v2.

- Computes Keyset ID v2 values from `tests/02-tests.md` using the NUT-02 algorithm.
  - Pubkeys are treated as hex-string bytes (UTF-8).
  - `input_fee_ppk` is omitted if missing/null/0.
  - `final_expiry` is omitted if missing/null/0.
- Recomputes NUT-13 V2 `secret_{0..4}` and `r_{0..4}` for the BIP39 mnemonic used in `tests/13-tests.md`.

This script prints values to stdout; you can then paste them into the markdown files.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_02 = REPO_ROOT / "tests" / "02-tests.md"

# From NUT-13 test vectors
DEFAULT_MNEMONIC = "half depart obvious quality work element tank gorilla view sugar picture humble"

# secp256k1 scalar field (group) order
SECP256K1_N = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16)


@dataclass(frozen=True)
class V2Vector:
    vector_name: str
    unit: str
    input_fee_ppk: Optional[int]
    final_expiry: Optional[int]
    keys: dict[int, str]  # amount -> pubkey_hex


def derive_keyset_id_v2(
    keys: dict[int, str],
    unit: str,
    input_fee_ppk: Optional[int],
    final_expiry: Optional[int],
) -> str:
    preimage = b",".join(
        [f"{k}:{v}".encode("utf-8") for k, v in sorted(keys.items(), key=lambda kv: kv[0])]
    )
    preimage += f"|unit:{unit}".encode("utf-8")
    if input_fee_ppk is not None and input_fee_ppk != 0:
        preimage += f"|input_fee_ppk:{input_fee_ppk}".encode("utf-8")
    if final_expiry is not None and final_expiry != 0:
        preimage += f"|final_expiry:{final_expiry}".encode("utf-8")
    return "01" + hashlib.sha256(preimage).hexdigest()


def bip39_seed(mnemonic: str, passphrase: str = "") -> bytes:
    # BIP39 seed: PBKDF2-HMAC-SHA512(mnemonic, salt="mnemonic"+passphrase, 2048, 64)
    salt = ("mnemonic" + passphrase).encode("utf-8")
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode("utf-8"), salt, 2048, dklen=64)


def derive_secret_and_r_hmac(seed: bytes, keyset_id_hex: str, counter_k: int) -> tuple[str, str]:
    message = (
        b"Cashu_KDF_HMAC_SHA256"
        + bytes.fromhex(keyset_id_hex)
        + counter_k.to_bytes(8, "big", signed=False)
    )
    secret = hmac.new(seed, message + b"\x00", hashlib.sha256).digest()
    r_digest = hmac.new(seed, message + b"\x01", hashlib.sha256).digest()
    r = int.from_bytes(r_digest, "big", signed=False) % SECP256K1_N
    return secret.hex(), r.to_bytes(32, "big", signed=False).hex()


def _parse_backticked_int(line: str) -> Optional[int]:
    m = re.search(r"`(null|[0-9]+)`", line)
    if not m:
        return None
    v = m.group(1)
    if v == "null":
        return None
    return int(v)


def parse_tests_02_v2_vectors(md_path: Path) -> list[V2Vector]:
    s = md_path.read_text(encoding="utf-8")
    # Split on headings; keep the heading text.
    parts = re.split(r"^### (Vector [0-9]+)\s*$", s, flags=re.MULTILINE)
    # parts = [preamble, name1, body1, name2, body2, ...]
    vectors: list[V2Vector] = []
    for i in range(1, len(parts), 2):
        name = parts[i].strip()
        body = parts[i + 1]
        if "## Version 2" not in parts[0] and i == 1:
            # still ok; we only care about vector bodies
            pass

        # Metadata lines can appear after an initial blank line; just regex-match anywhere.
        unit_m = re.search(r"^-\s*Unit:\s*`([^`]+)`\s*$", body, flags=re.MULTILINE)
        unit = unit_m.group(1) if unit_m else None
        if unit is None:
            raise ValueError(f"{name}: missing Unit")

        fee_m = re.search(r"^-\s*Input fee ppk:\s*`(null|[0-9]+)`\s*$", body, flags=re.MULTILINE)
        input_fee_ppk = None if fee_m is None else (None if fee_m.group(1) == "null" else int(fee_m.group(1)))

        expiry_m = re.search(r"^-\s*Final expiry:\s*`(null|[0-9]+)`\s*$", body, flags=re.MULTILINE)
        final_expiry = None if expiry_m is None else (None if expiry_m.group(1) == "null" else int(expiry_m.group(1)))

        # First JSON block after "Keys:"
        m = re.search(r"Keys:\s*\n\s*```json\s*\n(.*?)\n```", body, flags=re.DOTALL)
        if not m:
            raise ValueError(f"{name}: missing Keys JSON block")
        keys_raw = json.loads(m.group(1))
        keys: dict[int, str] = {int(k): v for k, v in keys_raw.items()}

        vectors.append(
            V2Vector(
                vector_name=name,
                unit=unit,
                input_fee_ppk=input_fee_ppk,
                final_expiry=final_expiry,
                keys=keys,
            )
        )

    return vectors


def main() -> None:
    vectors = parse_tests_02_v2_vectors(TESTS_02)

    print("# Regenerated Keyset ID v2 values from tests/02-tests.md")
    for v in vectors:
        kid = derive_keyset_id_v2(v.keys, v.unit, v.input_fee_ppk, v.final_expiry)
        print(f"{v.vector_name}: {kid}")

    # Use Vector 1 as the default NUT-13 V2 reference (smallest keyset; also used in NUT-02 examples).
    v1 = next((v for v in vectors if v.vector_name == "Vector 1"), None)
    if v1 is None:
        raise ValueError("Missing Vector 1")

    keyset_id_v1 = derive_keyset_id_v2(v1.keys, v1.unit, v1.input_fee_ppk, v1.final_expiry)
    seed = bip39_seed(DEFAULT_MNEMONIC)

    print("\n# Regenerated NUT-13 V2 secret/r values (counters 0..4)")
    print(f"keyset_id: {keyset_id_v1}")
    print(f"mnemonic: {DEFAULT_MNEMONIC}")
    for c in range(5):
        secret, r = derive_secret_and_r_hmac(seed, keyset_id_v1, c)
        print(f"counter {c}: secret={secret} r={r}")


if __name__ == "__main__":
    main()


