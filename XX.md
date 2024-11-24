NUT-XX: Cached Responses
==========================

`optional`

---

To mitigate the risk of potential ecash loss due to network errors during critical operations such as minting, swapping, and melting, we introduce a caching mechanism for successful responses. This mechanism uses the `POST` request path and body contents to derive a key and then cache the responses using that key. If an identical request is received, the system will provide the cached response, minimizing the risk of ecash loss in the event of network disruptions.
 

## Requests & Responses

Any Mint implementation should elect a data structure `D` that maps request objects to their respective responses. `D` should be fit for fast insertion, look-up and deletion (eviction) operations.

### Derive & Repeat

Upon the reception of a mint (`POST /v1/mint/{method}`), swap (`POST v1/swap`) or melt (`POST /v1/melt/{method}`) `request` Bob should immediately derive a key `k` for it. `k` should depend on the path of `request` as well as the contents of `request`'s payload.

Bob should perform a `k` based look-up `response = D[k]` and discriminate execution based  on the following check:
* If `response == null`: `request` has no matching `response`. Bob should process `request` as per usual.
* If `response != null`: `request` has a matching `response`. Bob should return the cached `response` (REPEAT).

### Store

After any mint, melt and swap request is processed and the response has been deemed to be successful (`status_code == 200`), Bob should store the response in `D`.

### Expiry

Bob autonomously decides the TTL (Time To Live) for each successful response, after which time has passed it can evict the entry from `D`.

## Settings

Support for NUT-XX **MUST** be announced as an extension to the `nuts` field of the `GetInfoResponse` object described in [NUT-6](06) and returned upon a `GET v1/info` request.

The entry must be structured as follows:
```json
"nuts": {
    ...,
    "xx": {
        "ttl": <int>,
        "cached_endpoints": [
            {
                "path": "v1/{mint|melt}/{method}",
                "method": "{POST|GET|...}",
            },
            {
                "path": "v1/swap",
                "method": "{POST|GET|...}",
            },
            ...
        ]
    }
}
```

Where `ttl` is the amount of seconds the responses are cached for and `cached_endpoints` is a list of the routes for which caching is enabled.
`path` and `method` describe respectively the cached route and its method.

if `ttl` is set to 0, then the responses are to be considered cached *indefinetely*

## Example

**Requests** of `Alice`:

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

If the first request is successful, `Bob` will respond with 5 identical `PostSwapResponse`s: 

```json
{
  "signatures": <Array[BlindSignature]>
}
```

[06]: 06.md