from task2_des import des_encrypt, des_decrypt
import sys


def is_valid_hex(hex_str, expected_bits):
    """Check if the input string is a valid hex string with the correct number of hex digits."""
    try:
        # Try to convert the hex string to an integer
        int(hex_str, 16)
        # Check if the length of the hex string is correct
        return len(hex_str) == expected_bits // 4
    except ValueError:
        # If conversion fails, it's not a valid hex string
        return False


def main():
    print("Welcome to DES Encryption/Decryption")

    operation = input("Enter 'E' to Encrypt or 'D' to Decrypt: ").strip().upper()

    if operation not in ['E', 'D']:
        print("Invalid operation. Please enter 'E' or 'D'.")
        sys.exit(1)

    data = input("Enter 64-bit data in hex (16 hex digits): ").strip()
    print(f"[DEBUG] You entered data: {data} (length: {len(data)})")  # Debug statement

    if not is_valid_hex(data, 64):
        print("Invalid data. It must be 16 hex digits (64 bits).")
        sys.exit(1)

    key = input("Enter 56-bit key in hex (14 hex digits): ").strip()
    print(f"[DEBUG] You entered key: {key} (length: {len(key)})")  # Debug statement

    if not is_valid_hex(key, 56):
        print("Invalid key. It must be 14 hex digits (56 bits).")
        sys.exit(1)

    # Show binary conversions
    data_bin = bin(int(data, 16))[2:].zfill(64)
    key_bin = bin(int(key, 16))[2:].zfill(56)
    print(f"[DEBUG] Binary data: {data_bin}")
    print(f"[DEBUG] Binary key : {key_bin}")

    if operation == 'E':
        cipher_bin = des_encrypt(data_bin, key_bin)
        cipher_hex = hex(int(cipher_bin, 2))[2:].upper().zfill(16)
        print(f"Ciphertext (hex): {cipher_hex}")
    else:
        plain_bin = des_decrypt(data_bin, key_bin)
        plain_hex = hex(int(plain_bin, 2))[2:].upper().zfill(16)
        print(f"Plaintext (hex): {plain_hex}")

if __name__ == "__main__":
    main()