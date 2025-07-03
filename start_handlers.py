from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from database.users import is_registered, register_user, set_lang, get_lang
from keyboards.menu import main_menu
from locales import get_text

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await message.answer(
            "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="🇺🇿 O‘zbekcha"), KeyboardButton(text="🇷🇺 Русский")]
                ],
                resize_keyboard=True
            )
        )
    else:
        lang = get_lang(user_id)
        texts = get_text(lang)
        await message.answer(texts["welcome"], reply_markup=main_menu(lang))

@router.message(F.text == "🇺🇿 O‘zbekcha")
async def set_lang_uz(message: Message):
    register_user(message.from_user.id, message.contact.phone_number if message.contact else "unknown", "uz")
    texts = get_text("uz")
    await message.answer(texts["welcome"], reply_markup=main_menu("uz"))

@router.message(F.text == "🇷🇺 Русский")
async def set_lang_ru(message: Message):
    register_user(message.from_user.id, message.contact.phone_number if message.contact else "unknown", "ru")
    texts = get_text("ru")
    await message.answer(texts["welcome"], reply_markup=main_menu("ru"))

@router.message(F.text.in_(["Texnik yordam", "Техническая поддержка"]))
async def help_handler(message: Message):
    admin_id = 2033317678
    user_id = message.from_user.id
    lang = get_lang(user_id)

    # Отправляем админу карточку клиента
    lang_text = "O‘zbekcha" if lang == "uz" else "Русский"
    admin_text = (
        "📩 <b>Yangi texnik yordam so‘rovi</b>\n\n"
        f"🆔 Telegram ID: <code>{user_id}</code>\n"
        f"🌐 Til: {lang_text}\n"
        f"👤 Mijoz: <a href='tg://user?id={user_id}'>Bog‘lanish</a>"
    )
    await message.bot.send_message(admin_id, admin_text, parse_mode="HTML")

    # Ответ клиенту
    if lang == "uz":
        reply = "✉️ Xabaringiz operatorimizga yuborildi. Tez orada siz bilan bog'lanamiz."
    else:
        reply = "✉️ Ваше сообщение отправлено оператору. Мы свяжемся с вами в ближайшее время."

    texts = get_text(lang)
    await message.answer(reply)
    await message.answer(texts["welcome"], reply_markup=main_menu(lang))











