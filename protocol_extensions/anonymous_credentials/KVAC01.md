# KVAC01: Core Protocol Foundations (Revised)

- Number: KVAC01
- Title: Protocol Foundations
- Type: Standards Track
- Status: Draft
- Created: 2024-01-20
- Authors: N/A
- Requires: BIP340, secp256k1

## Abstract

This document specifies the core components and structures of the KVAC protocol, based on the implementation in the cashu-kvac repository.

## Motivation

Provide precise specifications for the fundamental building blocks of KVAC, ensuring implementations are compatible and secure.

## Specification

### 1. Core Types

#### 1.1 Scalar
```rust
type Scalar = secp256k1::Scalar;
```
Properties:
- Elements of the secp256k1 scalar field
- Used for private keys, blinding factors, and amounts
- Must implement:
  - Random generation
  - Addition/multiplication
  - Conversion to/from bytes
  - Zero and one constants

#### 1.2 GroupElement
```rust
type GroupElement = secp256k1::Point;
```
Properties:
- Points on the secp256k1 curve
- Used for public keys and commitments
- Must implement:
  - Point addition/subtraction
  - Scalar multiplication
  - Conversion to/from bytes
  - Zero point (infinity)

### 2. Fundamental Structures

#### 2.1 Amount Attribute
```rust
struct AmountAttribute {
    a: Scalar,    // Amount value
    r: Scalar,    // Blinding factor
}

impl AmountAttribute {
    fn new(amount: u64, blinding_factor: Option<&[u8]>) -> Self;
    fn commitment(&self) -> GroupElement;
    fn tweak_amount(&mut self, amount: u64) -> &Self;
}
```

#### 2.2 Script Attribute
```rust
struct ScriptAttribute {
    s: Scalar,    // Script hash
    r: Scalar,    // Blinding factor
}

impl ScriptAttribute {
    fn new(script: &[u8], blinding_factor: Option<&[u8]>) -> Self;
    fn commitment(&self) -> GroupElement;
}
```

#### 2.3 Message Authentication Code (MAC)
```rust
struct MAC {
    t: Scalar,            // Random tag
    V: GroupElement,      // MAC value
}

impl MAC {
    fn generate(
        privkey: &MintPrivateKey,
        amount_commitment: &GroupElement,
        script_commitment: Option<&GroupElement>,
        t_tag: Option<&Scalar>
    ) -> Result<Self, Error>;
}
```

#### 2.4 Coin Structure
```rust
struct Coin {
    amount_attribute: AmountAttribute,
    script_attribute: Option<ScriptAttribute>,
    mac: MAC,
}
```

#### 2.5 Randomized Coin
```rust
struct RandomizedCoin {
    Ca: GroupElement,     // Randomized amount commitment
    Cs: GroupElement,     // Randomized script commitment
    Cx0: GroupElement,    // Randomized MAC generator U
    Cx1: GroupElement,    // Randomized tag commitment
    Cv: GroupElement,     // Randomized MAC
}

impl RandomizedCoin {
    fn from_coin(coin: &Coin, reveal_script: bool) -> Result<Self, Error>;
}
```

### 3. Key Management

#### 3.1 Mint Private Key
```rust
struct MintPrivateKey {
    w: Scalar,           // MAC primary key
    w_: Scalar,          // MAC secondary key
    x0: Scalar,          // MAC tag key 1
    x1: Scalar,          // MAC tag key 2
    ya: Scalar,          // Amount signing key
    ys: Scalar,          // Script signing key
    public_key: MintPublicKey,
}
```

#### 3.2 Mint Public Key
```rust
struct MintPublicKey {
    Cw: GroupElement,    // Public commitment to w,w'
    I: GroupElement,     // Public identity component
}
```

### 4. Commitment Scheme

#### 4.1 Amount Commitment
```
M_a = r_a·G_blind + a·G_amount
```
where:
- r_a is the blinding factor
- a is the amount
- G_blind, G_amount are generator points

#### 4.2 Script Commitment
```
M_s = r_s·G_blind + s·G_script
```
where:
- r_s is the blinding factor
- s is the script hash (SHA256)
- G_blind, G_script are generator points

### 5. Randomization Process

When spending a coin, it must be randomized to break linkability:

1. For an input coin (M_a, M_s, MAC):
```
Ca = r_a·G_zamount + M_a
Cs = r_a·G_zscript + M_s
Cx0 = r_a·G_x0 + U
Cx1 = r_a·G_x1 + t·U
Cv = r_a·G_zmac + V
```
where:
- r_a is the amount blinding factor
- U = HashToCurve(t)
- t is the MAC tag
- V is the MAC value

2. For script revelation:
```
Cs = r_a·G_blind  // Only blinding term
```

### 6. Transcript System

#### 6.1 Transcript Structure
```rust
struct CashuTranscript {
    state: Strobe128,
    domain_sep: Vec<u8>,
}

impl CashuTranscript {
    fn new() -> Self;
    fn domain_sep(&mut self, label: &[u8]);
    fn append_element(&mut self, label: &[u8], element: &GroupElement);
    fn get_challenge(&mut self, label: &[u8]) -> Scalar;
}
```

### 7. Constants and Limits

```rust
const RANGE_LIMIT: u64 = u32::MAX as u64;  // Maximum token value
```

## Security Considerations

1. **Key Generation**
   - Private keys must use secure random number generation
   - All scalars must be properly reduced modulo curve order

2. **Commitment Properties**
   - Hiding: Blinding factors must be random
   - Binding: Based on discrete logarithm hardness

3. **Randomization**
   - Must use the same r_a for all components
   - Script revelation destroys unlinkability

4. **Implementation Requirements**
   - Constant-time operations for all sensitive computations
   - Proper domain separation in transcripts
   - Secure random number generation

## Test Vectors

(To be added: Test vectors for key generation, commitments, and randomization)

## Reference Implementation

The reference implementation is available in:
- src/models.rs: Core data structures
- src/secp.rs: Cryptographic primitives
- src/generators.rs: Generator points
- src/transcript.rs: Transcript system

## Copyright

This document is licensed under the MIT License.
