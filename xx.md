# NUT-XX: External Fee

`optional`

`depends on: NUT-10`

---

## Summary

This NUT describes a external bitcoin transaction fee witch is one kind of spending condition based on NUT-10 well-known `Secret`. Using external fee, we can lock eCash `Proofs` (see NUT-00) to a receiver that include a specified transaction into a block. The spending condition is enforced by the mint.

Caution: if the mint does not support this type of spending condition, `Proofs` may be treated as regular anyone-can-spend proofs. Applications must ensure that the mint supports a specific kind of spending condition by checking the mint's info endpoint.

## Definition

NUT-10 Secret `kind: BTCFEE`

If for a `Proof`, `Proof.Secret` is a `Secret` of kind `BTCFEE`, the proof must be unlocked by providing a `Proof.witness` with a valid `Proof.witness.preimage` and a valid `Proof.witness.blockhash`. We can have a optional extra value `Proof.Secret.confirmations` that is validate the minimum block validations on chain.

Example of `Secret`:

```json
[
  "BTCFEE",
  {
    "nonce": "00001",
    "data": "0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000",
    "tags": [
      ["confirmations", "1"],
      ["locktime", "1767031051"],
      [
        "refund",
        "0311db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5c"
      ]
    ]
  }
]
```

- `data` is the `rawtx`
- `tags`:
  - `confirmations`: Transactions block confirmations to unlock eCash transaction
  - `locktime`: A lock time to refund system, 
  - `refund`: The public key for unlock eCash when `locktime` is expired

## Spending BTCFEE Proofs

A `Proof` with a `Secret` of kind `BTCFEE` can be spent in two ways:

### Receiver Pathway (mine block with transaction)

The receiver(s) can spend the proof by providing:
- The blockhash from mined block
- A valid preimage for hash inside `scriptSig` field in the mined block with containing the transaction

### Sender Pathway (timelocked refund)

The sender(s) listed in the `refund` can spend the proof once the `locktime` lock has "expired" by providing signature(s) as per the NUT-11 rules for *Refund MultiSig*.

## Witness format

`BTCFEEWitness` is a serialized JSON string of the form

```json
{
  "blockhash": <hex_str>,
  "preimage": <hex_str>
}
```

The witness for a spent proof can be obtained with a `Proof` state check (see NUT-07).

## Mint info setting

The NUT-06 `MintMethodSetting` indicates support for this feature:

```json
{
  "xx": {
    "supported": true
  }
}
```
