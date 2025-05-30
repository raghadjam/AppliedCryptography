import random
from task2_des import des_encrypt

def flip_bit(bin_str, index):
    """Flip the bit at the specified index (0-based)"""
    flipped = list(bin_str)
    flipped[index] = '0' if bin_str[index] == '1' else '1'
    return ''.join(flipped)

def count_differences(bin1, bin2):
    """Count differing bits between two binary strings"""
    return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))

def random_bin_string(length):
    """Generate a random binary string of given length"""
    return ''.join(random.choice('01') for _ in range(length))

def avalanche_experiment(trials=10):
    print("DES Avalanche Effect Analysis ({} Trials)".format(trials))
    print("------------------------------------------------------------")
    print("{:<8} {:<25} {:<25}".format("Trial", "# Diff Bits (Plain Flip)", "# Diff Bits (Key Flip)"))

    for trial in range(1, trials + 1):
        # Generate random 64-bit plaintext and 64-bit key
        plaintext = random_bin_string(64)
        key = random_bin_string(64)  # Assuming your DES implementation accepts 64-bit key

        try:
            # Encrypt with original inputs
            c1 = des_encrypt(plaintext, key)
            if len(c1) != 64:
                raise ValueError("Ciphertext length not 64 bits")
        except Exception as e:
            print(f"[Trial {trial}] Error during original encryption: {e}")
            continue

        # Flip one bit in the plaintext
        flip_index_plain = random.randint(0, 63)
        flipped_plaintext = flip_bit(plaintext, flip_index_plain)

        try:
            c2_plainflip = des_encrypt(key,flipped_plaintext)
            if len(c2_plainflip) != 64:
                raise ValueError("Ciphertext length not 64 bits (plaintext flip)")
        except Exception as e:
            print(f"[Trial {trial}] Error during plaintext flip encryption: {e}")
            continue

        # Flip one bit in the key
        flip_index_key = random.randint(0, 63)
        flipped_key = flip_bit(key, flip_index_key)

        try:
            c2_keyflip = des_encrypt(flipped_key, plaintext)
            if len(c2_keyflip) != 64:
                raise ValueError("Ciphertext length not 64 bits (key flip)")
        except Exception as e:
            print(f"[Trial {trial}] Error during key flip encryption: {e}")
            continue

        # Count differences in ciphertexts
        diff_plain = count_differences(c1, c2_plainflip)
        diff_key = count_differences(c1, c2_keyflip)

        print("{:<8} {:<25} {:<25}".format(trial, diff_plain, diff_key))

if __name__ == "__main__":
    avalanche_experiment()
