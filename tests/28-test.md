# NUT-28 Test Vectors

## Quote Lookup Signature

### Message Construction

For a request with:
- `pubkey` = `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac`
- `timestamp` = `1701704800`
- `unit` = `sat`
- `state` = `PAID`

```
msg_to_sign = "quote_lookup" || pubkey || timestamp || unit || state
            = "quote_lookup03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac1701704800satPAID"
```

For a request with null filters:
- `pubkey` = `03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac`
- `timestamp` = `1701704800`
- `unit` = null
- `state` = null

```
msg_to_sign = "quote_lookup" || pubkey || timestamp || "" || ""
            = "quote_lookup03d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac1701704800"
```

The signature is BIP340 Schnorr on `SHA256(msg_to_sign)`.

### Invalid Signature

A request with an invalid signature should return error code `20010`.
