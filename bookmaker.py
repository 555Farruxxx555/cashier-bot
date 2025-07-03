from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def bookmaker_keyboard(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Melbet")],
            [KeyboardButton(text="1xBet")],
            [KeyboardButton(text="❌ Bekor qilish" if lang == "uz" else "❌ Отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

