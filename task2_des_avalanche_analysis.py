import random
from task2_des import des_encrypt

def flip_bit(bin_str, index):
    # Flip the bit at the specified index (0-based)
    flipped = list(bin_str)
    flipped[index] = '0' if bin_str[index] == '1' else '1'
    return ''.join(flipped)

def count_differences(bin1, bin2):
    return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))

def random_bin_string(length):
    bin_str = ''.join(random.choice('01') for _ in range(length))
    assert len(bin_str) == length, f"Generated binary string is {len(bin_str)} bits instead of {length}"
    return bin_str

def avalanche_experiment(trials=10):
    print("DES Avalanche Effect Analysis ({} Trials)".format(trials))
    print("------------------------------------------------------------")
    print("{:<6} {:<25} {:<25}".format("Trial", "# Diff Bits (Plain Flip)", "# Diff Bits (Key Flip)"))

    for trial in range(1, trials + 1):
        # Generate 64-bit plaintext and 56-bit key
        plaintext = random_bin_string(64)
        print(plaintext)
        key = random_bin_string(56)
        print(key)
        # Encrypt original
        c1 = des_encrypt(plaintext, key)

        # Flip one random bit in plaintext
        bit_to_flip = random.randint(0, 63)
        flipped_plaintext = flip_bit(plaintext, bit_to_flip)
        c2_plainflip = des_encrypt(flipped_plaintext, key)

        # Flip one random bit in key
        bit_to_flip_k = random.randint(0, 55)
        flipped_key = flip_bit(key, bit_to_flip_k)
        c2_keyflip = des_encrypt(plaintext, flipped_key)

        # Count bit differences
        diff_plain = count_differences(c1, c2_plainflip)
        diff_key = count_differences(c1, c2_keyflip)

        print("{:<6} {:<25} {:<25}".format(trial, diff_plain, diff_key))

    print("------------------------------------------------------------")
    print("Higher bit differences indicate strong avalanche behavior.")

if __name__ == "__main__":
    avalanche_experiment()
