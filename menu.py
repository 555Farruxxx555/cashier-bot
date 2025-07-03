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




