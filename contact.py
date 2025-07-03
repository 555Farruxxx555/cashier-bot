from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def request_contact_keyboard(lang="uz"):
    text = "📱 Raqamni yuborish" if lang == "uz" else "📱 Отправить номер"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text, request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


