# NUT-XX: STARK-proven Computations (Cairo)

`optional`

`depends on: NUT-10`

---

This NUT describes the use of STARK proofs of Cairo program execution, which defines a spending condition based on [NUT-10][10]'s well-known `Secret` format. Using Cairo STARK proofs, ecash tokens can be locked to the successful execution of a specific Cairo program with a given output. Since Cairo is Turing-complete, this enables for user-defined arbitrary spending conditions, which can stay private even from the mint thanks to the zero-knowledge property of STARK proofs[^1].

[^1]: This can be achieved with bootloading, see section 2.2.1 of [GPR21] and [Optional feature: Bootloading](#optional-feature-bootloading) for more details.

> [!CAUTION]
> If the mint does not support this type of spending condition, proofs may be treated as a regular anyone-can-spend tokens. Applications need to make sure to check whether the mint supports a specific kind of spending condition by checking the mint's [info][06] endpoint.

## Cairo

[NUT-10][10] Secret `kind: Cairo`

> [!NOTE]
> We differentiate between three kinds of "proofs" in this section:
>
> 1. A `Proof` refers to an input as defined in [NUT-00][00]
> 2. A [`CairoProof`](https://github.com/starkware-libs/stwo-cairo/blob/205c7efe266a6c0df28725fdf6754643b39a994a/stwo_cairo_prover/crates/cairo-air/src/air.rs#L43) refers to a claim of a program's execution and output, along with a valid corresponding STARK proof of computation.
> 3. A STARK proof refers to the underlying proof generated using the [S-two prover].

If for a `Proof`, `Proof.secret` is a `Secret` of kind `Cairo`, the hash of the program's bytecode is in `Proof.secret.data`. The proof must be unlocked by providing a witness `Proof.witness` containing a valid `CairoProof`.

> [!NOTE]
> The Cairo program itself is not stored by the mint and must be communicated through other means (e.g., shared publicly, transmitted off-band, or derived from agreed-upon specifications). The mint only stores and verifies the hash of the program's bytecode in `Secret.data`.

The mint will check that hash of `CairoProof.claim.public_data.public_memory.program` matches with `Proof.secret.data`, and verify the correctness of the STARK proof.

Additionally, it will also check that the hash of `CairoProof.claim.public_data.public_memory.output` matches the value in `Proof.secret.tags.program_output`.

To give a concrete example of the basic case, to mint a locked token we first create a Cairo `Secret` that reads:

```json
[
  "Cairo",
  {
    "nonce": "859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f",
    "data": "0x0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7",
    "tags": [
      [
        "program_output",
        "0xa431d77da3757f6f3ba829b9cdc171ea170073d1b06caaaae58bf169e9bfc380"
      ]
    ]
  }
]
```

Here, `Secret.data` is the hash of the Cairo program's bytecode. We serialize this `Secret` to a string in `Proof.secret` and get a blind signature by the mint that is stored in `Proof.C` (see [NUT-03][03]).

The recipient who possesses a valid `CairoProof` of the program's execution that resulted in an output present in the `Secret.tags.program_output` can spend this `Proof` by providing it in `Proof.witness.cairo_proof`:

```json
{
  "amount": 1,
  "secret": "[\"Cairo\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"0x0249098aa8b9d2fbec49ff8598feb17b592b986e62319a4fa488a3dc36387157a7\",\"tags\":[[\"program_output\",\"0xa431d77da3757f6f3ba829b9cdc171ea170073d1b06caaaae58bf169e9bfc380\"]]}]",
  "C": "02698c4e2b5f9534cd0687d87513c759790cf829aa5739184a3e3735471fbda904",
  "id": "009a1f293253e41e",
  "witness": "{\"cairo_proof\":{\"claim\":{\"public_data\":{\"public_memory\":{\"program\":[[0,[2147450879,67600385,0,0,0,0,0,0]],[1,[2,0,0,0,0,0,0,0]],[2,[2147581952,285507585,0,0,0,0,0,0]],[3,[4,0,0,0,0,0,0,0]],[4,[2147450879,17268737,0,0,0,0,0,0]],[5,[0,0,0,0,0,0,0,0]]]]}}}..."
}
```

#### Witness Format

`CairoWitness` is a serialized JSON string of the form

```json
{
  "cairo_proof": <String>,
  "with_bootloader": <bool>,
  "with_pedersen": <bool>,
}
```

where `cairo_proof` is a serialized `CairoProof` and the `with_pedersen` flag indicates whether the proof contains a pedersen execution trace, necessary for instance when a bootloader is used.

#### STARK Proving Scheme

To spend a token locked with `Cairo`, the spender needs to include a `CairoProof` in the spent `Proof`s. It represents a claim of a [Cairo program]'s execution and output along with a valid corresponding STARK proof of computation, generated using the [S-two Cairo] prover. The STARK proof demonstrates that the specified Cairo program was executed correctly and produced the expected output.

> [!CAUTION]
> Applications must ensure that the mint supports the specific version of the S-two Cairo prover being used. Version compatibility should be verified through the mint's info.

#### Tags

`program_output: <felt_str>` determines the hash of the program's expected output.

The program output is a Cairo `Felt` values (field elements). It is hashed using the `Blake2s` hash function.

#### Optional feature: Bootloading

The mint can optionally choose to support the use of a [bootloader](https://zksecurity.github.io/stark-book/cairo/bootloader.html).
This enables the prover to keep the bytecode of the executed program private, as only the hash of the instructions are revealed to the mint.

The supported bootloader and its version should be specified in the mint info.

> [!NOTE]
> This feature is optional because the same behavior can be achieved without any additional mint-side logic (a bootloader is just a Cairo program after all). This is simply a more convenient and generic way to do it for the sender.

## Example Use Case

#### Prime Number Verification

Tokens can be locked to require proof that the spender knows a prime number (this is just a toy example, as finding a prime number is not something difficult to do).

Consider the following Cairo program that checks primality:

```cairo
/// Checks if a number is prime
///
/// # Arguments
///
/// * `n` - The number to check
///
/// # Returns
///
/// * `true` if the number is prime
/// * `false` if the number is not prime
fn is_prime(n: u32) -> bool {
    if n <= 1 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    let mut i = 3;
    let mut is_prime = true;
    loop {
        if i * i > n {
            break;
        }
        if n % i == 0 {
            is_prime = false;
            break;
        }
        i += 2;
    }
    is_prime
}

// Executable entry point
#[executable]
fn main(input: u32) -> bool {
    is_prime(input)
}
```

This programs returns `true` if the number is prime and `false` otherwise, which respectively corresponds to the outputs `[1]` and `[0]` as arrays of `Felt` values.

The following `Secret` requires the spender to prove that he knows a number `n` such that `is_prime(n) == true` (note that he doesn't need to reveal `n` itself).

```json
[
  "Cairo",
  {
    "nonce": "859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f",
    "data": "e8d4a51000d4c8a9f1b2e3c5d7a9b8c6e4f2a1d3c5b7e9f1a3b5c7d9e1f3a5b7",
    "tags": [
      [
        "program_output",
        "0xa431d77da3757f6f3ba829b9cdc171ea170073d1b06caaaae58bf169e9bfc380"
      ]
    ]
  }
]
```

The witness would contain the claim along with the STARK proof showing that the computation was performed correctly:

```json
{
  "amount": 1000,
  "secret": "[\"Cairo\",{\"nonce\":\"859d4935c4907062a6297cf4e663e2835d90d97ecdd510745d32f6816323a41f\",\"data\":\"e8d4a51000d4c8a9f1b2e3c5d7a9b8c6e4f2a1d3c5b7e9f1a3b5c7d9e1f3a5b7\",\"tags\":[[\"program_output\",\"154809849725474173771833689306955346864791482278938452209165301614543497938\"]]}]",
  "C": "03f1e2d3c4b5a69708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f80",
  "id": "009a1f293253e41e",
  "witness": "{\"cairo_proof\":{\"claim\":{\"public_data\":{\"public_memory\":{\"program\":[[0,[2147450879,67600385,0,0,0,0,0,0]],[1,[2,0,0,0,0,0,0,0]],[2,[2147581952,285507585,0,0,0,0,0,0]],[3,[4,0,0,0,0,0,0,0]],[4,[2147450879,17268737,0,0,0,0,0,0]],[5,[0,0,0,0,0,0,0,0]]]]}}}..."
}
```

## Mint info setting

The [NUT-06][06] `MintMethodSetting` indicates support for this feature, optional features, as well as some information for the configuration of the Cairo prover.

```json
{
  "xx": {
    "supported": true,
    "optional_features": {
      "bootloader": {
        "supported": true,
        "version": "0.14.0", // corresponds to https://github.com/starkware-libs/cairo-lang/blob/v0.13.0/src/starkware/cairo/bootloaders/bootloader/bootloader.cairo and https://github.com/Moonsong-Labs/cairo-bootloader
        "hash": "0xaee9298fc7ffd8f4cbcc277b689cbf3a545379fb09ab90cc0245b7fe15c393a9" // hash of the bootloader program
      }
    },
    "cairo_prover_config": {
      "version": "0.1.1" // the version of the `stwo_cairo_prover` dependency used
    }
  }
}
```

[00]: 00.md
[01]: 01.md
[02]: 02.md
[03]: 03.md
[04]: 04.md
[05]: 05.md
[06]: 06.md
[07]: 07.md
[08]: 08.md
[09]: 09.md
[10]: 10.md
[11]: 11.md
[12]: 12.md
[GPR21]: https://eprint.iacr.org/2021/1063.pdf
[Cairo program]: https://www.cairo-lang.org/
[S-two prover]: (https://github.com/starkware-libs/stwo)
[S-two Cairo]: https://github.com/starkware-libs/stwo-cairo
