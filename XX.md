# NUT-XX: Offline Spillman (unidirectional) channel 

`optional`

`depends on: NUT-11, NUT-12`

---

Alice and Bob wish to set up a payment channel, such that Bob's balance starts at zero and his balance
increases (unidirectional) over time. This is 'offline' because it allows - once the channel has been
set up - for the two parties to transact simply by Alice sending signatures to Bob which Bob can verify
without needing to contact the mint after each micropayment.

Bob can then unilaterally exit at any time, by taking the latest signature to the mint.
Alice can redeem the remainder after a certain pre-defined time has elapsed. A collaborative exit is
also possible, allowing both parties to immediately redeem their closing balances.

One simple alternative is for Alice to prepare a large number (millions perhaps) of tiny-denomination proofs
in advance. However, that requires a lot of bandwidth and places heavy strain on the mint.
This NUT describes how a smaller set of proofs, of various denominations, can solve the same
problem, allowing potentially billions of payments with only a few dozen proofs.

# Opening the channel

Alice takes Bob's public key and, with any mint supporting NUT-11, creates a set of 2-of-2 multisig proofs
of various denominations, where both Alice and Bob's signature is needed. Each of these proofs refunds to Alice after a pre-defined time (e.g. one week).
SIG_ALL is used.

## Denominations

_This assumes that 1 millisat is the smallest 'resolution' of interest, but another resolution may be agreed_

Alice shall prepare _2_ such proofs with 1-millisat value.
One of these 1-millisat proofs is a special proof that will be included in every transaction.
Alice shall prepare one proof for every other power of 2: 2-millisats, 4-millisats, 8-millisats, ..., up to some pre-agreed maximum.
The total value of all those proofs is the channel capacity and is the maximum amount that Alice can send to Bob through this channel

Bob can verify all of these proofs with the mint using NUT-12, before going offline.

When both Alice and Bob have all the following, the channel is open:

 - Bob prepares one _output_ for each of the proofs that Alice prepares. These are where Bob's final balance will be sent. In principle, Bob is free to choose any output, but Alice may require that they are locked up for a period of time in order to give Bob an incentive to cooperate with a cooperative close.
 - The proofs prepared prepared by Alice, each one based on an output prepared by Bob, which Bob can verify with the mint

# transactions

To update the balance, Alice shall take the special 1-millisat proof mentioned above, and combine it with
whatever subset of the other proofs is needed to reach the new balance, and sign the combination spending those proofs to the corresponding outputs prepared by Bob, and give the signature to Bob. Bob can verify this signature offline

For each update, Alice simply sends a number recording the new balance, and her signature on the updated transaction. That is sufficient to allow Bob to construct the updated transaction and verify the signature. This can allow a very high frequency of updates

# double-spending, and unidirecionality

As Alice is using SIG_ALL, and the special 1-millisat proof is used in all of the transactions,
Bob can redeem only one of the transactions. If he attempts to redeem a second transaction, he will need to
include the special proof (SIG_ALL), and the mint will see that the special proof has already been redeemed.
As he can only redeem one transaction, and therefore one set of proofs that were signed together, he will redeem
the most valuable transaction. This explains why these are unidirectional.

# cooperative channel close

The above gives Bob unilateral exit with immediate access. Alice has to wait some time before she can collect the refund

