# NUT-XX: Mint Quote Lookup by Public Key

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
- `pubkey_signatures` is an array of hex-encoded Schnorr signatures in the same order as `pubkeys` (64 bytes each)

For each `pubkey`, the corresponding `pubkey_signatures` entry signs the SHA-256 hash of:

```
"Cashu_MintQuoteLookup_v1" || mint_pubkey || pubkey
```

`mint_pubkey` is the mint's `pubkey` from its [NUT-06][06] info response, which a mint supporting this NUT **MUST** provide. Fields are concatenated as their UTF-8 string representations.

The mint **MUST** reject the request unless every signature is valid.

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
  "XX": {
    "supported": <bool>
  }
}
```

[04]: 04.md
[06]: 06.md
[20]: 20.md
[errors]: error_codes.md
