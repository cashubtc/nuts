# KVAC02: Operations and Zero-Knowledge Proofs (Revised)

- Number: KVAC02
- Title: Operations and Zero-Knowledge Proofs
- Type: Standards Track
- Status: Draft
- Created: 2024-01-20
- Authors: N/A
- Requires: KVAC01

## Abstract

This document specifies the core operations and zero-knowledge proofs used in KVAC transactions, based on the implementation in src/kvac.rs.

## Motivation

Define the standard operations and proof systems that ensure privacy and security in KVAC transactions.

## Specification

### 1. Core Proof System

#### 1.1 Schnorr Prover
```rust
struct SchnorrProver<'a> {
    random_terms: Vec<Scalar>,
    secrets: Vec<Scalar>,
    transcript: &'a mut CashuTranscript,
}

impl SchnorrProver {
    fn new(transcript: &mut CashuTranscript, secrets: Vec<Scalar>) -> Self;
    fn add_statement(self, statement: Statement) -> Self;
    fn prove(self) -> ZKP;
}
```

#### 1.2 Schnorr Verifier
```rust
struct SchnorrVerifier<'a> {
    responses: Vec<Scalar>,
    challenge: Scalar,
    transcript: &'a mut CashuTranscript,
}

impl SchnorrVerifier {
    fn new(transcript: &mut CashuTranscript, proof: ZKP) -> Self;
    fn add_statement(self, statement: Statement) -> Self;
    fn verify(&mut self) -> bool;
}
```

#### 1.3 Zero-Knowledge Proof Structure
```rust
struct ZKP {
    s: Vec<Scalar>,    // Responses
    c: Scalar,         // Challenge
}

struct Statement {
    domain_separator: &'static [u8],
    equations: Vec<Equation>,
}

struct Equation {
    lhs: GroupElement,
    rhs: Vec<Vec<GroupElement>>,
}
```

### 2. Operation-Specific Proofs

#### 2.1 Bootstrap Proof
Purpose: Prove an amount commitment encodes zero
```rust
impl BootstrapProof {
    // Create statement: M_a = r·G_blind
    fn statement(amount_commitment: &GroupElement) -> Statement;
    
    // Create proof for initial zero tokens
    fn create(
        amount_attribute: &AmountAttribute,
        transcript: &mut CashuTranscript
    ) -> ZKP;
    
    // Verify bootstrap proof
    fn verify(
        amount_commitment: &GroupElement,
        proof: ZKP,
        transcript: &mut CashuTranscript
    ) -> bool;
}
```

#### 2.2 MAC Proof
Purpose: Prove a randomized coin was derived from a valid MAC
```rust
impl MacProof {
    // Create statement for MAC verification
    fn statement(
        Z: GroupElement,
        I: GroupElement,
        randomized_coin: &RandomizedCoin
    ) -> Statement;
    
    // Create proof of MAC validity
    fn create(
        mint_publickey: &MintPublicKey,
        coin: &Coin,
        randomized_coin: &RandomizedCoin,
        transcript: &mut CashuTranscript
    ) -> ZKP;
    
    // Verify MAC proof
    fn verify(
        mint_privkey: &MintPrivateKey,
        randomized_coin: &RandomizedCoin,
        script: Option<&[u8]>,
        proof: ZKP,
        transcript: &mut CashuTranscript
    ) -> bool;
}
```

#### 2.3 Issuance Parameters Proof
Purpose: Prove mint keys are used consistently
```rust
impl IssuanceProof {
    // Create statement for key consistency
    fn statement(
        mint_publickey: &MintPublicKey,
        mac: &MAC,
        amount_commitment: &GroupElement,
        script_commitment: &GroupElement
    ) -> Statement;
    
    // Create proof of key consistency
    fn create(
        mint_privkey: &MintPrivateKey,
        mac: &MAC,
        amount_commitment: &GroupElement,
        script_commitment: Option<&GroupElement>
    ) -> ZKP;
    
    // Verify key consistency
    fn verify(
        mint_publickey: &MintPublicKey,
        coin: &Coin,
        proof: ZKP
    ) -> bool;
}
```

#### 2.4 Balance Proof
Purpose: Prove conservation of value
```rust
impl BalanceProof {
    // Create statement for balance
    fn statement(B: GroupElement) -> Statement;
    
    // Create proof of balance conservation
    fn create(
        inputs: &[AmountAttribute],
        outputs: &[AmountAttribute],
        transcript: &mut CashuTranscript
    ) -> ZKP;
    
    // Verify balance proof
    fn verify(
        inputs: &[RandomizedCoin],
        outputs: &[GroupElement],
        delta_amount: i64,
        proof: ZKP,
        transcript: &mut CashuTranscript
    ) -> bool;
}
```

#### 2.5 Script Equality Proof
Purpose: Prove scripts match across coins
```rust
impl ScriptEqualityProof {
    // Create statement for script equality
    fn statement(
        inputs: &[RandomizedCoin],
        outputs: &[(GroupElement, GroupElement)]
    ) -> Statement;
    
    // Create proof of script equality
    fn create(
        inputs: &[Coin],
        randomized_inputs: &[RandomizedCoin],
        outputs: &[(AmountAttribute, ScriptAttribute)],
        transcript: &mut CashuTranscript
    ) -> Result<ZKP, Error>;
    
    // Verify script equality
    fn verify(
        randomized_inputs: &[RandomizedCoin],
        outputs: &[(GroupElement, GroupElement)],
        proof: ZKP,
        transcript: &mut CashuTranscript
    ) -> bool;
}
```

### 3. Transaction Flow

#### 3.1 Bootstrap Operation
1. Client creates AmountAttribute encoding 0
2. Client generates BootstrapProof
3. Client sends (M_a, π_bootstrap) to mint
4. Mint verifies proof
5. Mint issues MAC and IParamsProof
6. Client verifies IParamsProof

#### 3.2 Spend Operation
1. Client creates RandomizedCoins from inputs
2. Client creates new AmountAttributes for outputs
3. Client generates:
   - MacProof for each input
   - BalanceProof for conservation
   - ScriptEqualityProof if needed
4. Mint verifies all proofs
5. Mint generates MACs for outputs
6. Mint provides IParamsProof
7. Client verifies IParamsProof

### 4. Error Handling

```rust
enum Error {
    InvalidMintPrivateKey,
    EmptyList,
    NoScriptProvided,
    // Add other error types
}
```

## Security Considerations

1. **Proof System**
   - Domain separation for each proof type
   - Non-zero scalar verification
   - Challenge generation through transcript

2. **Transaction Verification**
   - All proofs must be verified
   - Script revelation handled carefully
   - Balance checked precisely

3. **Implementation Requirements**
   - Secure random number generation
   - Constant-time operations
   - Complete verification required

## Test Vectors

(Include key test cases from src/kvac.rs tests)

## Reference Implementation

The reference implementation is available in:
- src/kvac.rs: Main protocol operations
- src/models.rs: Data structures
- Tests show correct usage patterns

## Copyright

This document is licensed under the MIT License.
