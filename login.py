import sqlite3
import hashlib

def create_user_table():
    conn = sqlite3.connect("database.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("database.db")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        print("User already exists")
    conn.close()

def verify_login(username, password):
    conn = sqlite3.connect("database.db")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    result = cursor.fetchone()
    conn.close()
    return result is not None