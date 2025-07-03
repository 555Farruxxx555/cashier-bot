from aiogram import Router, types
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(lambda message: message.text.lower() in ["🇺🇿 uzbek", "🇷🇺 русский"])
async def set_language(message: types.Message, state: FSMContext):
    lang = "uz" if "uz" in message.text.lower() else "ru"
    await state.update_data(lang=lang)
    await message.answer(f"Til tanlandi: {lang.upper()}" if lang == "uz" else f"Язык выбран: {lang.upper()}")
