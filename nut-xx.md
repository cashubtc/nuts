# NUT-XX: Remote signer communications

`optional`

---

This NUT define a standard way for Mints to communicate with a remote signer. The mint can protect its private key by isolating it to a service.

Mints will connect to the signer and ask for validation of proofs as well signing blinded messages. This NUT does not specify the transport method needed to communicate with the mint.

## Protocol

The signer MUST speak the same language using the GRPC protobuf defined in `remote-signer.proto` inside the repository.

### Authentication

The signer and the mint can communicate with each other over different transports.
The signer MUST NOT accept any request if authentication has not occurred.

#### Over the Network

The Mint and the Signer MUST authenticate with each other using mTLS.

## Seedphrase usage

[BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) mnemonic seedphrase must be used for generation
of the keysets.

Example: `legal winner thank year wave sausage worth useful legal winner thank yellow`

### Canonical unit reference parsing

Implementations **MUST** accept currency unit labels case-insensitively and ignore leading or trailing ASCII whitespace. When serializing a unit into JSON (e.g., as part of a keyset description in NUT-01 responses), implementations **SHOULD** emit the uppercase representation of the unit so that mints and wallets display consistent labels.

Before deriving an index, the input label **MUST** be transformed as follows:

1. Remove leading and trailing ASCII whitespace characters (space, tab, carriage return, line feed).
2. Apply Unicode Normalization Form C (NFC).
3. Convert the normalized string to uppercase using Unicode-aware semantics.

| Input unit   | Canonical form | Index        |
| ------------ | -------------- | ------------ |
| `sat`        | `SAT`          | `1967237907` |
| `SAT`        | `SAT`          | `1967237907` |
| `nuts`       | `NUTS`         | `1502388627` |
| `USD`        | `USD`          | `577560378`  |
| `usD`        | `USD`          | `577560378`  |
| `café`       | `CAFÉ`         | `642348965`  |
| `cafe\u0301` | `CAFÉ`         | `642348965`  |
| `eurc`       | `EURC`         | `1321886550` |

NOTE: Mints **MUST** make sure that the unit_reference integer has not been repeated before for a different normalized
unit string.

## Generating keys for the signer.

For compatibility reasons all signers SHOULD implement the following BIP32 derivation path.

- m = master key
- 129372' (UTF-8 for 🥜)
- unit_reference = Big endian encoded integer of the first 4 bytes of the sha256 hash of the canonical unit string reference modulo by 2^31. We modulo because we want to stay inside the `2^31 - 1` range.
  ex: sha256sum('auth')[:4] = bdf49c3c = 3186924604
  3186924604 % 2^31 = 1039440956.
- version: uint32
- index_of_amount = index of and the amounts of the keyset as if the where laid in an array. ex: [1, 2, 4, 8, 16, ...]

`m / 129372' / unit_reference' / version' / index_of_amount'`

## Configuration

The Signer can also be configured to have some rate limiting features. Limiting the amount of minting that can happen by
time or single action.
