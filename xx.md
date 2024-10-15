# NUT-XX: Clear Authentication

`optional`

---

This NUT defines a clear authentication scheme that allows mints operators to limit the use of their mint to certain users. The mint operator can protect endpoints from access by requiring the user to authenticate. Only users with a clear authentication token (CAT) from the specified OpenID Connect (OIDC) service can use the protected endpoints. The CAT is a JWT that contains user information, a signature from the OIDC service, and an expiry. To access protected endpoints, the wallet includes the CAT in the HTTP request header.

**Warning:** This authentication scheme breaks the user's privacy as the CAT contains user information. Mint operators should require clear authentication only on selected endpoints, such as those for obtaining blind authentication tokens (see [NUT-XX+1][XX+1]).

## OpenID Connect service configuration
The OpenID Connect (OIDC) service can be run by the mint operator (but does not have to). The requirements for the OIDC service are relatively minimal. 
- The OIDC service MUST enable the client ID `cashu-client` which is used by all authenticating wallets. 
- The OIDC server MUST use `ES256` as the Access token signature algorithm and the ID token signature algorithm.
- To support the standard OpenID Connect redirect based authentication with authorization code, the OIDC service MUST allow redirect URLs that correspond to the wallets it wants to support. You can find a list of common redirect URLs for well-known Cashu wallets **here TODO: Link**.

## Mint

A mint that supports and requires clear authentication for access to some endpoints announces the following `MintClearAuthSetting` in its [NUT-06][06] info response.

```json
"XX" : {
  "openid_configuration": "https://mint.com:8080/realms/nutshell/.well-known/openid-configuration",
  "protected_endpoints": [
    {
        "method": "POST",
        "path": "/v1/auth/blind/mint"
    }
  ]
}
```
`openid_configuration` is the URL of the OpenID Connect configuration endpoint which has all the information necessary for a client to authenticate. `protected_endpoints` is an array of objects that specify each endpoint that requires a CAT in the request headers. `method` denominates the HTTP method and `path` the path for the endpoint that is protected.

When receiving a request to a protected endpoint, the mint checks the included CAT (which is a JWT) in the HTTP request header (see below) and verifies the JWT. To verify the JWT, the mint checks the signature of the OIDC and the expiry of the JWT. The JWT includes a `sub` field which identifies the user. The mint does not verify the *audience*. More on OpenID Connect ID token validation [here](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation).

## Wallet
To make a request to the mint to an endpoint that is protected via clear authentication, the wallet includes the clear auth token (CAT) in the HTTP request header:

```
Authorization: Bearer <clear_auth_token>
```

The `clear_auth_token` is a JWT that is signed by the OIDC authority. The mint verifies the JWT as described above.

[06]: 06.md
[XX+1]: xx+1.md