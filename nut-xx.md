# NUT-XX: Remote signer communications

`optional`

---

This NUT define a standard way for Mints to communicate with a remote signer. The mint can protect its private key by isolating it to a service.

Mints will connect to the signer and ask for validation of proofs as well signing blinded messages. This NUT does not specify the transport method needed to communicate with the mint.

The purpose of this signers is only for cryptographic operations it should not keep any state about the proofs and
blinded messages it sees.

## Protocol

The signer MUST speak the same language using the GRPC protobuf defined in `remote-signer.proto` inside the repository.

### Authentication

The signer and the mint can communicate with each other over different transports.
The signer MUST NOT accept any request if authentication has not occurred.

#### Over the Network

The Mint and the Signer MUST authenticate with each other using mTLS.

## Generating keys for the signer.

For compatibility reasons all signers SHOULD implement the following BIP32 derivation path.

- m = master key
- 129372' (UTF-8 for 🥜)
- unit string integer hash = first 4 bytes sha256 hash of the unit string.
  ex: sha256sum('sat')[:4] = 339efeab = 866057899
- version: uint32
- index_of_amount = index of and the amounts of the keyset as if the where laid in an array. ex: [1, 2, 4, 8, 16, ...]

`m / 129372' / unit_index' / version' / index_of_amount'`

## Configuration

The Signer can also be configured to have some rate limiting features. Limiting the amount of minting that can happen by
time or single action.
