# NUT-XX: Payment Requests

`optional`

---

This NUT introduces a standardised format for payment requests, that supply a sending wallet with all information necessary to complete the transaction. This enables many use-cases where a transaction is better initiated by the receiver (e.g. point of sale).

## Flow

1. Receiver creates a payment request, encodes it and displays it to the sender
2. Sender scans the request and constructs a matching token
3. Sender sends the token according to the transport specified in the payment request
4. Receiver receives the token and finalises the transaction

## Payment Request

A Payment Request is defined as follows

```json
{
  "a": int <optional>,
  "u": str,
  "r": str <optional>,
  "d": str <optional>,
  "m": str <optional>,
  "l": str <optional>,
  "t": Transport
}
```

while Transport is defined as

- a: The amount of the requested token (payment amount)
- u: The unit of the requested token (e.g. sats)
- r: The mint to use to mint the token
- d: A human readable description that the sending wallet will display after scanning the request
- m: The memo of the requested token (can be used for accounting purposes)
- l: The lock script of the requested token
- t: The method of transport chosen to transmit the created token to the sender (can be multiple, sorted by preference)

The sending wallet MUST honor all parts of a payment request that are specified

## Transport

Transport is an important part of Cashu Payment Requests. Receivers can choose what kind of transport they want to support and where they want to receive the token. By making this clear in the payment requests, wallets can handle payment requests accordingly (or decline them if they do not support the transport layer). A transport consists of a type and a target.

```json
{
  "t": str,
  "ta": Target
}
```

- t: type of Transport
  - ta: target of Transport

There can be many transport layers, but here are some recommendations:

- nostr
  - type: "nostr"
  - target: `{nprofile: "nprofile..."}`
- post
  - type: "post"
  - target: `{url: "<endpoint url>"}`
- email
  - type: "email"
  - target: `{email: "<email adddress>"}`
- sms
  - type: "sms"
  - target: `{num: "phone number"}`

## Encoded Request

Cashu Payment Requests can be encoded and displayed/sent as string or qr code. They underlying object is serialised using CBOR and finally base64 encoded and prefixed with a version byte and standard prefix.

_Example_

```sh
cashrqAaVhQRVhVWNzYXRhTXgiaHR0cHM6Ly9taW50Lm1pbmliaXRzLmNhc2gvQml0Y29pbmFEeCNQbGVzYXNlIHBheSB0aGUgdmVyeSBmaXJzdCBjYXNodSBwcmFUgaJhVGVub3N0cmJUYXhGbnByb2ZpbGUxcXFzZG11cDZlMno2bWNwZXVlNno2a2wwOGhlNDloY2VuNXhucmMzdG5wdncwbWRndGplbWgwc3V4YTBrag
```
