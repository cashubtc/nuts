# NUT-XX: Offline Spilman (unidirectional) channel

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), NUT-09 (restore signatures), NUT-07 (token state check) (NUT-17 is beneficial, but not required)`

---

_TODO: should this, or a separate NUT, talked about the transport for all of this, e.g. JSON over Websockets?_

_TODO: the mint could notice that the 2x2 P2PK swap happens just before two separate 1x1 swaps that add to the same amount, and therefore reasonably conclude that this was a channel. Should Alice and Charlie delay stage 2 in order to have a little more privacy?_

_TODO: For a little more privacy (for those not using P2BPK) Alice and Charlie could specify two public keys, one for the 2-of-2 multisig in the funding and another in the 1-of-1 multisig that pays to each specifically? Or maybe we ignore this issue and just make use of Blinded keys throughout the channel, in cases where the receiver's wallet support it_

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
If Charlie never exits, there is an expiry time in the channel and Alice is able to
unilaterally reclaim the entire funding token when that expiry time is reached.

The mint, Bob, is involved only at the start for the initial swap where Alice prepares
the _funding token_, and at the end where each of the two parties swap their
final balances into their wallets.

# Overview and terminology

Before defining everything in detail, we summarize the overall flow in order
to introduce and clarify terminology.

Alice, the sender, takes Charlie's public information - such as his public key and the mints
and units and keysets that he trusts - and defines the _channel parameters_.
There is a corresponding _channel id_, which is defined deterministically from those parameters
and also from a _shared secret_ derived via Diffie Hellman.

Alice computes the _funding outputs_ , i.e. BlindedMessages, and then pays
the mint (Bob) via a _swap_ or _mint_ to sign those outputs.
She then _unblinds_ the resulting BlindSignatures that come from the mint
in order to create the _funding proofs_, also known as the _funding token_.
The _secret_ in those _funding proofs_ is a 2-of-2 P2PK secret, requiring
both signatures to spend; but where Alice's signature alone is sufficient
after the channel's _expiry_ time has been reached.

Alice sends the _funding proofs_ and _channel parameters_ to Charlie
before - or along with - the first payment.

To make a payment, Alice creates and signs a _commitment transaction_ which
spends all the proofs in the _funding proof_ and which distributes the
outputs between herself and Charlie.
Some of these _commitment outputs_ are 1-of-1 P2PK outputs locked to Charlie,
giving him his current balance, and the remainder of the _commitment outputs_
are 1-of-1 P2PK outputs for Alice.

Each payment increases the balance in favour of Charlie.
Unless otherwise specified, _balance_ will always refer to
Charlie's balance.

Alice makes the payment by sending three pieces of data to Charlie:
the channel id, the new balance for charlie, and her signature.

When Charlie wishes to close the channel, he adds his signature to the
most recent _commitment transaction_ which was signed by Alice.
This gives him a set of BlindSignatures and he can then _unblind_
all the _commitment outputs_ for both himself and Alice.
He then has his 1-of-1 P2PK proofs and he can complete his exit
by swapping them for anyone-can-spend proofs to store in his wallet.

He should send Alice's BlindSignatures to her.
But if he doesn't, she can use NUT-09 to restore the BlindSignatures
and construct her 1-of-1 P2PK proofs.

If Charlie never exits, Alice can wait until the channel's expiry time
and then she can spend all of the _funding token_ with just her signature.

There are three kinds of P2PK outputs, the _funding outputs_ and the
_commitment outputs_ for each of the two parties.
All of these outputs are _deterministic_; the output's _secret_ (including the _nonce_)
and the _blinding factor_ can be computed by both Alice and Bob
based on the data available to both of them:
the channel parameters, the shared secret, and the amount of the current _balance_.
This determinism minimizes the communication that is needed between Alice and Bob.

At the end of this NUT, we define all the steps that Charlie should take
to verify everything.
If he follows the verification steps carefully, he can be confident
that Alice's payments are valid and he doesn't need to contact the mint
until he decides to close the channel.

As Charlie's exits requires two _stages_, a first stage where
he executes the _commitment transaction_, and a second stage
where each parties swap their 1-of-1 P2PK outputs into their wallets,
there are fees to be paid.
Alice is responsible for the fees, and therefore there is some
complexity to ensure that the payments cover fees for both stages.

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

Now we can define the precise details


> [!NOTE]
> _Keyset malleability:_ The keyset for the _funding outputs_ is defined in the _channel parameters_.
> When Charlie executes the commitment transaction, he can choose which keyset to use as the commitment outputs. He should choose the same keyset, but he is not required to do so.
> In fact, if that keyset is no longer _active_, he will be required by the mint to choose a different keyset.
> He has this freedom because Alice's SIG_ALL signature commits to the _amounts_, but not the _keysets_, of the outputs.
> This means that the fee rate in the second stage may be different from the fee rate in the first stage, and the final amounts after the second stage might not be what was expected.
> We ignore this issue and assume that the same keyset will be used for all the outputs (funding outputs, and both sets of commitment outputs), and base all our fee calculations on this assumption.
> If the assumption is wrong, and Charlie uses a different keyset, then this simply means that the final
amounts that each party gets after completing the exit will be slightly different than they expected.

# Channel parameters, `channel_id` and the shared secret.

Knowing Charlie's public key, and the set of mints and _units_ and keysets that are trusted by Charlie,
and a minimum channel lifetime that Charlie requires, Alice defines the channel parameters as follows:

 - `sender_pubkey`: Alice's key. Could be an ephemeral pubkey just for this channel
 - `receiver_pubkey`: Charlie's key.

 - `mint` string: URL of mint
 - `unit`: typically `sat` or `msat`
 - `capacity`: the maximum balance that will be payable to Charlie.

 - `active_keyset_id`: An _active_ keyset for that unit at that mint
 - `input_fee_ppk`: the fee rate for that keyset.
 - `maximum_amount_for_one_output`: used in the deterministic amount-selection algorithm as an upper bound on the size of any individual output in the funding token or in the commitment outputs. Maybe help with privacy, in the case of large-capacity channels.

 - `expiry`  unix timestamp: If Charlie doesn't close before this time, Alice can re-claim all the funds after this has expired
 - `setup_timestamp` unix timestamp: the time when Alice is setting up this channel
 - `sender_nonce`: Random data selected by Alice to add more randomness. May be useful if Alice and Charlie have multiple concurrent channels with the same pair of pubkeys.

There is also a _shared secret_, computed via Diffie Helman using the
keys of the two parties.
 
The `channel_id` is the SHA256 hash of the concatenation of all the parameters, including the _shared secret_.

The shared secret is to add a little extra privacy here, by making it more difficult
for a third party, especially the mint, to predict what the `channel_id` might be.
If a user publicly shares an error message that contains a channel_id`, we don't
want any third party, especially the mint, to be able to tie that id to the public keys.

# Deterministic selection of amounts

To construct the deterministic outputs in the funding token and also
in the commitment outputs, we start with the target amount we
wish to reach and the set
of amounts that are available in the keyset of the `active_keyset_id`.
We ignore any amounts greater than `params.maximum_amount_for_one_output`,
they are not considered as available to this amount-selection algorithm.

The algorithm greedily takes the largest amount,
smaller than that maximum amount,
until it can't take any more as it would overflow the target.
Then it moves on to the next-smallest amount repeatedly
until the target is reached. Here is a pseudocode implementation:


```

def compute_the_set_of_deterministic_amounts(target):

    selected_amounts = [] # the vector to store all selected amounts

    # loop over all amounts available in this keyset, largest first
    for amount in available_amounts__largest_first:
        if amount <= channel_params.maximum_amount_for_one_output:
            while amount <= target:
                selected_amounts.append(amount)
                target -= amount
    assert target == 0
    return selected_amounts
```

While it is common for mints to use powers-of-2 for all the amounts in a given keyset,
it is not required by the protocol.
In a power-of-2 mint, there will be at most one selected for each available amount.
But for other mints, a given _amount_ may be selected more than once.

For example, if the target is 543 sats, and the keyset has powers of ten
(1, 10, 100, 100 ...) as the amounts, then we'll use 5 of the 100-sat
outputs and 4 of the 10-sat outputs and 3 single-sat outputs.
We use an _index_ - starting from zero for each amount - to distinguish them from each other
when we are computing the deterministic nonces and deterministic blinding factors.

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

if the `maximum_amount_for_one_output` was defined as 99 in this channel, then the algorithm
would select fifty four 10-sat outputs and three 1-sat outputs.

# Fees

That algorithm gives us a set of amounts that reach a given target
value when constructing the various kinds of P2PK outputs.
Any time those outputs are spent, fees will be paid.
The fee rate is `input_fee_ppk` for all the outputs in the channel,
as we assume the same keyset is used in all outputs,
Therefore, the post-swap value of any set of deterministic outputs
can be computed as follows, where `num_deterministic_outputs(x)` is
the number of outputs selected by the determistic algorithm described
above.

```
deterministic_value_after_fees(x)
  =
    x - (input_fee_ppk * num_deterministic_outputs(x) + 999) // 1000
```

We know that `deterministic_value_after_fees(x) <= x`, attaining equality only if `input_fee_ppk == 0`.

We also have a function to invert that, `inverse_deterministic_value(y)`,
which finds the smallest `x` such that `deterministic_value_after_fees(x) >= y`
Notice the `>=`, not `=`, in that previous paragraph.
Sometimes, due to fees, there is no value `x` for which equality can be attained.

For example, if `input_fee_ppk=400` and `x=6`, then 
`x=7` is too small as that would require three outputs (7= 4 + 2 +1)
and as there are three outputs, the fees would cost 1200 ppk and leave
only 5 sats after paying the fees.
Therefore, we need `x=8`. That requires just a single 8-sat output
and theref, after fees, it's worth 7 sats.
If this example is creating Charlie's commitment outputs, then
he'll ultimately get 7 sats in his wallet even though the intended
_balance_ was just 6 sats.

We will refer to Charlie's _balance_ in the above example as 6 sats,
even though - due to that issue - the de facto balance after swapping
might be slightly larger in some cases.
This allows the _balance_ to increase at whichever rate suits both parties,
without forcing them to skip any of these special values.

# Creating the funding token

Where `capacity` is one of the channel parameters and specifies the maximum
possible balance for Charlie, Alice must create the funding token with this
value:

```
total_funding_token_amount = inverse_deterministic_value(inverse_deterministic_value(capacity))
```

There are two applications of `inverse_deterministic_value` there because Charlie will
perform two swaps during his exit.

The fees in the first stage will always be `total_funding_token_amount - deterministic_value_after_fees(total_funding_token_amount)`.
The fees in the second stage can vary, as they depend on the distribution between the two parties.

To make a payment which brings Charlie's balance to `balance`, the following describes how Alice computes the values of the various parts.

 - `balance`, we start our computation with this, the balance that we wish Charlie to have in this transaction.
 - `c` = `inverse_deterministic_value(balance)`, the nominal value of Charlie's commitment outputs.
 - `a` = `deterministic_value_after_fees(total_funding_token_amount) - c`, the value that is left from the funding token to create Alice's commitment outputs, after the stage1 fees and creating Charlie's commitment outputs.
 - Alice is then left with `deterministic_value_after_fees(a)`, the final amount left in her wallet after swapping her commitment outputs into her wallet, assuming the keyset is the same 

In other words, as we saw in the diagram above, the value in the
funding token is split up as follows in the commitment transaction:

```
total_funding_token_amount
 =
   c   # the 'nominal' value of Charlie's 'commitment outputs'
   + a # the 'nominal' value of Alice's 'commitment outputs'
   + stage1fees # the fees taken by the mint in this swap
```

where `c = balance + stage2fees_for_charlie`
and   `a = alices_final_balance + stage2fees_for_alice`

... TODO: should we recommend that the first payment be for zero sats, to allow the channel to be instantly closed by Charlie if he is unable to provide service now. Typically, therefore, Alice will provide two payments immediately the at the start, one with zero sats and another with the first 'real' payment ...

# Deterministic secrets, nonces, and blinding factors

The deterministic outputs are created in one of three contexts:
 - `context = "funding"` for creating the funding token, where each secret is 2-of-2 P2PK
 - `context = "receiver"` for creating the commitment outputs for Charlie, which result from swapping the funding token, which are P2PK-locked to him.
 - `context = "sender"` for creating the commitment outputs for Alice, which send the remaining balance to Alice, which are P2PK-locked to her.

The deterministic process is a function of five things:

 - the `channel_id`
 - the `context`
 - the `amount`
 - the `index`
 - the `shared_secret` mentioned earlier. Using this ensures that the mint cannot compute the outputs even if they know the channel_id.

As these are all deterministic and based on information known to both parties,
both parties can construct all these outputs and secrets and blinding factors.

The secret's _nonce_ is computed as follows:

```
deterministic_nonce(...)
 =
   SHA256(shared_secret || channel_id || context || amount || "nonce" || index)`
```

The secret itself is computed as follows, depending on the _context_:

```
secret_for_funding_token = [
  "P2PK",
  {
    "nonce": "<deterministic nonce computed above>",
    "data": "..."
    "tags": [
        TODO: fill this in correctly: 2-of-2 with expiry like this:
            let conditions = Conditions::new(
                Some(locktime),                       // Locktime for Alice's refund
                Some(vec![*charlie_pubkey]),          // Charlie's key as additional pubkey for 2-of-2
                Some(vec![*alice_pubkey]),            // Alice can refund after locktime
                Some(2),                              // Require 2 signatures before locktime
                Some(SigFlag::SigAll),                // SigAll: signatures commit to outputs
                Some(1),                              // Only 1 signature needed for refund (Alice)
            )?;
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

The corresponding blinding factor is `SHA256(shared_secret || channel_id || context || amount || "blinding" || index)`,
and so the deterministic output (BlindedMessage) is contructed by applying that
blinding factor to that secret in the usual way.

_TODO? Optional: If Charlie advertizes that he supports receiving pay-to-blinded-pubkey, we could deterministically compute an ephemeral private key for blinding, and include the corresponding ephemeral public key in the proof, to be compatible the P2BPK NUT_


# Order of outputs in the commitment transaction

The commitment transaction can now be specified more completely.
It is a _swap_ which takes the _funding proof_ as input.
Alice prepares the values of the various parts, and their deterministic outputs, as described above.

As recommended in NUT-03, the outputs are in ascending order of amount.

The outputs include all the commitment outputs for Charlie and also
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
... followed by the 10-sat outputs ...
```

> [!NOTE]
> If you have a vector of Charlie's outputs, ordered by increasing amount and index,
> and then you append Alice's similarly ordered,
> then you can apply a _stable sort_, such as Rust's `all_outputs.sort_by_key(|(output, _)| output.amount)` or Python's `sorted(all_outputs, key = lambma o: o.amount` to get the required ordering.

Alice then signs this (SIG_ALL).
Alice can then send three pieces of data to Charlie: the `channel_id`, the balance for Charlie, and her signature.

As already mentioned, Alice must send the full set of channel parameters to Charlie in the first payment - if she hasn't already sent them beforehard -
but after this it is sufficient for her to send those three pieces of data.

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
If Charlie chooses a different keyset (not `params.active_keyset_id`), Alice can
use NUT-09 to learn the keyset that he selected.

While we assume that Charlie will usually take the most recent commitment, as it's
the most valuable, it is not guaranteed that he will do that.

To restore the signatures, where she isn't sure which particular balance
Charlie exited with, Alice can iterate over the amounts available, and - for each amount - loop over the indices - restarting the index at `0` for each amount -
in order to reconstruct the deterministic output and restore the signature.
When a given restoration fails, she can stop increasing the _index_ and
move on to the next amount instead.

```
for amount in amounts_in_this_keyset:
    if amount > params.maximum_amount_for_one_output:
        continue

    index = 0
    while True:
        ... attempt to restore this blinded signature
        if (restore fails for this 'amount' and this 'index'):
            continue # to the next amount
        else:
            .. unblind the signature and add the proof to Alice's wallet
```

This ensures she will get all the outputs and BlindedSignatures which Charlie
created when he did the swap, even if she doesn't know which balance he exited with.

_(Question: Does NUT-09 specify what should happen if the outputs are a mixture of unspent outputs and outputs that were never signed? i.e. Does Alice have to call restore once for each possible output, or can she do a batch call where some will fail and some will succeed?)

# Charlie's verification

The following information should be sent by Alice to Charlie with, or before, the first payment in this channel,
enabling Charlie to verify everything. He can verify without communicating with the mint:

 - the channel parameters
 - the funding token, including the DLEQ proofs (NUT-12)

Charlie can then verify that the parameters are acceptable to him; he can check:

 - that the expiry time is reasonably far in the future
 - that the mint is a mint that he trusts, and the keyset is active for the correct `unit`
 - that the channel_id is computed correctly
 - the DLEQ proofs in the funding token are correct
 - The secrets in the funding token have the correct deterministic P2PK setup, with the keys and expiry and so on


For every payment received, Charlie can reconstruct the entire commitment
transaction as he has the funding token and he can compute the outputs
of the commitment transaction deterministically.
With this, he can verify the signature that Alice included in the payment update.


Charlie should remember to close channels as the expiry time closes.
He should also keep a record of channel_ids that he has closed, where
the expiry time has not been reached, in order to ensure that
Alice does not attempt to reuse a pre-expiry channel that was already closed.

Charlie should maintain a mapping from the channel_id to the balance, to ensure that
Alice doesn't attempt to decrease the balance or otherwise attempt to reuse an older channel.
This map should also store the channel parameters.

Charlie's record of a closed channel should not be deleted until after it has expired,
in order to avoid channel reuse.

If Alice pays using a `channel_id` that is not in either of the two datasets mentioned above,
then Alice is opening a new channel, and Charlie should check everything described above.


# proof-of-concept

_As of 2025-11-27, the PoC is up-to-date with the description above, but not released yet. The funding and commitment outputs are deterministic. Fees are taken into account fully. The token-state-check and toekn-restore endpoints are used. I'm gradually adding more unit tests_
