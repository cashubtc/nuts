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
  "i": str <optional>,
  "a": int <optional>,
  "u": str <optional>,
  "r": bool <optional>,
  "m": Array[str] <optional>,
  "d": str <optional>,
  "t": Transport
}
```

while Transport is defined as

- `i`: Payment id to be included in the payment payload
- `a`: The amount of the requested payment
- `u`: The unit of the requested payment (MUST be set if `a` is set)
- `s`: Whether the payment request is for single use
- `m`: A set of mints from which the payment is requested
- `d`: A human readable description that the sending wallet will display after scanning the request
- `t`: The method of transport chosen to transmit the payment (can be multiple, sorted by preference)

## Transport

Transport specifies methods for sending the ecash to the receiver. A transport consists of a type and a target.

```json
{
  "t": str,
  "a": str,
  "g": Array[Array[str, str]] <optional>
}
```

- t: type of Transport
- a: target of Transport
- g: optional tags for the Transport 

There are different transport layers:

- nostr
  - type: `nostr`
  - target: `<nprofile>`
  - tags: `[["1", "NIP-04"], ["2", "NIP-17"], ["3", "NIP-61"]]`
- post
  - type: `post`
  - target: `<endpoint url>`

## Payment payload

Regardless of the transport layer, the payload sent to the receiver is a JSON serialized object as follows:

```json
{
  "id": str <optional>,
  "memo": str <optional>,
  "mint": str,
  "unit": <str_enum>,
  "proofs": Array<Proof>
}
```

Here, `id` is the payment id (corresponding to `i` in request), `memo` is an optional memo to be sent to the receiver with the payment, `mint` is the mint URL from which the ecash is from, `unit` is the unit of the payment, and `proofs` is an array of proofs (see [NUT-00][00], can also include DLEQ proofs).

## Encoded Request

The payment request is serialized using CBOR, encoded in `base64_urlsafe`, together with a prefix `creq` and a version `A`:

`"creq" + "A" + base64(CBOR(PaymentRequest))`

_Example_

```sh
creqAaVhQRVhVWNzYXRhTXgiaHR0cHM6Ly9taW50Lm1pbmliaXRzLmNhc2gvQml0Y29pbmFEeCNQbGVzYXNlIHBheSB0aGUgdmVyeSBmaXJzdCBjYXNodSBwcmFUgaJhVGVub3N0cmJUYXhGbnByb2ZpbGUxcXFzZG11cDZlMno2bWNwZXVlNno2a2wwOGhlNDloY2VuNXhucmMzdG5wdncwbWRndGplbWgwc3V4YTBrag
```

[00]: 00.md