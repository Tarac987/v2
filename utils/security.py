from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key():
    key = base64.urlsafe_b64encode(hashlib.sha256().digest())
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    return open("secret.key", "rb").read()

def encrypt_password(password: str, key: bytes) -> str:
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password: str, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
