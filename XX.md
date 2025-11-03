# NUT-XX: Offline Spilman (unidirectional) channel

`optional`

`depends on: NUT-11 (P2PK), NUT-12 (DLEQ), NUT-09 (restore signatures), NUT-07 (token state check) (NUT-17 is beneficial, but not required)`

_TODO: who pays the fees? (see the multi-swap zero-receiver-setup deterministic outputs below) If Alice spends 101 sats to fund the 'funding token' which has a _nominal_ value of 100 sats, and Bob's exit with the full capacity gives him just nominal 99 sats in his 1-of-1 P2PK outputs, which decrease to 98 sats when he finally swaps them to anyone-can-spend tokens in his wallet, then who should pay those fees? Which of those four numbers is the capacity of the network?_

_TODO: question for the reviewer: Could we use pay-to-blinded-pubkey here? Where exactly? And should we make P2BPK required or optional?_

---

Alice and Bob wish to set up a payment channel, funded by Alice, such that Bob's balance starts at zero and his balance
increases (unidirectional) over time. This is 'offline' because it allows - once the channel has been
set up - for the two parties to transact simply by Alice sending signatures to Bob which Bob can verify
without needing to contact the mint after each micropayment.
A small number of swaps are needed to setup and to close the channel, but there is no mint involvement
while the channel is open and while the channel payments are made.

Knowing only Bob's pubkey and a mint trusted by him, Alice can set up the channel - via one swap with the mint - and make the
first payment to Bob without any setup from Bob.
This may be useful in streaming video services or with Nostr relays, where it will be convenient
for Alice to start a HTTP download from Bob and make the first payment within the HTTP request,
or to include the first payment when opening any WebSocket.

Assuming Bob checks that this channel is new to him (the channel ids are deterministic, so he can easily
check if the channel is new), Bob can verify everything offline and doesn't need to
check the state with the mint and he can immediately provide the service that Alice has paid for
with the first payment.

# Trust

Both parties trust the mint, but not each other.
Bob can unilaterally exit at any time, by adding his signature to Alice's and swapping at the mint.
That swap will spend all the 'funding proofs' that Alice prepared in the funding token, and the swap
will also unlock Alice's outputs allowing her to immediately exit with her balance.

If Bob never exits, then - after the predefined locktime has expired - all the funding becomes spendable
by Alice alone, allowing her to reclaim her funds.

# Efficiency

Alice funds the channel by making one swap with the mint which creates a 2-of-2 P2PK token.
This token can have an arbitrarily large value, and it doesn't require many proofs within the token;
dozens of proofs are sufficient for billions of sats (or millisats) of channel capacity.

Each payment simply requires Alice sending the new amount as an integer and her signature
on an updated transaction, along with some metadata to identify the channel.

Closing the channel requires a maximum of three swaps.

# Setting up the channel, and paying via 'commitment transactions'

Alice takes Bob's public key and create one _funding token_.
Each proof in that token is a P2PK _funding proof_, with two spending paths.
Before the locktime, the signatures of both Alice and Bob are required to spend.
After the locktime, only Alice's is needed.
`SIG_ALL` is used, as described in NUT-11.

While the channel is open, any payment is made by Alice constructing an
updated _commitment transaction_ for the new balance and by her signing it
and sending the amount and the signature to Bob,
where he can independently construct the same commitment transaction and verify Alice's signature.

The commitment transaction is a swap which spends all the funding proofs,
distributing some of the value to Bob's outputs and the remainder to Alice's outputs.

Most of these transactions are never taken to the mint to be swapped.
Only the final one is taken by Bob when he chooses to exit.

# Deterministic outputs, and how Alice gets an immediate refund if Bob exists uncooperatively

The commitment transaction takes the funding proofs as input.
The outputs of the commitment transaction follow a deterministic scheme (details to be written up precisely, based
on the channel params...)
to compute the secrets and blinding factors and outputs (blinded messages) which distribute to Bob and Alice.

This deterministic scheme is known to both Alice and Bob, allowing either to construct the transaction
and allowing either party to unblind all BlindSignatures when the channel is closed.

This determinism allows Alice to setup the channel with no input from Bob, where she can
'cold open' with a first payment to Bob.

While both parties know all the secrets and blinding factors for these outputs, they cannot
steal each other's outputs as all the outputs are P2PK-locked in a 1-of-1 proof to the
intended recipient.

When Bob exits, that spends all the funding proofs.
Using NUT-07, Alice can monitor the state of any of the funding proofs to detect
when Bob has exited. (... [websockets in NUT17](https://github.com/cashubtc/nuts/blob/e8a23cc73f84ac8e1f171ea984a0ea471b718c65/17.md#example-proofstate-subscription))

Usually, Bob is rational and will have spent the latest transaction as it has the maximum
value for him. But that is not guaranteed.
If Bob doesn't cooperate with Alice, she can use the response of the NUT-07 to get
the `witness` from the mint and identify which of her signatures was used and from
there to idenfity the amount that Bob took. With the amount, she can reconstruct the transcation
and the deterministic outputs. As she now knows that all outputs have been blind-signed by the mint,
she can use NUT-09 (restore token) to get the blind signatures from the mint
and can unblind to get her 1-of-1 P2PK output.

_The paragraph above requires Alice to remember all the signatures and amounts
that she has sent, but I'm pretty sure there is a way to avoid this dependence
and allow her to restore even if she doesn't know the balance; I'll update my code soon to use
a deterministic system that doesn't require this knowledge._



## Channel capacity

The channel capacity is ??? _depends on the fee policy. As mentioned at the top, there are mulitiple swaps; how is responsible for
paying all those swaps?_

## Channel parameters, and channel reuse

The channel parameters include:
 - sender pubkey (Alice)
 - receiver pubkey (Bob)
 - mint
 - active_keyset_id - the keyset of the funding token and also of the 1-of-1 P2PK outputs
 - unit (e.g. 'sat' or 'msat', or 'usd')
 - locktime - the time after which Alice can spend all the funding proofs to herself
 - setup_timestamp - the time at which Alice created the funding token
 - sender_nonce - a random/arbritrary string added by the sender Alice, in case it's desirable to have two channels at the same time between the same parties

and the channel_id is a deterministic function of the above.

In the naive case, Alice could try to reuse a channel with Bob that she earlier reused, or otherwise lie about the
current balance.
To avoid this, Bob should remember the current balance of every channel which he hasn't yet closed, and
he should also keep a set of the recently-closed channels.
He can assume that any channel past its `locktime`
has been closed, and therefore he doesn't need to keep a record of older channels.

If Bob follows this, he doesn't need to check with the mint in order to consider the channel
open.
He can know when a new channel has been setup, and he can use DLEQ proofs to verify
that the funding proof is valid and unspent.
As the deterministic outputs are different in every channel (the determinism depends on the channel id),
this gives Bob confidence that his outputs in any new channel are unspent outputs.

# proof-of-concept

There is a proof of concept based on the CDK, showing how both parties can do the verification at each step, also including
the latest SIG_ALL message update. _TODO: link to it. As of 2025-11-02, it's implemented and working with this new deterministic output setup, but the latest code isn't on github yet_
