# NUT-XX: Quote ID Lookup

`optional`

`depends on: NUT-04, NUT-20`

---

This NUT defines an API for looking up quote IDs using public keys. This allows wallets to recover quote IDs when they are unknown, which is useful for wallet recovery scenarios or when quote information needs to be retrieved across sessions.

## Quote Lookup by Public Key

Wallets **MAY** retrieve mint quote IDs by providing the public key(s) used during quote creation with NUT-20. This allows quote recovery when the quote ID is unknown.

### Lookup Request

To lookup quote IDs by public key, the wallet makes a `POST /v1/mint/quote/lookup` request with the following `PostMintQuoteLookupRequest`:

```json
{
  "pubkeys": [<str>]
}
```

Where `pubkeys` is an array of hex-encoded public keys to lookup quotes for.

```http
POST https://mint.host:3338/v1/mint/quote/lookup
```

### Lookup Response

The mint responds with a `PostMintQuoteLookupResponse` containing only the quote IDs:

```json
{
  "quotes": [
    {
      "pubkey": <str>,
      "quote": <str>
    }
  ]
}
```

Where:
- `quotes` is an array of quote objects matching the provided public keys (empty array if no matches)
- `pubkey` is the public key associated with this quote
- `quote` is the quote ID that can be used for further operations

**Note:** Only public keys that have associated quotes are included in the response. Public keys without matching quotes are omitted from the response array.

### Example

Request with curl:

```bash
curl -X POST http://localhost:3338/v1/mint/quote/lookup -H "Content-Type: application/json" -d \
'{
  "pubkeys": [
    "1a02b9355b1df74574ca1a85ee96f2a8cad9d650aacbec26734f9ba7309b07b2",
    "8d4f72043ca8ccb7dfb62b351e7589ca34b58ffa069834ecb0f069e3e1504c24"
  ]
}'
```

Response:

```json
{
  "quotes": [
    {
      "pubkey": "1a02b9355b1df74574ca1a85ee96f2a8cad9d650aacbec26734f9ba7309b07b2",
      "quote": "85233cdc-02ea-45e6-b96f-dd6dad19d28e"
    },
    {
      "pubkey": "8d4f72043ca8ccb7dfb62b351e7589ca34b58ffa069834ecb0f069e3e1504c24",
      "quote": "490fd953-89da-441d-b43e-9df6029be769"
    }
  ]
}
```

## Errors

See [Error Codes][errors]:

- `XX001`: Invalid public key format provided in lookup request.

## Settings

The settings for this NUT indicate support for quote lookup functionality. They are part of the info response of the mint ([NUT-06][06]) which in this case reads

```json
{
  "XX": {
    "supported": <bool>
  }
}
```

Where:
- `supported` indicates whether the quote lookup API is available

[04]: 04.md
[06]: 06.md
[20]: 20.md
[errors]: error_codes.md