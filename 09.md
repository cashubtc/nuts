# NUT-09: Restore signatures

`optional`

`used in: NUT-13`

---

In this document, we describe how wallets can recover blind signatures, and with that their corresponding `Proofs`, by requesting from the mint to reissue the blind signatures. This can be used for a backup recovery of a lost wallet (see [NUT-13][13]) or for recovering the response of an interrupted swap request (see [NUT-03][03]).

Mints must store the `BlindedMessage` and the corresponding `BlindSignature` in their database every time they issue a `BlindSignature`. Wallets provide the `BlindedMessage` for which they request the `BlindSignature`. Mints only respond with a `BlindSignature`, if they have previously signed the `BlindedMessage`. Each returned `BlindSignature` also contains the `amount` and the keyset `id` (see [NUT-00][00]) which is all the necessary information for a wallet to recover a `Proof`.

**Request** of `Alice`:

```http
POST https://mint.host:3338/v1/restore
```

With the data being of the form `PostRestoreRequest`:

```json
{
  "outputs": <Array[BlindedMessages]>
}
```

**Response** of `Bob`:

The mint `Bob` then responds with a `PostRestoreResponse`.

```json
{
  "outputs": <Array[BlindedMessages]>,
  "signatures": <Array[BlindSignature]>
}
```

The returned arrays `outputs` and `signatures` are of the same length and for every entry `outputs[i]`, there is a corresponding entry `signatures[i]`.

## Mint info setting

The [NUT-06][06] `MintMethodSetting` indicates support for this feature:

```json
{
  "9": {
    "supported": true
  }
}
```

[00]: 00.md
[02]: 02.md
[03]: 03.md
[07]: 07.md
[09]: 09.md
[11]: 11.md
[13]: 13.md
