# NUT-XX: Currency unit metadata

`optional`

`depends on: NUT-06`

---

This NUT defines how a mint publishes display metadata for the currency units of its keysets. Wallets use the metadata to display amounts of units that are not defined elsewhere, such as custom units, without guessing. The metadata is display-only: it plays no role in transaction validation or in the keyset ID derivation described in [NUT-02][02].

## Unit metadata

The mint publishes the metadata in the settings for this NUT in the info response ([NUT-06][06]):

```json
{
  "XX": {
    "units": {
      "ora": { "precision": 2, "name": "Ora" },
      "usd": { "precision": 2, "name": "US Dollar", "symbol": "$" }
    }
  }
}
```

`units` maps a unit string, as used in the `unit` field of a keyset ([NUT-02][02]), to a metadata object with the fields

- `precision`: The number of decimal places of the unit. An amount `a` of this unit represents the value `a * 10^(-precision)`. **MUST** be an integer between `0` and `18`.
- `name` (optional): The full name of the currency
- `symbol` (optional): A symbol that wallets can display next to amounts of the unit

For example, with the metadata above, the amount `500` of the unit `ora` is displayed as `5.00 ORA`.

The metadata of a unit applies to all keysets of that unit. Mints **SHOULD** keep it stable over time. Wallets **SHOULD** refresh it together with the rest of the info response.

The presence of the setting indicates that the mint supports this NUT.

## Precedence

The metadata fills gaps; it **MUST NOT** change how amounts of units that are already defined elsewhere are interpreted. Wallets determine the precision of a unit in the following order:

1. For the units defined in [NUT-01][01] (`btc`, `sat`, `msat`, `auth`), wallets **MUST** use the values defined there (`btc`: 8 decimal places, all others: 0).
2. For ISO 4217 currency codes, wallets **MUST** use the Minor Unit of the currency as defined by ISO 4217.
3. For all other units, the published metadata is authoritative.

Mints **MAY** include units covered by rules 1 and 2 in `units`. If they do, the published `precision` **MUST** match the values defined there. Wallets use the values of rules 1 and 2 regardless of what is published; a mismatch has no further consequence.

[NUT-01][01] requires stablecoin amounts to represent the Minor Unit of the pegged currency. A wallet cannot verify which currency an unknown stablecoin code is pegged to. For codes a wallet does not recognize, rule 3 applies: the published metadata communicates the result of the [NUT-01][01] requirement.

If a unit is not covered by rules 1 and 2 and the mint publishes no metadata for it, wallets **MUST NOT** guess a precision and **SHOULD** display the raw amount together with the unit string.

## Wallet handling

The metadata is display-only:

- Wallets **MUST NOT** use it to accept, reject, or compare keysets.
- It is not part of the keyset ID derivation ([NUT-02][02]).

Since any unit can publish any `symbol`, wallets **SHOULD** use their own names and symbols for units covered by rules 1 and 2, and **SHOULD** display the unit string alongside a published symbol that collides with the symbol of a well-known currency.

[01]: 01.md
[02]: 02.md
[06]: 06.md
