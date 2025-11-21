# NUT-XX: Offline Spilman (unidirectional) channel

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), NUT-09 (restore signatures), NUT-07 (token state check) (NUT-17 is beneficial, but not required)`

_TODO: who pays the fees? (see the multi-swap zero-receiver-setup deterministic outputs below) If Alice spends 101 sats to fund the 'funding token' which has a _nominal_ value of 100 sats, and Charlie's exit with the full capacity gives him just nominal 99 sats in his 1-of-1 P2PK outputs, which decrease to 98 sats when he finally swaps them to anyone-can-spend tokens in his wallet, then who should pay those fees? Which of those four numbers is the capacity of the network?_

_TODO: question for the reviewer: Could we use pay-to-blinded-pubkey here? Where exactly? And should we make P2BPK required or optional?_

---

Alice and Charlie wish to set up a payment channel, funded by Alice, such that Charlie's balance starts at zero and his balance
increases (unidirectional) over time. This is 'offline' because it allows - once the channel has been
set up - for the two parties to transact simply by Alice sending signatures to Charlie which Charlie can verify
without needing to contact the mint after each micropayment.
A small number of swaps are needed to setup and to close the channel, but there is no mint involvement
while the channel is open and while the channel payments are made.

Knowing only Charlie's pubkey and a mint trusted by him, Alice can set up the channel - via one swap with the mint - and make the
first payment to Charlie without any setup from Charlie.

# Trust

Both parties trust the mint, but not each other.
Charlie can unilaterally exit at any time, by adding his signature to Alice's and swapping at the mint.
That swap will spend all the 'funding proofs' that Alice prepared in the funding token, and the swap
will also unlock Alice's outputs allowing her to immediately exit with her balance.

If Charlie never exits, then - after the predefined locktime has expired - all the funding becomes spendable
by Alice alone, allowing her to reclaim her funds.

# The channel parameters, and channel_id

Knowing Charlie's public key, and the set of mints and _units_ that are trusted by Charlie, and a minimum channel lifetime that Charlie requires, Alice defines the channel parameters as follows:

 - `sender_pubkey`: Alice's key ?how exactly to encode this?
 - `receiver_pubkey`: Charlie's key ?how exactly to encode this?
 - `mint` string: URL of mint
 - `unit`: typically `sat` or `msat`
 - `capacity`: the number of sats in the _funding token_ that Alice will create while funding the channel. _**If the fees are non-zero, Charlie's maximum possible balance will be less than the `capacity`**_
 - `active_keyset_id`: An _active_ keyset for that unit at that mint
 - `expiry`  unix timestamp: If Charlie doesn't close before this time, Alice can re-claim all the funds after this has expired
 - `setup_timestamp`: unix timestamp: the time when Alice is setting up this channel
 - `sender_nonce`: Random data selected by Alice to add more randomness. May be useful if Alice and Charlie have multiple concurrent channels.

The `channel_id` is the SHA256 hash of the '|'-delimited concatenation of all the above.

# Funding the channel

Alice, with the mint, creates a _funding token_ worth `capacity` units.
Each proof in this token is a P2PK (NUT-11) proof which requires both signatures
before the expiry of the channel, and where Alice's signature alone is sufficient afterwards:

 - `data`: Alice's key
 - `pubkeys`: Charlie's key
 - `n_sigs`: 2
 - `locktime`: the `expiry` timestamp defined in the channel parameters
 - `refund`: Alice's key
 - `sig_flag`: `SIG_ALL`


# Charlie's verification

The following information should be sent to Charlie with, or before, the first payment in this channel,
enabling Charlie to verify everything. He can verify without communicating with the mint:

 - the channel parameters
 - the funding token, including the DLEQ proofs (NUT-12) allowing Charlie to verify that the funding proofs have been signed.

Both sides should store the funding proofs in the order that Alice created them, to ensure both sides can construct the relevant transactions deterministically.

# Payments

Each payment requires Alice to update the balance and then construct the updated
'commitment' transaction. She then signs the transaction and sends her signature
and the new balance to Charlie. This signature and amount, combined with the channel parameters,
is sufficient for Charlie to reconstruct the commitment transaction and verify the signature

The commitment transaction spends all of the _funding token_, sending Charlie's balance
to deterministic outputs (defined below) that only Charlie can redeem, and the remainder
are sent to deterministic outputs that are redeemable only by Alice

## determistic outputs

To construct the deterministic outputs, i.e. the set of _Blinded Messages_ that
transfer a given amount to one of the two parties, we start with the set
of amounts that are available in the keyset of the `active_keyset_id`.

While it is common for mints to use powers-of-2, it is not required. (TODO: or is it?)

Remember, the 'outputs' described here are just BlindedMessages and their blinding factors
that are computed by Alice and Charlie.
They are _not_ sent to the mint until Charlie decides to exit; many of the outputs computed
during the lifetime of a channel will never be seen by the mint.

For a given target amount (Charlie's balance, or Alice's remainder),
we first identify the largest amount in the keyset which is less than
the target amount. We'll use as many proofs as possible of this largest
amount, as long as we don't exceed the target.

_TODO: don't forget about fees!_

For example, if the target is 543 sats, and the keyset has powers of 
ten (1, 10, 100, 100 ...) as the amounts, then we'll use 5 of the 100-sat
proofs.

The remainder, 43 in this example, will undergo the same process, taking
as many copies as possible of the next biggest amount until the target
is reached.

As 543 = 5 * 100 + 4 * 10 + 3 * 1 in this example, the outputs will
be created an ordered from smallest to biggest

1, 1, 1, 10, 10, 10 , 10,  100, 100, 100, 100, 100

Assuming these outputs are for Charlie (the same procedure will be repeated for Alice's remainder),
each output is created deterministically.
Everything about the output (the secret, the BlindMessage, and the blinding factor)
can be constructed by either party (and by any third party that knows all the channel parameters).

When contructing the four 10-sat amounts, in this example, we have an _index_
ranging from 0 to 3 inclusive to identify each of those four outputs.
(Where the keyset amounts are just powers of 2, the index will never be non-zero.)
Each output will be constructed as follows: the channel_id, pubkey(Charlie in this case), amount (in this example, the power of ten), and the index are combined and hashed to compute the _deterministic nonce_ `SHA256(channel_id || pubkey || amount || "nonce" || index)`

Deterministic Secret:

```
[
  "P2PK",
  {
    "nonce": "<deterministic nonce computed above>",
    "data": "<Charlie's pubkey>",
    "tags": [["sigflag", "SIG_INPUTS"]]
  }
]
```

The corresponding blinding factor is `SHA256(channel_id || pubkey || amount || "blinding" || index)`,
and so the deterministic output (BlindedMessage) is contructed by applying that
blinding factor to that secret in the usual way.

That describes how Charlie's balance is paid in the commitment transaction.
The same process is applied to send the remainder to Alice.

# Commitment transaction, and balance update, in detail

The commitment transaction can now be specified more clearly.
It is a _swap_ which takes the _funding proof_ as input.
The outputs start with the payments to Charlie, ordered
by amount and then by index, followed by Alice's outputs similarly ordered.

Alice then signs this (SIG_ALL). Alice can then send three pieces of data to Charlie: the `channel_id`, the balance for Charlie, and her signature.

As already mentioned, Alice must send the full set of channel parameters to Charlie in the first payment -
if she hasn't already sent them beforehard - but after this it is sufficient for her to send those
three pieces of data.

Charlie can reconstruct the transaction and verify the signature.

Charlie should maintain a dictionary mapping the `channel_id` to the current balance of that channel,
in order to ensure that Alice doesn't decrease the balance and to allow him to identify
the magnitude of the increase in each payment.
This map doesn't need to store any channels that have expired.

# Closing the channel

Most of the commitment transactions are never sent to the mint.

When Charlie exits, he adds his signature to Alice's on the most recent transaction and sends the complete
swap to the mint. This swap spends the _funding token_ and returns
blind signatures (the deterministic outputs, signed by the mint) for both parties.

As the swap spends the entire funding token, Alice can detect Charlie's spend
via NUT-07 (token state check). NUT-17, if supported by the mint, helps here too.

Charlie should return Alice's blind signatures to her, but if he doesn't then Alice
can use NUT-09 to restore the signatures.
While we assume that Charlie will usually take the most recent commitment, as it's
the most valuable, it is not guaranteed that he will do that.
Alice can iterate over the amounts, and - for each amount - loop over the indices
in order to reconstruct the deterministic output and restore the signature.
When a given restoration fails, she can stop increasing the _index_ and
move on to the next amount instead.

```
for amount in amounts_in_this_keyset:
    index = 0
    while True:
        if (restore fails for this 'amount' and this 'index'):
            continue # to the next amount
        else:
            .. unblind the signature and add the proof to Alice's wallet
```

# Expiry

Charlie should remember to close channels as the expiry time closes.
He should also keep a record of channel_ids that he has closed, where
the expiry time has not been reached, in order to ensure that
Alice does not attempt to reuse a channel that was already closed.


# Channel capacity

The channel capacity is ??? _depends on the fee policy. As mentioned at the top, there are mulitiple swaps; how is responsible for
paying all those swaps?_

# proof-of-concept

_This PoC is now (2025-11-17) quite out of date. It has deterministic outputs and so on, and makes use of NUT-09 and NUT-07, but it doesn't follow the above closely_

There is a proof of concept based on the CDK, showing how both parties can do the verification at each step, also including
the latest SIG_ALL message update. _TODO: link to it. As of 2025-11-02, it's implemented and working with this new deterministic output setup, but the latest code isn't on github yet_
