import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "passwords.db")
KEY_PATH = os.path.join(BASE_DIR, "data", "secret.key")
