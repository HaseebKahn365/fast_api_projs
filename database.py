import sqlite3
from datetime import datetime

DATABASE = 'chat_app.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, hashed_password):
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def add_message(username, message):
    conn = get_db()
    conn.execute('INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)',
                 (username, message, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_last_messages(limit=20):
    conn = get_db()
    messages = conn.execute('SELECT username, message, timestamp FROM messages ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [dict(msg) for msg in messages][::-1]  # Reverse to get oldest first

def get_messages_with_offset(offset=0, limit=20):
    conn = get_db()
    messages = conn.execute('SELECT username, message, timestamp FROM messages ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset)).fetchall()
    conn.close()
    return [dict(msg) for msg in messages][::-1]