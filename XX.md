# NUT-XX: Offline Spilman (unidirectional) channel

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), NUT-09 (restore signatures), NUT-07 (token state check) (NUT-17 is beneficial, but not required)`

---

This describes how Alice can set up a one-way payment channel from herself to Charlie.
Using public information such as Charlie's public key and his preferred mints,
Alice prepares a _funding token_
and she can send an initial payment to Charlie without any prior involvement from Charlie.

Throughout the lifetime of the channel, Alice signs transactions which redistribute
the value in that funding token between herself and Charlie,
where each transaction increases the balance in favour of Charlie.

Charlie does not need to trust Alice; he can verify each transaction in the
channel locally without needing to check anything with the mint.

Charlie can unilaterally exit at any time, by adding his signature to the most recent
signature from Alice and swapping the _funding token_ for the outputs.
Alice can then immediately claim her balance, even if Charlie does not cooperate with her.

The mint, Bob, is involved only at the start for the initial swap where Alice prepares
the _funding token_, and at the end where each of the two parties swap their
final balances into their wallets.

# Exiting and fees, and the capacity of the channel

There is an ASCII art diagram below, showing all the fees and the two-stage exit process.

When the channel is closing, there are two stages, and there are fees to be paid
in each of those two stages.
In the first stage, the _funding token_ token is swapped to create the _deterministic outputs_
(defined below) for each of the two parties.
Some of the deterministic outputs are P2PK-locked to Charlie's public key, and the remainder
are of the deterministic outputs are P2PK-locked to Alice's public key.

All the proofs in the _funding token_ are in the same _active_ keyset, with fee rate `input_fee_ppk`.
If there are `n_funding_proofs` proofs in that funding token, the fees of that first stage are
`(input_fee_ppk * n_funding_proofs + 999) // 1000`,
where `//` rounds non-integer results down to an integer.

In the second stage of the exit, Alice and Charlie swap their deterministic outputs
for conventional anyone-can-spend proofs.
This also requires paying fees. These deterministic outputs are also in the same keyset as the funding token.

The method for constructing the deterministic outputs is described in more detail later in this document.
For now, we focus on the fees.
Consider a function `deterministic_value_after_fees(x)` which constructs the
deterministic outputs with _nominal_ value `x` and then substracts the fees that would
result from swapping those deterministic outputs.
Where `num_deterministic_outputs(x)` is the number of outputs needed,

```
deterministic_value_after_fees(x)
  =
    x - (input_fee_ppk * num_deterministic_outputs(x) + 999) // 1000
```

To ensure that Charlie's final balance is `charlies_balance`, Alice must compute the inverse
of `deterministic_value_after_fees`, i.e. `x = inverse_deterministic_value(charlies_balance)`,
which is the smallest `x` such that `deterministic_value_after_fees(x) = charlies_balance`.

To make a payment which brings Charlie's balance to `charlies_balance`, the following summarizes the values and fees:

 - `charlies_balance`, we start our computation with this, the balance that we wish Charlie to have in this transaction.
 - `x` = `inverse_deterministic_value(charlies_balance)`, the nominal value of Charlie's deterministic outputs.
 - `y` = `funding_token_total_value - x - (input_fee_ppk * n_funding_proofs + 999) // 1000`, the value that is left in the funding token to create Alice's deterministic outputs, after the remaining value is used for paying fees and creating Charlie's deterministic outputs.
 - Alice is then left with `deterministic_value_after_fees(y)`, the final amount left in her wallet after swapping her determististic outputs into her wallet

If the nominal value of the funding token is `total_value_of_funding_token`, then Charlie's maximum balance is

```
capacity
 = 
   deterministic_value_after_fees(total_value_of_funding_token - (input_fee_ppk * n_funding_proofs + 999) // 1000)
```

This `capacity`, and also represents that value that Alice can reclaim if the channel is closed
with `charlies_balance = 0`.

## Fee and value distribution diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FUNDING TOKEN                                   │
│                  (total_value_of_funding_token)                         │
│                                                                         │
│  Created by Alice with P2PK proofs requiring both signatures (SIG_ALL)  │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ STAGE 1 of channel closure: Swap funding token
                                  │
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
    ┌───────────────────┐  ┌──────────────┐  ┌───────────────────┐
    │ Charlie's         │  │  Stage 1     │  │ Alice's           │
    │ Deterministic     │  │  Fees        │  │ Deterministic     │
    │ Outputs           │  │  (to mint)   │  │ Outputs           │
    │ (nominal value x) │  │              │  │ (nominal value y) │
    │                   │  └──────────────┘  │                   │
    │ P2PK locked to    │                    │ P2PK locked to    │
    │ Charlie           │                    │ Alice             │
    └───────────────────┘                    └───────────────────┘
                    │                                    │
                    │ STAGE 2:                           │ STAGE 2:
                    │ Charlie swaps                      │ Alice swaps
                    │ his outputs                        │ her outputs
                    │                                    │
              ┌─────┴─────┐                        ┌─────┴─────┐
              │           │                        │           │
              ▼           ▼                        ▼           ▼
        ┌─────────┐ ┌──────────┐            ┌─────────┐ ┌──────────┐
        │Charlie's│ │Charlie's │            │ Alice's │ │ Alice's  │
        │ Final   │ │ Stage 2  │            │ Final   │ │ Stage 2  │
        │ Balance │ │ Fees     │            │ Balance │ │ Fees     │
        │         │ │          │            │         │ │          │
        └─────────┘ └──────────┘            └─────────┘ └──────────┘

Where:
  Stage 1 Fees = (input_fee_ppk * n_funding_proofs + 999) // 1000
  x = inverse_deterministic_value(charlies_balance)
  y = total_value_of_funding_token - x - stage1_fees
  Charlie's Stage 2 Fees = (input_fee_ppk * num_outputs(x) + 999) // 1000
  Alice's Stage 2 Fees = (input_fee_ppk * num_outputs(y) + 999) // 1000
  charlies_balance = deterministic_value_after_fees(x) = x - Charlie's Stage 2 Fees
  Alice's final balance = deterministic_value_after_fees(y) = y - Alice's Stage 2 Fees

Maximum Charlie can receive (capacity):
  = deterministic_value_after_fees(total_value_of_funding_token - stage1_fees)
```

.... TODO: tidy up the remainder of this, especially to sync with the fees issue discussed above

... TODO: recommend that the first payment be for zero sats, to allow the channel to be instantly closed if Charlie is unable to provide service now. Typically, therefore, Alice will provide two payments immediately the at the start ...


# The channel parameters, and channel_id

Knowing Charlie's public key, and the set of mints and _units_ that are trusted by Charlie, and a minimum channel lifetime that Charlie requires, Alice defines the channel parameters as follows:

 - `sender_pubkey`: Alice's key ?how exactly to encode this?
 - `receiver_pubkey`: Charlie's key ?how exactly to encode this?
 - `mint` string: URL of mint
 - `unit`: typically `sat` or `msat`
 - `total_value_of_funding_token`
 - `capacity`: the maximum balance that will be payable to Charlie. Equals `total_value_of_funding_token - (input_fee_ppk * n_funding_proofs + 999) // 1000`, where `n_funding_proofs` is the number of proofs in the funding token.
 - `active_keyset_id`: An _active_ keyset for that unit at that mint
 - `input_fee_ppk`: As all the proofs in the funding token, and in the deterministic outputs, are in the same keyset, the `input_fee_ppk` is fixed.
 - `expiry`  unix timestamp: If Charlie doesn't close before this time, Alice can re-claim all the funds after this has expired
 - `setup_timestamp`: unix timestamp: the time when Alice is setting up this channel
 - `sender_nonce`: Random data selected by Alice to add more randomness. May be useful if Alice and Charlie have multiple concurrent channels.

The `channel_id` is the SHA256 hash of the '|'-delimited concatenation of all the above.

_TODO: should the channel parameters have a `maximum_output_size`, to put an upper bound on the size of any deterministic output? This could help a little with privacy._

# Funding the channel

Alice, with the mint, creates a _funding token_ worth `total_value_of_funding_token` units.
Each proof in this token is a P2PK (NUT-11) proof which requires both signatures
before the expiry of the channel, and where Alice's signature alone is sufficient after the expiry:

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

## deterministic outputs

To construct the deterministic outputs, i.e. the set of _Blinded Messages_ that
transfer a given amount to one of the two parties, we start with the set
of amounts that are available in the keyset of the `active_keyset_id`.

While it is common for mints to use powers-of-2, it is not required.

Remember, the 'outputs' described here are just BlindedMessages and their blinding factors
that are computed by Alice and Charlie.
They are _not_ sent to the mint until Charlie decides to exit; many of the outputs computed
during the lifetime of a channel will never be seen by the mint.

For a given target amount (Charlie's balance, or Alice's remainder),
we first identify the largest amount in the keyset which is less than
the target amount. We'll use as many proofs as possible of this largest
amount, as long as we don't exceed the target.

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

In our 543-sat example, where the available amounts are powers of 10, there are 12 determistic outputs:

```
amount | index
100    |     0
100    |     1
100    |     2
100    |     3
100    |     4
10     |     0
10     |     1
10     |     2
10     |     3
1      |     0
1      |     1
1      |     2
```

_TODO? Optional: If Charlie, along with his public key, advertizes that he supports pay-to-blinded-pubkey, we could determistically compute an ephemeral private key for blinding, and include the corresponding ephemeral public key in the proof, as per the P2BPK NUT_

The corresponding blinding factor is `SHA256(channel_id || pubkey || amount || "blinding" || index)`,
and so the deterministic output (BlindedMessage) is contructed by applying that
blinding factor to that secret in the usual way.

That describes how Charlie's balance is paid in the commitment transaction.
The same process is applied to send the remainder to Alice.

# Commitment transaction, and balance update, in detail

The commitment transaction can now be specified more clearly.
It is a _swap_ which takes the _funding proof_ as input.
The outputs start with the payments to Charlie, ordered
by decreasing amount and then by increasing index, followed by Alice's outputs similarly ordered.

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
Alice can iterate over the amounts available in this keyset, and - for each amount - loop over the indices
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

# Charlie's security

To ensure that Charlie can trust that a given payment is valid without needing to check
with the mint, Charlie should be careful to check everything.

Charlie should maintain a mapping from the channel_id to the balance, to ensure that
Alice doesn't attempt to decrease the balance in his favour.
This map should also store the channel parameters.

As the expiry time approach, Charlie should close the channel as he will lose the balance if the
expiry time is reached.
When Charlie closes the channel, he should keep a set of all the closed channels to avoid
Alice reusing a closed channel.

The record of a closed channel should not be deleted until after it has expired.

If Alice pays using a channel that is not in either of the two datasets mentioned above,
then Alice appears to be opening a new channel, and Charlie should check:
 - that the expiry time is reasonably far in the future
 - that the mint is a mint that he trusts, and the keyset is active
 - that the channel_id is computed correctly
 - the DLEQ proofs in the funding token are correct
 - The proofs in the funding token have the correct P2PK setup, with the keys and expiry and so on

# proof-of-concept

_This PoC is now (2025-11-23) quite out of date. It has deterministic outputs and so on, and makes use of NUT-09 and NUT-07, but it doesn't follow the above closely_

There is a proof of concept based on the CDK, showing how both parties can do the verification at each step, also including
the latest SIG_ALL message update. _TODO: link to it. As of 2025-11-02, it's implemented and working with this new deterministic output setup, but the latest code isn't on github yet_
