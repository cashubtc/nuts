# NUT-XX: Nostr Broadcast

`optional`

---

This document outlines a protocol for publishing Nostr notes that include blind signatures `B'` and spent secrets `x` (defined in [NUT-00](00)), which are associated with e-cash minting and burning events on the Mint.

### Rationale

When a sender transfers e-cash to a recipient, there is no direct way to confirm whether the recipient has claimed the payment without creating a link between their identity and receiving wallet's.
More specifically, the sending wallet can use the `v1/checkstate` API call (see [NUT-07](07)) to query the Mint about the status of sent e-cash with message `Y = hash_to_curve(x)`.
However, this approach has a significant privacy drawback: when the recipient attempts to claim the e-cash, they will reveal the same `Y` to the Mint, allowing it to potentially associate that token with both the sender's and recipient's identity (i.e. IP addresses). This compromises the protocol's inteded privacy guarantees.
Conversely, when the Mint publishes notes about freshly spent e-cash, the notes are simply broadcast to anyone who is listening, without creating a direct connection between the mint and any specific wallet.
Then, when a wallet wants to check if a particular e-cash was claimed, it can query the Nostr notes published by the mint, searching for the inclusion of specific e-cash it sent. This query is also anonymous, as the wallet is simply retrieving publicly available information.
As a result, the mint never learns which wallet is querying the information.

### PoL Scheme

The proposed protocol also streamlines the creation of a *Proof of Liabilities Report* (see [PoL scheme](PoL)), as each note represents a signed contribution to the "Mint Proof" or "Burn Proof" attestations of the mint for a particular epoch.

## Mint Nostr Identity
The Mint's Nostr public-private key pair is derived directly from the Mint's seed. Example (from Nushell):

```python
def derive_pubkey(seed: str):
    return PrivateKey(
        hashlib.sha256((seed).encode("utf-8")).digest()[:32],
        raw=True,
    ).pubkey
```
The public key is advertised in the `pubkey` field of the `GetInfoResponse` object returned by the Mint upon receiving a `v1/info` request, as specified in [NUT-06](06).

Upon startup, the Mint must broadcast a `kind: 0` event, reserved for setting *"Metadata"*. The event must have its `content` field set to the JSON-serialization of the following object:
```json
{
    "name": str,
    "about": str,
    "picture": str
}
``` 

Where:
* `name` can be the Mint's name, reachable URL or empty
* `about` is the Mint's short description or empty
* `picture` is the URL to an image for the Mint or empty.

## Posting Notes

The Mint regularly (about every 5 seconds) broadcasts events of `kind: 30078`, which is reserved for *"Application Specific Data"*. The Mint must also specificy a `created_at` unix timestamp in seconds along with the `content` of the note, which is initially set as follows:

```json
[
    {
        "epoch": int,
        "event": "MINT"|"BURN",
        "contents": Array<str>
    },
    ...
]
```
Where:
* `epoch`: is the current number of key rotations
* `event`: specifies whether this entry is a mint or burn
* `contents`: depends on `event`:
  + if `event` is `BURN`: array of hex-encoded spent    secrets.
  + if `event` is `MINT`: array of serialized, compressed and hex-encoded blind signature points


`content` is then finalized by taking its cbor-serialization and encoding the result to a Base64 string. Example:

```python
import cbor2
import base64
binary_content = cbor2.dumps(self.pending_events)
final_content = base64.b64encode(binary_content).decode('utf-8')
```

[00]: 00.md
[06]: 06.md
[07]: 07.md
[PoL]: https://gist.github.com/callebtc/ed5228d1d8cbaade0104db5d1cf63939

## Use Cases
TODO