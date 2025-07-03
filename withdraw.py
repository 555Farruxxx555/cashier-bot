
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import ADMIN_IDS
from keyboards.common import back_cancel_keyboard, bookmaker_keyboard, main_menu
from locales import get_text
from database.users import get_lang

router = Router()

class WithdrawStates(StatesGroup):
    choosing_bookmaker = State()
    entering_card = State()
    entering_id = State()
    entering_code = State()

@router.message(F.text.in_(["Pul chiqarish", "Вывести деньги"]))
async def start_withdraw(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await state.clear()
    await state.set_state(WithdrawStates.choosing_bookmaker)
    await message.answer(texts["choose_bookmaker"], reply_markup=bookmaker_keyboard(lang))

@router.message(WithdrawStates.choosing_bookmaker)
async def choose_bookmaker(message: Message, state: FSMContext):
    bookmaker = message.text.lower()
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)

    if bookmaker in ["melbet", "1xbet"]:
        await state.update_data(bookmaker=bookmaker)

        # 🔹 Красивый адрес кассы
        address_text = (
            "🏦 Kassamiz manzili:\n📍 Andijon — Mashrab 25 (24/7)\n\n"
            "Saytda ushbu manzilni tanlab, 4 xonali kod oling."
            if lang == "uz"
            else
            "🏦 Адрес нашей кассы:\n📍 Андижан — Машраб 25 (24/7)\n\n"
            "На сайте выберите этот адрес и получите 4-значный код."
        )
        await message.answer(address_text)

        await state.set_state(WithdrawStates.entering_card)
        msg = "💳 Kartangiz raqamini kiriting:" if lang == "uz" else "💳 Введите номер вашей карты:"
        await message.answer(msg, reply_markup=back_cancel_keyboard(lang))

    elif bookmaker in ["❌ bekor qilish", "❌ отмена"]:
        await state.clear()
        await message.answer(texts["cancel"], reply_markup=main_menu(lang))
    else:
        await message.answer(texts["invalid_bookmaker"], reply_markup=bookmaker_keyboard(lang))

@router.message(WithdrawStates.entering_card)
async def enter_card(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    if message.text.startswith("❌"):
        await state.clear()
        await message.answer(texts["cancel"], reply_markup=main_menu(lang))
        return

    card_number = message.text.strip()
    if not card_number.isdigit() or len(card_number) < 12:
        await message.answer("❗️ Noto‘g‘ri karta raqami. Qaytadan kiriting.")
        return

    await state.update_data(card=card_number)
    await state.set_state(WithdrawStates.entering_id)
    msg = "🆔 Bukmeker ID raqamingizni kiriting:" if lang == "uz" else "🆔 Введите ID от букмекера:"
    await message.answer(msg, reply_markup=back_cancel_keyboard(lang))

@router.message(WithdrawStates.entering_id)
async def enter_id(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    if message.text.startswith("❌"):
        await state.clear()
        await message.answer(texts["cancel"], reply_markup=main_menu(lang))
        return

    user_id = message.text.strip()
    if not user_id.isdigit():
        await message.answer(texts["amount_number"])
        return

    await state.update_data(bookmaker_id=user_id)
    await state.set_state(WithdrawStates.entering_code)
    msg = "🔢 4 xonali kodni kiriting:" if lang == "uz" else "🔢 Введите 4-значный код:"
    await message.answer(msg, reply_markup=back_cancel_keyboard(lang))

@router.message(WithdrawStates.entering_code)
async def enter_code(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    if message.text.startswith("❌"):
        await state.clear()
        await message.answer(texts["cancel"], reply_markup=main_menu(lang))
        return

    code = message.text.strip()
    if not code.isdigit() or len(code) != 4:
        await message.answer("❗️ Kod 4 xonali raqam bo‘lishi kerak.")
        return

    data = await state.get_data()
    bookmaker = data["bookmaker"]
    card = data["card"]
    bookmaker_id = data["bookmaker_id"]

    msg_admin = f"""📥 <b>Yangi yechish so‘rovi:</b>
<b>🧾 Bukmeker:</b> {bookmaker}
<b>🆔 ID:</b> {bookmaker_id}
<b>💳 Karta:</b> {card}
<b>🔢 Kod:</b> {code}
<b>👤 Telegram ID:</b> <code>{message.from_user.id}</code>"""

    await state.clear()
    await message.answer("✅ So‘rovingiz qabul qilindi. Tez orada ko‘rib chiqiladi.", reply_markup=main_menu(lang))
    await message.bot.send_message(ADMIN_IDS[0], msg_admin)











