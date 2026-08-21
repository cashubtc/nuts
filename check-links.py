#!/usr/bin/env python3
"""Link, anchor and legacy-leak check for the NUTs tree.

Run after every rebase onto the taproot branch. A clean rebase can silently
carry new pre-v3 prose into a v3-only file, which no conflict reports.
"""
import glob
import os
import re
import sys

ROOTS = ["*.md", "tests/*.md", "suppl/*.md", "legacy/*.md", "legacy/tests/*.md"]
# Prose that belongs in legacy/, listed per file where a current NUT may still
# name it: a hit outside this map is either new legacy text or a stale mention.
ALLOWED_LEGACY_MENTIONS = {
    "00.md", "01.md", "07.md", "10.md", "13.md", "18.md", "20.md", "22.md",
    "24.md", "02.md", "03.md", "23.md", "28.md", "29.md", "README.md",
    "tests/28-tests.md", "26.md",
}
LEGACY_MARKERS = re.compile(
    r"pre-v3|version byte `0[01]`|SIG_ALL|sigflag|DLEQ|dleq|deprecated", re.I
)


def slug(heading):
    h = re.sub(r"`", "", heading.strip().lstrip("#").strip())
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h).lower()
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", h)).strip("-")


def main():
    files = sorted(f for pat in ROOTS for f in glob.glob(pat))
    anchors = {}
    for f in files:
        seen, out = {}, set()
        for line in open(f):
            if line.startswith("#"):
                a = slug(line)
                n = seen.get(a, 0)
                seen[a] = n + 1
                out.add(a if n == 0 else f"{a}-{n}")
        anchors[f] = out

    bad = 0
    for f in files:
        s = open(f).read()
        body = re.sub(r"```.*?```", "", s, flags=re.S)
        targets = [(t, "inline") for t in re.findall(r"\]\(([^)\s]+)\)", body)]
        targets += [
            (t, f"ref [{k}]")
            for k, t in re.findall(r"^\[([^\]]+)\]:\s*(\S+)", s, flags=re.M)
        ]
        for t, how in targets:
            if t.startswith(("http", "mailto:")):
                continue
            if t.startswith("#"):
                if t[1:] not in anchors[f]:
                    print(f"{f}: {how} dead local anchor {t}")
                    bad += 1
                continue
            path, _, anc = t.partition("#")
            full = os.path.normpath(os.path.join(os.path.dirname(f), path))
            if not os.path.exists(full):
                print(f"{f}: {how} missing file {t}")
                bad += 1
            elif anc and full in anchors and anc not in anchors[full]:
                print(f"{f}: {how} dead anchor {t}")
                bad += 1

        if not f.startswith("legacy/") and f not in ALLOWED_LEGACY_MENTIONS:
            for i, line in enumerate(s.split("\n"), 1):
                if LEGACY_MARKERS.search(line):
                    print(f"{f}:{i}: legacy prose in a current NUT: {line.strip()[:70]}")
                    bad += 1

    print(f"{bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
