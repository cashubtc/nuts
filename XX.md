NUT-XX: Cached Responses
==========================

`optional`

---

To mitigate the risk of potential ecash loss due to network errors during critical operations such as minting, swapping, and melting, we introduce a caching mechanism for successful responses. This mechanism uses the `POST` request path and the serialized body contents to derive a key and then cache the responses using that key. If an identical request is received, the system will provide the cached response, minimizing the risk of ecash loss in the event of network disruptions.
 

## Requests & Responses

The Mint should elect a data structure `D` that maps request objects to their respective responses. `D` should be fit for fast insertion and look-up operations.

### Derive & Repeat

Upon the reception of a mint (`POST /v1/mint/{method}`), swap (`POST v1/swap`) or melt (`POST /v1/melt/{method}`) `request` the Mint should immediately derive a key `k` for it. `k` should depend on the path of `request` and the JSON-serialization of the contents of `request`'s payload.

The Mint should perform a `k` based look-up `response = D[k]` the following and discriminate execution based on the following comparison:
* If `response == null`: `request` has no matching `response`. The Mint should process `request` as per usual.
* If `response != null`: `request` has a matching `response`. The Mint should return the cached `response` (REPEAT).

### Store

After the request is processed and the response has been deemed to be successful (`status_code == 200`), the Mint should store the response in `D`.

### Expiry

The Mint autonomously decides the TTL (Time To Live) for each successful response, after which time has passed it can evict the entry from the cache.

The TTL should be _**AT LEAST**_ 3600 seconds.


## Examples

## Example

**Request** of `Alice`:

```http
POST https://mint.host:3338/v1/swap
```

With the data being of the form `PostSwapRequest`:

```json
{
  "inputs": <Array[Proof]>,
  "outputs": <Array[BlindedMessage]>,
}
```

With curl:

```bash
for i in {1..5}; do
    curl -X POST https://mint.host:3338/v1/swap -d \
    {
    "inputs": 
        [
        {
            "amount": 2,
            "id": "009a1f293253e41e",
            "secret": "407915bc212be61a77e3e6d2aeb4c727980bda51cd06a6afc29e2861768a7837",
            "C": "02bc9097997d81afb2cc7346b5e4345a9346bd2a506eb7958598a72f0cf85163ea"
        },
        {
        ...
        }
        ],
    "outputs":
        [
        {
            "amount": 2, 
            "id": "009a1f293253e41e",
            "B_": "02634a2c2b34bec9e8a4aba4361f6bf202d7fa2365379b0840afe249a7a9d71239"
        },
        {
        ...
        }
        ],
    }
done
```

If the first request is successful, `Bob` (The Mint) will respond with 5 identical `PostSwapResponse`: 

```json
{
  "signatures": <Array[BlindSignature]>
}
```