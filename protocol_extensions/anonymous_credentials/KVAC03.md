# KVAC03: Transcript System and Proof Framework (Revised)

- Number: KVAC03
- Title: Transcript System and Proof Framework
- Type: Standards Track
- Status: Draft 
- Created: 2024-01-20
- Authors: N/A
- Requires: KVAC01, KVAC02

## Abstract

This document specifies the transcript system and proof framework used in KVAC for Fiat-Shamir transformations and zero-knowledge proofs.

## Motivation

Define the standard transcript system that ensures proper domain separation and challenge generation for all proofs in KVAC.

## Specification

### 1. Transcript System

#### 1.1 Core Structure
```rust
struct CashuTranscript {
    inner: merlin::Transcript,
}

impl CashuTranscript {
    // Create new transcript with Cashu domain
    fn new() -> Self {
        Transcript::new(b"Secp256k1_Cashu_")
    }
    
    // Add domain separator
    fn domain_sep(&mut self, message: &[u8]);
    
    // Append group element
    fn append_element(
        &mut self,
        label: &'static [u8],
        element: &GroupElement
    );
    
    // Get challenge scalar
    fn get_challenge(&mut self, label: &'static [u8]) -> Scalar;
}
```

#### 1.2 Data Serialization 

Group Elements:
```rust
// Convert GroupElement to compressed bytes
fn into_bytes(element: &GroupElement) -> [u8; 33] {
    element.serialize_compressed()
}
```

Challenge Generation:
```rust
// Generate 32-byte challenge
fn get_challenge(&mut self, label: &[u8]) -> Scalar {
    let mut bytes = [0u8; 32];
    self.inner.challenge_bytes(label, &mut bytes);
    Scalar::new(&bytes)
}
```

### 2. Domain Separation

#### 2.1 Protocol Domains
```rust
const DOMAINS = {
    "Bootstrap": b"Bootstrap_Statement_",
    "MAC": b"MAC_Statement_",
    "IParams": b"Iparams_Statement_",
    "Balance": b"Balance_Statement_",
    "Script": b"Script_Equality_Statement_",
    "Bulletproof": b"Bulletproof_Statement_"
};
```

#### 2.2 Label Convention
```rust
const LABELS = {
    "Commitment": b"Com(P)_",
    "Generator": b"G_",
    "Response": b"R_",
    "Value": b"V_",
    "Challenge": b"chall_"
};
```

### 3. Statement Framework

#### 3.1 Basic Statement
```rust
struct Statement {
    // Protocol-specific domain separator
    domain_separator: &'static [u8],
    
    // List of equations to prove
    equations: Vec<Equation>
}

impl Statement {
    fn new(
        domain_separator: &'static [u8],
        equations: Vec<Equation>
    ) -> Self;
}
```

#### 3.2 Equation Structure
```rust
struct Equation {
    // Left-hand side (verification value)
    lhs: GroupElement,
    
    // Right-hand side (relation construction)
    rhs: Vec<Vec<GroupElement>>
}

impl Equation {
    fn new(lhs: GroupElement, rhs: Vec<Vec<GroupElement>>) -> Self;
}
```

### 4. Proof Generation Framework

#### 4.1 Proof Creation
```rust
// Generate proof using statement
fn create_proof<'a>(
    statement: Statement,
    secrets: Vec<Scalar>,
    transcript: &'a mut CashuTranscript
) -> ZKP {
    // 1. Initialize prover
    let prover = SchnorrProver::new(transcript, secrets);
    
    // 2. Add statement
    let prover = prover.add_statement(statement);
    
    // 3. Generate proof
    prover.prove()
}
```

#### 4.2 Proof Verification
```rust
// Verify proof against statement
fn verify_proof<'a>(
    statement: Statement,
    proof: ZKP,  
    transcript: &'a mut CashuTranscript
) -> bool {
    // 1. Initialize verifier
    let verifier = SchnorrVerifier::new(transcript, proof);
    
    // 2. Add statement
    let verifier = verifier.add_statement(statement);
    
    // 3. Verify proof
    verifier.verify()
}
```

### 5. Transcript Usage Pattern

#### 5.1 Prover Side
```rust
let mut transcript = CashuTranscript::new();

// 1. Domain separation
transcript.domain_sep(statement.domain_separator);

// 2. Append public inputs
for equation in statement.equations {
    // Add commitment R
    transcript.append_element(b"R_", &R);
    
    // Add verification value V
    transcript.append_element(b"V_", &equation.lhs);
}

// 3. Get challenge
let c = transcript.get_challenge(b"chall_");
```

#### 5.2 Verifier Side
```rust
let mut transcript = CashuTranscript::new();

// 1. Domain separation
transcript.domain_sep(statement.domain_separator);

// 2. Recompute commitments
for equation in statement.equations {
    let R = recompute_commitment(equation, proof.responses);
    transcript.append_element(b"R_", &R);
    transcript.append_element(b"V_", &equation.lhs);
}

// 3. Verify challenge
let c = transcript.get_challenge(b"chall_");
assert_eq!(c, proof.challenge);
```

### 6. Security Properties

1. **Domain Separation**
   - Each proof type has unique domain
   - Labels prevent cross-protocol attacks
   - Hierarchical separation structure

2. **Challenge Generation**
   - Based on all transcript state
   - Uses cryptographic hash function
   - 256-bit security level

3. **Transcript Properties**
   - Append-only operation
   - No state rollback allowed
   - Sequential challenge derivation

## Security Considerations

1. **Implementation Requirements**
   - Must use constant-time operations
   - Proper domain separation required
   - Complete verification needed

2. **Transcript Usage**
   - Fresh transcript per proof
   - Proper label usage required
   - No transcript reuse

3. **Challenge Security**
   - Must use all public inputs 
   - Strong collision resistance
   - Non-malleability guarantees

## Test Vectors

(Include test vectors from transcript.rs unit tests)

## Reference Implementation

The reference implementation is available in:
- src/transcript.rs: Transcript system
- src/kvac.rs: Proof framework usage
- Unit tests demonstrate correct patterns

## Copyright

This document is licensed under the MIT License.
