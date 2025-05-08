import sqlite3
from config import DB_PATH

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            login TEXT NOT NULL,
            password_encrypted TEXT NOT NULL,
            comment TEXT
        )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f'Ошибка: {e}')

def insert_entry(service, login, password_encrypted, comment):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (service, login, password_encrypted, comment) VALUES (?, ?, ?, ?)',
                   (service, login, password_encrypted, comment))
    conn.commit()
    conn.close()

def get_entry():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, service, login, password_encrypted, comment FROM passwords')
    rows = cursor.fetchall()
    conn.close()
    return rows
