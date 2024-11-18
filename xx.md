# NUT-XX: Clear Authentication

`optional`

`used in: NUT-XX+1`

---

This NUT defines a clear authentication scheme that allows mints operators to limit the use of their mint to certain users. The mint operator can protect endpoints from access by requiring the user to authenticate. Only users with a clear authentication token (CAT) from the specified OpenID Connect (OIDC) service can use the protected endpoints. The CAT is a JWT that contains user information, a signature from the OIDC service, and an expiry. To access protected endpoints, the wallet includes the CAT in the HTTP request header.

**Warning:** This authentication scheme breaks the user's privacy as the CAT contains user information. Mint operators should require clear authentication only on selected endpoints, such as those for obtaining blind authentication tokens (BATs, see [NUT-XX+1][XX+1]).

## OpenID Connect service configuration
The OpenID Connect (OIDC) service is typically run by the mint operator (but it does not have to). The OIDC service must be configured to meet the following criteria:  
- **Client ID:** The OIDC service MUST enable the client ID `cashu-client` which is used by all authenticating wallets. 
- **Signature algorithm:** The OIDC server MUST use `ES256` as the Access token signature algorithm and the ID token signature algorithm. **(#TODO: should we drop this?)**
- **Wallet redirect URLs:** To support the standard OpenID Connect redirect based authentication with authorization code, the OIDC service MUST allow redirect URLs that correspond to the wallets it wants to support. You can find a list of common redirect URLs for well-known Cashu wallets **here TODO: Link**. 
- **Localhost redirect URL:** The OICD service MUST also allow redirects to any port on localhost via the URL `http://localhost:*`. If a wildcard for the port is not possible, the URL `http://localhost:33388` should be used.

## Mint

A mint that requires clear authentication for access to some endpoints announces the following `MintClearAuthSetting` in its [NUT-06][06] info response:

```json
"XX" : {
  "openid_discovery": "https://mint.com:8080/realms/nutshell/.well-known/openid-configuration",
  "protected_endpoints": [
    {
        "method": "POST",
        "path": "/v1/auth/blind/mint"
    }
  ]
}
```
`openid_discovery` is the OpenID Connect Discovery endpoint which has all the information necessary for a client to authenticate with the service. `protected_endpoints` is an array of objects that specify each endpoint that requires a CAT in the request headers. `method` is the HTTP method and `path` the path for the endpoint that is protected.

In this example, the entry in `protected_endpoints` is the [NUT-XX+1][xx+1] endpoint for obtaining blind authentication tokens (BATs).

When receiving a request to a protected endpoint, the mint checks the included CAT (which is a JWT) in the HTTP request header (see below) and verifies the JWT. To verify the JWT, the mint checks the signature of the OIDC and the expiry of the JWT. The JWT includes a `sub` field which identifies a specific user. The `sub` identification can, for example, be used to rate limit the user. The mint does not verify the *audience*. More on OpenID Connect ID token validation [here](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation).

## Wallet
To make a request to the mint to an endpoint that is protected via clear authentication, the wallet includes the clear auth token (CAT) in the HTTP request header:

```
Authorization: Bearer <clear_auth_token>
```

The `clear_auth_token` is a JWT that is signed by the OIDC authority. The mint verifies the JWT as described above.

### Getting a clear authentication token

To get a CAT, the wallet needs to enable the user to either create a new account with the OpenID Connect (OIDC) service if the user has never used this mint before, or to log in to the OIDC service using a login page or using username and password 

[06]: 06.md
[XX+1]: xx+1.md