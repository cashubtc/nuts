# Cashu protocol hardening plan: non-malleable transactions (v3)

**Branch context:** `bls-protocol-hardened` (BLS / keyset version `02`)  
**Date:** 2026-07-18  
**Status:** design plan only — no normative NUT text applied yet  
**Related finding:** SEC-2026-07-17-01 — Member authorization does not authenticate client spend intent

---

## 1. Problem statement

### 1.1 Protocol gap

Cashu’s ordinary (non–NUT-10) proofs are **bearer instruments**. Possession of a `Proof` — specifically the tuple `(amount, id, secret, C)` — is sufficient authorization to spend. Swap (`NUT-03`) and melt (`NUT-05`) requests bind inputs to outputs only by transport integrity between wallet and mint. The protocol does **not** require the party that knows `secret` to sign a commitment to the full transaction (inputs, outputs, quote, fees, witnesses).

Consequently, any party that observes a valid spend request can:

1. copy the valid input proofs;
2. replace blinded outputs (or melt destination material) with attacker-controlled values;
3. submit the mutated request;
4. race the honest request so that the inputs are spent to the attacker.

The database double-spend check still fires (only one spend commits), but **client intent is not preserved**. Funds go to whoever’s mutated transaction lands first.

### 1.2 Where this bites hardest

| Setting | Exposure |
| --- | --- |
| Single honest mint | Classic MITM / malicious proxy / buggy middleware that rewrites JSON |
| Federated / multi-member mint | One Byzantine member can receive the wallet request, rewrite outputs, authorize the replacement at consensus, and steal value (SEC-2026-07-17-01) |
| Quote front-running | Unlocked mint quotes (`NUT-04` without `NUT-20`) allow anyone who learns `quote` id to mint the outputs |

Existing mitigations are incomplete:

- **NUT-11 `SIG_ALL`**: only on P2PK/HTLC proofs, optional, default is `SIG_INPUTS` (signs the secret string only — **does not bind outputs**).
- **NUT-20 locked mint quotes**: optional; unlocked quotes remain anyone-who-knows-the-id.
- **`SIG_ALL` message formats**: ad-hoc string concatenation, different per operation (swap vs melt vs NUT-20), fragile as new quote types and fields appear.
- **Locktime expiry → anyone-can-spend**: after `locktime` with no `refund` keys, proofs become bearer again and are malleable.

### 1.3 Security review residual requirement

From SEC-2026-07-17-01 remediation:

> Define a proof-bound client authorization over the canonical unsigned operation, including every input, output, quote, fee term, and relevant witness. Require verification at consensus admission and again at deterministic apply. For ordinary Cashu, require NUT-11-style P2PK with `SIG_ALL` — a detached key not committed at issuance does not solve the attack.

This plan makes that authorization **mandatory for all v3 spends**, not an optional P2PK feature.

---

## 2. Design goals

1. **Non-malleability:** no party who saw only the wire request (without the wallet’s private keys) can alter publicly relevant fields and still pass mint verification.
2. **Uniform auth model:** one message construction for swap, melt, mint, and (later) BAT-protected requests — not three hand-rolled concats.
3. **Reuse existing primitives:** secp256k1 BIP340 Schnorr, NUT-10/11 witness shapes, NUT-11 multisig pathways — extended rather than replaced.
4. **Scoped break:** **keyset version `02` (BLS v3) only.** Legacy keysets keep current bearer semantics until migrated by swap into v3.
5. **Token UX preserved:** Alice can still send tokens to Carol as a bearer package; the package must carry enough key material for Carol to later produce spend signatures (`secret_private`).
6. **Incremental reviewability:** land normative text in small steps.
7. **Minimal, not maximal, spec surface (the coal):** solve the security gap with **as few lines of normative change as possible**. Prefer one shared rule over rewrites in every NUT; delete conflicting text rather than leave dual paths; avoid new abstractions, endpoints, or field names when an existing one can be reused or retargeted; no essay-length motivation in normative NUTs. Every step should ask: *can this be a pointer + a MUST, or does it need a new section?*

### Non-goals (this plan)

- Changing BLS blind-signature math (`NUT-00` pairing protocol).
- Changing DLEQ (`NUT-12`) offline mint-signature checks.
- Solving mint availability / liveness; only intent authentication.
- Migrating already-issued v1/v2 bearer secrets into signable keys without a reclaim swap.

---

## 3. Locked design decisions

Gathered in the pre-implementation Q&A.

| Topic | Decision |
| --- | --- |
| Who enforces | **Per input**, by keyset version: version `02` inputs require the rules below; legacy inputs keep today’s bearer rules. No special “mixed request” policy |
| Normal-proof ownership | Wallet holds `secret_private` (secp256k1 scalar); wire `secret` **MUST** be a valid **compressed SEC1 secp256k1 pubkey** as lowercase hex (33 bytes → 66 hex chars) for unencumbered v3 proofs — or a NUT-10 scripted secret |
| `Y = hash_to_curve(secret)` | Still hash the UTF-8 bytes of the `secret` string; for unencumbered v3 the string is that pubkey hex (not arbitrary random hex) |
| Spend signatures | **BIP340 Schnorr** over secp256k1 on `SHA256(jcs_bytes)` |
| Multi-input layout | **Per-input `SIG_ALL`**: every **v3** input carries its own witness; each signs the **same** stripped request bytes |
| Message bytes | **RFC 8785 JCS** of the HTTP JSON body with all `witness` / `signature` / auth `signatures` fields **deep-omitted** |
| Ordinary witness shape | Reuse `P2PKWitness`: `{"signatures":["…"]}`; **exactly one** BIP340 sig for ordinary proofs (mint rejects other lengths). NUT-10 multisig keeps multi-element arrays |
| Mint quotes | **Dissolve NUT-20 into NUT-04**: `pubkey` + execute-time `signature` mandatory for all methods |
| Mint execute signed payload | JCS of mint request body minus `signature`; quote lock pubkey is **not** in that body — mint checks `signature` verifies under the quote’s stored `pubkey` separately |
| NUT-10 / NUT-11 | **`SIG_ALL` only**; remove / reject `SIG_INPUTS` |
| Locktime expiry | Remove anyone-can-spend; after expiry only **refund** pathway (if configured), else unspendable |
| HTLC | Keep kind `HTLC`; `data` = compressed pubkey; hash lives in **`tags`: `["hashlock", "<sha256_hex>"]`** |
| Token handoff | Token carries **`secret_private` only**; receiver derives `secret = compressed_pubkey(sk)` |
| TokenV4 CBOR | Repurpose field **`s` = `secret_private`** (not public `secret`) |
| NUT-13 | Derive `secret_private` from KDF; `secret` is the public key encoding |
| BATs (`NUT-22`) | **Deferred.** Ideal end state: BATs behave like any other v3 input (keyed secret + witness over the same request JCS) without BAT-specific signing rules — exact header/body glue left for Step 7 |

### Conceptual model after the change

```
Issuance (mint/swap outputs):
  wallet samples secret_private
  secret = compress(secp256k1_pubkey(secret_private))   # 66 hex chars
  Y = hash_to_curve_G1(utf8(secret))
  B_ = r · Y   → mint blind-signs → C

Spend (swap/melt inputs):
  stripped = deep_omit(request, {"witness","signature","signatures"})
  msg = SHA256(JCS(stripped))          # RFC 8785 UTF-8 bytes
  for each input:
      sig_i = BIP340_sign(secret_private_i, msg)   # or NUT-10 key(s)
      input.witness = {"signatures":[sig_i, …]}

Mint quote redeem:
  quote created with pubkey (mandatory)
  stripped mint body signed under quote.pubkey
```

Ordinary proofs become **self-P2PK-to-ephemeral-key** at issuance: the pubkey is committed inside `secret` (and thus inside the mint signature `C`), so the signing key is not “detached after the fact.”

---

## 4. Threat model notes

| Attacker | What they see | After hardening |
| --- | --- | --- |
| Byzantine federation member / HTTP MITM | Full swap/melt JSON including proofs | Can replay **exact** body; **cannot** change outputs/quote/fees without invalidating input signatures |
| Party who only saw a TokenV4 | `secret_private` | Same as today’s bearer token theft — intended |
| Party who saw spent proof without witness (e.g. bad logging) | `secret` (pubkey) + `C` | **Cannot** spend; needs `secret_private` or NUT-10 key |
| Quote-id sniffer | quote id only | **Cannot** mint; needs NUT-04 signature under locked pubkey |
| Finder of expired HTLC/P2PK without refund | secret structure | Unspendable (funds burned unless refund path exists) — intentional tradeoff |

**Important:** v3 tokens in flight that encode `secret_private` remain bearer under theft/courtesy leak. Non-malleability protects the **mint-facing request**, not token confidentiality.

---

## 5. Incremental steps

Each step is meant to be reviewable on its own. Later steps must not redefine earlier rules — only reference them.

---

### Step 0 — Normative "signed request" foundation

**Summary**  
Add a single, **short** normative definition for: (a) ownership keys for v3; (b) JCS strip; (c) BIP340 domain; (d) per-input spend auth; (e) mint-quote auth message. One place later NUTs point at — not a parallel treatise.

**Minimal-surface bias**  
- Prefer a tight NUT (or NUT-00 section) that is **reference-only** from 03/04/05/11 — later steps are ideally "MUST authenticate per NUT-31" plus deletion of old concat text, not copy-paste.
- Do not restate full P2PK/HTLC locktime rules here.
- Do not invent new witness types if `P2PKWitness` fits.
- Motivation: a few sentences max in the NUT; depth stays in this plan doc.

**Rationale**  
Today NUT-11 swap concat, NUT-11 melt concat, and NUT-20 quote||B_* are three incompatible "what did I sign?" answers. One JCS rule + deep-omit kills all three and future quote-field special cases — fewer total lines than extending each concat.

**Notes / double-check**

- Specify **RFC 8785** exactly (UTF-8, key lexicographic order, number formatting, no insignificant whitespace). Cite libraries only as non-normative.
- Define **deep omit**: recursively delete keys named `witness`, `signature`, and (where used for client auth) `signatures` on request objects. Clarify that NUT-04 response `signatures` (blind sigs) are not part of the request.
- Ambiguity risk: response field collisions vs request — keep omit list request-scoped.
- Confirm hash is `SHA256(jcs_utf8_bytes)` then BIP340 (as NUT-11/20 already hash-then-sign).
- Domain separation: do we need a DST prefix before JCS bytes (`b"Cashu_SignedRequest_v1" || jcs`)? **Recommend yes** so signatures cannot be replayed into unrelated protocols that also JCS-sign JSON. Decide before writing.
- **Mixed keysets:** enforcement is per-input. A v3 input MUST carry a valid spend witness; a legacy input is validated under legacy rules. No extra “reject mixed swaps” rule — each input carries its own requirements.
- CBOR endpoints (if any later): out of scope unless introduced; JSON only for now.
- Test vectors: strip examples + known Schnorr signatures on fixed JSON.
- Mint path: confirming quote-bound pubkey is **state**, not in the signed body (locked — see §3).

**Risks**

- JCS path dependence / Unicode normalisation edge cases — keep keys ASCII as today.
- Floating-point amounts do not appear in Cashu JSON (integers only) — good; state that non-integer numbers are invalid in signed bodies forever.
- Forward compatibility: unknown fields **are** signed if present → wallets/mints that inject extra fields must agree or verification fails (feature, not bug).

---

### Step 1 — `NUT-00` models and token serialization

**Summary**  
Update `Proof`, TokenV3, and TokenV4 for v3 ordinary proofs:

- Wallet/mint wire `Proof.secret` = compressed secp256k1 pubkey hex (66 chars).
- Wallet DB and **token handoff** carry `secret_private` (32-byte seckey, 64 hex).
- TokenV3 JSON uses `secret_private` instead of `secret`; receiver derives `secret` before reserve/swap.
- TokenV4 CBOR: field `s` holds `secret_private` (bytes); public `secret` is derived.
- Document that mint APIs never accept `secret_private` on swap/melt/mint inputs.
- Allow `Proof.witness` on ordinary proofs (not only NUT-10).

**Rationale**  
If `secret` remains a random preimage with no algebraic structure, there is no long-term key committed at issuance, and any later “sign with a detached key” fails SEC-2026-07-17-01’s “must be committed when the proof was issued” test. Encoding the pubkey as `secret` binds the BLS/BDHKE signature `C` to that ownership key via `Y = hash_to_curve(secret)`.

Carrying `secret_private` in the token preserves “paste this string to pay” UX without interactive key exchange (unlike locking to Carol’s long-term P2PK).

**Notes / double-check**

- Unencumbered v3 `Proof.secret` **MUST** decode as a valid compressed secp256k1 public key (33 bytes, `02`/`03` prefix). Mints **MUST** reject spends/issuance patterns that use non-key strings as ordinary v3 secrets.
- NUT-10 scripted secrets remain JSON `Secret` strings (not forced to be a bare pubkey string overall — the pubkey lives in `data`).
- BIP340 uses x-only keys internally; verification must align with NUT-11 public key canonicalisation (including case folding on x).
- Fingerprinting: 66-char hex pubkey secrets vs old recommended 64-char random hex — acceptable and intentional for v3.
- Token sent to Carol including `secret_private` means Carol can spend **and** any logger that stores tokens can spend — same as today with bearer `secret`, but clearer that the token **is** the private key. Wording in specs should not downplay that.
- V3 TokenV3 deprecation path: still specify for completeness or v3-only TokenV4? Still update both if both may carry v3 proofs.
- DLEQ (`d` on TokenV4): still optional; siemens independent of `secret_private`.
- NUT-10 proofs: tokens still carry scripted `secret` string (not `secret_private` of the lock recipient). Do **not** put recipient sk in the token. Clarify questions in Step 4/5.
- Migration of conceptual names: some dirs already call internal wallet field `secret`; rename carefully in non-normative notes only here.

**Risks**

- Wallets that restore old backups without `secret_private` cannot spend v3 proofs — require NUT-13 derivation after Step 6.
- Accidental submission of `secret_private` to mint logs → total loss; forbid in API schemas and ignore/reject if present.

---

### Step 2 — Swap (`NUT-03`) and melt (`NUT-05`)

**Summary**  
For any request whose inputs include a v3 keyset proof (or, per Step 0, exclusively v3):

- Mint MUST validate each input’s mint signature `C` as today.
- Mint MUST require each input to present a witness satisfying Step 0 over the stripped request JCS.
- Ordinary v3 inputs: single BIP340 sig under `secret` (as pubkey) is enough (1-of-1).
- NUT-10 inputs: rules of Steps 4–5 (still SIG_ALL on same JCS message).
- Reject missing/invalid witnesses with explicit error codes.

Melt blank outputs (`NUT-08`) are fields on the melt body — automatically covered by JCS; delete any melt-specific concat guidance once Step 0 is referenced.

**Rationale**  
Swap and melt are the two spend paths that move value. Binding every input key to the full body closes the output-replacement race for both single mints and federation members who only have membership auth, not wallet keys.

Per-input signatures matter because ordinary proofs each have distinct `secret_private`s. Reusing NUT-11’s “first input only + identical Secret.data” aggregator would be unusable for normal multi-proof wallets.

**Notes / double-check**

- Order of checks: amount balance / fees → proof `C` verify (batch) → **spend auth** → mark spent → sign outputs. For federation: verify client auth **at admission and at apply**.
- Async melt (`prefer_async`): signatures MUST be verified **before** moving quote to `PENDING` and before marking proofs in-flight; otherwise a mutated pending op could be substituted.
- Does `prefer_async` itself need to be in the signed body? Yes if present — JCS includes it.
- NUT-15 MPP / multi-method fields: covered automatically.
- Fees paid as balance difference of inputs vs outputs: no separate fee field today for swap; if introduced later如表, JCS covers it if in the body with a stable name.
- Idempotency / NUT-19 cached responses: cache key should be over the same stripped body (or full body including witnesses). Document interaction to avoid signature-stripping cache hits.
- Input proofs in the stripped body **still contain** `secret`, `C`, `amount`, `id` — good; those are committed. Only `witness` is stripped on those objects.

**Risks**

- Replay of identical body is still valid until inputs are spent — same as today; mint must spend-mark atomically with acceptance.
- Large multi-input txs: n BIP340 verifies — cheap relative to BLS pairings.
- Cross-endpoint replay (swap body signed vs melt body): different JSON shapes / endpoints → different JCS; still add DST (Step 0) for defense in depth.

---

### Step 3 — Mint flow (`NUT-04`) and dissolve `NUT-20`

**Summary**

- Merge locked-mint-quote behavior into `NUT-04` as **mandatory** for all payment methods.
- Quote request MUST include compressed `pubkey`.
- Quote response echoes `pubkey`.
- Mint execute body MUST include `signature` over JCS(stripped mint request) verified under quote’s `pubkey`.
- Mark `NUT-20` superseded (stub redirect or historical appendix).
- Update method NUTs: `NUT-23` (bolt11), `NUT-25` (bolt12), `NUT-30` (onchain), `NUT-29` (batch mint).
- Error codes: fold/replace `20008` / `20009` into mandatory-path errors.

**Rationale**  
Unlocked mint quotes are a second malleability/front-run surface with the same economic result (stolen mint). Optional NUT-20 left a footgun in the mandatory mint NUT. Dissolving it matches “any transaction requires the proposer to sign.”

**Notes / double-check**

- Quote id remains secret (UUID v7 CSPRNG) **and** insufficient alone — both required.
- Fresh pubkey per quote (NUT-20 privacy guidance) stays SHOULD/MUST decide: keep SHOULD unique per quote.
- Batch mint (`NUT-29`): one sig per quote entry; JaCS payload must define whether each sig covers only its subset of outputs or the full batch document. Prefer: stripped full batch body signed once per quote key is wrong if multiple keys — keep **per-quote** signed messages as NUT-29 does today: sign the material that authorizes that quote’s outputs. Redefine each as JCS of a canonical per-quote object e.g. `{"quote":id,"outputs":[…]}` deep-stripped — not three different concats trá.
- Description / amount / unit are unbound by execute-time sig if only quote+outputs are signed — amount was fixed at quote time by mint state. Ensure mint binds paid amount to quote server-side (already true); client sig need not re-bind payment request string if immutable on quote record.
- If mint allows outputs amount ≤ paid, silent underpayment mint? Existing NUT-04 rules stay; auth does not loosen them.

**Risks**

- Breaking all wallets that mint without NUT-20 — intentional on v3 mints; coordinate release.
- LN wallets that create invoices before knowing result still work; only the mint call gains a signature.
- Lighting anonymous minting (no client key) goes away for v3 — acceptable under threat model that rejects unlocked quotes.

---

### Step 4 — Spending conditions base + P2PK (`NUT-10`, `NUT-11`)

**Summary**

- `NUT-10`: document that for known kinds used with v3, `data` is always a compressed secp256k1 pubkey; tags remain extension mechanism.
- `NUT-11`:
  - Remove `SIG_INPUTS` (or: if present → reject as unspendable).
  - Default and only mode: **per-input SIG_ALL** over Step 0 JCS message.
  - Delete concat aggregation sections; reference Step 0.
  - Multisig (`n_sigs`, `pubkeys`, `refund`, `n_sigs_refund`): verify BIP340 against candidate keys; count unique valid keys (unchanged intuition).
  - Locktime:
    - Permanent / active: locktime multisig / basic path as today.
    - Expired: **only** refund pathway if `refund` present; if absent → **unspendable** (no anyone-can-spend).
  - Same-key / identical-tags constraint of old SIG_ALL first-input design: remove; keys may differ per input; each input unlocks itself but signs shared tx bytes.

**Rationale**  
`SIG_INPUTS` signs only `Proof.secret` and leaves outputs/mutable fields free — exactly the federation rewrite attack. Anyone-can-spend after locktime reintroduces bearer malleability at the worst time (refund window). Forcing SIG_ALL + refund-or-burn makes expiry explicit.

**Notes / double-check**

- Refund-after-expiry **still** signs full JCS body (not a free-for-all).
- Multisig + per-input: for k-of-n on one proof, that proof’s `witness.signatures` holds k sigs on the **same** JCS msg — still true.
- Heterogeneous inputs (ordinary + P2PK + HTLC) in one swap: each uses its pathway; all sign same stripped request — **allowed**.
- Old published equatorology that said “all SIG_ALL inputs must share Secret.data” goes away — good for mixing change + locked coins carefully.
- `NUT-28` P2BK depends on NUT-11: after change, blinded keys still switch for lock paths; SIG_ALL+JCS still apply. Compel P2BK SIG_ALL same-ephemeral-key rule only where secrets must match — re-read P2BK constraints when editing.
- Tokens of NUT-10 locked proofs: still serial`ize` the scripted secret; witness may be empty until spend; **no secret_private of the lock**.

**Risks**

- Funds locked with old mental model “after locktime anyone can spoil” become burned if no `refund` — document loudly; wallet UX must always set refund keys for HTLC/P2PK time locks.
- Existing in-the-wild SIG_INPUTS proofs on **v2** keysets unchanged; v3 issuances never produce SIG_INPUTS.
- Tooling that only signed secrets must upgrade.

---

### Step 5 — HTLC (`NUT-14`)

**Summary**

- Kind remains `HTLC`.
- `Secret.data` = compressed receiver pubkey (Locktime Multisig primary key), **not** the hash.
- Move the hash out of `data`: SHA-256 hash lives in **`tags` as `["hashlock", "<64 lowercase hex>"]`** (same meaning as today’s `Secret.data` for HTLC).
- `Secret.data` = compressed receiver pubkey (Locktime Multisig primary key).
- Receiver path: valid `preimage` under `hashlock` **and** SIG_ALL under Locktime Multisig keys (`data` + `pubkeys`).
- Sender/refund path: only after locktime via Refund Multisig; always signature-gated.
- Witness remains `HTLCWitness` `{preimage, signatures}` with signatures = SIG_ALL over JCS.

**Rationale**  
If every NUT-10 secret needs a stable pubkey for spend auth, stuffing the hash into `data` collides with that invariant. Putting the hash in tags keeps the Secret object shape stable (`kind` / `nonce` / `data` / `tags` only) and matches how other HTLC/P2PK features already extend via tags.

**Notes / double-check**

- JSON Secret shape becomes:

  ```json
  [
    "HTLC",
    {
      "nonce": "...",
      "data": "<compressed_pubkey_hex>",
      "tags": [
        ["hashlock", "<sha256_hex>"],
        ...
      ]
    }
  ]
  ```

- Hash verification: `SHA256(preimage) == hashlock` tag value.
- `hashlock` tag appears at most once; malformed otherwise (same discipline as other NUT-11 tags).
- Preimage-only without sig: **forbidden**.
- NUT-07 witness download still returns preimage+sigs for settlement proofs.

**Risks**

- Breaking all existing HTLC secrets (`data`=hash) — v3 clean break; no dual-parse.
- Users who omit a receiver pubkey in `data` have no receiver path — `data` required.

---

### Step 6 — Deterministic secrets (`NUT-13`)

**Summary**  
For keyset version `02`:

1. KDF (HMAC-SHA256 tree as today) produces **`secret_private` candidate**.
2. Rejection-sample / validate as secp256k1 scalar ∈ `1 … n-1`.
3. `secret = compressed_sec1_hex(pubkey(secret_private))`.
4. Blinding factor `r` remains BLS Fr rejection sampling (existing V3 path).
5. Restore flow reconstructs `(secret_private, r)` → derives `secret` → rebuilds `BlindedMessage` / `Proof`.
6. Update `tests/13-tests.md` vectors.

**Rationale**  
Restore must recover the signing key, not only the old random secret bytes. Deriving sk from seed keeps 12-word backup sufficient for both rebound and future spend auth.

**Notes / double-check**

- Do **not** treat raw 32-byte HMAC as UTF-8 secret anymore.
- secp256k1 order rejection vs keep-mod-n: prefer rejection sampling for uniformity (same rationale as BLS Fr for `r`).
- Derivation_type_byte: keep `0x00` = secret_private material, `0x01` = r (V3 attempt loop) — document rename in prose.
- Counter increment semantics unchanged.
- After restore, wallet persists `secret_private` for spends.
- Interaction with Step 1 token format: exported tokens after restore still export `secret_private`.V

**Risks**

- Incompatible with any experimental v3 wallets that already shipped random 32-byte secrets-as-strings — this branch may still be pre-production; confirm.
- BIP32 legacy (`00`) and HMAC v2 (`01`) paths unchanged.

---

### Step 7 — Blind authentication tokens (`NUT-22`) — **deferred**

**Summary**  
Defer normative BAT changes until after core spend/mint paths land. **Ideal end state (non-binding until this step):** BATs are just v3 keyed proofs — same `secret` / `secret_private` / `witness` model as ordinary inputs — and authorize a request by signing the **same** stripped JCS of that request, without BAT-specific concat schemes or special signature flags.

Today BATs ride in the `Blind-auth` header as a serialized `AuthProof`, not as `inputs[]` on the body. Making them “like any other input” may require either:

- attaching a witness on the header `AuthProof` over JCS(body) (and possibly method/path), or
- reshaping BATs into body `inputs` (bigger break).

**Rationale**  
Avoid inventing a second auth stack. If BATs are cryptographically the same object as spend inputs, every non-malleability rule from Steps 0–2 applies for free. Details of header glue are mechanical and should not block NUT-03/04/05.

**Notes / double-check**

- Keep one-time spend semantics.
- BAT mint (`POST /v1/auth/blind/mint`) is CAT-gated today, not quote-locked — separate from NUT-04 dissolve.
- DLEQ on BAT mint stays.
- Explicitly out of Steps 0–6 normative MUST text except “v3 auth keysets use keyed secrets when issued.”

**Risks**

- Header size + witness until design is specified.
- If left bearer while sinks use SIG_ALL, a proxy could still slide a BAT onto a different body — document residual risk until Step 7 closes.

---

### Step 8 — Cross-cutting cleanup and tests

**Summary**

- `NUT-07`: spent v3 proofs SHOULD/MUST return witness used.
- `NUT-08`: reference melt SIG_ALL/JCS; no new message format.
- `NUT-12`: no change (mint blind-sig proof).
- `NUT-15`, `NUT-17`, `NUT-18`, `NUT-19`, `NUT-28`, `NUT-29`: consistency pass for signed fields and cache keys.
- `error_codes.md`: codes for missing witness, bad JCS/sig, unlocked mint quote rejected, SIG_INPUTS rejected, expired without refund.
- `README.md`: NUT-20 superseded; flag non-malleable v3 spends.
- Tests: `tests/00`, `11`, `13`, `14`, `20`→`04`, `22`, plus new JCS/SIG vectors.

**Rationale**  
Without a housekeeping step, references left pointing at concat schemes and optional NUT-20 will fork implementations.

**Notes / double-check**

- Prettier / CI on markdown.
- Implementation mates (cdk, nutshell, cashu-ts) are **out of this repo** but call out release order: specs → mints → wallets.
- Federation-specific apply checks live outside nuts but depend on Steps 0–2 being unambiguous.

**Risks**

- Docs-only drift if test vectors lag; make vectors mandatory for Steps 0, 1, 4, 5, 6.

---

## 6. Suggested PR / review order

| Order | Step | Primary files |
| --- | --- | --- |
| 1 | Step 0 | `00.md` (new section) and/or new `31.md` |
| 2 | Step 1 | `00.md` token + Proof |
| 3 | Step 2 | `03.md`, `05.md`, `08.md` (refs), `error_codes.md` |
| 4 | Step 3 | `04.md`, `20.md` stub, `23.md`, `25.md`, `29.md`, `30.md` |
| 5 | Step 4 | `10.md`, `11.md` |
| 6 | Step 5 | `14.md` |
| 7 | Step 6 | `13.md`, `tests/13-tests.md` |
| 8 | Step 7 | `22.md` |
| 9 | Step 8 | remaining + README + tests |

Do not merge Step 4 before Stepˊ 0 is stable — NUT-11 will delete large concat sections in favor of the foundation.

---

## 7. Open nits

### 7.1 Settled (this round)

| # | Question | Decision |
| --- | --- | --- |
| S1 | `hashlock` placement | **In `tags`**: `["hashlock", "<sha256_hex>"]` — not a top-level Secret field |
| S2 | Mint execute message vs quote pubkey | **OK:** sign JCS(mint body minus `signature`); verify under quote’s stored `pubkey` (pubkey not duplicated in body) |
| S3 | What is unencumbered v3 `secret`? | **MUST** be a valid compressed secp256k1 pubkey, 33 bytes hex-encoded — or a NUT-10 script. Not arbitrary random UTF-8 / random 64-hex |
| S4 | Mixed v2+v3 in one swap | **Per-input rules only.** Signatures required on v3 inputs only; no extra mixed-case specification |
| S5 | NUT-22 BATs | **Defer.** Ideal: treat like any other v3 input without extra BAT-only signing rules |
| S6 | Ordinary-proof `witness.signatures` cardinality | **Exactly one** BIP340 sig; mint rejects empty or `len ≠ 1`. NUT-10 multisig unchanged |

### 7.2 Still open

| # | Question | Default lean | Resolve in |
| --- | --- | --- | --- |
| O1 | DST prefix before JCS bytes? | `Cashu_SignedRequest_v1` \|\| jcs | Step 0 |
| O5 | Batch mint per-quote JCS shape? | Explicit per-quote object | Step 3 |
| O7 | New NUT number vs NUT-00 section? | NUT-00 section first; split if large | Step 0 |
| O8 | TokenV3 still required to carry v3 proofs? | Specify both V3 JSON + V4 CBOR | Step 1 |
| O10 | NUT-20 file kept as historical? | Stub + redirect | Step 3 |

---

## 8. Mapping back to SEC-2026-07-17-01

| Remediation item | Plan coverage |
| --- | --- |
| Proof-bound client auth over canonical unsigned op | Steps 0–2: JCS body + per-input BIP340 under issued keys |
| Verify at consensus admission and apply | Step 2 notes (federation); normative mint MUST verify before accept |
| NUT-11 P2PK SIG_ALL for federated spends | Steps 1+4: ordinary proofs are issued as committed pubkeys; SIG_ALL mandatory |
| Detached post-hoc keys insufficient | Step 1: pubkey is the `secret` inside mint signature |
| Bearer proofs + single trusted member | Eliminated for v3; document that v1/v2 still trust mint/members |

---

## 9. What this does *not* fix

- Malicious mint that simply refuses to honor honest requests (liveness / theft by freeze).
- Theft of Token strings (`secret_private` handoff).
- Physical / malware wallet key extraction.
- HTLC refund misconfiguration leading to burned coins post-expiry.
- Privacy: mint still sees input-output link structure on spend (existing Cashu swap model).

---

## 10. Working glossary

| Term | Meaning in this plan |
| --- | --- |
| `secret_private` | secp256k1 private scalar; wallet+token only |
| `secret` | For v3 ordinary proofs: compressed pubkey hex; for NUT-10: scripted JSON string |
| Stripped request | Request JSON deep-omitting client auth fields |
| JCS | RFC 8785 JSON Canonicalization Scheme |
| Per-input SIG_ALL | Every input witnesses the same stripped request |
| v3 | Keyset ID version byte `02` (BLS blind sigs on this branch) |

---

## 11. Next action

1. Lock O1/O7 if desired (DST + NUT-00 vs new NUT) with **minimal-line** preference in mind (one short foundation doc > scattered edits).
2. Implement **Step 0** as the shortest normative text that later steps can mostly pointer-delete against.
3. Proceed step-by-step without bundling NUT-11 rewrite into the foundation PR.
4. When editing any NUT: measure success partly by **net lines** — prefer delete-old-concat + one MUST link over additive dual specifications.
