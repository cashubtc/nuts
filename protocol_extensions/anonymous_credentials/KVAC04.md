# KVAC04: Bulletproof Range Proofs (Revised)

- Number: KVAC04
- Title: Bulletproof Range Proofs Implementation
- Type: Standards Track
- Status: Draft
- Created: 2024-01-20
- Authors: N/A
- Requires: KVAC01, KVAC02, KVAC03

## Abstract

This document specifies the Bulletproof range proof implementation used in KVAC to prove that amounts lie within valid ranges.

## Motivation

Define the exact Bulletproof implementation for proving amount ranges without revealing values, based on the paper "Bulletproofs: Short Proofs for Confidential Transactions and More".

## Specification

### 1. Constants and Parameters

```rust
// Maximum amount limit
const RANGE_LIMIT: u64 = 1 << 32;
const LOG_RANGE_LIMIT: usize = 32;

// Pre-computed values
static POWERS_OF_TWO: Vec<Scalar> = [1, 2, 4, ..., 2^31];

// Generators (NUMS points)
static G: Vec<GroupElement> = hash_to_curve("IPA_G_i_") for i in 0..32
static H: Vec<GroupElement> = hash_to_curve("IPA_H_i_") for i in 0..32
static U: GroupElement = hash_to_curve("IPA_U_")
```

### 2. Core Structures

#### 2.1 Inner Product Argument
```rust
struct InnerProductArgument {
    // Log n proof elements
    recursion_inputs_left: Vec<GroupElement>,
    recursion_inputs_right: Vec<GroupElement>,
    
    // Final scalars
    recursion_end_scalar_left: Scalar,
    recursion_end_scalar_right: Scalar,
}
```

#### 2.2 Bulletproof
```rust
struct BulletProof {
    A: GroupElement,     // Bit commitment
    S: GroupElement,     // Blinding commitment
    T1: GroupElement,    // Polynomial coefficient 1
    T2: GroupElement,    // Polynomial coefficient 2
    t_x: Scalar,        // Polynomial evaluation
    tau_x: Scalar,      // Blinding evaluation
    mu: Scalar,         // Combined blinding factor
    ipa: InnerProductArgument,
}
```

### 3. Protocol Steps

#### 3.1 Proof Generation

1. **Initialize**:
```rust
fn new(transcript: &mut CashuTranscript, attributes: &[AmountAttribute]) -> Self {
    // Domain separation
    transcript.domain_sep(b"Bulletproof_Statement_");
    
    let m = attributes.len();
    let n = LOG_RANGE_LIMIT;
    
    // Pad to power of 2 if needed
    let next_len_pow2 = 1 << ((n * m).ilog2() + 1);
}
```

2. **Bit Decomposition**:
```rust
// Convert amounts to bit vectors
let mut a_left = Vec::new();
let mut a_right = Vec::new();
for attribute in attributes {
    let amount: u64 = attribute.a.into();
    for i in 0..n {
        let bit = (amount >> i) & 1;
        a_left.push(Scalar::from(bit));
        a_right.push(Scalar::from(1 - bit));
    }
}
```

3. **Initial Commitments**:
```rust
// Commit to bits
let alpha = Scalar::random();
let mut A = G_blind * alpha;
for (a_l_i, G_i, a_r_i, H_i) in izip!(a_left, G, a_right, H) {
    A = A + (G_i * a_l_i + H_i * a_r_i);
}

// Commit to blinding factors
let rho = Scalar::random();
let mut S = G_blind * rho;
for (s_l_i, G_i, s_r_i, H_i) in izip!(s_l, G, s_r, H) {
    S = S + (G_i * s_l_i + H_i * s_r_i);
}
```

4. **Polynomial Creation**:
```rust
// Get challenges
let y = transcript.get_challenge(b"y_chall_");
let z = transcript.get_challenge(b"z_chall_");

// Create l(X) polynomial
let l_0 = a_left + z;
let l_1 = s_l;

// Create r(X) polynomial  
let r_0 = y^n * (a_right + z) + z^2 * z^j * 2^i;
let r_1 = y^n * s_r;
```

5. **Polynomial Commitments**:
```rust
// Hide polynomial coefficients
let tau_1 = Scalar::random();
let tau_2 = Scalar::random();
let T1 = G_amount * t_1 + G_blind * tau_1;
let T2 = G_amount * t_2 + G_blind * tau_2;
```

6. **Inner Product Creation**:
```rust
// Evaluate polynomials at x
let x = transcript.get_challenge(b"x_chall_");
let l_x = l_0 + x*l_1;
let r_x = r_0 + x*r_1;

// Create inner product argument
let ipa = InnerProductArgument::new(
    transcript,
    (G, H, U),
    P,
    l_x,
    r_x
);
```

#### 3.2 Proof Verification

1. **Initial Checks**:
```rust
fn verify(
    self,
    transcript: &mut CashuTranscript,
    attribute_commitments: &[GroupElement]
) -> bool {
    // Verify proof size matches input size
    let n = LOG_RANGE_LIMIT;
    let len_pow2 = 1 << self.ipa.public_inputs_len();
    let m = len_pow2 / n;
    
    // Check length is correct
    let check = n * attribute_commitments.len();
    if (check.count_ones() != 1) {
        return false;
    }
}
```

2. **Challenge Recreation**:
```rust
// Recreate challenges
let y = transcript.get_challenge(b"y_chall_");
let z = transcript.get_challenge(b"z_chall_");
let x = transcript.get_challenge(b"x_chall_");
```

3. **Polynomial Verification**:
```rust
// Verify polynomial evaluation
if G_amount * t_x + G_blind * tau_x != 
   V_z_m * z^2 + G_amount * delta + T1 * x + T2 * x^2 {
    return false;
}
```

4. **Inner Product Verification**:
```rust
// Switch generators
let H_new = y^(-n) * H;

// Verify inner product argument
self.ipa.verify(transcript, (G, H_new, U), P, t_x)
```

### 4. Inner Product Protocol

#### 4.1 Argument Generation
```rust
impl InnerProductArgument {
    fn new(
        transcript: &mut CashuTranscript,
        generators: (Vec<GroupElement>, Vec<GroupElement>, GroupElement),
        P: GroupElement,
        mut a: Vec<Scalar>,
        mut b: Vec<Scalar>
    ) -> Self {
        // Recursive subdivision
        while n > 1 {
            n >>= 1;
            
            // Calculate cross terms
            let c_left = inner_product(&a[..n], &b[n..]);
            let c_right = inner_product(&a[n..], &b[..n]);
            
            // Create L,R terms
            let L = compute_L(c_left, ...);
            let R = compute_R(c_right, ...);
            
            // Get challenge and fold
            let x = transcript.get_challenge(b"IPA_chall_");
            let x_inv = x.invert();
            
            // Fold vectors a,b
            fold_vectors(&mut a, &mut b, x, x_inv);
            
            // Fold generators
            fold_generators(&mut G, &mut H, x, x_inv);
        }
    }
}
```

#### 4.2 Verification
```rust
impl InnerProductArgument {
    fn verify(
        self,
        transcript: &mut CashuTranscript,
        generators: (Vec<GroupElement>, Vec<GroupElement>, GroupElement),
        mut P: GroupElement,
        c: Scalar
    ) -> bool {
        // Verify P commitment
        let mut G_aH_b = GENERATORS.O;
        
        // Unroll recursion efficiently
        for (i, (G_i, H_i)) in G.iter().zip(H.iter()).enumerate() {
            let s = compute_challenge_product(i, challenges);
            G_aH_b += G_i * (s * a) + H_i * (s.invert() * b);
        }
        
        G_aH_b + (U * (a * b)) == P
    }
}
```

### 5. Optimizations

1. **Generator Caching**:
   - Pre-compute and cache generators
   - Cache powers of two
   - Reuse generators when possible

2. **Vector Operations**:
   - Efficient vector folding
   - Batch inversions where possible
   - Minimize allocations

3. **Verification Speed**:
   - Unroll recursion in verification
   - Batch scalar multiplications
   - Efficient challenge computation

## Security Considerations

1. **Range Requirements**
   - Values must be 32 bits or less
   - Proper bit decomposition required
   - No negative values allowed

2. **Implementation Security**
   - Constant-time operations
   - No early termination
   - Proper padding to powers of 2

3. **Proof System**
   - Zero-knowledge property
   - Strong soundness guarantee
   - Proper challenge generation

## Test Vectors

(Include test vectors from bulletproof.rs tests)

## Reference Implementation

The reference implementation is available in:
- src/bulletproof.rs: Main implementation
- Unit tests demonstrate usage

## Copyright

This document is licensed under the MIT License.
