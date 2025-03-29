from cryptography.fernet import Fernet
import os


def encrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(filepath + '.enc', 'wb') as file:
        file.write(encrypted)
    os.remove(filepath)


def decrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, 'rb') as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    orig_path = filepath.replace('.enc', '')
    with open(orig_path, 'wb') as file:
        file.write(decrypted)
    os.remove(filepath)
