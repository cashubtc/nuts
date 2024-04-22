# NUT-XX: WebSockets

`optional`

---

This NUT defines a optional, WebSocket-based communication layer that enables bidirectional
communication between apps and mints.

## Flow

1. Clients sends a `Request` specifying the subscription parameters as well as it's
   `subId`. The request has a `method` of `sub`.
2. Mint checks the requests and sends a `Response` containing an ok or error.
3. If the `Request` was accepted the mint sends updates via `Notifications` whenever
   an update is available. The mint does reference the `subId` in these messages.
4. Once the client has all the information they require from this subscription they
   send a second `Request`. This request has a method of `unsub`

## Specifications

`NUT-XX` uses the JSON-RPC format for all messages. There are three types
of messages defined in this NUT.

### Requests

Requests are sent from apps to mints. Mints SHOULD not send requests.
A request is sent for requesting a certain subscription. The format is as follows:

```ts
{ "jsonrpc": "2.0", "method": RequestMethods, "params": RequestParams, "id": 1 }
```

Where `RequestMethods` and `RequestParams` are defined as follows:

```ts
enum RequestMethods {
  sub = "sub",
  unsub = "unsub",
}

type RequestParams = {
  kind: "bolt11_melt_quote" | "bolt11_mint_quote" | "proof_status";
  subId: string;
  filters: string[];
};
```

Please note that `id` and `subId` are unrelated.

As per JSON-RPC spec `id` is defined as:

> An identifier established by the Client that MUST contain a String, Number,
> or NULL value if included. If it is not included it is assumed to be a notification.
> The value SHOULD normally not be Null and Numbers SHOULD NOT contain
> fractional parts.

### Responses

Responses are sent by Mints in response (and SHOULD only be send in response) to
a request. Responses do not contain any data that has been subscribed to,
but information about the subscription.

A result has the following format:

```json
{ "jsonrpc": "2.0", "result": { "status": "OK", "subId": "..." }, "id": 1 }
```

As `Request` can potentially be invalid, mints can return an error at
this stage. Please refer to the error section below.

### Notifications

Notifcations are sent by the mint and contain subscription data. They
have the following format:

```ts
{"jsonrpc": "2.0", "method": "sub", "params": {"subId": "<subId>", "payload": NotificationPayload}}
```

Again `payload` will be specific to the kind of subscription

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

## Errors

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
