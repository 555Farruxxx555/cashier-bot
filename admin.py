from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_lang
from locales import get_text

router = Router()

# Команда /approve <user_id>
@router.message(F.text.startswith("/approve "))
async def manual_approve(message: Message):
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        lang = get_lang(user_id)
        texts = get_text(lang)

        await message.bot.send_message(chat_id=user_id, text=texts["approved"])
        await message.answer("✅ Ulgurildi — foydalanuvchi xabardor qilindi." if lang == "uz" else "✅ Готово — пользователь уведомлён.")
    except Exception as e:
        await message.answer(f"❗️ Xatolik: {e}")

# Пример кнопки для заявки (можно встроить в population.py при отправке админу)
def approval_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_{user_id}")
            ]
        ]
    )

@router.callback_query(F.data.startswith("approve_"))
async def callback_approve(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    lang = get_lang(user_id)
    texts = get_text(lang)

    await call.bot.send_message(chat_id=user_id, text=texts["approved"])
    await call.answer("✅ Foydalanuvchi xabardor qilindi." if lang == "uz" else "✅ Пользователь уведомлён.")
