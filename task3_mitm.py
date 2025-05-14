import pickle
import os
from tqdm import tqdm
from task2_des import des_encrypt, des_decrypt, bytes_to_bitlist, bitlist_to_bytes
from task3_client import query_server

STUDENT_ID = "1220848"


def generate_keys():
    return [i for i in range(0x1000)]


def key_to_56bit(key12):
    return (key12 << 44).to_bytes(7, byteorder='big')


def mitm_attack():
    # Step 1: Get plaintext and ciphertext from the server
    plaintext_hex = "0123456789ABCDEF"
    ciphertext_hex = query_server(STUDENT_ID, plaintext_hex)

    plaintext_bytes = bytes.fromhex(plaintext_hex)
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)

    plaintext_bits = bytes_to_bitlist(plaintext_bytes)
    ciphertext_bits = bytes_to_bitlist(ciphertext_bytes)

    k1_candidates = generate_keys()
    k2_candidates = generate_keys()

    # Step 2: Encrypt plaintext with all possible K1 -> store intermediate results
    print("Generating intermediate E_K1(plaintext) values...")
    intermediate_dict = {}
    for k1 in tqdm(k1_candidates):
        k1_bytes = key_to_56bit(k1)
        k1_bits = bytes_to_bitlist(k1_bytes)
        intermediate = des_encrypt(k1_bits, plaintext_bits)
        intermediate_dict[tuple(intermediate)] = k1

    # Step 3: Decrypt ciphertext with all possible K2 -> look for matches
    print("Searching for matching keys...")
    for k2 in tqdm(k2_candidates):
        k2_bytes = key_to_56bit(k2)
        k2_bits = bytes_to_bitlist(k2_bytes)
        intermediate = des_decrypt(k2_bits, ciphertext_bits)
        if tuple(intermediate) in intermediate_dict:
            k1 = intermediate_dict[tuple(intermediate)]
            print(f"Potential match found! K1={k1:03X}, K2={k2:03X}")

            # Verify full triple DES: ciphertext = E_K1(D_K2(E_K1(plaintext)))
            k1_bits = bytes_to_bitlist(key_to_56bit(k1))
            k2_bits = bytes_to_bitlist(key_to_56bit(k2))

            step1 = des_encrypt(k1_bits, plaintext_bits)
            step2 = des_decrypt(k2_bits, step1)
            step3 = des_encrypt(k1_bits, step2)

            if step3 == ciphertext_bits:
                print(f"✅ Keys verified! K1 = {k1:03X}, K2 = {k2:03X}")
                return
            else:
                print("❌ Match failed on verification.")

    print("❌ No matching keys found.")


if __name__ == "__main__":
    mitm_attack()
