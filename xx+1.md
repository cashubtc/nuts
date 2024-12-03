# NUT-XX: Blind Authentication

`optional`

`depends on: NUT-XX`

---

This NUT defines a blind authentication scheme that allows mint operators to limit the use of their mint to a set of authorized users while still providing privacy within that anonymity set.

We use two authentication schemes in conjunction: _clear authentication_ using an external OpenID Connect / OAuth 2.0 service (described in [NUT-XX][XX]), and _blind authentication_ with the mint to access its resources. A user's wallet first needs to obtain a clear authentication token (CAT) from an OpenID Connect authority that the mint selected, which is not subject of this specification. Once the user has obtained the CAT from the OpenID Connect service, they can use it to obtain multiple blind authentication tokens (BAT) from the mint. We describe this process in this document.

Blind authentication tokens (BATs) are used to access the protected endpoints of the mint and make sure that only users that previously presented a valid CAT can access the mint's features such as minting, melting, or swapping ecash. Wallets provide a BAT in the request header when making a request to one of the mint's protected endpoints. The mint parses the header for a BAT, verifies the signature (like with normal ecash as described in [NUT-00][00]), checks if the token has previously been spent, and if not, adds it to its spent BAT token database.

## Blind authentication tokens are ecash

Blind authentication tokens (BATs) are essentially the same as normal ecash tokens and are minted in the same way. They are signed with a special keyset of the mint that has the unit `auth` and a single amount `1`.

BATs can only be used a single time for each request that the wallet makes to the mint's protected endpoints. After each for each successful request, the BAT is added to the mint's spent token list after which they are regarded as spent. The BAT is not marked as spent if the request results in an error.

To summarize:

- Wallet connects to mint and user is prompted to register or log in with an OAuth 2.0 service
- Upon login, wallet receives a clear authentication (CAT) token that identifies the user
- CAT is used to obtain blind authentication tokens (BAT) from the mint
- BATs are used to access the mint

The diagram below illustrates the protocol flow.

```

┌──────────────────────────────────────────────────────────────────────────┐
│ ┌────────┐                     ┌────────┐                  ┌───────────┐ │
│ │  User  │                     │  Mint  │                  │   OpenID  │ │
├─┴────────┘─────────────────────└────────┴──────────────────└───────────┴─┤
│                                                                          │
│                           1. Clear authentication                        │
│                           =======================                        │
│                                                                          │
│                                       Mint registers OpenID service      │
│                                     ◄───────────────────────────────     │
│                                                                          │
│           Wallet GET /v1/info                                            │
│    ─────────────────────────────────►                                    │
│                                                                          │
│                                OpenID login                              │
│    ────────────────────────────────────────────────────────────────►     │
│                                                                          │
│                              Respond with CAT                            │
│    ◄────────────────────────────────────────────────────────────────     │
│                                                                          │
│                           2. Blind authentication                        │
│                           =======================                        │
│                                                                          │
│           Request BAT using CAT                                          │
│    ─────────────────────────────────►                                    │
│                                                                          │
│                Return BAT                                                │
│    ◄─────────────────────────────────                                    │
│                                                                          │
│           Use BAT to access mint                                         │
│    ─────────────────────────────────►                                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

```

The steps for `1. Clear authentication` are described in [NUT-XX][XX], whereas the steps in `2. Blind authentication` are subject of this document.

## Endpoints

The mint offers new endpoints that behave similarly to the endpoints for getting the keys, keysets, and minting tokens with normal ecash ([NUT-01][01], [NUT-02][02], [NUT-04][04]). These endpoints start with a prefix `/v1/auth/` to differentiate them from the normal endpoints of the mint. Using these endpoints, wallets can mint blind authentication tokens (BATs) and use them later when accessing the protected endpoints of the mint. Note that BATs cannot be swapped against other BATs.

### Keys

Like in [NUT-01][01] and [NUT-02][02], the mint responds with its BAT keyset for the following request:

```
GET /v1/auth/blind/keys
```

or

```
GET /v1/auth/blind/keys/{keyset_id}
```

where the mint returns a `GetKeysResponse`:

```json
{
  "keysets": [
    {
      "id": "000e479673849bf6",
      "unit": "auth",
      "keys": {
        "1": "024ec000e31e230e4c59760def29601557c0b1650617dc8f38d3b2cfd21ad0351b"
      }
    }
  ]
}
```

Notice that the unit is `auth` and only a single amount of `1` is supported.

### Keysets

Like in [NUT-02][02] the mint also offers the endpoints returning the keysets:

```
GET v1/auth/blind/keysets
```

The mint returns the same `GetKeysetsResponse` response types as described in [NUT-02][02].

## Minting blind authentication tokens

To mint blind authentication tokens (BATs), the wallet makes a request to the following endpoint:

```http
POST /v1/auth/blind/mint
```

To access this endpoint the wallet MUST provide a valid CAT (obtained via [NUT-XX][XX]) in its request header, IF this endpoint is marked as protected in the info response of the mint as per [NUT-XX][XX].

```
Clear-auth: <CAT>
```

Like in [NUT-04][04], the wallet includes a `PostAuthBlindMintRequest` in the request body:

```json
{
  "outputs": <Array[BlindedMessage]>
}
```

where `outputs` are `BlindedMessages` (see [NUT-00][00]) from the blind auth keyset of the mint with a unit `amount`. The sum of all amounts of the outputs cannot exceed the maximum allowed amount of BATs as specified in `bat_max_mint` in the mint's `MintBlindAuthSetting` (see **TODO: Add ref**)

Notice that in contrast to [NUT-04][04], we did not create a quote and did not include it in this request. Instead, we directly minted the maximum allowed amount of BATs.

The mint responds with a `PostAuthBlindMintResponse`:

```json
{
  "signatures": <Array[BlindSignature]>
}
```

The wallet un-blinds the response to obtain the signatures `C` as described in [NUT-00][00]. It then stores the resulting `AuthProofs` in its database:

```json
{
  "id": hex_str,
  "secret": str,
  "C": hex_str
}
```

## Using blind authentication tokens

The wallet checks the `MintBlindAuthSetting` of the mint to determine which endpoints require blind authentication. Similar to `NUT-XX`, the wallet performs a match on the `protected_endpoints` in the `MintBlindAuthSetting` before attempting a request to one of the mint's endpoints. If the match is positive, the wallet needs to add a blind authentication token (BAT) to the request header.

### Serialization

To add a blind authentication token (BAT) to the request header, we need to serialize a single `AuthProof` JSON in base64 with the prefix `authA`:

```sh
authA[base64_authproof_json]
```

This string is a BAT.

### Request header

We add this serialized BAT to the request header:

```
Blind-auth: <BAT>
```

and make the request as we usually would.

`AuthProofs` are single-use. The wallet MUST delete the `AuthProof` after a successful request, and SHOULD delete it even if request results in an error. If the wallet runs out of `AuthProofs`, it can [mint new ones](#minting-blind-authentication-tokens) using its clear authentication token (CAT).

## Mint

### Signaling protected endpoints and settings

The mint lists each protected endpoint that requires a blind authentication token (BAT) in the `MintBlindAuthSetting` in its [NUT-06][06] info response:

```json
"XX+1" : {
  "bat_max_mint": 50,
  "protected_endpoints": [
    {
      "method": "GET",
      "path": "^/v1/mint/.*"
    },
    {
      "method": "POST",
      "path": "^/v1/mint/.*"
    }
  ]
}
```

`bat_max_mint` is the number of blind authentication tokens (BATs) that can be minted in a single request using the `POST /v1/auth/blind/mint` endpoint.

`protected_endpoints` contains the endpoints that are protected by blind authentication. `method` denotes the HTTP method of the endpoint, and `path` is a regex pattern that must match the path of the URL. In this example, all `/v1/mint/*` endpoints are protected and require blind authentication.

## Errors (TODO)

**TODO: define error codes**

[00]: 00.md
[01]: 01.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[XX]: xx.md
