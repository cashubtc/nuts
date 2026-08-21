# NUT-18 (legacy) Test Vectors

Payment requests carrying the pre-v3 `nut10` locking option ([legacy NUT-18](../18.md)).

## Complete Payment Request

A payment request with all optional fields included.

```json
{
  "i": "4840f51e",
  "a": 1000,
  "u": "sat",
  "s": true,
  "m": ["https://mint.example.com"],
  "d": "Product purchase",
  "t": [
    {
      "t": "post",
      "a": "https://api.example.com/pay"
    }
  ],
  "nut10": {
    "k": "P2PK",
    "d": "03baf0c3ac220366c2c397bf930579c4163435584f573b10910987c544c59e61f1",
    "t": [["purpose", "offline"]]
  }
}
```

Encoded:

```
creqAqGF0gaNhdGRwb3N0YWF4G2h0dHBzOi8vYXBpLmV4YW1wbGUuY29tL3BheWFn92FpaDQ4NDBmNTFlYWEZA+hhdWNzYXRhbYF4GGh0dHBzOi8vbWludC5leGFtcGxlLmNvbWFkcFByb2R1Y3QgcHVyY2hhc2Vhc/VlbnV0MTCjYWtkUDJQS2FkeEIwM2JhZjBjM2FjMjIwMzY2YzJjMzk3YmY5MzA1NzljNDE2MzQzNTU4NGY1NzNiMTA5MTA5ODdjNTQ0YzU5ZTYxZjFhdIGCZ3B1cnBvc2Vnb2ZmbGluZQ==
```

## Payment Request with NUT-10 Locking

A payment request requiring P2PK-locked tokens.

```json
{
  "i": "c9e45d2a",
  "a": 500,
  "u": "sat",
  "m": ["https://mint.example.com"],
  "nut10": {
    "k": "P2PK",
    "d": "02c3b5bb27e361457c92d93d78dd73d3d53732110b2cfe8b50fbc0abc615e9c331",
    "t": [["timeout", "3600"]]
  }
}
```

Encoded:

```
creqApWFpaGM5ZTQ1ZDJhYWEZAfRhdWNzYXRhbYF4GGh0dHBzOi8vbWludC5leGFtcGxlLmNvbWVudXQxMKNha2RQMlBLYWR4QjAyYzNiNWJiMjdlMzYxNDU3YzkyZDkzZDc4ZGQ3M2QzZDUzNzMyMTEwYjJjZmU4YjUwZmJjMGFiYzYxNWU5YzMzMWF0gYJndGltZW91dGQzNjAw
```
