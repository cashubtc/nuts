# NUT-XX: Blind Authentication

`optional`

`depends on: NUT-XX`

---

This NUT defines a blind authentication scheme that allows mints operators to limit the use of their mint to a set of authorized users while still providing privacy within that anonymity set. 

We use two authentication schemes in conjunction: *clear authentication* using an external OpenID Connect / OAuth 2.0 service, and *blind authentication* with the mint to access its resources. A user's wallet first needs to obtain a clear authentication token (CAT) from an OpenID Connect authority that the mint selected. This is typically done with a username and password but any other OpenID Connect authentication can be used and is not subject of this specification. Once the user has obtained the clear authentication token from the OpenID Connect service, they can use it to obtain blind authentication tokens (BAT) from the mint. The blind authentication tokens are used to access the protected endpoints of the mint, making sure that only registered users can access the mint. 

To summarize:
- Wallet connects to mint and user is prompted to register or login with an OAuth 2.0 service
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

## Obtaining clear authentication token
[NUT-XX][XX] specifies how the users's wallet obtains a clear authentication token (CAT) that identifies the user. The `MintClearAuthSetting` of NUT-XX MUST list the endpoint that is used to obtain blind authentication tokens in its `protected_endpoints`:

```json
"protected_endpoints": [
  {
      "method": "POST",
      "path": "/v1/auth/blind/mint"
  },
  {
      "method": "GET",
      "path": "^/v1/mint/quote/bolt11/.*"
  },
]
```
`method` denotes the HTTP method of the endpoint, and `path` is a regex pattern that must match the path of the URL.

In this example, the filters above will match for `POST /v1/auth/blind/mint` requests, and for `GET /v1/mint/quote/bolt11/<quote_id>`.

## Obtaining blind authentication tokens
```json
"XX+1" : {
  "max_mint": 50,
  "protected_endpoints": [
    {
      "method": "POST",
      "path": "/v1/swap"
    },
    {
      "method": "GET",
      "path": "^/v1/mint/quote/bolt11/.*"
    },
    {
      "method": "POST",
      "path": "/v1/mint/quote/bolt11"
    },
    {
      "method": "POST",
      "path": "/v1/mint/bolt11"
    },
    {
      "method": "GET",
      "path": "^/v1/melt/quote/bolt11/.*"
    },
    {
      "method": "POST",
      "path": "/v1/melt/quote/bolt11"
    },
    {
      "method": "POST",
      "path": "/v1/melt/bolt11"
    }
  ]
}
```

## Notes
- Blind auth tokens are invalidated by the mint before the request is processed (also for failed or errored request)
- Blind auth keysets have only one value, the price for accessing an endpoint is 1 AUTH

[XX]: xx.md