# NUT-XX Test vectors

## NUT-11 (P2PK) key derivation

Using [NUT-XX](../XX.md) derivation with DST `Cashu_KDF_HMAC_SHA256_NUT11`, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble",
  "seed_hex": "dd44ee516b0647e80b488e8dcc56d736a148f15276bef588b37057476d4b2b25780d3688a32b37353d6995997842c0fd8b412475c891c16310471fbc86dcbda8"
}
```

The compressed public keys derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "pubkey_0": "0202bf842ee2e4a3aba0728238bb073a9a3ab383695a58fd26e3f03f70bf671890",
  "pubkey_1": "028adf592a715df71b60857b20c4ff5c3630e305432fd8ec6a02daf5f3beef3083",
  "pubkey_2": "028932541412a283dd7c1c4e16ffe527d837425003d325c18fcb959cdaffdf9215",
  "pubkey_3": "0348a2251a9752830363300b9ac6f8ff7201e1932a2bb72ba9e00d1685d0bee6c6",
  "pubkey_4": "033fdbee6157b5e35e33c4d8541f42c0a7096dad480e44b0fb74818743ca45a275"
}
```

## NUT-20 (quote locking) key derivation

Using [NUT-XX](../XX.md) derivation with DST `Cashu_KDF_HMAC_SHA256_NUT20`, we derive values starting from the following BIP39 mnemonic:

```json
{
  "mnemonic": "half depart obvious quality work element tank gorilla view sugar picture humble",
  "seed_hex": "dd44ee516b0647e80b488e8dcc56d736a148f15276bef588b37057476d4b2b25780d3688a32b37353d6995997842c0fd8b412475c891c16310471fbc86dcbda8"
}
```

The compressed public keys derived for the first five counters from `counter=0` to `counter=4` are:

```json
{
  "pubkey_0": "020509f7911de3c948ba971938cee5f588d3d3a41c13bc7bb308823896c5778c32",
  "pubkey_1": "023b614a85de226083698217bcf3b1f84d91c91846629491342b7134eb849af18a",
  "pubkey_2": "03668b29ad91a1763afa773ade6920106d10edb3b378c2f2ddc0b8e65fd3b5e23c",
  "pubkey_3": "0262a8ce41fe91e9856e29c0f447db4d968d5db55c2400eb5c5c2cd3cec80227dd",
  "pubkey_4": "025f78058b39825e2e575a501319d8b3510387be6c7f9245037a38b76fa29cb12a"
}
```
