# NUT-28: Mint Quote Lookup by Public Key

`optional`

`depends on: NUT-04, NUT-20`

---

This NUT adds an endpoint for wallets to get all NUT-20 locked mint quotes associated with a set of public keys. Queries require a valid signature from the owner of the corresponding private keys.

## Request

To query quotes assigned to a public key, the wallet makes a `POST /v1/mint/quote/{method}/pubkey` request.

```http
POST https://mint.host:3338/v1/mint/quote/bolt11/pubkey
```

The wallet includes the following `PostMintQuotesByPubkeyRequest` data:

```json
{
  "pubkeys": <Array[str]>,
  "pubkey_signatures": <Array[str]>
}
```

- `pubkeys` is an array of hex-encoded compressed secp256k1 NUT-20 public keys (33 bytes each)
- `pubkey_signatures` is an array of hex-encoded Schnorr signatures on `pubkeys` in the same order (64 bytes each)

The wallet **MUST** provide a valid signature in `pubkey_signatures` for each public key in `pubkeys` with the corresponding private key in the same order as the `pubkeys` array. The message to sign is the byte representation of the public key.

## Response

The mint responds with a `PostMintQuotesByPubkeyResponse`:

```json
{
  "quotes": <Array[MintQuoteResponse]>
}
```

Where `MintQuoteResponse` is the quote response type defined in [NUT-04][04].

## Settings

The settings for this NUT are part of the mint info response ([NUT-06][06]):

```json
{
  "29": {
    "supported": <bool>
  }
}
```

[04]: 04.md
[06]: 06.md
[20]: 20.md
[errors]: error_codes.md
