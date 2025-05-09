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

def entry_exists(service, login):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM passwords WHERE service=? AND login=? LIMIT 1',
                  (service, login))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def insert_entry(service, login, password_encrypted, comment):
    if entry_exists(service, login):
        raise ValueError("Запись с таким сервисом и логином уже существует")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (service, login, password_encrypted, comment) 
        VALUES (?, ?, ?, ?)
    ''', (service, login, password_encrypted, comment))
    conn.commit()
    conn.close()


def delete_entry(entry_id):
    """Удаление записи с обработкой ошибок"""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('SELECT 1 FROM passwords WHERE id = ?', (entry_id,))
        if not cursor.fetchone():
            return False

        cursor.execute('DELETE FROM passwords WHERE id = ?', (entry_id,))
        conn.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise Exception(f"Ошибка SQLite: {str(e)}")
    finally:
        if conn:
            conn.close()

def get_entry():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, service, login, password_encrypted, comment FROM passwords')
    rows = cursor.fetchall()
    conn.close()
    return rows

