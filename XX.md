# NUT-XX: Offline Spilman (unidirectional) channel

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), NUT-09 (restore signatures), NUT-07 (token state check), NUT-?28? P2BK, (NUT-17 is beneficial, but not required)`

_TODO: This is a bit badly-structured and repetitive now. I need to tidy it up._

---

This describes how Alice can set up a one-way payment channel from herself to Charlie.
Using public information such as Charlie's public key and his preferred mints and keysets,
Alice prepares a _funding token_
and she can send an initial payment to Charlie without any prior involvement from Charlie.

Throughout the lifetime of the channel, Alice signs transactions which redistribute
('commit') the value in that funding token between herself and Charlie,
where each transaction increases the balance in favour of Charlie and decreases hers.

Charlie does not need to trust Alice; he can verify each channel transaction
locally without needing to check anything with the mint.
He does not need to contact the mint until he decides to close the channel.

Charlie can unilaterally exit at any time, by adding his signature to the most recent
signature from Alice and swapping the _funding token_ for the outputs.
Alice can then immediately claim her balance, even if Charlie does not cooperate with her.
If Charlie never exits, there is an expiry time in the channel and Alice is able to
unilaterally reclaim the entire funding token when that expiry time is reached.

The mint, Bob, is involved only at the start for the initial swap where Alice prepares
the _funding token_, and at the end where each of the two parties swap their
final balances into their wallets.

No change or extension to the mint's behaviour is needed.
The mint simply sees and executes standard P2PK swaps.
The mint doesn't know that there is a channel, due to various techniques - including
pay-to-blinded-pubkey (... NUT-28? ...) - which make it difficult for
the mint to correlate the swaps and tokens.

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
both signatures to spend, but where Alice's signature alone is sufficient
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

If Charlie never exits, Alice can wait until the channel's _expiry_ time
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
that Alice's payments are valid, and that she hasn't reused an older
channel or an older funding token, and he doesn't need to contact the mint
until he decides to close the channel.

> [!NOTE]
> _Blinding_ The term 'blinding' is used in two different contexts here.
> One context is the _blinding factor_ which is applied to every every secret in Cashu,
> creating the `BlindedMessage` (aka _output_) which is then signed by the mint.
> This blinding factor is computed deterministically as described below.
> Also, we blind the public keys that are used as the pubkeys to which the tokens
> are locked, in accordance with NUT-?28?, as described below.

# Fees

Closing the channel ('exiting') involves two _stages_, a first stage where
Charlie executes the _commitment transaction_, and a second stage
where each party swap their 1-of-1 P2PK outputs into their wallets.
In each stage, there are fees to be paid.
Alice is responsible for the fees, and therefore there is some
complexity to ensure that the payments cover fees for both stages.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FUNDING TOKEN                                   │
│                  (total_funding_token_amount)                           │
│                                                                         │
│  Created by Alice with P2BK proofs requiring both signatures (SIG_ALL)  │
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
    │ P2BK-locked to    │                    │ P2BK-locked to    │
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

> [!NOTE]
> _Keyset malleability:_ The keyset for the _funding outputs_ is defined in the _channel parameters_.
> When Charlie executes the commitment transaction, he can choose which keyset to use as the commitment outputs. He should choose the same keyset, but he is not required to do so.
> In fact, if that keyset is no longer _active_, he will be required by the mint to choose a different keyset.
> He has this freedom because Alice's SIG_ALL signature commits to the _amounts_, but not the _keysets_, of the outputs.
> This means that the fee rate in the second stage may be different from the fee rate in the first stage, and the final amounts after the second stage might not be what was expected.
> We ignore this issue and assume that the same keyset will be used for all the outputs (funding outputs, and both sets of commitment outputs), and base all our fee calculations on this assumption.
> If the assumption is wrong, and Charlie uses a different keyset, then this simply means that the final
amounts that each party gets after completing the second stage of the exit will be slightly different than they expected.

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
 - `maximum_amount_for_one_output`: used in the deterministic amount-selection algorithm as an upper bound on the size of any individual output in the funding token or in the commitment outputs. May be helpful with privacy, in the case of large-capacity channels.

 - `expiry`  unix timestamp: If Charlie doesn't close before this time, Alice can re-claim all the funds after this has expired
 - `setup_timestamp` unix timestamp: the time when Alice is setting up this channel
 - `sender_nonce`: Random data selected by Alice to add more randomness. May be useful if Alice and Charlie have multiple channels with otherwise-identical parameters.

There is also a _shared secret_, computed via Diffie Helman using the
keys of the two parties.
 
The `channel_id` is the SHA256 hash of the concatenation of all the parameters, including the _shared secret_.

The shared secret is to add a little extra privacy here, by making it more difficult
for a third party, especially the mint, to predict what the `channel_id` might be.
If a user publicly shares an error message that contains a `channel_id`, we don't
want any third party, especially the mint, to be able to tie that id to the public keys.

# Deterministic selection of amounts

To construct the deterministic outputs in the funding token and also
in the commitment outputs, we start with the target amount we
wish to reach and the set
of amounts that are available in the keyset of the `active_keyset_id`.
We ignore any amounts greater than `params.maximum_amount_for_one_output`,
they are not considered as available to this amount-selection algorithm.
If `params.maximum_amount_for_one_output` is zero, then no filtering is
applied and all the keyset's amounts are available.

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
        # if the max is non-zero, consider only amounts less than this max:
        if amount <= channel_params.maximum_amount_for_one_output or channel_params.maximum_amount_for_one_output == 0:
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
would select fifty-four 10-sat outputs and three 1-sat outputs.

_TODO: clarify the order of the outputs when Alice is creating the funding transaction. Make sure it fits the code and follows best practices_

# Alice pays the fees

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
`x=7` is too small as that would require three outputs (7 = 4 + 2 +1)
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
total_funding_token_amount
   = inverse_deterministic_value(
        inverse_deterministic_value(capacity)
     )
```

There are two applications of `inverse_deterministic_value` there because Charlie will
perform two swaps during his exit.

The fees in the first stage will always be `total_funding_token_amount - deterministic_value_after_fees(total_funding_token_amount)`.
The fees in the second stage can vary, as they depend on the distribution between the two parties.

To make a payment which brings Charlie's balance to `balance`, the following describes how Alice computes the values of the various parts.

 - `balance`, we start our computation with this, the balance that we wish Charlie to have in this transaction.
 - `c` = `inverse_deterministic_value(balance)`, the nominal value of Charlie's commitment outputs.
 - `a` = `deterministic_value_after_fees(total_funding_token_amount) - c`, the value that is left from the funding token to create Alice's commitment outputs, after the stage1 fees and creating Charlie's commitment outputs.
 - Alice is then left with `deterministic_value_after_fees(a)`, the final amount left in her wallet after swapping her commitment outputs into her wallet.

In other words, as we saw in the diagram above, the value in the
funding token is split up as follows in the commitment transaction:

```
total_funding_token_amount
 =
   c             # the 'nominal' value of Charlie's 'commitment outputs'
   + a           # the 'nominal' value of Alice's 'commitment outputs'
   + stage1fees  # the fees taken by the mint in this swap
```

where `c = balance + stage2fees_for_charlie`
and   `a = alices_final_balance + stage2fees_for_alice`
take account of the fees that are paid by each party in the second stage.

_... TODO: maybe we should recommend that the first payment be for zero sats, to allow the channel to be instantly closed by Charlie if he is unable to provide service now. Typically, therefore, Alice will provide two payments immediately the at the start, one with zero sats and another with the first 'real' payment ..._

# Deterministic outputs: secrets, nonces, and blinding factors

When Alice is creating the funding token, and when either party is creating
the outputs to be signed in the swap, they must create them using the algorithm
descibed in 'Deterministic selection of amounts' described above.
In doing so, they will have the _amount_ and _index_ for each output.
Everything about these outputs is deterministic, including the `Secret.nonce`,
and also the _blinding factor_.

The deterministic outputs are created in one of three `context` values:
 - `context = "funding"` for creating the funding token, where each secret is 2-of-2 P2PK with blinded pubkeys
 - `context = "receiver"` for creating the commitment outputs for Charlie, which are P2PK-locked to his per-proof blinded pubkey
 - `context = "sender"` for creating the commitment outputs for Alice, which are P2PK-locked to her per-proof blinded pubkey

The deterministic process is a function of five things:

 - the `channel_id`, the hex representation of the channel_id.
 - the `context` as a string
 - the `amount` in decimal representation, e.g. "32" for 32 satoshis
 - the `index` in decimal representation. (As this is rarely be greater than, an probably never greater than 255, then maybe this should just be represented as one byte?)
 - the `shared_secret` mentioned earlier. Using this ensures that the mint cannot compute the outputs even if they know the channel_id.

As these are all deterministic and based on information known to both parties,
both parties can construct all these outputs and secrets and blinding factors.

The secret's _nonce_ is computed as follows:

```
deterministic_nonce(...)
 =
   SHA256(shared_secret || channel_id || output_context || amount || "nonce" || index)
```

## Funding Token Secret (2-of-2 with Blinded Pubkeys)

The keys are blinded following NUT-?28?, where an ephemeral public key (called `p2pk_e` in that NUT)
is generated deterministically and that key is then used to derive a
tweak that can be applied to each pubkey.
While Alice and Charlie know the tweaks that are applied, the mint (Bob) does not.

The funding token uses a 2-of-2 P2PK secret with three blinded pubkeys:
- `data` field: Alice's blinded pubkey
- `pubkeys` tag: Charlie's blinded pubkey
- `refund` tag: Alice's refund blinded pubkey

_(Needs more clarity: ...)_ For the 2-of-2 P2PK secret in the funding token, an ephemeral _private_ key is computed as `SHA256("ChannelFundingP2BK" || shared_secret || channel_id)`. That gives us the corresponding
ephemeral public key `p2pk_e`. Following that NUT, there is a process which takes that p2pk_e and the recipient's key (params.sender_pubkey or params.receiver_pubkey), and the position of that key in the secret, and tweaks it.

While Alice is the intended recipient of both the `data` and `refund` key, NUT-28 blinds them differently due to their position in the P2PK Secret, and therefore the mint cannot see that `data == refund`.

As the swap that spends this funding token use SIG_ALL, the same blinding is used for every output
in the funding token.

Example funding token secret (JSON):

```json
[
  "P2PK",
  {
    "nonce": "a1b2c3d4e5f678901234567890abcdef...",
    "data": "02abc123def456789...",
    "tags": [
      ["pubkeys", "03def456abc789012..."],
      ["refund", "02789abcdef012345..."],
      ["n_sigs", "2"],
      ["locktime", "1737500000"],
      ["sigflag", "SIG_ALL"]
    ]
  }
]
```

Where:
- `"data"` contains Alice's blinded pubkey.
- The `"pubkeys"` tag contains Charlie's blinded pubkey.
- The `"refund"` tag contains Alice's blinded pubkey.
- `"n_sigs": "2"` requires both Alice and Charlie's signatures before locktime
- After locktime, Alice can spend alone using her refund blinded secret key

## Commitment Output Secrets (1-of-1 with Per-Proof Blinded Pubkeys)

Each commitment output is locked to a **unique** blinded pubkey derived from the specific `(amount, index)` of that output.

_(Needs more clarity: ...)_ For the 1-of-1 P2PK secret in the commitment outputs, an ephemeral _private_ key is computed as `SHA256("ChannelClosingP2BK" || <"receiver" or "sender"> || shared_secret || channel_id || amount || index)`.
That gives us the corresponding
ephemeral public key `p2pk_e` for this particular output.
Following that NUT, there is a process which takes that p2pk_e and the recipient's key (params.sender_pubkey or params.receiver_pubkey), and the position of that key in the secret, and tweaks it.

Example commitment output secret for Charlie (JSON):

```json
[
  "P2PK",
  {
    "nonce": "b2c3d4e5f6a1234567890abcdef01234...",
    "data": "02charlie_blinded_pubkey_for_this_output...",
    "tags": [
      ["sigflag", "SIG_INPUTS"]
    ]
  }
]
```

The `"data"` field contains Charlie's blinded pubkey derived as described above.

Example commitment output secret for Alice (JSON):

```json
[
  "P2PK",
  {
    "nonce": "c3d4e5f6a1b234567890abcdef012345...",
    "data": "02alice_blinded_pubkey_for_this_output...",
    "tags": [
      ["sigflag", "SIG_INPUTS"]
    ]
  }
]
```

The `"data"` field contains Alice's blinded pubkey derived as described above.

## Blinding Factor for Blind Signatures

The blinding factor (for the Cashu blind signature scheme) is computed separately from the P2BK blinding:

```
blinding_factor = SHA256(shared_secret || channel_id || context || amount || "blinding" || index)
```

where `context` is one of "funding", "sender" or "receiver".

This is used to blind the secret before sending to the mint, and to unblind the mint's signature.

Every output in this system, i.e. those in the funding token and also those which result when
spending the funding, is fully deterministic and can be created by either party but not by the mint.
The determinism covers the amounts, the `Secret.nonce`, the blinding of the pubkeys, and
also the blinding factor that is applied to the Secret to generate the BlindedMessage which
is sent to the mint as input to any swap.

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

Alice then signs this (`SIG_ALL`).
Alice can then send three pieces of data to Charlie: the `channel_id`, the balance for Charlie, and her signature.

As already mentioned, Alice must send the full set of channel parameters to Charlie in the first payment - if she hasn't already sent them beforehard -
but after this it is sufficient for her to send those three pieces of data.

# Closing the channel

Most of the commitment transactions are never sent to the mint.

When Charlie exits, he adds his signature to Alice's on the most recent transaction and
sends the complete swap to the mint.
This swap spends the _funding token_ and returns
blind signatures (the deterministic outputs, signed by the mint) for both parties.

The two parties can cooperatively close using any balance, including a balance
smaller than the most recent signed transaction, by applying both of their signatures
and swapping.

## Signing with Blinded Secret Keys

When closing the channel, both parties sign with their **blinded** secret keys:

- **Charlie** signs with his blinded secret key derived as described above.
- **Alice** signs with her blinded secret key derived as described above.

These signatures verify against the blinded pubkeys in the funding token.

For the **locktime refund path**, Alice signs with her **refund** blinded secret key derived from `p2bk_context = "sender_stage1_refund"`. This key corresponds to the blinded pubkey in the `refund` tag.

When spending the commitment outputs in stage 2:
- **Charlie** signs each of his proofs with the per-proof blinded secret key for that `(amount, index)`, as described above.
- **Alice** signs each of her proofs with the per-proof blinded secret key for that `(amount, index)`, as described above.

As the swap spends the entire funding token, Alice can detect Charlie's spend
via NUT-07 (token state check). NUT-17, if supported by the mint, helps here too.

Charlie should return Alice's blind signatures to her, but if he doesn't then Alice
can use NUT-09 to restore the signatures.
If Charlie chooses a different keyset (not `params.active_keyset_id`), Alice can
use NUT-09 to learn the keyset that he selected.

While we assume that Charlie will usually take the most recent commitment, as it's
the most valuable, it is not guaranteed that he will do that.
There may be a cooperative closing mechanism to agree on any other balance.

To restore the signatures, where she isn't sure which particular balance
Charlie exited with, Alice can iterate over the amounts available, and - for each amount - loop over the indices - restarting the index at `0` for each amount -
in order to reconstruct the deterministic output and restore the signature.
When a given restoration fails, she can stop increasing the _index_ and
move on to the next amount instead.

```
for amount in amounts_in_this_keyset:
    if params.maximum_amount_for_one_output > 0 and amount > params.maximum_amount_for_one_output:
        continue

    index = 0
    while True:
        ... attempt to restore with (amount, index) with NUT-09
        if (restore fails for this 'amount' and 'index'):
            break # stop incrementing the index and skip to the next 'amount'
        else:
            .. unblind the signature and add the proof to Alice's wallet
            index += 1
```

This ensures she will get all the outputs and BlindedSignatures which Charlie
created when he did the swap, even if she doesn't know which balance he exited with.

_(Question: Does NUT-09 specify what should happen if the outputs are a mixture of unspent outputs and outputs that were never spent? i.e. Does Alice have to call restore once for each possible output, or can she do a batch call where some will fail and some will succeed?)_

# Charlie's verification

The following information should be sent by Alice to Charlie with, or before, the first payment in this channel,
enabling Charlie to verify everything. He can verify without communicating with the mint.

 - the channel parameters
 - the funding token, including the DLEQ proofs (NUT-12)

Charlie can then verify that the parameters are acceptable to him; he can check:

 - that the expiry time is reasonably far in the future
 - that the mint is a mint that he trusts, and the keyset is active for the correct `unit`
 - that the channel_id is computed correctly
 - the DLEQ proofs in the funding token are correct
 - the secrets in the funding token have the correct deterministic P2PK setup, with the keys and expiry and so on
 - the blinded pubkeys in the funding token are correctly derived:
   - `data` field matches Alice's blinded pubkey
   - `pubkeys` tag matches Charlie's blinded pubkey
   - `refund` tag matches Alice's blinded pubkey
   - the `refund` pubkey differs from the `data` pubkey (they use different blinding tweaks)


For every payment received, Charlie can reconstruct the entire commitment
transaction as he has the funding token and he can compute the outputs
of the commitment transaction deterministically.
With this, he can verify the signature that Alice included in the payment update.

Charlie should remember to close channels as the expiry time approaches.
He should also keep a record of channel_ids that he has closed, where
the expiry time has not been reached, in order to ensure that
Alice does not attempt to reuse a pre-expiry channel that was already closed.

Charlie should maintain a mapping from the channel_id to the balance, to ensure that
Alice doesn't attempt to decrease the balance or otherwise attempt to reuse an older channel.
Alternatively, Charlie could maintain a per-channel record of the amount of service that
has been provided (image files server, LLM tokens used, kilobytes of data routed by a router ...)
and ensure that each new balance is sufficient to cover the amount due to Charlie for
the service.

Charlie's record of a closed channel should not be deleted until after it has expired,
in order to avoid channel reuse.

If Alice pays using a `channel_id` that is not in either of the two datasets mentioned above,
then Alice is opening a new channel, and Charlie should check everything described above.
As it's a new channel, and assuming the verification is successful, Charlie knows that
the funding token is valid and hasn't already been spent, and he knows that any
commitment transaction that is formed deterministically will also have unspent outputs.

# Timing

To improve privacy further, when the channel is closed and the first of the two stages
is executed, both parties should delay the second stage.
This delay is to make it more difficult for the mint to correlate the swaps with each other.


# proof-of-concept

_As of 2026-01-13, the implementation includes P2BK (Pay-to-Blinded-Key) with per-proof blinding for stage 2 outputs. The funding and commitment outputs are deterministic with blinded pubkeys. Fees are taken into account fully. The token-state-check and token-restore endpoints are used. The implementation is [here](https://github.com/SatsAndSports/demo_of_spillman_cashu_channel/tree/spilman.channel/crates/cdk/src/spilman), with integration tests verifying blinded signatures are accepted by the mint._
