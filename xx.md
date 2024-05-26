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

```go
type PaymentRequest struct {
  A int         `amount (optional)`
  U string      `unit`
  R string      `mint url (optional)`
  D string      `description (optional)`
  M string      `memo (optional)`
  T []Transport `transport`
}
```

while Transport is defined as

```go
type Transport struct {
    T  string `type`
    Ta string `target`
}
```

- amount: The amount of the requested token (payment amount)
- unit: The unit of the requested token (e.g. sats)
- mint: The mint to use to mint the token
- description: A human readable discription that the sending wallet will display after scanning the request
- transport: The method of transport chosen to transmit the created token to the sender (can be multiple, sorted by preference)

## Encoded Request

Cashu Payment Requests can be encoded and displayed/sent as string or qr code. They underlying object is serialised using CBOR and finlly base64 encoded and prefixed with a version byte and standard prefix.

_Example_

```sh
cashrqAaVhQRVhVWNzYXRhTXgiaHR0cHM6Ly9taW50Lm1pbmliaXRzLmNhc2gvQml0Y29pbmFEeCNQbGVzYXNlIHBheSB0aGUgdmVyeSBmaXJzdCBjYXNodSBwcmFUgaJhVGVub3N0cmJUYXhGbnByb2ZpbGUxcXFzZG11cDZlMno2bWNwZXVlNno2a2wwOGhlNDloY2VuNXhucmMzdG5wdncwbWRndGplbWgwc3V4YTBrag
```

## Reference Implementation

```go
package main

import (
	"encoding/base64"
	"fmt"
	"log"

	"github.com/fxamacker/cbor/v2"
)

const (
	pre     = "cashrq"
	version = byte(0x01)
)

type Transport struct {
	T  string
	Ta string
}
type PaymentRequest struct {
	A int
	U string
	M string
	D string
	T []Transport
}

func encodeRequest(pr PaymentRequest) string {
	b, err := cbor.Marshal(pr)
	if err != nil {
		log.Fatal("CBOR encoding failed...")
	}
	b = append([]byte{version}, b...)
	encodedString := base64.RawURLEncoding.EncodeToString(b)
	res := pre + encodedString
	return res
}

func main() {
	t := Transport{T: "nostr", Ta: "nprofile1qqsdmup6e2z6mcpeue6z6kl08he49hcen5xnrc3tnpvw0mdgtjemh0suxa0kj"}
	pr := PaymentRequest{A: 21, U: "sat", M: "https://mint.minibits.cash/Bitcoin", D: "Plesase pay the very first cashu pr", T: []Transport{t}}
	res := encodeRequest(pr)
	fmt.Printf("%s", res)
}
```
