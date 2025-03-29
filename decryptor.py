import os
from core import keygen, encryptor
from utils import file_finder


def run_decrypt(base_path, password, salt_file="salt.bin"):
    if not os.path.exists(salt_file):
        print("[ERROR] Salt file not found. Cannot decrypt.")
        return

    key = keygen.generate_key(password, salt_file)
    files = file_finder.find_files(base_path, [".enc"])

    for f in files:
        try:
            encryptor.decrypt_file(f, key)
            print(f"[DECRYPTED] {f}")
        except Exception as e:
            print(f"[FAILED] Could not decrypt {f}: {e}")


if __name__ == "__main__":
    path = input("Decrypt path: ")
    pw = input("Password: ")
    run_decrypt(path, pw)
