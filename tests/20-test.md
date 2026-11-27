# NUT-20 Test Vectors

## Deterministic quote locking key derivation

Using [NUT-20](../20.md) quote locking key derivation, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble"
}
```

The public keys derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "m/129373'/20'/0'/0'/0": "03062837166e56114b59a4d1fd3a5a812bf7aadc1dde758428cf943d80acd41539",
  "m/129373'/20'/0'/0'/1": "02b47d9d41725f5ce6f08c874835cef25376cb1e95f6cb073fef52ca8fd986cf15",
  "m/129373'/20'/0'/0'/2": "029acbd3a46fd75bc05ba0226d0b4d909b2fb6e96c80544a094a1a3567737e44d3",
  "m/129373'/20'/0'/0'/3": "0373e4a42fbe0a4e18aadb57cf500b655f2446b4071ee579121d2ed8905bcc49c2",
  "m/129373'/20'/0'/0'/4": "02b8709bfce17c10f1864f5218844533ae60930d52089669b317d8b5f474eec071"
}
```
