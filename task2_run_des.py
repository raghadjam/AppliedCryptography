import sys
from task2_des import des_encrypt, des_decrypt
def is_valid_hex(hex_str, expected_bits):
    valid_hex_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", 
                       "a", "b", "c", "d", "e", "f"]
    
    if len(hex_str) != expected_bits // 4:
        return False
    
    for char in hex_str:
        if char not in valid_hex_chars:
            return False
    
    return True


def main():
    print("Welcome to DES Encryption/Decryption")

    operation = input("Enter 'E' to Encrypt or 'D' to Decrypt: ").strip().upper()

    if operation not in ['E', 'D', 'e', 'd']:
        print("Invalid operation.")
        sys.exit(1)

    data = input("Enter 64-bit data in hex (16 hex digits): ").strip()
    if not is_valid_hex(data, 64):
        print("Invalid data. It must be 16 hex digits (64 bits).")
        sys.exit(1)

    key = input("Enter 56-bit key in hex (14 hex digits): ").strip()
    if not is_valid_hex(key, 56):
        print("Invalid key. It must be 14 hex digits (56 bits).")
        sys.exit(1)

    # Convert to bit lists
    data_bits = [int(b) for b in bin(int(data, 16))[2:].zfill(64)]
    key_bits = [int(b) for b in bin(int(key, 16))[2:].zfill(56)]

    if operation == 'E':
        cipher_bits = des_encrypt(key_bits, data_bits)
        cipher_hex = hex(int(''.join(str(b) for b in cipher_bits), 2))[2:].upper().zfill(16)
        print(f"Ciphertext (hex): {cipher_hex}")
    else:
        plain_bits = des_decrypt(key_bits, data_bits)
        plain_hex = hex(int(''.join(str(b) for b in plain_bits), 2))[2:].upper().zfill(16)
        print(f"Plaintext (hex): {plain_hex}")

if __name__ == "__main__":
    main() 