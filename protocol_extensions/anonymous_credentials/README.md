# KVAC: Keyed-Verification Anonymous Credentials Extension

This extension implements the KVAC (Keyed-Verification Anonymous Credentials) protocol for Cashu, providing privacy-preserving digital token management using advanced cryptographic primitives.

## Protocol Specifications

The KVAC protocol is defined in the following specifications:

1. [KVAC01](KVAC01.md): Core Protocol Foundations
   - Basic cryptographic types
   - Key structures and operations
   - Commitment schemes
   - Randomization process

2. [KVAC02](KVAC02.md): Operations and Zero-Knowledge Proofs
   - Core operations (bootstrap, spend)
   - Zero-knowledge proof system
   - Transaction flow
   - Error handling

3. [KVAC03](KVAC03.md): Transcript System and Proof Framework
   - Transcript implementation
   - Domain separation
   - Challenge generation
   - Proof framework

4. [KVAC04](KVAC04.md): Bulletproof Range Proofs
   - Bulletproof implementation
   - Inner product arguments
   - Range proof generation and verification
   - Optimizations

## Implementation

The reference implementation is available at:
https://github.com/lollerfirst/cashu-kvac

## Security Considerations

The KVAC protocol provides:
- Privacy through zero-knowledge proofs
- Double-spend prevention through keyed verification
- Amount confidentiality via range proofs
- Script privacy with optional revelation

## License

This extension and its specifications are licensed under the MIT License.
