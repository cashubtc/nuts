# Supplementary: NUT-CTF-split-merge Complete Example

This document provides a full end-to-end example of the CTF split/merge lifecycle. For the normative specification, see [NUT-CTF-split-merge][CTF-split-merge].

## Complete Example

### Step 1a: Register Condition

First, register the condition via `POST /v1/conditions` ([NUT-CTF][CTF]):

**Request** of `Alice`:

```http
POST https://mint.host:3338/v1/conditions
```

```json
{
  "threshold": 1,
  "tags": [["description", "Will BTC reach $100k by June 2025?"]],
  "announcements": ["fdd824fd<...hex-encoded oracle_announcement TLV...>"]
}
```

`Bob` responds with:

```json
{
  "condition_id": "a1b2c3d4e5f67890..."
}
```

### Step 1b: Register Partition

**Request** of `Alice`:

```http
POST https://mint.host:3338/v1/conditions/a1b2c3d4e5f67890.../partitions
```

```json
{
  "collateral": "sat",
  "partition": ["YES", "NO"]
}
```

`Bob` responds with:

```json
{
  "keysets": {
    "YES": "00abc123def456",
    "NO": "00def789abc012"
  }
}
```

### Step 2: Split Collateral

`Alice` wants to participate with 100 sats:

**Request** of `Alice`:

```http
POST https://mint.host:3338/v1/ctf/split
```

```json
{
  "condition_id": "a1b2c3d4e5f67890...",
  "inputs": [
    {
      "amount": 64,
      "id": "009a1f293253e41e",
      "secret": "random_secret_1",
      "C": "02..."
    },
    {
      "amount": 32,
      "id": "009a1f293253e41e",
      "secret": "random_secret_2",
      "C": "02..."
    },
    {
      "amount": 4,
      "id": "009a1f293253e41e",
      "secret": "random_secret_3",
      "C": "02..."
    }
  ],
  "outputs": {
    "YES": [
      { "amount": 64, "id": "00abc123def456", "B_": "03..." },
      { "amount": 32, "id": "00abc123def456", "B_": "03..." },
      { "amount": 4, "id": "00abc123def456", "B_": "03..." }
    ],
    "NO": [
      { "amount": 64, "id": "00def789abc012", "B_": "03..." },
      { "amount": 32, "id": "00def789abc012", "B_": "03..." },
      { "amount": 4, "id": "00def789abc012", "B_": "03..." }
    ]
  }
}
```

`Bob` responds with:

```json
{
  "signatures": {
    "YES": [
      { "amount": 64, "id": "00abc123def456", "C_": "02..." },
      { "amount": 32, "id": "00abc123def456", "C_": "02..." },
      { "amount": 4, "id": "00abc123def456", "C_": "02..." }
    ],
    "NO": [
      { "amount": 64, "id": "00def789abc012", "C_": "02..." },
      { "amount": 32, "id": "00def789abc012", "C_": "02..." },
      { "amount": 4, "id": "00def789abc012", "C_": "02..." }
    ]
  }
}
```

`Alice` now holds 100 sats of YES tokens and 100 sats of NO tokens.

### Step 3: Trading

`Alice` believes YES will win, so she sells her NO tokens to `Carol` for 40 sats via a normal Cashu token transfer. `Carol` swaps at the mint using a standard [NUT-03][03] swap — all inputs and outputs use the NO conditional keyset. No oracle witness is needed.

### Step 4: Oracle Attestation

The oracle attests that YES won by publishing a DLC attestation signature on `"YES"`.

### Step 5: Winner Redemption

`Alice` redeems her YES tokens via `POST /v1/redeem_outcome` ([NUT-CTF][CTF]) with `oracle_sigs` witness. Inputs use the YES conditional keyset, outputs use a regular keyset. The mint verifies the oracle signatures and returns regular proofs.

[00]: ../00.md
[02]: ../02.md
[03]: ../03.md
[06]: ../06.md
[CTF]: ../CTF.md
[CTF-split-merge]: ../CTF-split-merge.md
