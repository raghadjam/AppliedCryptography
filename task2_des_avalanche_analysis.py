import random
from task2_des import des_encrypt

def flip_bit(bin_str, index):
    # Flip the bit at the specified index (0-based)
    flipped = list(bin_str)
    flipped[index] = '0' if bin_str[index] == '1' else '1'
    return ''.join(flipped)

def count_differences(bin1, bin2):
    # Count differing bits between two binary strings
    return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))

def random_bin_string(length):
    # Generate a random binary string of given length
    return ''.join(random.choice('01') for _ in range(length))

def avalanche_experiment(trials=10):
    print("DES Avalanche Effect Analysis ({} Trials)".format(trials))
    print("------------------------------------------------------------")
    print("{:<8} {:<25} {:<25}".format("Trial", "# Diff Bits (Plain Flip)", "# Diff Bits (Key Flip)"))

    for trial in range(1, trials + 1):
        # Generate random 64-bit plaintext and 64-bit key
        plaintext = random_bin_string(64)
        key = random_bin_string(64)

        # Encrypt with original inputs
        try:
            c1 = des_encrypt(plaintext, key)
        except AssertionError as e:
            print(f"[Trial {trial}] ERROR in original encryption: {e}")
            continue

        # Flip one bit in the plaintext
        flip_index_plain = random.randint(0, 63)
        flipped_plaintext = flip_bit(plaintext, flip_index_plain)
        try:
            c2_plainflip = des_encrypt(flipped_plaintext, key)
        except AssertionError as e:
            print(f"[Trial {trial}] ERROR in plaintext flip encryption: {e}")
            continue

        # Flip one bit in the key
        flip_index_key = random.randint(0, 63)
        flipped_key = flip_bit(key, flip_index_key)
        try:
            c2_keyflip = des_encrypt(plaintext, flipped_key)
        except AssertionError as e:
            print(f"[Trial {trial}] ERROR in key flip encryption: {e}")
            continue

        # Count differences in ciphertexts
        diff_plain = count_differences(c1, c2_plainflip)
        diff_key = count_differences(c1, c2_keyflip)

        print("{:<8} {:<25} {:<25}".format(trial, diff_plain, diff_key))

    print("------------------------------------------------------------")
    print("Higher bit differences indicate strong avalanche behavior.")

if __name__ == "__main__":
    avalanche_experiment()
