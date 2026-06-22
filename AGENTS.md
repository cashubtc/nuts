# AGENTS.md

## Overview

This repository contains the **Cashu protocol specifications**, called **NUTs** (Notation, Usage, and Terminology). Cashu is an open-source ecash protocol for Bitcoin. Each NUT specifies a part of the protocol that wallets and mints implement to interoperate.

This is a **markdown-only** specs repo. There is no application code, no build system, and no test runner. The only CI check is **Prettier** formatting on every push and pull request.

## Repository Layout

```
.
├── 00.md – 29.md          # NUT specifications (zero-padded two-digit numbers)
├── README.md               # Spec index with mandatory/optional tables and implementation support matrix
├── error_codes.md          # Protocol error code registry
├── SECURITY.md             # Vulnerability reporting
├── LICENSE                 # MIT
├── tests/
│   └── NN-tests.md        # Test vectors for NUTs involving crypto or serialization
├── suppl/
│   └── NN.md              # Supplementary material for specific NUTs
└── .github/
    └── workflows/
        ├── prettier.yml    # Formatting CI (runs on every push/PR)
        └── pages.yml       # MkDocs deployment to GitHub Pages
```

## NUT Spec Conventions

Every NUT file follows these conventions:

- **Filename**: Zero-padded two-digit number matching the NUT number (e.g. `30.md` for NUT-30).
- **Title**: `# NUT-NN: Title` as the first line.
- **Status badge**: `` `mandatory` `` or `` `optional` `` on its own line after the title.
- **Dependencies** (if any): `` `depends on: NUT-NN` `` and/or `` `uses: NUT-NN` `` on separate lines.
- **Horizontal rule**: `---` separating the header block from the body.
- **RFC 2119 language**: Use `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`, and `CAN` (capitalized) per RFC 2119 when specifying protocol requirements.
- **API endpoints**: All REST endpoints use the `/v1/` prefix. Show the HTTP method and URL in a ` ```http ` code block, followed by request/response bodies in ` ```json ` blocks.
- **Type annotations in JSON**: Use angle-bracket placeholders for types: `<str>`, `<int>`, `<bool>`, `<Array[Type]>`, `<optional>`.
- **Curl examples**: Include a `bash` code block with a representative `curl` command when documenting an endpoint.
- **Mint info settings**: If the NUT is discoverable via NUT-06, include a `## Mint info setting` section showing the JSON structure under `"nuts"`.
- **Reference links**: Every NUT file ends with a block of reference-style Markdown links. At minimum include all NUTs referenced in the document. The full block looks like:

```
[00]: 00.md
[01]: 01.md
[02]: 02.md
...
```

## NUT Template

When creating a new NUT, use this skeleton:

```markdown
# NUT-NN: Title

`optional`

`depends on: NUT-XX`

---

Description of what this NUT specifies and why it exists.

## Section

Details, protocol flow, and requirements using RFC 2119 language.

## Example

**Request** of `Alice`:

\`\`\`http
POST https://mint.host:3338/v1/endpoint
\`\`\`

With the data being of the form `PostExampleRequest`:

\`\`\`json
{
  "field": <type>
}
\`\`\`

If successful, `Bob` will respond with a `PostExampleResponse`:

\`\`\`json
{
  "field": <type>
}
\`\`\`

## Mint info setting

\`\`\`json
"nuts": {
    "NN": {
      ...
    }
}
\`\`\`

[00]: 00.md
[01]: 01.md
...
```

## Formatting

Prettier is enforced via CI on every push and PR (Node.js 20, default Prettier config).

- **Check**: `npx prettier --check .`
- **Auto-fix**: `npx prettier --write .`

Always run the check before committing. If Prettier reformats your changes, that is the canonical style — do not override it.

## Test Vectors

Test vector files live in `tests/` and are named `NN-tests.md` (matching the NUT number). Add or update test vectors when a NUT involves:

- Cryptographic operations (hashing, signing, blinding, DLEQ)
- Serialization or encoding formats (token encoding, bech32m, CBOR)
- Deterministic derivation (secret generation, keyset IDs)

Test vectors use `shell` code blocks with labeled hex-encoded values.

## Error Codes

The file `error_codes.md` is the central registry of protocol error codes. When a new NUT introduces error conditions:

- Assign codes within the appropriate range (see existing ranges in the file).
- Add rows to the table with the code, description, and relevant NUT references.
- Use the same reference-link style as the NUT files.

## README Updates

`README.md` contains the spec index and an implementation support matrix. When adding a new NUT:

1. Add the NUT to the **Optional** (or **Mandatory**) table in the correct numeric position.
2. The support matrix columns (Wallets, Mints) should initially be empty (`-`) until implementations adopt the spec.
3. Add the corresponding `[NN]: NN.md` reference link at the bottom of the file.

## Common Pitfalls

- **Do not renumber existing NUTs.** NUT numbers are permanent identifiers referenced by implementations.
- **Do not alter the reference link block format.** Keep one `[NN]: NN.md` per line, sorted numerically.
- **Do not change existing API endpoint paths** unless the NUT is explicitly being revised with a breaking change.
- **Preserve the role names.** The protocol uses `Alice` (wallet), `Bob` (mint), and `Carol` (receiver) consistently across all specs.
- **Keep JSON examples valid** (modulo the `<type>` placeholder convention). Trailing commas are acceptable in illustrative examples per existing convention.
- **Do not add supplementary material to the NUT file itself.** Extended material (e.g. redirect URL flows) belongs in `suppl/NN.md`.
