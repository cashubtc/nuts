# NUT-XX: Offline Spilman (unidirectional) channel

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), NUT-09 (restore signatures), NUT-07 (token state check) (NUT-17 is beneficial, but not required)`

---

_TODO: For a little more privacy (for those not using P2BPK) Alice and Charlie could easy specify two public keys, one for the 2-of-2 multisig in the funding and another in the 1-of-1 multisig that pays to each specificcally. What do you think?_

This describes how Alice can set up a one-way payment channel from herself to Charlie.
Using public information such as Charlie's public key and his preferred mints and keysets,
Alice prepares a _funding token_
and she can send an initial payment to Charlie without any prior involvement from Charlie.

Throughout the lifetime of the channel, Alice signs transactions which redistribute
('commit') the value in that funding token between herself and Charlie,
where each transaction increases the balance in favour of Charlie and decreases hers.

Charlie does not need to trust Alice; he can verify each transaction in the
channel locally without needing to check anything with the mint.
He does not need to contact the mint until he decides to close the channel.

Charlie can unilaterally exit at any time, by adding his signature to the most recent
signature from Alice and swapping the _funding token_ for the outputs.
Alice can then immediately claim her balance, even if Charlie does not cooperate with her.

The mint, Bob, is involved only at the start for the initial swap where Alice prepares
the _funding token_, and at the end where each of the two parties swap their
final balances into their wallets.

# Exiting, fees, the `capacity` of the channel, and "impossible" balances

This text is followed by an ASCII art diagram, showing all the fees and the two-stage exit process.

An important parameter is the `capacity`; it's the maximum balance that can be sent to Charlie in this channel.
If the fee-rate is non-zero, then Alice is responsible for the fees, as described here:

When the channel is closing, there are two stages, and there are fees to be paid
in each of those two stages.
In the first stage, the _funding token_ token is swapped to create the _commitment outputs_
for each of the two parties.
Some of the commitment outputs are P2PK-locked to Charlie's public key, and the remainder
are of the commitment outputs are P2PK-locked to Alice's public key.
This first swap will cost fees.

In the second stage of the exit, Alice and Charlie each separately swap their commitment outputs - which are locked to them via 1-of-1 P2PK -
for conventional anyone-can-spend proofs to store in their wallet.
This second swap also requires paying fees.

All of the P2PK outputs discussed above, those in the _funding token_ and in the
_commitment outputs_, are in the same keyset and therefore a single feerate `input_fee_ppk`
applies to all.

The method for constructing the _secrets_ and _blinding factors_ for all those P2PK
outputs is deterministic; the details and motivation are given below.
With this determinism, there is a function `deterministic_value_after_fees(x)`
which computes the 'post-swap' value of proofs where the proofs are deterministically
constructed to have total nominal value `x`.
Where `num_deterministic_proofs(x)` is the number of outputs required by this
deterministic algorithm, we can implement `deterministic_value_after_fees(x)` as

```
deterministic_value_after_fees(x)
  =
    x - (input_fee_ppk * num_deterministic_outputs(x) + 999) // 1000
```

We also have a function to invert that, `inverse_deterministic_value`,
to find the smallest `y` such that `deterministic_value_after_fees(y) >= x`
Notice the `>=`, not `=`, in that previous paragraph.
Sometimes, due to fees, there is no value `y` for which equality can be attained;
in this case Charlie will find he is slightly overpaid as the desired balance
is impossible.

As there are two stages to the swapping, and each costs fees, Alice must
create the _funding token_ with value:

```
total_funding_token_amount = inverse_deterministic_value(inverse_deterministic_value(capacity))
```

The fees in the first stage will always be `total_funding_token_amount - deterministic_value_after_fees(total_funding_token_amount)`.
The fees in the second stage can vary, as they depend on the distribution between the two parties.

To make a payment which brings Charlie's balance to `charlies_balance`, the following describes how Alice computes the values of the various parts. Where `deterministic_value_after_fees(total_funding_token_amount)` is the nominal value when the _funding token_ goes through the first swap:

 - `charlies_balance`, we start our computation with this, the balance that we wish Charlie to have in this transaction.
 - `p` = `inverse_deterministic_value(charlies_balance)`, the nominal value of Charlie's commitment outputs.
 - `q` = `deterministic_value_after_fees(total_funding_token_amount) - p`, the value that is left from the funding token to create Alice's commitment outputs, after the fees and creating Charlie's commitment outputs.
 - Alice is then left with `deterministic_value_after_fees(q)`, the final amount left in her wallet after swapping her commitment outputs into her wallet

## Fee and value distribution diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FUNDING TOKEN                                   │
│                  (total_funding_token_amount)                           │
│                                                                         │
│  Created by Alice with P2PK proofs requiring both signatures (SIG_ALL)  │
│  After the expiry time, Alice's signature alone is sufficient           │
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
    │ Commitment        │  │  Fees        │  │ Commitment        │
    │ Outputs           │  │  (to mint)   │  │ Outputs           │
    │                   │  └──────────────┘  │                   │
    │ P2PK-locked to    │                    │ P2PK-locked to    │
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

```

... TODO: recommend that the first payment be for zero sats, to allow the channel to be instantly closed if Charlie is unable to provide service now. Typically, therefore, Alice will provide two payments immediately the at the start, one with zero sats and another with the first 'real' payment ...

# The channel parameters, and channel_id

Knowing Charlie's public key, and the set of mints and _units_ that are trusted by Charlie, and a minimum channel lifetime that Charlie requires, Alice defines the channel parameters as follows:

 - `sender_pubkey`: Alice's key ?how exactly to encode this?
 - `receiver_pubkey`: Charlie's key ?how exactly to encode this?

 - `mint` string: URL of mint
 - `unit`: typically `sat` or `msat`
 - `capacity`: the maximum balance that will be payable to Charlie

 - `active_keyset_id`: An _active_ keyset for that unit at that mint
 - `input_fee_ppk`: As all the proofs in the funding token, and in the commitment outputs, are in the same keyset, the `input_fee_ppk` is fixed.
 - `maximum_amount_for_one_output`: used in the deterministic amount-selection algorithm as an upper bound on the size of any output in the funding token or in the commitment outputs.

 - `expiry`  unix timestamp: If Charlie doesn't close before this time, Alice can re-claim all the funds after this has expired
 - `setup_timestamp` unix timestamp: the time when Alice is setting up this channel
 - `sender_nonce`: Random data selected by Alice to add more randomness. May be useful if Alice and Charlie have multiple concurrent channels.

The `channel_id` is the SHA256 hash of the '|'-delimited concatenation of all the above.

# Funding the channel

Alice, with the mint, creates a _funding token_ worth `total_funding_token_amount` units.
Each proof in this token is a P2PK (NUT-11) proof which requires both signatures
before the expiry of the channel, and where Alice's signature alone is sufficient after the expiry:

 - `data`: Alice's key
 - `pubkeys`: Charlie's key
 - `n_sigs`: 2
 - `locktime`: the `expiry` timestamp defined in the channel parameters
 - `refund`: Alice's key
 - `sig_flag`: `SIG_ALL`

_TODO: replace that list of 6 items with the correspoding Json of the secret

# Charlie's verification

The following information should be sent to Charlie with, or before, the first payment in this channel,
enabling Charlie to verify everything. He can verify without communicating with the mint:

 - the channel parameters
 - the funding token, including the DLEQ proofs (NUT-12) allowing Charlie to verify that the funding proofs have been signed.

Both sides should store the funding proofs in the order that Alice created them, to ensure both sides can construct the relevant transactions deterministically.

The secrets and blinding factors in the outputs that created this funding token are created
deterministically. Charlie can verify these. _TODO: clarify the full verification details somewhere_

# Payments

Each payment requires Alice to update the balance and then construct the updated
'commitment' transaction. She then signs the transaction and sends her signature
and the new balance to Charlie. This signature and amount, combined with the `channel_id`,
is sufficient for Charlie to reconstruct the commitment transaction and verify the signature,
as long as Alice has sent all the channel parameters with - or before - the first payment.

## deterministic outputs, for the funding token and also for the commitment outputs

To construct the deterministic outputs in the funding token and also
in the commitment outputs, we start with the target amount we
wish to reach and the set
of amounts that are available in the keyset of the `active_keyset_id`.
A _deterministic output_ is a _secret_ and a _blinding factor_ constructed deterministically.

We ignore any amounts greater than `params.maximum_amount_for_one_output`.
The algorithm greedily takes the largest amount,
smaller than that maximum amount,
until it can't take any more as it would overflow the target.
Then it moves on to the next-smallest amount repeatedly
until the target is reached

```

# Pseudocode implementation, showing how the amounts are selected

def compute_the_set_of_deterministic_amounts(target):

    selected_amounts = [] # the vector to store all selected amounts

    # loop over all amounts available in this keyset, largest first
    for amount in available_amounts__largest_first:
        if amount <= params.maximum_amount_for_one_output:
            while amount <= target:
                selected_amounts.append(amount)
                target -= amount
    assert target == 0
    return selected_amounts
```

While it is common for mints to use powers-of-2, it is not required.
In a power-of-2 mint, there will be at most one selected for each available amount.
But for other mints, a given _amount_ may be selected more than once.

For example, if the target is 543 sats, and the keyset has powers of ten
(1, 10, 100, 100 ...) as the amounts, then we'll use 5 of the 100-sat
outputs and 4 of the 10-sat outputs and 3 single-sat outputs.
We use an _index_ - starting from zero for each amount - to distinguish them.

In our 543-sat example, where the available amounts are powers of 10, there are 12 deterministic outputs:

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

The deterministic outputs are created in one of three contexts:
 - `context = "funding"` for creating the funding token, where each secret is 2-of-2 P2PK
 - `context = "receiver"` for creating the commitment outputs for Charlie, which result from swapping the funding token, which are P2PK-locked to him.
 - `context = "sender"` for creating the commitment outputs for Alice, which send the remaining balance to Alice, which are P2PK-locked to her.

A deterministic output is a _BlindedMessage_ created from
a deterministic _secret_ (P2PK-locked to one or both parties),
and a deterministic _blinding factor_.
The deterministic process is a function of four things:

 - the `channel_id`
 - the `context`
 - the `amount`
 - the `index`

As these are all deterministic and based on information known to both parties,
both parties can construct all these outputs.
We use P2PK to stop either party from stealing the other's funds.

Each output iso be constructed as follows: the channel_id, context, amount, and the index are combined and hashed to compute the _deterministic nonce_:

```
deterministic_nonce(...)
 =
   SHA256(channel_id || context || amount || index || "nonce")`
```

Deterministic Secret:

```
secret_for_funding_token = [
  "P2PK",
  {
    "nonce": "<deterministic nonce computed above>",
    "data": "..."
    "tags": [
        TODO: fill this in correctly: 2-of-2 with expiry
    ["sigflag", "SIG_ALL"]
    ]
  }
]

secret_for_charlies_commitment_output = [
  "P2PK",
  {
    "nonce": "<deterministic nonce computed above>",
    "data": "<Charlie's pubkey>",
    "tags": [["sigflag", "SIG_INPUTS"]]
  }
]

secret_for_alices_commitment_output = [
  "P2PK",
  {
    "nonce": "<deterministic nonce computed above>",
    "data": "<Alice's pubkey>",
    "tags": [["sigflag", "SIG_INPUTS"]]
  }
]
```

_TODO? Optional: If Charlie, along with his public key, advertizes that he supports pay-to-blinded-pubkey, we could determistically compute an ephemeral private key for blinding, and include the corresponding ephemeral public key in the proof, as per the P2BPK NUT_

The corresponding blinding factor is `SHA256(channel_id || context || amount || index || "blinding")`,
and so the deterministic output (BlindedMessage) is contructed by applying that
blinding factor to that secret in the usual way.

We use determinism as it minimizes the communication that is required,
in particular it allows Alice to send the initial payment with zero
prior communication with Charlie and also minimizing the bandwidth.
If Charlie sees a payment from a new `channel_id`, he knows that the
funding token is new, i.e. it hasn't been used in a previous channel.

# Commitment transaction, and balance update, in detail

The commitment transaction can now be specified more clearly.
It is a _swap_ which takes the _funding proof_ as input.

As recommended in NUT-03, the outputs are in ascending order of amount.

The outputs includes all the commitment outputs for Charlie and also
those for Alice.
They are ordered by amount (increasing). For any given amount,
we have Charlie's deterministic outputs first, ordered by _index_ (increasing),
and then Alice's similarly ordered. For example, if you're distributing
a few hundred sats to each party, the first few outputs of the swap are:

```
context    | amount | index

"receiver" | 100    |     0
"receiver" | 100    |     1
"sender"   | 100    |     0
"sender"   | 100    |     1
...
```

> [!NOTE]
> If you have a vector of Charlie's outputs, ordered by amount and index, and then you append
> Alice's similarly ordered,
> then you can apply a _stable sort_, such as Rust's `all_outputs.sort_by_key(|(output, _)| output.amount)` or Python's `sorted(all_outputs, key = lambma o: o.amount` to get the required ordering.

Alice then signs this (SIG_ALL). Alice can then send three pieces of data to Charlie: the `channel_id`, the balance for Charlie, and her signature.

As already mentioned, Alice must send the full set of channel parameters to Charlie in the first payment - if she hasn't already sent them beforehard -
but after this it is sufficient for her to send those three pieces of data.

Charlie can reconstruct the transaction and verify the signature.

# Closing the channel

Most of the commitment transactions are never sent to the mint.

When Charlie exits, he adds his signature to Alice's on the most recent transaction and
sends the complete swap to the mint.
This swap spends the _funding token_ and returns
blind signatures (the deterministic outputs, signed by the mint) for both parties.

As the swap spends the entire funding token, Alice can detect Charlie's spend
via NUT-07 (token state check). NUT-17, if supported by the mint, helps here too.

Charlie should return Alice's blind signatures to her, but if he doesn't then Alice
can use NUT-09 to restore the signatures.
While we assume that Charlie will usually take the most recent commitment, as it's
the most valuable, it is not guaranteed that he will do that.

To restore, Alice can iterate over the amounts available in this keyset, and - for each amount - loop over the indices - restarting the index at `0` for each amount -
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
Alice doesn't attempt to decrease the balance or otherwise attempt to reuse an older channel.
This map should also store the channel parameters.

As the expiry time approach, Charlie should close the channel as he will lose the balance if the
expiry time is reached.
When Charlie closes the channel, he should keep a set of all the closed channels to avoid
Alice reusing a closed channel.

The record of a closed channel should not be deleted until after it has expired,
in order to avoid channel reuse.

If Alice pays using a channel that is not in either of the two datasets mentioned above,
then Alice is opening a new channel, and Charlie should check:
 - that the expiry time is reasonably far in the future
 - that the mint is a mint that he trusts, and the keyset is active
 - that the channel_id is computed correctly
 - the DLEQ proofs in the funding token are correct
 - The secrets in the funding token have the correct P2PK setup, with the keys and expiry and so on

# proof-of-concept

_As of 2025-11-27, the PoC is up-to-date with the description above, but not released yet. The funding and commitment outputs are deterministic. Fees are taken into account fully. The token-state-check and toekn-restore endpoints are used. I'm gradually adding more unit tests_
