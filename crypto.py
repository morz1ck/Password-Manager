from config import KEY_PATH
import os
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open(KEY_PATH, 'rb') as key_file:
        return key_file.read()

def encrypt(text: str) -> str:
    fernet = Fernet(load_key())
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    fernet = Fernet(load_key())
    return fernet.decrypt(token.encode()).decode()