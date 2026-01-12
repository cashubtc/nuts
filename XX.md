# NUT-XX: Mining Share Payment Method

`optional`

`depends on: NUT-04 NUT-05 NUT-20`

---

This document describes minting ehash with the `mining_share` payment method. Mining-share quotes represent proof-of-work shares submitted to a mining pool affiliated with the mint. A share is identified by its block header hash and its quote becomes eligible for ehash issuance once the pool validates the share; the resulting ehash token is the authoritative record of the mining share credit until it is redeemed for a mining reward.

## Definitions

- **Ehash**: Ecash issued by a mint to represent the value of a valid mining share. Ehash denominations correspond to powers of two derived from share difficulty.
- **Share difficulty**: The number of leading zero bits in the 256-bit `header_hash` supplied with a mining-share quote request.
- **Keyset minimum difficulty**: The minimum number of leading zero bits a mint requires for shares associated with a given keyset and currency unit. This value is configured and advertised by the mint.

All difficulty comparisons in this specification use these definitions.

## Mint Quote

Wallets request a mining-share quote with `POST /v1/mint/quote/mining_share` and the following `PostMintQuoteMiningShareRequest` payload:

```json
{
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "header_hash": <str>,
  "description": <str|null>,
  "pubkey": <str>
}
```

- `amount` **MUST** be greater than zero and **MUST** equal `2^(share difficulty - keyset minimum difficulty)`, as defined above. If the share difficulty is lower than the keyset minimum difficulty the mint **MUST** reject the quote.
- `unit` **MUST** begin with the uppercase prefix `"HASH"` and otherwise comply with the currency unit rules defined in [NUT-02][02]. Implementations MAY append identifiers after the prefix (for example `"HASH-POOL1-EPOCH42"`) to scope shares to a pool and mining epoch.
- `header_hash` **MUST** be the 32-byte share header hash encoded as a lowercase hex string.
- `description` allows optional metadata for the share.
- `pubkey` **MUST** be provided in accordance with [NUT-20][20]; the mint **MUST NOT** accept quotes without a public key.

The mint responds with a `PostMintQuoteMiningShareResponse`:

```json
{
  "quote": <str>,
  "request": <str>,
  "amount": <int>,
  "unit": <str_enum[UNIT]>,
  "state": <str_enum[STATE]>,
  "expiry": <int|null>,
  "pubkey": <str>,
  "keyset_id": <str>
}
```

Where:

- `quote` is the opaque quote identifier used by subsequent requests.
- `request` echoes the share `header_hash` supplied in the request.
- `state` is one of `"UNPAID"`, `"PAID"`, or `"ISSUED"`.
- `expiry` is the Unix timestamp (in seconds) until which the share credit remains valid.
- `keyset_id` identifies the keyset that will sign any issued proofs.

The initial `state` reflects the mining backend's validation workflow. Mints MAY return `"UNPAID"` while the pool verifies a miner-supplied block template and MUST transition to `"PAID"` once the share is credited. When the mint controls the block template, it MAY respond with `"PAID"` immediately.

### Example

Request:

```bash
curl -X POST https://mint.host/v1/mint/quote/mining_share \
  -H "Content-Type: application/json" \
  -d '{
        "amount": 512,
        "unit": "HASH",
        "header_hash": "000000000053d929ef22bef424cc607adac340e241190dad36eed3e9a57699a5",
        "pubkey": "02d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac"
      }'
```

Response:

```json
{
  "quote": "621ea695-624b-4e53-9643-5e36fc1f8004",
  "request": "000000000053d929ef22bef424cc607adac340e241190dad36eed3e9a57699a5",
  "amount": 512,
  "unit": "HASH",
  "state": "PAID",
  "expiry": 1701704757,
  "pubkey": "02d56ce4e446a85bbdaa547b4ec2b073d40ff802831352b8272b7dd7a4de5a7cac",
  "keyset_id": "01e2f8..."
}
```

### Checking Quote State

Wallets poll the quote status with `GET /v1/mint/quote/mining_share/{quote}`. The mint responds with the same structure as the quote creation response and updates the `state` field as minting progresses. Once the mint has signed the full share amount for the quote, it **MUST** return `state = "ISSUED"`.

## Minting Tokens

After the quote is in the `"PAID"` state, wallets call `POST /v1/mint/mining_share` with a standard [NUT-04][04] `MintRequest`:

```json
{
  "quote": <str>,
  "outputs": <Array[BlindedMessage]>,
  "signature": <str|null>
}
```

- `quote` references the mining-share quote identifier.
- `outputs` contains the blinded messages (and associated keyset identifiers) to be signed.
- `signature` **MUST** be a valid Schnorr signature produced with the private key that corresponds to the `pubkey` sent in the quote request, as specified in [NUT-20][20]. Wallets **MUST** sign every mining-share mint request.

Mints **MUST** validate that the total amount represented by `outputs` equals `2^(share difficulty - keyset minimum difficulty)`, using the same difficulty measurements recorded when the quote was created. If the request is valid, the mint signs each output and responds with the usual `MintResponse`.

Wallets **MUST** construct mint requests whose summed output amount matches this exponential value exactly. Once the mint marks the quote `"ISSUED"`, wallets **SHOULD** treat it as fully spent and avoid additional mint requests for that quote.

### Example

```bash
curl -X POST https://mint.host/v1/mint/mining_share \
  -H "Content-Type: application/json" \
  -d '{
        "quote": "621ea695-624b-4e53-9643-5e36fc1f8004",
        "outputs": [
          {
            "amount": 256,
            "id": "009a1f293253e41e",
            "keyset_id": "01e2f8...",
            "B_": "035015e6d7ade60ba8426cefaf1832bbd27257636e44a76b922d78e79b47cb689d"
          },
          {
            "amount": 256,
            "id": "009a1f293253e41e",
            "keyset_id": "01e2f8...",
            "B_": "0288d7649652d0a83fc9c966c969fb217f15904431e61a44b14999fabc1b5d9ac6"
          }
        ],
        "signature": "f5b9a3..."
      }'
```

Mint response:

```json
{
  "signatures": [
    {
      "id": "009a1f293253e41e",
      "keyset_id": "01e2f8...",
      "amount": 256,
      "C_": "0224f1c4c564230ad3d96c5033efdc425582397a5a7691d600202732edc6d4b1ec"
    },
    {
      "id": "009a1f293253e41e",
      "keyset_id": "01e2f8...",
      "amount": 256,
      "C_": "0277d1de806ed177007e5b94a8139343b6382e472c752a74e99949d511f7194f6c"
    }
  ]
}
```

## Mint Settings

Mints advertise support for mining-share minting via [NUT-04][04] `MintMethodSettings` entries. A simple example:

```json
{
  "method": "mining_share",
  "unit": "HASH",
  "min_amount": 32,
  "max_amount": 96,
  "options": {}
}
```

`min_amount` and `max_amount` encode the acceptable difficulty window for share hashes. Each value **MUST** be between `0` and `255`, inclusive, and represents the count of leading zero bits in the 256-bit header hash (difficulty `0` means no leading zero bits; difficulty `255` means all but the final bit are zero). Shares with fewer leading zeros than `min_amount` **MUST** be rejected. Shares that exceed `max_amount` **MUST** be accepted but paid out only up to the reward implied by `max_amount`. Mints **SHOULD** publish windows that align with their pool's payout policy.

## Security Considerations

- Mints **MUST** treat `header_hash` values as unique payment identifiers and **MUST** reject duplicate shares.
- Wallets **SHOULD** generate a fresh NUT-20 key pair per mining-share quote to avoid linking multiple quotes.
- Wallets **SHOULD** redeem mining-share quotes before they expire and **SHOULD** discard any quote that remains in the `"UNPAID"` state once its `expiry` elapses, as the mint will reject further minting attempts.

[02]: https://github.com/cashubtc/nuts/blob/main/02.md
[04]: https://github.com/cashubtc/nuts/blob/main/04.md
[05]: https://github.com/cashubtc/nuts/blob/main/05.md
[20]: https://github.com/cashubtc/nuts/blob/main/20.md
