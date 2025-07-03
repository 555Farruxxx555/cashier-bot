import json
import os
from datetime import datetime

USERS_FILE = "data/users.json"

def is_registered(user_id):
    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return False

    return user_id in data

def register_user(user_id, phone_number, lang):
    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        data = {}
    else:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    if user_id not in data:
        data[user_id] = {
            "phone": phone_number,
            "lang": lang,
            "registered": datetime.now().strftime("%Y-%m-%d"),
            "bookmakers": {}
        }

        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def get_lang(user_id):
    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        return "uz"

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return "uz"

    return data.get(user_id, {}).get("lang", "uz")

def set_lang(user_id, lang):
    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        return

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    if user_id in data:
        data[user_id]["lang"] = lang

        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def save_id(user_id, bookmaker, bookmaker_id):
    # Не сохраняем недопустимые значения
    forbidden = ["orqaga", "bekor", "назад", "отмена", "🔙", "❌"]
    if any(x in bookmaker_id.lower() for x in forbidden):
        return

    user_id = str(user_id)
    if not os.path.exists(USERS_FILE):
        data = {}
    else:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    if user_id not in data:
        data[user_id] = {
            "registered": datetime.now().strftime("%Y-%m-%d"),
            "bookmakers": {}
        }

    if "bookmakers" not in data[user_id]:
        data[user_id]["bookmakers"] = {}

    data[user_id]["bookmakers"][bookmaker.lower()] = bookmaker_id

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)





