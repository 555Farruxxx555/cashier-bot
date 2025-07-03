from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def confirm_keyboard(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Tasdiqladim ✅")],
            [KeyboardButton(text="🔙 Orqaga" if lang == "uz" else "🔙 Назад")],
            [KeyboardButton(text="❌ Bekor qilish" if lang == "uz" else "❌ Отмена")]
        ],
        resize_keyboard=True
    )

