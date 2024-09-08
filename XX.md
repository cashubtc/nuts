# NUT-XX: Nostr Broadcast

`optional`

---

This document outlines a protocol for publishing Nostr notes that include blind signatures `B'` and spent point-projections of the secrets `Y` (defined in [NUT-00](00)), which are associated with minting and burning events on the Mint.

### Rationale

When a sender transfers e-cash to a recipient, they need to confirm that the recipient has claimed the payment in order to safely mark the proof in their wallet as `SPENT`.
More specifically, the sending wallet can use the `v1/checkstate` API call (see [NUT-07](07)) to query the Mint about the status of sent e-cash.
It does so by querying the status of `Y = hash_to_curve(x)`.

However, this approach has a significant privacy drawback: when the recipient attempts to claim the e-cash, they will reveal the same `Y` to the Mint, allowing it to potentially associate that token with both the sender's and recipient's identity (i.e. IP addresses). This compromises the protocol's inteded privacy guarantees.

Conversely, when the Mint publishes notes about freshly spent e-cash, the notes are simply broadcast to anyone who is listening.
Then, when a wallet wants to check if its e-cash was claimed, it can query the Nostr notes published by the mint and look for the inclusion of specific secrets' `Y` it sent. 
As a result, the mint never learns which wallet is querying the information.

### PoL Scheme

The proposed protocol also streamlines the creation of a *Proof of Liabilities Report* (see [PoL scheme](PoL)), as each note represents a signed contribution to the "Mint Proof" or "Burn Proof" attestations of the mint for a particular epoch.

## `CASHU_MINT_IDENTITY`: Mint Nostr Identity

The public key associated with the Mint's nostr identity is identical to the one provided in the `pubkey` field of the `GetInfoResponse` object, which is returned by the Mint when it receives a `v1/info` request, as outlined in the [NUT-06](06) specification.

> [!NOTE]
> It's essential to be aware that nostr public keys are x-only, whereas the "pubkey" field in the `GetInfoResponse` object contains a compressed public key. As a result, clients should ensure to strip the initial byte before using the public key for nostr queries.

The generation of the public-private key pair is outside the scope of the spec, but here is an example (from Nushell):

```python
def derive_pubkey(seed: str):
    return PrivateKey(
        hashlib.sha256((seed).encode("utf-8")).digest()[:32],
        raw=True,
    ).pubkey
```

Upon startup, the Mint must broadcast a `kind: 11467` repleceable event. This event must have its `content` field set to the cbor-serialized, base64 encoded `GetInfoResponse` object described in [NUT-06](06).

## `CASHU_DATA`: Publishing MINT and BURN events.

The Mint regularly (about every 5 seconds) broadcasts events of `kind: 4919`, if any `MINT` or `BURN` as occurred.

> [!NOTE]
> These events are **BATCHES** of `MINT` and `BURN` events that have happened on the mint.

Each event must specify:
* a `created_at` unix timestamp in seconds

Each event can optionally specify:
* `tags`, containing an `e` tag that 
references the event ID of the previous publication.
  
The `content` field is initially set as follows:

```json
[
    {
        "epoch": <int>,
        "event": "MINT"|"BURN",
        "unit": <str>,
        "contents": [<Minted>|<Burnt>, ...]
    },
    ...
]
```
Where:
* `epoch`: is the current number of key rotations
* `event`: specifies whether this entry is a mint or burn
* `contents`: depends on `event`:
  + if `event` is `BURN`: array of one or more `Burnt` objects.
  + if `event` is `MINT`: array of one or more `Minted` obects.

`Burnt` contains the point-projection of the spent secrets (`Y = hash_to_curve(x)`) and relative amounts:
```json
{
    "Y": <lowercase-hex of 33-byte compressed curve point>,
    "amount": <int>
}
```

`Minted` contains blinded message, blinded signature and the respective amount:
```json
{
    "C_": <lowercase-hex of 33-byte compressed curve point>,
    "B_": <lowercase-hex of 33-byte compressed curve point>,
    "amount": <int>
}
```

`content` is then finalized by taking its cbor-serialization and encoding the result to a Base64 string. Example:

```python
import cbor2
import base64
binary_content = cbor2.dumps(self.pending_events)
final_content = base64.b64encode(binary_content).decode('utf-8')
```

## `CASHU_FIN_EPOCH`: Publishing the outstanding balance

Upon performing a key rotation the Mint can optionally publish a `kind: 1337` event (`CASHU_FIN_EPOCH`), signalling the
end of the current epoch.

If the Mint chooses not to publish this information, the end of an epoch is determined by `CASHU_DATA` events which reference an epoch bigger than the current one, and the outstanding balance for that epoch and unit currency is presumed to be 0.

The event can optionally contain `e` tags referencing the event ID of the publication of the Outstanding Balance for the previous epoch and unit.
The event's `content` field is made from the following payload:

```json
{
    "epoch": <int>,
    "outstanding_balance": <int>,
    "unit": <str>
}
```

## Use Cases

### Ecash Transactions
When `Alice` prepares a token to be sent to `Carol`, she can mark these tokens in her database as `RESERVED`. She can then, periodically or upon user input, query its connected relays for notes referencing the Mint's pubkey as the author and a timestamp for filtering out older notes. `Alice` can then scan the notes' content and look for the inclusion of the spent secrets (sent to `Carol`). If it finds any, the token has been redeemed by `Carol` already, i.e., is `SPENT`. If the proof is not spendable anymore (and, thus, has been redeemed by `Carol`), she can safely delete the proof from her database.

### Wallet Restoration
Suppose `Alice` has lost or corrupted her wallet, if she knows her seed phrase, she can restore the unspent secrets:
1) `Alice` derives secrets and blinding factors from her seed phrase, then blinds the secrets to generate blinded messages `B_` (see [NUT-13](13)).
2) She queries her relays, filtering for events generated by the Mint's public key.
3) For each note, she decodes the payload:
    + for any `MINT` event, Alice looks for a match with `B_`
    + for any match, she unblinds `B_` to obtain `C_` and she checks for occurrences of `C_` in any of the `BURN` events
    + if she can't find any, then the corresponding secret is unspent, and can save it.

It is worth mentioning that this is just an example approach and certainly not the most efficient one.


### Facilitating Proof of Liabilities Reports
<img src="https://user-images.githubusercontent.com/93376500/249383182-ed572841-cd78-40ea-b171-c1f768cd13dc.png" alt="PoL" width="50%"/>
<!-- ![](https://user-images.githubusercontent.com/93376500/249383182-ed572841-cd78-40ea-b171-c1f768cd13dc.png) -->

Each note represents signed contributions to "Mint proofs" (issued ecash) and "Burn proofs" (redeemed ecash) for the epoch specified in `epoch` field. The notes can then be compiled into a succint Proof of Liabilities report for each epoch by anyone requesting the publicly available information about the mint through nostr relays.



[00]: 00.md
[06]: 06.md
[07]: 07.md
[13]: 13.md
[PoL]: https://gist.github.com/callebtc/ed5228d1d8cbaade0104db5d1cf63939