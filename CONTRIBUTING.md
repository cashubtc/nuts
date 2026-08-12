# Contributing to Cashu NUTs

This repository contains the protocol specifications for Cashu, defined as **NUTs** (Notation, Usage, and Terminology). Changes to these documents directly affect the interoperability of wallets and mints across the ecosystem. Please read this guide before contributing.

## Opening an Issue

Before making a pull request, consider opening an issue first to discuss your proposed change. This is especially important for new NUTs or significant changes to existing specifications. Issues allow the community to weigh in on the direction before significant effort is invested.

## Pull Request Naming

- **New NUTs:** Use the placeholder `NUT-XX` for all references to the new NUT. Do not try to reserve a number; the final NUT number will be assigned by maintainers before merge.
- **Changes to existing NUTs:** Prefix the PR title with the relevant NUT number(s) (e.g., `NUT-04: Add support for...` or `NUT-04, NUT-05: Update fee model...`).

## Specification Style

NUTs use [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) keywords to indicate requirement levels:

- `MUST`, `MUST NOT`, `REQUIRED` — absolute requirements
- `SHOULD`, `SHOULD NOT`, `RECOMMENDED` — strong recommendations
- `MAY`, `OPTIONAL`, `CAN` — truly optional

Use these keywords consistently and in uppercase when specifying normative requirements. Descriptive or informational text does not need these keywords.

## Review Process

All NUT changes go through a community review process before being merged.

### Required Reviewers

**A minimum of two approving reviews from core Cashu maintainers and contributors are required before a NUT change can be merged.** Additional review from wallet developers, mint operators, library maintainers, and other ecosystem contributors is strongly encouraged to ensure broad consensus.

### Time for Review

Give the community adequate time to review and comment on a proposed change. The exact duration depends on the scope and complexity of the change and whether active discussion is ongoing. Avoid merging while substantive feedback is still being resolved.

### Merge Process

The merge process ensures that specifications are validated by real implementations before becoming part of the spec:

1. **Consensus reached** — Once the NUT PR has been sufficiently ACK'd by reviewers (minimum two approvals from the required reviewer list, discussion resolved), it is labeled **"Awaiting Implementation PRs"**.
2. **Implementation PRs** — Contributors open implementation PRs in their respective wallet or mint repositories that implement the proposed specification change.
3. **Ready to merge** — Once **at least two implementation PRs** across different projects are marked as **"Ready to Merge"**, the NUT specification PR is merged first.
4. **Implementation merge** — The implementation PRs are then merged in their respective repositories.

The reference implementations used for this gate are typically [cashu-ts](https://github.com/cashubtc/cashu-ts), [CDK](https://github.com/cashubtc/cdk), and [Nutshell](https://github.com/cashubtc/nutshell). Implementations from other projects may count if they are public, verifiable, and reviewed.

This process ensures that no specification is merged without proof that it can be correctly implemented and that multiple independent implementations agree on the spec's interpretation.

## Formatting

All files are formatted with [Prettier](https://prettier.io), and a CI check enforces it on every push and pull request.

Run the same pinned version CI uses (see [`.github/workflows/prettier.yml`](.github/workflows/prettier.yml)):

```bash
# check formatting (same as CI)
npx prettier@3.9.1 --check .

# auto-fix
npx prettier@3.9.1 --write .
```

## Questions?

If you have questions about the contribution process, reach out in the [Cashu community channels](https://github.com/cashubtc) or open a discussion on this repository.
