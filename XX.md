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

An app can close an active subscription by posting the following messages.
Once a mint receives a `CLOSE` message it SHOULD assume the app is no longer listening on this `REQ ID`
and should no longer send updates. **This does not mean it should close the socket**

```json
["CLOSE", "<REQ ID>"]
```

All responses sent from mints to apps MUST look like this

```json
["RES", "<REQ ID>", "<DATA>"]
```

A mint can send error messages or other data by sending a message that looks like this

```json
["NOTICE", "<MESSAGE>"]
```

`PARAMS` and `DATA` for each NUT are defined below. `REQ ID` SHOULD be a random string that is unique per subscription.

### Commands

#### check_quote

Can be used to check the current state of a mint quote.
Mints SHOULD send an updated `DATA` object when the payment status changes.

PARAMS

```json
{
"ids": ["<quote_id>", ...],
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

#### check_proof

Can be used to check the current state of a proof.
Mints SHOULD send an updated `DATA` object when the proof's status changes.

PARAMS

```json
{
"points": ["<hex_str>", ...],
}
```

DATA

```json
{
  "Y": "<hex_str>",
  "state": "<str_enum[STATE]>",
  "witness": "<str|null>"
}
```

##### EXAMPLE

Client:

```json
[
  "REQ",
  "e1699f8e006c264d",
  "check_proof",
  {
    "points": [
      "02599b9ea0a1ad4143706c2a5a4a568ce442dd4313e1cf1f7f0b58a317c1a355ee"
    ]
  }
]
```

Mint:

```json
[
  "RES",
  "e1699f8e006c264d",
  {
    "Y": "02599b9ea0a1ad4143706c2a5a4a568ce442dd4313e1cf1f7f0b58a317c1a355ee",
    "state": "SPENT",
    "witness": "{\"signatures\": [\"b2cf120a49cb1ac3cb32e1bf5ccb6425e0a8372affdc1d41912ca35c13908062f269c0caa53607d4e1ac4c8563246c4c8a869e6ee124ea826fd4746f3515dc1e\"]}"
  }
]
```
