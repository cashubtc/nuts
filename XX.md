# NUT-XX: Offline Spillman (unidirectional) channel 

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), (and probably NUT-09) too`

_2025-11-01: we'll likely make a change to this, by signing over _all_ inputs, not just the inputs that are sufficient to cover Bob's latest balance.
Combined with the restore endpoint (NUT-09), Alice will be able to get her refund immediately in the case of an uncooperative close.`._

---

Alice and Bob wish to set up a payment channel, funded by Alice, such that Bob's balance starts at zero and his balance
increases (unidirectional) over time. This is 'offline' because it allows - once the channel has been
set up - for the two parties to transact simply by Alice sending signatures to Bob which Bob can verify
without needing to contact the mint after each micropayment.

Both parties trust the mint, but not each other. This works with any mint that supports NUT-11 and NUT-12.

Bob can then unilaterally exit at any time, by taking the latest signature to the mint.
If, after this exit, Bob doesn't sign a transaction which releases Alice's remaining balance to her immediately,
she can redeem the remainder after a certain pre-defined time has elapsed.

One simple alternative is for Alice to prepare a large number (millions perhaps) of tiny-amount proofs
in advance. However, that requires a lot of bandwidth and places heavy strain on the mint.
This NUT describes how a smaller set of proofs, of various amounts, can solve the same
problem, allowing potentially billions of payments with only a few dozen proofs.

# The channel

Alice takes Bob's public key and 'outputs' provided by him and, with any mint supporting NUT-11, creates a set of 2-of-2 multisig proofs
of various amounts, where both Alice and Bob's signature is needed to redeem.
Each of these proofs refunds to Alice after a pre-defined 'locktime' (e.g. one week).
Before the locktime, the proofs can only be redeemed with a signature from both. After the locktime, Alice's signature is sufficient.
`SIG_ALL` is used, for reasons described in 'double-spending' below.
The signature scheme and locktime and `SIG_ALL`, are as described in NUT-11.

The details of the amounts and outputs are described next.

## Amounts, and the details of opening and funding the channel

_This assumes that 1 millisat is the smallest 'resolution' of interest, but another resolution may be agreed_

_This assumes that the mint's amounts are in powers of two. While that appears to be the typical case, it's not required by the protocol_

There shall be _2_ such proofs with 1-millisat value, and one proof for every other power of 2: 2-millisats, 4-millisats, 8-millisats, ..., up to some pre-agreed maximum.
The total value of all those proofs is the channel capacity and is the maximum amount that Alice can send to Bob through this channel.

First, Bob prepares his outputs (BlindedMessage), one for each of those amounts (two 1-millisat outputs).
These are where Bob's final balance will be sent. Bob is free to choose any output, and will typically prepare an anyone-can-spend output with a random secret that he created.

Alice then takes Bob's outputs and funds a 'swap' with her own inputs. The result is a set of proofs with the 2-of-2-multisig rules mentioned above, including the refund to Alice after a locktime has expired.

Alice then sends all those proofs to Bob. Bob can verify all of these proofs with the mint using NUT-12, and also check  that the signatures and locktimes have been set up correctly, before going offline.

One of these 1-millisat proofs is a special proof that will be included in every transaction.

# transactions

To update the balance, Alice shall take the special 1-millisat proof mentioned above, and combine it with
whatever subset of the other proofs is needed to reach the new balance, and sign the combination spending those proofs to the corresponding outputs prepared by Bob, and give the signature to Bob.
For example, to update the balance to 16 msat, Alice will take the special proof and the unique set of proofs which add to 15, because 16=1+15=1+1+2+4+8.

Bob can verify this signature offline. Bob _could_ sign this transaction himself immediately and 'swap' it for the proofs, but he will not do so until he is ready to exit and close the channel.

For each update, Alice simply sends a number recording the new balance, and her signature on the updated transaction. That is sufficient to allow Bob to construct the updated transaction and verify the signature; he has the same proofs and outputs that Alice is working on and therefore he can reconstruct the same updated transaction that Alice just signed.
This can allow a very high frequency of updates

# double-spending, and unidirecionality

As Alice is using SIG_ALL, and the special 1-millisat proof is used in all of the transactions,
Bob can redeem only one of the transactions. If he attempts to redeem a second transaction, he will need to
include the special proof (SIG_ALL), and the mint will see that the special proof has already been redeemed.
As he can only redeem one transaction, and therefore one set of proofs that were signed together, he will redeem
the most valuable transaction.
This explains why these are unidirectional.

# cooperative channel close

The above gives Bob unilateral exit with immediate access. Alice has to wait some time before she can collect the refund.
When closing the channel, Bob should sign a similar transaction returning the remaining proofs to Alice,
but we cannot force him to do so and therefore Alice may need to way until the locktime has expired.

# proof-of-concept

There is a proof of concept based on the CDK, showing how both parties can do the verification at each step. TODO: link to it
