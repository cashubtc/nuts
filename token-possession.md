# NUT: Token Possession Proof

`optional`

`depends on: NUT-00, NUT-06`

---

This NUT defines a mechanism for mints to restrict access to specific endpoints based on **possession** of Cashu tokens from a designated keyset. It can be seen as a generalization of [NUT-22][22]: where NUT-22 uses a dedicated `auth` keyset and single-use BATs, this NUT allows any keyset's proofs to serve as reusable bearer authorization with a minimum amount requirement.

It is distinct from [NUT-22][22] and [NUT-24][24]:

- [NUT-22][22] answers _"are you an authorized user?"_ — identity, via CAT → BAT
- [NUT-24][24] answers _"will you pay?"_ — tokens are spent as payment
- This NUT answers _"do you hold tokens from keyset X with at least amount Y?"_ — possession, without spending

Proofs presented for possession verification are **not spent**. They remain valid for future use (swaps, redemptions, or further possession proofs) until the holder explicitly spends them through a normal operation.

Caution: This mechanism is only safe when the verifier is the mint itself. See [Security Considerations](#security-considerations).

## Overview

```
Client  ───GET /v1/protected/resource──►  Mint
        ◄──401 + keyset_id + min_amount─
        ───GET + Cashu-Authorization ──►  (verify proofs, do NOT spend)
        ◄──200 + response body ────────
```

1. Client requests a protected endpoint
2. Mint responds with `401`, the required `keyset_id`, and `min_amount`
3. Client retries with proofs from that keyset in the `Cashu-Authorization` header
4. Mint verifies proofs (signature, spent status, amount) and returns the response

If the client already knows the required `keyset_id` and `min_amount` (e.g., from a previous 401 or application logic), it MAY include the `Cashu-Authorization` header on the initial request to skip the 401 round trip.

## Signaling Protected Endpoints

Mints declare token-possession-protected endpoint patterns in their [NUT-06][06] info response. This tells wallets which endpoints may require token possession, so they can prepare or inform the user.

The `protected_endpoints` list signals which paths are protected, but the **specific** `keyset_id` and `min_amount` are communicated per-request in the [401 response](#401-response). This is necessary because the required keyset may depend on the requested resource (e.g., a different keyset per market or per condition).

## 401 Response

When a client requests a protected endpoint without a valid `Cashu-Authorization` header, the mint responds:

```
HTTP/1.1 401 Unauthorized
Content-Type: application/json
```

Response body:

```json
{
  "detail": "Token possession required",
  "code": 32001,
  "keyset_id": <hex_str>,
  "min_amount": <int>
}
```

- `keyset_id`: The keyset ID from which the client must present proofs
- `min_amount`: Minimum total amount across all presented proofs (default `1` if omitted)

## Client Request

The client includes proofs from the required keyset in the request header:

```
Cashu-Authorization: <base64_proofs_json>
```

Where `<base64_proofs_json>` is the base64 encoding of a JSON array of `Proof` objects ([NUT-00][00]):

```json
[
  {
    "id": <hex_str>,
    "amount": <int>,
    "secret": <str>,
    "C": <hex_str>
  }
]
```

Multiple proofs MAY be included to meet the `min_amount` requirement. For example, if `min_amount` is `100` and the client holds proofs of amounts `64` and `32` and `4`, they include all three (total: `100`).

> [!CAUTION]
>
> The `dleq` field MUST NOT be included in proofs sent in the header. Including DLEQ proofs would allow the mint to correlate the proof back to the blinding session in which it was minted, breaking the unlinkability between minting and usage. This is the same privacy rationale as [NUT-22][22].

## Mint Verification

When the mint receives a request with a `Cashu-Authorization` header on a protected endpoint:

1. Decode the proofs array from the base64 header value
2. Verify all `proof.id` fields match the required `keyset_id` for this endpoint (error 32002)
3. Verify each proof's signature `C` against the keyset's public keys ([NUT-00][00]) (error 32002)
4. Verify no proof secret is in the spent set (error 32002)
5. Verify `sum(proof.amount) >= min_amount` (error 32002)
6. If all checks pass, process the request and return the response

**Proofs are NOT marked as spent.** The same proofs can be reused across multiple requests. A proof becomes invalid for possession verification only when it is spent through a normal operation ([NUT-03][03] swap, redemption, etc.).

This non-destructive verification is safe because the verifier is the mint itself — it has authoritative, real-time access to the spent set without needing to mutate it.

## Security Considerations

- **Mint-only verification**: This mechanism relies on the mint checking its own spent set without marking proofs as spent. An external server cannot safely perform this check — it has no way to verify spent status. For external server payment gating, use [NUT-24][24] instead.
- **Request linkability**: Reusing the same proofs across requests allows the mint to link those requests. For privacy, clients SHOULD periodically rotate proofs via [NUT-03][03] swap.
- **Natural revocation**: When proofs are spent (via swap, redemption, etc.), they immediately become invalid for possession verification. Transferring tokens naturally revokes access from the previous holder.
- **Transport security**: Proofs in headers MUST be protected by TLS. An intercepted proof grants access to the protected resource until the proof is spent.
- **Proof sharing**: A holder can share proofs to grant another party access. The original holder can revoke this by swapping their tokens, which moves the old secrets to the spent set.

## Error Codes

| Code  | Description                          |
| ----- | ------------------------------------ |
| 32001 | Token possession required            |
| 32002 | Token possession verification failed |

## Mint Info Setting

The [NUT-06][06] info response:

```json
{
  "token-possession": {
    "supported": true,
    "protected_endpoints": [
      {
        "method": <str>,
        "path": <str>
      }
    ]
  }
}
```

- `supported`: Boolean indicating token possession proof support
- `protected_endpoints`: Endpoint patterns that require token possession. `method` is the HTTP method, `path` uses the same matching rules as [NUT-22][22]: exact match (no trailing `*`) or prefix match (trailing `*`). Paths MAY contain dynamic segments (e.g., `/v1/resources/*/details`).

[00]: 00.md
[03]: 03.md
[06]: 06.md
[22]: 22.md
[24]: 24.md
