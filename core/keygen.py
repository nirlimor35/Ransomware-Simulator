import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


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
