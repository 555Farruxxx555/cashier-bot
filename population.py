
import random
import json
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, any_state

from keyboards.common import back_cancel_keyboard, amount_keyboard
from keyboards.menu import main_menu
from locales import get_text
from database.users import get_lang, save_id
from data.cards import get_random_card

router = Router()

class PopolnenieStates(StatesGroup):
    waiting_for_bookmaker = State()
    waiting_for_id = State()
    waiting_for_card = State()
    waiting_for_amount = State()
    waiting_for_confirm = State()

@router.message(F.text.in_(["Hisob to‘ldirish", "Пополнить счёт"]))
async def start_payment(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)

    bookmaker_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Melbet"), KeyboardButton(text="1xBet")],
            [KeyboardButton(text="❌ Bekor qilish ❌")]
        ],
        resize_keyboard=True
    )

    await state.set_state(PopolnenieStates.waiting_for_bookmaker)
    await message.answer(texts["choose_bookmaker"], reply_markup=bookmaker_keyboard)

@router.message(PopolnenieStates.waiting_for_bookmaker, F.text.in_(["❌ Bekor qilish ❌", "❌ Отменено"]))
async def cancel_or_back_bookmaker(message: Message, state: FSMContext):
    await state.clear()
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await message.answer(texts["cancel"], reply_markup=main_menu(lang))

@router.message(PopolnenieStates.waiting_for_bookmaker)
async def choose_bookmaker(message: Message, state: FSMContext):
    bookmaker = message.text.lower()
    if bookmaker not in ["melbet", "1xbet"]:
        lang = get_lang(message.from_user.id)
        texts = get_text(lang)
        await message.answer(texts["invalid_bookmaker"])
        return

    await state.update_data(bookmaker=bookmaker)

    user_id = str(message.from_user.id)
    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        prev_id = users.get(user_id, {}).get("bookmakers", {}).get(bookmaker)
    except:
        prev_id = None

    lang = get_lang(message.from_user.id)
    texts = get_text(lang)

    if prev_id:
        await state.update_data(bookmaker_id=prev_id)
        await message.answer(texts["enter_card"], reply_markup=back_cancel_keyboard(lang))
        await state.set_state(PopolnenieStates.waiting_for_card)
    else:
        await message.answer(texts["enter_id"], reply_markup=back_cancel_keyboard(lang))
        await state.set_state(PopolnenieStates.waiting_for_id)

@router.message(PopolnenieStates.waiting_for_id)
async def enter_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        lang = get_lang(message.from_user.id)
        texts = get_text(lang)
        await message.answer(texts["amount_number"])
        return

    data = await state.get_data()
    bookmaker = data.get("bookmaker")
    save_id(message.from_user.id, bookmaker, message.text)

    await state.update_data(bookmaker_id=message.text)

    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await message.answer(texts["enter_card"], reply_markup=back_cancel_keyboard(lang))
    await state.set_state(PopolnenieStates.waiting_for_card)

@router.message(PopolnenieStates.waiting_for_card, F.text.in_(["❌ Bekor qilish ❌", "❌ Отменено"]))
async def cancel_during_card_input(message: Message, state: FSMContext):
    await state.clear()
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await message.answer(texts["cancel"], reply_markup=main_menu(lang))

@router.message(PopolnenieStates.waiting_for_card)
async def enter_card(message: Message, state: FSMContext):
    card = message.text.replace(" ", "")
    if not card.isdigit() or len(card) < 12:
        lang = get_lang(message.from_user.id)
        texts = get_text(lang)
        await message.answer(texts["amount_number"])
        return

    await state.update_data(client_card=card)

    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await message.answer(texts["enter_amount"], reply_markup=amount_keyboard(lang))
    await state.set_state(PopolnenieStates.waiting_for_amount)

@router.message(PopolnenieStates.waiting_for_amount)
async def enter_amount(message: Message, state: FSMContext):
    if not message.text.replace(" ", "").isdigit():
        lang = get_lang(message.from_user.id)
        texts = get_text(lang)
        await message.answer(texts["amount_number"])
        return

    amount = int(message.text.replace(" ", ""))
    if amount < 25000 or amount > 5000000:
        lang = get_lang(message.from_user.id)
        texts = get_text(lang)
        await message.answer(texts["amount_limit"])
        return

    exact_amount = round(amount + random.uniform(0.01, 0.99), 2)
    receiver_card = get_random_card()

    await state.update_data(amount=amount, exact_amount=exact_amount, receiver_card=receiver_card)

    data = await state.get_data()
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)

    await message.answer(
        texts["confirm_required"] +
        f"\n\n💳 Sizning kartangiz: <b>{data['client_card']}</b>" +
        f"\n💰 To‘lov summasi: <b>{exact_amount} so‘m</b>" +
        f"\n📥 Qabul qiluvchi karta: <b>{receiver_card}</b>",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Tasdiqladim ✅")], [KeyboardButton(text="❌ Bekor qilish ❌")]],
            resize_keyboard=True
        )
    )

    await state.set_state(PopolnenieStates.waiting_for_confirm)

@router.message(PopolnenieStates.waiting_for_confirm, F.text == "Tasdiqladim ✅")
async def confirm_payment(message: Message, state: FSMContext):
    data = await state.get_data()

    admin_id = 2033317678
    text = (
        "📥 <b>Yangi to‘lov!</b>\n\n"
        f"👤 Telegram ID: <code>{message.from_user.id}</code>\n"
        f"📲 Bukmeker: <b>{data['bookmaker'].capitalize()}</b>\n"
        f"🆔 ID: <b>{data['bookmaker_id']}</b>\n"
        f"💳 Mijoz karta: <code>{data['client_card']}</code>\n"
        f"💰 Summa: <b>{data['exact_amount']} so‘m</b>\n"
        f"📥 Qabul qiluvchi karta: <code>{data['receiver_card']}</code>"
    )
    await message.bot.send_message(admin_id, text)

    try:
        with open("data/transactions.json", "r", encoding="utf-8") as f:
            transactions = json.load(f)
    except:
        transactions = {"transactions": []}

    transactions["transactions"].append({
        "type": "popolnenie",
        "amount": data["amount"],
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    with open("data/transactions.json", "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)

    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await message.answer(texts["payment_received"], reply_markup=main_menu(lang))
    await state.clear()

@router.message(any_state, F.text.in_(["❌ Bekor qilish ❌", "❌ Отменено"]))
async def cancel_process(message: Message, state: FSMContext):
    await state.clear()
    lang = get_lang(message.from_user.id)
    texts = get_text(lang)
    await message.answer(texts["cancel"], reply_markup=main_menu(lang))














