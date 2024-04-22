# NUT-XX: WebSockets

`optional`

---

This NUT defines a optional, WebSocket-based communication layer that enables bidirectional
communication between apps and mints.

## Signaling Support via NUT-06

NUT-XX is optional. Mints can signal support via NUT-06 and it's `/info` endpoint.
Furthermore mints might choose to support only certain commands.
The `nuts` key of `GetInfoResponse` for NUT-XX looks as follows:

```json
"nuts": {
    "xx": {
      "supported": [
        ["bolt11_mint_quote", "bolt11_melt_quote"]
      ],
    }
}
```

This example shows a Mint signaling support of WebSocket only for `check_quote`

## Specifications

`NUT-XX` uses the JSON-RPC format for all messages. There are three types
of messages defined in this NUT.

### Requests

Requests are sent from apps to mints. Mints SHOULD not send requests.
A request is sent for requesting a certain subscription. The format is as follows:

```json
{ "jsonrpc": "2.0", "method": "sub | unsub", "params": "...", "id": 1 }
```

Where `params` are specific to what kind of subscription is requested, but
always includes a `subId` to identify this subscription.
This identifier is unrelated to `id`.

As per JSON-RPC spec `id` is defined as:

> An identifier established by the Client that MUST contain a String, Number,
> or NULL value if included. If it is not included it is assumed to be a notification.
> The value SHOULD normally not be Null and Numbers SHOULD NOT contain
> fractional parts.

### Responses

Responses are sent by Mints in response (and SHOULD only be send in response) to
a request. Responses do not contain any data that has been subscribed to,
but information about the subscription.

A result can have two different formats:

Success:

```json
{ "jsonrpc": "2.0", "result": { "status": "OK", "subId": "..." }, "id": 1 }
```

Error:

```json
{
  "jsonrpc": "2.0",
  "error": { "code": -32601, "message": "Human readable error message" },
  "id": "1"
}
```

Example: If a mint accepts a subscription requests it send back a result
`{"status":"OK", "subId": "..."}` to signal that the subscription has been
accepted.

### Notifications

Notifcations are sent by the mint and contain subscription data. They
have the following format:

```json
{"jsonrpc": "2.0", "method": "sub", "params": ...}
```

Again `params` will be specific to the kind of subscription but always contain
`subId`.

## Flow

1. Clients sends a `Request` specifying the subscription parameters as well as it's
   `subId`. The request has a `method` of `sub`.
2. Mint checks the requests and sends a `Response` containing an ok or error.
3. If the `Request` was accepted the mint sends updates via `Notifications` whenever
   an update is available. The mint does reference the `subId` in these messages.
4. Once the client has all the information they require from this subscription they
   send a second `Request`. This request has a method of `unsub`

### Commands

#### bolt11_mint_quote

Can be used to check the current state of a mint quote.
Mints SHOULD send a `Notification` when the quote status changes.

REQUEST PARAMS

```json
{
  "kind": "bolt11_mint_quote",
  "filters": ["<quoteId>", ...],
  "subId": "<subId>"
}
```

NOTIFICATION PARAMS

```json
{
  "subId": "<subId>",
  "payload": {}
}
```

##### EXAMPLE

Client:

```json
[
  "REQ",
  "673b02c512dda11b44fb3f23e7c58930",
  "check_quote",
  { "ids": ["d8195234c8ac8c129611d40f2144688d"] }
]
```

Mint:

```json
[
  "RES",
  "673b02c512dda11b44fb3f23e7c58930",
  {
    "quote_id": "d8195234c8ac8c129611d40f2144688d",
    "request": "lnbc1...",
    "paid": false,
    "expiry": 1711036570
  }
]
```
