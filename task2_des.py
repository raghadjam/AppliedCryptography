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
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]
SBOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # Copy the first S-box to the rest for consistency
    *[[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]] for _ in range(7)
]
]

def permute(bits, table):
    return [bits[i - 1] for i in table]
def xor(bits1, bits2):
    return [int(b1) ^ int(b2) for b1, b2 in zip(bits1, bits2)]
def left_shift(bits, n):
    return bits[n:] + bits[:n]
def sbox_substitute(bits):
    output = []
    for i in range(8):
        row = (bits[i*6] << 1) + bits[i*6 + 5]
        col = (bits[i*6 + 1] << 3) + (bits[i*6 + 2] << 2) + (bits[i*6 + 3] << 1) + bits[i*6 + 4]
        val = SBOX[i][row][col]
        output += [int(x) for x in f"{val:04b}"]
    return output
def bytes_to_bitlist(data):
    return [((byte >> (7 - i)) & 1) for byte in data for i in range(8)]
def bitlist_to_bytes(bits):
    return bytes([int(''.join(str(bit) for bit in bits[i:i+8]), 2) for i in range(0, len(bits), 8)])
def key_schedule(key):
    C, D = key[:28], key[28:]
    subkeys = []
    for shift in SHIFT_SCHEDULE:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        combined = C + D
        subkeys.append(permute(combined, PC2))
    return subkeys
def f_function(R, subkey):
    return permute(sbox_substitute(xor(permute(R, E), subkey)), P)
def des_encrypt(key, plaintext):
    plaintext = permute(plaintext, IP)
    subkeys = key_schedule(key)
    L, R = plaintext[:32], plaintext[32:]
    for i in range(16):
        L, R = R, xor(L, f_function(R, subkeys[i]))
    return permute(R + L, FP)
def des_decrypt(key, ciphertext):
    ciphertext = permute(ciphertext, IP)
    subkeys = key_schedule(key)
    L, R = ciphertext[:32], ciphertext[32:]
    for i in reversed(range(16)):
        L, R = R, xor(L, f_function(R, subkeys[i]))
    return permute(R + L, FP)
