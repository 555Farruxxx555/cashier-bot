from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu(lang: str):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Hisob to‘ldirish")],
                [KeyboardButton(text="Pul chiqarish")],
                [KeyboardButton(text="Texnik yordam")]
            ],
            resize_keyboard=True
        )
    else:  # lang == "ru"
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Пополнить счёт")],
                [KeyboardButton(text="Вывести деньги")],
                [KeyboardButton(text="Техническая поддержка")]
            ],
            resize_keyboard=True
        )

def back_cancel_keyboard(lang: str):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="❌ Bekor qilish")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="❌ Отмена")]
            ],
            resize_keyboard=True
        )

def bookmaker_keyboard(lang: str):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Melbet"), KeyboardButton(text="1xBet")],
                [KeyboardButton(text="❌ Bekor qilish")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Melbet"), KeyboardButton(text="1xBet")],
                [KeyboardButton(text="❌ Отмена")]
            ],
            resize_keyboard=True
        )

def amount_keyboard(lang: str):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="50000"), KeyboardButton(text="100000")],
                [KeyboardButton(text="250000"), KeyboardButton(text="500000")],
                [KeyboardButton(text="❌ Bekor qilish")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="50000"), KeyboardButton(text="100000")],
                [KeyboardButton(text="250000"), KeyboardButton(text="500000")],
                [KeyboardButton(text="❌ Отмена")]
            ],
            resize_keyboard=True
        )



