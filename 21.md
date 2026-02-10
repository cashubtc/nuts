# NUT-21: Clear Authentication

`optional`

`used in: NUT-22`

---

This NUT defines a clear authentication scheme that allows operators to limit the use of their mint to registered users using the OAuth 2.0 and OpenID Connect protocols. The mint operator can protect chosen endpoints from access by requiring user authentication. Only users that provide a clear authentication token (CAT) from the specified OpenID Connect (OIDC) service can use the protected endpoints. The CAT is an Oauth 2.0 Access token (also known as the `access_token`) commonly in the form of a JWT that contains user information, a signature from the OIDC service, and an expiry time. To access protected endpoints, the wallet includes the CAT in the HTTP request header.

**Note:** The primary purpose of this NUT is to restrict access to a mint by allowing registered users to obtain Blind Authentication Tokens as specified in [NUT-22][22].

**Warning:** This authentication scheme breaks the user's privacy as the CAT contains user information. Mint operators SHOULD require clear authentication **only on selected endpoints**, such as those for obtaining blind authentication tokens (BATs, see [NUT-22][22]).

## OpenID Connect service configuration

The OpenID Connect (OIDC) service is typically run by the mint operator (but it does not have to be). The OIDC service must be configured to meet the following criteria:

- **No client secret:** The OIDC service MUST NOT use a client secret.
- **Authorization code flow:** The OIDC service MUST enable the _authorization code flow_ with PKCE for public clients, so that an authorization code can be exchanged for an access token and a refresh token.
- **Signature algorithm:** The OIDC service MUST support at least one of the two asymmetric JWS signature algorithms for access token and ID token signatures: `ES256` and `RS256`.
- **Wallet redirect URLs:** To support the OpenID Connect Authorization Code flow, the OIDC service MUST allow redirect URLs that correspond to the wallets it wants to support. You can find a list of common redirect URLs for well-known Cashu wallets [here][21-SUPPL].
- **Localhost redirect URL:** The OIDC service MUST also allow redirects to the URL `http://localhost:33388/callback`.
- **Authentication flows:** Although, strictly speaking, this NUT does not restrict the OpenID Connect grant types that can be used to obtain a CAT, it is recommended to enable at least the `authorization_code` (Authorization Code) flow and the `urn:ietf:params:oauth:grant-type:device_code` (Device Code) flow in the `grant_types_supported` field of the `openid_discovery` configuration. The `password` (Resource Owner Password Credentials, ROPC) flow SHOULD NOT be used as it requires handling the user's credentials in the wallet application.

## Mint

### Signalling protected endpoints

The mint lists each protected endpoint that requires a clear authentication token (CAT) in the `MintClearAuthSetting` in its [NUT-06][06] info response:

```json
"21" : {
  "openid_discovery": "https://mint.com:8080/realms/nutshell/.well-known/openid-configuration",
  "client_id": "cashu-client",
  "protected_endpoints": [
    {
        "method": "POST",
        "path": "/v1/auth/blind/mint"
    }
  ]
}
```

`openid_discovery` is the OpenID Connect Discovery endpoint which has all the information necessary for a client to authenticate with the service.

`client_id` is the OpenID Connect Client ID that the wallet needs to use to authenticate.

`protected_endpoints` is an array of objects that specify each endpoint that requires a CAT in the request headers. `method` is the HTTP method, and `path` is either:

1. **Exact match**: no trailing `*` → request path MUST equal `path`
2. **Prefix match**: ends with `*` → request path MUST start with the prefix (`*` removed)

The `*` wildcard, if present, MUST be the final character only.

For example:

- `/v1/*` matches any path starting `/v1/` (all endpoints)
- `/v1/auth/*` matches any path that starts with `/v1/auth/` (all auth endpoints)
- `/v1/mint/*` matches any path that starts with `/v1/mint/` (all minting endpoints)
- `/v1/mint/bolt*` matches any path starting `/v1/mint/bolt` (bolt11/12 minting endpoints)

In the example above, the `/v1/auth/blind/mint` path is the **exact match** [NUT-22][22] endpoint for obtaining blind authentication tokens (BATs).

> [!CAUTION]
> Wallets **MUST** treat mint provided `path` values as untrusted input and use exact or prefix matching only. Never use regex matching on untrusted input.

### Clear authentication token verification

When receiving a request to a protected endpoint, the mint checks the included CAT (which is a JWT) in the HTTP request header (see below in section [Wallet](#cat-in-request-header)) and verifies the JWT. To verify the JWT, the mint checks the signature of the OIDC and the expiry of the JWT.

The JWT includes a `sub` field which identifies a specific user. The `sub` identifier can, for example, be used to rate limit the user.

**Note:** The JWT _MAY_ include an _audience_ field called `aud` that contains the mint's public key

More on OpenID Connect ID token validation [here](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation).

## Wallet

To make a request to one of the `protected_endpoints` of the mint, the wallet needs to obtain a valid clear auth token (CAT) from the OIDC service. The wallet uses the `openid_discovery` URL in the `MintClearAuthSetting` from the info endpoint of the mint to authenticate with the OIDC service and obtain a CAT.

### Obtaining a CAT

Depending on the wallet implementation and use case, an appropriate authorization flow should be used. For mobile wallets, the Authorization Code is recommended. For command-line wallets, the Device Code flow is recommended. For headless wallets, the ROPC flow may be used.

It is recommended to use language-specific libraries that can handle OpenID Connect authentication on behalf of the user. The wallet should be able to handle and store access tokens and refresh tokens for each mint that it authenticates with. If the wallet connects to a mint for the first time, or if the refresh token is about to expire, the wallet should allow the user to log in again to obtain a new access token (`access_token`) and a new refresh token (`refresh_token`).

The `access_token` is what is referred to as a clear authentication token (CAT) throughout this document.

### CAT in request header

When making a request to the mint's endpoint, the wallet matches the requested URL with the `protected_endpoints` from the `MintClearAuthSetting` (either exact match or prefix pattern match). If the match is positive, the mint requires the wallet to provide a CAT with the request.

After obtaining a CAT from the OIDC service, the wallet includes a valid CAT in the HTTP request header when it makes requests to one of the mint's `protected_endpoints`:

```
Clear-auth: <CAT>
```

The `CAT` is a JWT (or `access_token`) encoded with base64 that is signed by and obtained from the OIDC authority. The mint verifies the JWT as described [above](#clear-authentication-token-verification).

## Error codes

See [Error Codes][errors]:

- `30001`: Endpoint requires clear auth
- `30002`: Clear authentication failed

[06]: 06.md
[21-SUPPL]: suppl/21.md
[22]: 22.md
[errors]: error_codes.md
