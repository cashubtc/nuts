# NUT-XX: Token non-adjacent form (NAF)

`optional`

---

This NUT proposes a more compact scheme for representing token amounts using powers of two.

---

Every natural number has a unique binary representation, which means it can be written as a sum of distinct powers of two. This is a common way of choosing proof amounts when constructing a token.

With this scheme, the token ends up containing as many proofs as there are 1s in the binary representation of the token amount. To minimize the number of proofs in a token and thereby the size of the token, we need a more compact way to encode the token amount.

The non-adjacent form (NAF[^1]) is the signed binary (-1, 0, 1) representation of an integer. It has three useful properties for our use-case:

First, for any token amount, the NAF form is more compact or at worst the same size as in the binary scheme. The NAF form has a Hamming weight (number of non-zero symbols) less than or equal to that of the binary representation. Since the zero elements have no bearing on the size of the token, this means there is no token amount for which the NAF representation is larger than the binary scheme.

Second, tokens using NAF are on aggregate `1/6 = ~16%` more compact than those using the binary scheme. If the token's value has `k` binary digits, the Hamming weight of its binary representation is on average `k/2`. Using the NAF representation, it's on average `k/3`. This means the number of proofs used to build the token amount is on average `1/2 - 1/3 = 1/6` times lower.

Third, it requires only 2x more signatures in a keyset than the binary scheme.


### Mint Considerations

To support this, the mint's keyset has to include signatures for all powers of 2 between `-2^n` to `2^n`.


### Wallet Considerations

To construct tokens using this scheme, wallets will need outputs for negative amounts. They can get negative outputs when swapping or minting. For example, when minting a token of amount `5`, the output amounts could be `[1, 4, -1, 1, -2, 2, -4, 4]` instead of `[1, 4]`.



[^1]: For theoretical background and algorithms on how to efficiently calculate the NAF, see https://phlay.de/post/non-adjacent-form/