# NUT-XX: Currency unit metadata

`optional`

`depends on: NUT-06`

---

This NUT defines how a mint publishes display metadata for the currency units of its keysets. Wallets use the metadata to display amounts of units that are not defined elsewhere, such as custom units, without guessing. The metadata is display-only: it plays no role in transaction validation or in the keyset ID derivation described in [NUT-02][02].

## Unit metadata

The mint publishes the metadata in the settings for this NUT in the info response ([NUT-06][06]):

```json
{
  "XX": [
    { "unit": "ora", "precision": 2, "name": "Ora" },
    { "unit": "usd", "precision": 2, "name": "US Dollar", "symbol": "$" }
  ]
}
```

The setting is an array of metadata objects with the fields:

- `unit`: The unit string, exactly as used in the `unit` field of a keyset ([NUT-02][02])
- `precision`: The number of decimal places of the unit. An amount `a` of this unit represents the value `a * 10^(-precision)`. **MUST** be an integer between `0` and `18`.
- `name` (optional): The full name of the currency
- `symbol` (optional): A symbol that wallets can display next to amounts of the unit

Mints **MUST NOT** publish multiple entries for the same `unit`. Array order has no significance. Different units may share the same precision, name, or symbol.

For example, with the metadata above, the amount `500` of the unit `ora` is displayed as `5.00 ora`.

The metadata is scoped to the publishing mint and applies to all of its keysets of that unit. Mints **MUST NOT** change the precision of an existing unit. Mints **SHOULD** keep names and symbols stable over time. Wallets **SHOULD** refresh the metadata together with the rest of the info response.

The presence of the setting indicates that the mint supports this NUT.

## Precedence

The metadata fills gaps; it **MUST NOT** change how amounts of units that are already defined elsewhere are interpreted. Wallets determine the precision of a unit in the following order:

1. For the units defined in [NUT-01][01] (`btc`, `sat`, `msat`, `auth`), wallets **MUST** use the values defined there (`btc`: 8 decimal places, all others: 0).
2. For ISO 4217 currency codes, wallets **MUST** use the Minor Unit of the currency as defined by ISO 4217.
3. For all other units, wallets use the published precision for display.

Mints **MAY** publish metadata for units covered by rules 1 and 2. If they do, the published `precision` **MUST** match the values defined there. Wallets use the values of rules 1 and 2 regardless of what is published; a mismatch has no further consequence.

[NUT-01][01] requires stablecoin amounts to represent the Minor Unit of the pegged currency. A wallet cannot verify which currency an unknown stablecoin code is pegged to. For codes a wallet does not recognize, rule 3 applies: the published metadata communicates the result of the [NUT-01][01] requirement.

If a unit is not covered by rules 1 and 2 and the mint publishes no metadata for it, wallets **MUST NOT** guess a precision and **SHOULD** display the raw amount together with the unit string. Metadata ignored under the wallet handling rules below is treated as absent for this purpose.

## Wallet handling

The metadata is display-only:

- Wallets **MUST NOT** use it to accept, reject, or compare keysets.
- It is not part of the keyset ID derivation ([NUT-02][02]).

Wallets **MUST** check for duplicate unit identifiers before using the metadata, including before converting the array to a map. If a unit occurs more than once, wallets **MUST** ignore all entries for that unit, even if the entries are identical.

Mints **MUST NOT** repeat member names within a metadata object. If a wallet detects repeated member names, it **MUST** ignore this NUT's metadata for that response. Duplicate JSON member names are a parsing concern distinct from duplicate unit entries in the array.

Wallets **SHOULD** detect changes to previously observed precision for the same mint and unit, and notify the user before applying changed precision to existing balances.

Wallets **MUST NOT** use published names or symbols as unit identifiers, or infer that units are interchangeable because their metadata matches. Wallets **SHOULD** use their own names and symbols for units covered by rules 1 and 2. For all other units, wallets **MUST** display the unit string alongside any published name or symbol they display.

The metadata is a mint's claim about how to display amounts. It does not establish currency identity, value, backing, or a stablecoin peg. A mint can publish misleading metadata or different metadata to different wallets without including duplicate entries. Duplicate checks and keyset verification cannot establish the truth of these claims.

[01]: 01.md
[02]: 02.md
[06]: 06.md
