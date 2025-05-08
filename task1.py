import binascii
import re

def strxor(a, b):
    return bytearray([x ^ y for x, y in zip(a, b)])

# Load all ciphertexts from the given file
def load_ciphertexts(filename):
    ciphertexts = []
    with open(filename, 'r') as file:
        current_cipher = ""
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Ciphertext"):
                if current_cipher:
                    ciphertexts.append(bytearray.fromhex(current_cipher))
                current_cipher = ""
            else:
                current_cipher += line.strip()
        if current_cipher:
            ciphertexts.append(bytearray.fromhex(current_cipher))
    ciphertexts = [c for c in ciphertexts if c is not None]
    print(f"Loaded {len(ciphertexts)} valid ciphertexts.")
    return ciphertexts

# Attempt to recover keystream using XOR pair analysis
def recover_keystream(ciphertexts):
    max_len = max(len(c) for c in ciphertexts)
    key = [None] * max_len
    space_hits = [ [0]*max_len for _ in range(len(ciphertexts)) ]
    for i in range(len(ciphertexts)):
        for j in range(len(ciphertexts)):
            if i == j:
                continue
            c1 = ciphertexts[i]
            c2 = ciphertexts[j]
            xor = strxor(c1, c2)
            for k in range(len(xor)):
                if (65 <= xor[k] <= 90) or (97 <= xor[k] <= 122):
                    space_hits[i][k] += 1
    for i, hits in enumerate(space_hits):
        c = ciphertexts[i]
        for j, count in enumerate(hits):
            if count >= 7 and j < len(c):
                key[j] = c[j] ^ 0x20
    return key

# Decrypt the given ciphertext using the partially recovered keystream
def decrypt_with_key(ciphertext, key):
    decrypted = []
    for i in range(len(ciphertext)):
        if i < len(key) and key[i] is not None:
            decrypted_char = chr(ciphertext[i] ^ key[i])
        else:
            decrypted_char = '*'
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

# Main process
if __name__ == "__main__":
    # Load all ciphertexts
    ciphertexts = load_ciphertexts("given_ciphertext.txt")

    # Load the target ciphertext from file
    with open("target_ciphertext.txt", "r") as f:
        lines = f.readlines()

    # Improved block to extract the hex string
    target_hex = ''
    for i, line in enumerate(lines):
        if line.startswith("Target Ciphertext:"):
            hex_part = line.split(":", 1)[-1].strip()
            if re.fullmatch(r'[0-9a-fA-F]+', hex_part):
                target_hex = hex_part
            else:
                if i + 1 < len(lines):
                    target_hex = lines[i + 1].strip()
            break

    if re.fullmatch(r'[0-9a-fA-F]+', target_hex):
        print("Target ciphertext extracted successfully.")
        target_ciphertext = bytearray.fromhex(target_hex)
    else:
        print("Failed to load or convert the target ciphertext.")
        target_ciphertext = None

    # Proceed if the target ciphertext is valid
    if target_ciphertext is not None:
        key = recover_keystream(ciphertexts)
        plaintext = decrypt_with_key(target_ciphertext, key)
        print("Recovered partial plaintext:")
        print(plaintext)
    else:
        print("Target ciphertext is invalid. Aborting.")