from cryptography.fernet import Fernet
from config import load_key

key = load_key()

def encrypt_password(password: str, key: bytes) -> str:
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password: str, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

def check_password(password: str, encrypted_password: str) -> bool:
    try:
        decrypted_password = decrypt_password(encrypted_password, key)
        return password == decrypted_password
    except Exception:
        return False
