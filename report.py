import json
from aiogram import Router
from aiogram.types import Message
from datetime import datetime

router = Router()

ADMIN_ID = 2033317678
TRANSACTIONS_FILE = "data/transactions.json"

@router.message(lambda msg: msg.text == "/admin report" and msg.from_user.id == ADMIN_ID)
async def report_today(message: Message):
    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await message.answer("❌ Ma'lumotlar topilmadi.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    top_up_count = top_up_sum = 0
    withdraw_count = withdraw_sum = 0

    for tx in data.get("transactions", []):
        if tx.get("date") == today:
            if tx["type"] == "popolnenie":
                top_up_count += 1
                top_up_sum += int(tx["amount"])
            elif tx["type"] == "withdraw":
                withdraw_count += 1
                withdraw_sum += int(tx["amount"])

    report_text = (
        f"📊 Bugungi hisobot:\n\n"
        f"📥 Popolneniya: {top_up_count} ta — {top_up_sum:,} so‘m\n"
        f"📤 Pul chiqarish: {withdraw_count} ta — {withdraw_sum:,} so‘m"
    )

    await message.answer(report_text)