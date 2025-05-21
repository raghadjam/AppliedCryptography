import requests

URL = "https://triple-des-server.onrender.com/encrypt"


def query_server(student_id, plaintext_hex):
    if len(plaintext_hex) != 16:
        raise ValueError("Plaintext must be 64 bits (16 hex characters)")

    response = requests.post(URL, json={
        "student_id": student_id,
        "plaintext": plaintext_hex
    })

    if response.status_code == 200:
        return response.json().get("ciphertext")
    else:
        raise ValueError(f"Server Error: {response.text}")


if __name__ == "__main__":
    stu_id = input("Enter your student ID: ").strip()
    pt = input("Enter 64-bit plaintext in hex (16 hex digits): ").strip().lower()

    try:
        ct = query_server(stu_id, pt)
        print(f"Ciphertext: {ct}")
    except ValueError as e:
        print(e)
