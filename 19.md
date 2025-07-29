# NUT-19: Cached Responses

`optional`

---

To minimize the risk of loss of funds to due network errors during critical operations such as minting, swapping, and melting, we introduce a caching mechanism for successful responses. This allows wallet to replay requests on cached endpoints and allow it to recover the desired state after a network interruption.

## Requests & Responses

Any Mint implementation should elect a data structure `D` that maps request objects to their respective responses. `D` should be fit for fast insertion, look-up and deletion (eviction) operations. This could be an in-memory database or a dedicated caching service like Redis.

### Derive & Repeat

Upon receiving a `request` on a cached endpoint, the mint derives a unique key `k` for it which should depend on the method, path, and the payload of `request`.

The mint uses `k` to look up a `response = D[k]` and discriminates execution based on the following checks:

- If no cached `response` is found: `request` has no matching `response`. The mint processes `request` as per usual.
- If a cached `response` is found: `request` has a matching `response`. The mint returns the cached `response`.

### Store

For each successful response on a cached endpoint (`status_code == 200`), the mint stores the response in `D` under key `k` (`D[k] = response`).

### Expiry

The mint decides the `ttl` (Time To Live) of cached response, after which it can evict the entry from `D`.

## Settings

Support for NUT-19 is announced as an extension to the `nuts` field of the `GetInfoResponse` described in [NUT-06][06].

The entry is structured as follows:

```json
"nuts": {
    ...,
    "19": {
        "ttl": <int|null>,
        "cached_endpoints": [
            {
                "method": "POST",
                "path": "/v1/mint/bolt11",
            },
            {
                "method": "POST",
                "path": "/v1/swap",
            },
            ...
        ]
    }
}
```

Where:

- `ttl` is the number of seconds the responses are cached for
- `cached_endpoints` is a list of the methods and paths for which caching is enabled.
- `path` and `method` describe the cached route and its method respectively.

If `ttl` is `null`, the responses are expected to be cached _indefinitely_.

[06]: 06.md
