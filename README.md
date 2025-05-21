# Applied Cryptography 

This repository contains three cryptographic tasks focused on symmetric key cryptography. All cryptographic primitives and attacks were implemented from scratch without the use of third-party crypto libraries.

## Contents

### Task 1 – Stream Cipher Cryptanalysis  
This task targets ciphertexts encrypted with the same keystream (a Many Time Pad vulnerability). The approach involves:
- XORing pairs of ciphertexts to identify probable space characters based on ASCII behavior.
- Using these inferences to recover parts of the plaintexts and keystream.
- Decrypting a target ciphertext using the partially or fully recovered keystream.

### Task 2 – DES Implementation and Analysis  
Implements the DES algorithm in full detail:
- Modular design covering initial/final permutations, expansion, S-boxes, P-box, and key scheduling.
- An interactive script for encrypting/decrypting 64-bit inputs with 56-bit DES keys.
- An analysis script that demonstrates the avalanche effect by flipping a single bit in the key or plaintext and measuring changes in the ciphertext.

### Task 3 – Meet-in-the-Middle Attack on Triple DES  
Performs a Meet-in-the-Middle attack on a simplified 3DES system where both keys have only 12 bits of entropy:
- Generates all possible encryptions with K1 on a known plaintext and stores the results.
- Decrypts the corresponding ciphertext using all possible K2 values.
- Matches intermediate states to recover both keys.
- Uses checkpointing to resume long computations and includes a query API for encryption.

## Contributors

- [Raghad Jamhour](https://github.com/raghadjam)  
- [Yasmin Al Shawawrh](https://github.com/YasminAlShawawrh)
