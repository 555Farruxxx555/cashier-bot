# database.py

# Простая временная "база" — сохраняется в оперативной памяти (слетает при перезапуске)
user_data = {}

def save_user_id(user_id: int, lang: str):
    """Сохраняет язык пользователя по его Telegram ID"""
    user_data[user_id] = {"lang": lang}

def get_user_id(user_id: int) -> str:
    """Возвращает язык пользователя по его Telegram ID, если нет — по умолчанию 'uz'"""
    return user_data.get(user_id, {}).get("lang", "uz")
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()
