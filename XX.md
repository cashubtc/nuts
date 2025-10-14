# NUT-XX: Offline Spillman (unidirectional) channel 

`optional`

`depends on: NUT-11`

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

Bob can verify all of these proofs with the mint, before going offline.

# transactions

To update the balance, Alice shall take the special 1-millisat proof mentioned above, and combine it with
whatever subset of the other proofs is needed to reach the new balance, and sign the combination and give the
signature to Bob. Bob can verify this signature offline

# double-spending, and unidirecionality

As Alice is using SIG_ALL, and the special 1-millisat proof is used in all of the transactions,
Bob can redeem only one of the transactions. If he attempts to redeem a second transaction, he will need to
include the special proof (SIG_ALL), and the mint will see that the special proof has already been redeemed.
As he can only redeem one transaction, and therefore one set of proofs that were signed together, he will redeem
the most valuable transaction. This explains why these are unidirectional.

# Fees

???
