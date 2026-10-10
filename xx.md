# NUT-XX: Mint Quote Lookup by Public Key

`optional`

`depends on: NUT-04, NUT-20`

---

This NUT adds an endpoint for wallets to get all NUT-20 locked mint quotes associated with a set of public keys, one page at a time. Queries require a valid signature from the owner of the corresponding private keys.

## Request

To query quotes assigned to a public key, the wallet makes a `POST /v1/mint/quote/{method}/pubkey` request.

```http
POST https://mint.host:3338/v1/mint/quote/bolt11/pubkey
```

The wallet includes the following `PostMintQuotesByPubkeyRequest` data:

```json
{
  "pubkeys": <Array[str]>,
  "pubkey_signatures": <Array[str]>,
  "timestamp": <int>,
  "limit": <int>, // Optional
  "cursor": <str|null> // Optional
}
```

- `pubkeys` is an array of hex-encoded compressed secp256k1 NUT-20 public keys (33 bytes each)
- `pubkey_signatures` is an array of hex-encoded Schnorr signatures in the same order as `pubkeys` (64 bytes each)
- `timestamp` is the wallet's current Unix time in whole seconds, expressed as a non-negative integer. It is required and shared by every signature in the request.
- `limit` is the requested maximum number of quotes in the response, across all requested public keys. It **MUST** be a positive integer when provided. The effective page size is the smaller of `limit` and the mint's advertised `max_page_size`; when omitted, it is `max_page_size`.
- `cursor` is an opaque continuation value returned by the mint in a previous response. Omit it or use `null` to start a new scan. Wallets **MUST** pass continuation values back unchanged and **MUST NOT** interpret their contents.

For each `pubkey`, the corresponding `pubkey_signatures` entry signs the SHA-256 hash of:

```
"Cashu_MintQuoteLookup_v1" || mint_pubkey || pubkey || timestamp
```

`mint_pubkey` is the mint's `pubkey` from its [NUT-06][06] info response, which a mint supporting this NUT **MUST** provide. Fields are concatenated as their UTF-8 string representations, without separators. For signing, `timestamp` is encoded as its base-10 integer representation with no leading zeros, sign, whitespace, fractional part, or exponent (for example, `1788825600`). All signatures **MUST** commit to the request's `timestamp`.

### Request validation

Before verifying signatures or looking up quotes, the mint **MUST** reject the entire request if:

- `timestamp` is missing or is not a non-negative integer; or
- `abs(now - timestamp) > 300`, where `now` is the mint's current Unix time in whole seconds when it receives the request; or
- the `pubkeys` and `pubkey_signatures` arrays differ in length; or
- `pubkeys` is empty, contains duplicate public keys, or exceeds the mint's advertised `max_pubkeys`; or
- `limit` is present but is not a positive integer.

Requests exceeding `max_pubkeys` **MUST** fail with error code `11017` (max batch size exceeded). Wallets **SHOULD** split larger sets of public keys into separate scans within that limit.

The timestamp window is inclusive: timestamps exactly 300 seconds before or after `now` pass the time check. The mint **MUST** use its own clock for this check. Wallets and mints **SHOULD** keep their clocks synchronized.

The mint **MUST** then verify every signature against its corresponding public key and the message above. If any signature is invalid, the mint **MUST** reject the entire request without returning quotes. Requests using signatures that omit the timestamp **MUST NOT** be accepted.

When rejecting a timestamp, the mint **SHOULD** indicate whether it was missing, invalid, or outside the accepted window in its error response. A wallet retrying after the window has elapsed **MUST** use a fresh timestamp and regenerate every signature. If its clock is outside the accepted window, the wallet needs to correct its clock before retrying.

### Replay protection limits

Signing the timestamp prevents an observer from refreshing a captured request without the corresponding private keys. The time check bounds replay but does not prevent it within the accepted window; a request can be accepted while the mint's time is between `timestamp - 300` and `timestamp + 300`, inclusive. This scheme does not require a challenge endpoint or the mint to store used nonces.

An observer who captures a valid request can discover matching quotes during that window. Expiration prevents further discovery using that request, but does not revoke access to quote IDs already disclosed: those IDs may still be queried through the ordinary quote status endpoint. Lookup signatures do not authorize minting; minting a locked quote still requires the separate [NUT-20][20] signature.

## Response

The mint responds with a `PostMintQuotesByPubkeyResponse`:

```json
{
  "quotes": <Array[MintQuoteResponse]>,
  "next_cursor": <str|null>
}
```

Where `MintQuoteResponse` is the quote response type defined in [NUT-04][04].

### Pagination

The mint **MUST** return at most the effective page size of quotes. Every returned quote **MUST** match the requested payment method and one of the authenticated public keys. Quotes in every payment and issuance state are eligible; expiry alone **MUST NOT** exclude a matching quote.

`next_cursor` is required. The mint **MUST** return a non-empty continuation value when more matching quotes remain after the returned page, or `null` when the scan has reached its end. The mint **MUST NOT** silently truncate results without providing a continuation value. An empty result **MUST** have `next_cursor: null`.

To continue, the wallet sends another request to the same endpoint with the same set of public keys and `cursor` set to the previous `next_cursor`. It **MAY** change `limit` between pages. The wallet **MUST** continue until `next_cursor` is `null`, even if a page contains fewer quotes than requested.

The mint **MUST** bind a cursor to the payment method and set of public keys for which it was issued, and reject invalid, expired, or mismatched cursors with an error. It **MUST NOT** treat such a cursor as an empty result or silently restart the scan. Cursor format, encoding, and storage are implementation details.

Every page request **MUST** pass the same timestamp and signature validation as the initial request. A cursor does not authorize access to quotes. Wallets **MAY** use a fresh timestamp and signatures with an existing cursor; the mint **MUST NOT** require subsequent pages to reuse the initial timestamp or signatures.

The mint **MUST** traverse matching quotes in a stable, unique order based on their immutable quote IDs. Changes to payment or issuance state **MUST NOT** change a quote's position in the scan. For an unchanged set of matching quotes, following the continuation values to completion **MUST** return every quote exactly once. Retrying a page can return quotes the wallet has already seen; wallets **SHOULD** deduplicate by quote ID and apply the `updated_at` rules from [NUT-04][04].

Pagination does not provide a snapshot. Quotes added during a scan may appear in that scan or fall before its current position and be absent from it. Wallets **MUST** start a new scan to reliably discover additions after a previous scan; a cursor is not a permanent synchronization checkpoint. If a cursor expires, a wallet **MAY** restart from the first page and deduplicate quotes already received.

## Settings

The settings for this NUT are part of the mint info response ([NUT-06][06]):

```json
{
  "XX": {
    "supported": <bool>,
    "max_pubkeys": <int>,
    "max_page_size": <int>
  }
}
```

When `supported` is `true`, both limits are required positive integers:

- `max_pubkeys` is the maximum number of public keys accepted in one request.
- `max_page_size` is the maximum number of quotes returned in one response, across all requested public keys. It is also the default when `limit` is omitted.

Mints **MUST** enforce both limits. Operators **MAY** configure their values according to available resources. These limits bound individual requests and responses; they **MUST NOT** impose a maximum total number of quotes recoverable through pagination.

[04]: 04.md
[06]: 06.md
[20]: 20.md
[errors]: error_codes.md
