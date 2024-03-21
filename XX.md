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
        ["check_quote"]
      ],
    }
}
```

This example shows a Mint signaling support of WebSocket only for `check_quote`

## Specifications

All requests sent from apps to mints over Websocket MUST look like this

```json
["REQ", "<REQ ID>", "<COMMAND>", "<PARAMS>"]
```

All responses / messages sent from mints to apps MUST look like this

```json
["RES", "<REQ ID>", "<DATA>"]
```

`PARAMS` and `DATA` for each NUT are defined below.

### Commands

#### check_quote

Can be used to check the current state of a mint quote.
Mints SHOULD send an updated `DATA` object when the payment status changes.

PARAMS

```json
{
quote_id: <quote_id>,
}
```

DATA

```json
{
  "quote": "<quote id>",
  "request": "<payment request>",
  "paid": "<bool>",
  "expiry": "<unix timestamp>"
}
```

##### EXAMPLE

Client:

```json
[
  "REQ",
  "673b02c512dda11b44fb3f23e7c58930",
  "check_quote",
  { "quote_id": "d8195234c8ac8c129611d40f2144688d" }
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
