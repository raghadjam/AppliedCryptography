import pickle
import os
from tqdm import tqdm
from task2_des import des_encrypt, des_decrypt, bytes_to_bitlist, bitlist_to_bytes
from task3_client import query_server

def generate_keys():
    return list(range(0x1000))

def key_to_56bit(key12):
    return (key12).to_bytes(7, byteorder='big')


def add_des_parity(hex56):
    key56 = bytes.fromhex(hex56)
    out = []
    for b in key56:
        b &= 0xFE                     
        if bin(b).count("1") % 2 == 0:
            b |= 1                  
        out.append(f"{b:02x}")
    return "".join(out)



def build_inner_map(P_bits):
    filename = "inner_maptest.pkl"
    if os.path.exists(filename):
        print("Found cached inner map, loading...")
        with open(filename, 'rb') as f:
            return pickle.load(f)

    print("Building inner map")
    keys = generate_keys()
    inner_map = {}

    for K1 in tqdm(keys, desc="Inner K1"):
        K1_bits = bytes_to_bitlist(key_to_56bit(K1))
        E1 = des_encrypt(K1_bits, P_bits)
        for K2 in keys:
            K2_bits = bytes_to_bitlist(key_to_56bit(K2))
            Q = des_decrypt(K2_bits, E1)
            Q_tuple = tuple(Q)
            if Q_tuple not in inner_map:
                inner_map[Q_tuple] = []
            inner_map[Q_tuple].append((K1, K2))

    print("Saving inner map")
    with open(filename, 'wb') as f:
        pickle.dump(inner_map, f)

    return inner_map

def mitm_2key_3des(student_id, plaintext_hex):
    key1 = 0x566
    key2 = 0x656
    P_bits = bytes_to_bitlist(bytes.fromhex(plaintext_hex))

    part1 = des_encrypt(bytes_to_bitlist(key_to_56bit(key1)), P_bits)
    part2 = des_decrypt(bytes_to_bitlist(key_to_56bit(key2)), part1)
    ciphertext_binary = des_encrypt(bytes_to_bitlist(key_to_56bit(key1)), part2)
    ciphertext_hex = bitlist_to_bytes(ciphertext_binary).hex()

    #ciphertext_hex1 = query_server(student_id, plaintext_hex).lower()

    C_bits = bytes_to_bitlist(bytes.fromhex(ciphertext_hex))

    inner_map = build_inner_map(P_bits)

    print("Probing outer stage…")
    keys = generate_keys()
    for K1 in tqdm(keys, desc="Outer K1"):
        K1_bits = bytes_to_bitlist(key_to_56bit(K1))
        R = des_decrypt(K1_bits, C_bits)
        R_tuple = tuple(R)
        if R_tuple in inner_map:
            for cand_K1, cand_K2 in inner_map[R_tuple]:
                print(f"Candidate pair found! K1={cand_K1:03X}, K2={cand_K2:03X}")

                step1 = des_encrypt(bytes_to_bitlist(key_to_56bit(cand_K1)), P_bits)
                step2 = des_decrypt(bytes_to_bitlist(key_to_56bit(cand_K2)), step1)
                step3 = des_encrypt(bytes_to_bitlist(key_to_56bit(cand_K1)), step2)
                result_hex = bitlist_to_bytes(step3).hex()

                print(f"Comparing result {result_hex.lower()} with expected {ciphertext_hex.lower()}")
                if result_hex.lower() == ciphertext_hex.lower():
                    print(f"Keys verified! K1={cand_K1}, K2={cand_K2}")

                    # Final output
                    k1_56 = key_to_56bit(cand_K1).hex()
                    k2_56 = key_to_56bit(cand_K2).hex()
                    k1_64 = add_des_parity(k1_56)
                    k2_64 = add_des_parity(k2_56)

                    print("\nFinal Recovered Keys:")
                    print(f"K1 (14-digit, no parity): {k1_56}")
                    print(f"K2 (14-digit, no parity): {k2_56}")
                    print(f"K1 (16-digit with parity): {k1_64}")
                    print(f"K2 (16-digit with parity): {k2_64}")
                    return

                print("Verification failed—trying next candidate.")

    print("No matching key pair found.")

if __name__ == "__main__":
    sid = input("Enter your student ID: ").strip()
    ptxt = input("Enter 64-bit plaintext in hex (16 hex digits): ").strip().lower()
    mitm_2key_3des(sid, ptxt)
