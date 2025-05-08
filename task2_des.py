# task2_des.py

# Initial Permutation Table
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation Table
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion Table (E-box)
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation function P
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# PC-1 for Key Compression (64 -> 56 bits)
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# PC-2 for Subkey compression (56 -> 48 bits)
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of bit shifts per round
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

# S-Boxes (8 boxes, each 4x16)
SBOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    # S2 (Rest of S-Boxes not included for brevity)
]


# Helper: Bit permutation using a table
def permute(bits, table):
    return [bits[i - 1] for i in table]


# Helper: XOR two bit lists
def xor(bits1, bits2):
    return [bit1 ^ bit2 for bit1, bit2 in zip(bits1, bits2)]


# Helper: Left shift a bit list by n positions
def left_shift(bits, n):
    return bits[n:] + bits[:n]


# Helper: S-Box substitution
def sbox_substitute(bits):
    output = []
    for i in range(8):  # 8 S-boxes
        row = (bits[i * 6] << 1) + bits[i * 6 + 5]  # first and last bit
        col = bits[i * 6 + 1] * 8 + bits[i * 6 + 2] * 4 + bits[i * 6 + 3] * 2 + bits[i * 6 + 4]
        output += [int(x) for x in format(SBOX[i][row][col], '04b')]  # convert to 4-bit binary
    return output


# Key schedule (generate 16 subkeys)
def key_schedule(key):
    key = permute(key, PC1)
    C, D = key[:28], key[28:]
    subkeys = []
    for i in range(16):
        C = left_shift(C, SHIFT_SCHEDULE[i])
        D = left_shift(D, SHIFT_SCHEDULE[i])
        combined = C + D
        subkey = permute(combined, PC2)
        subkeys.append(subkey)
    return subkeys


# f-function: Expansion, XOR with subkey, S-box, and P-box
def f_function(right_half, subkey):
    expanded = permute(right_half, E)  # Expand to 48 bits
    xor_result = xor(expanded, subkey)  # XOR with subkey
    substituted = sbox_substitute(xor_result)  # Apply S-box
    return permute(substituted, P)  # Apply P-box


# DES encryption
def des_encrypt(key, plaintext):
    # Initial Permutation
    plaintext = permute(plaintext, IP)

    # Generate subkeys
    subkeys = key_schedule(key)

    # Split into left and right halves
    left, right = plaintext[:32], plaintext[32:]

    for i in range(16):
        new_left = right
        right = xor(left, f_function(right, subkeys[i]))
        left = new_left

    # Combine halves and apply final permutation
    combined = left + right
    return permute(combined, FP)


# DES decryption
def des_decrypt(key, ciphertext):
    # Initial Permutation
    ciphertext = permute(ciphertext, IP)

    # Generate subkeys
    subkeys = key_schedule(key)

    # Split into left and right halves
    left, right = ciphertext[:32], ciphertext[32:]

    for i in range(15, -1, -1):  # Reverse order of subkeys for decryption
        new_left = right
        right = xor(left, f_function(right, subkeys[i]))
        left = new_left

# Combine halves and apply final permutation
    combined = left + right
    return permute(combined, FP)
