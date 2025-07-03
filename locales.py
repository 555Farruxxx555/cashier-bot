def get_text(lang: str) -> dict:
    texts = {
        "welcome": {
            "uz": "👋 Assalomu alaykum! Xush kelibsiz!",
            "ru": "👋 Здравствуйте! Добро пожаловать!"
        },
        "choose_lang": {
            "uz": "🌍 Tilni tanlang:",
            "ru": "🌍 Выберите язык:"
        },
        "choose_bookmaker": {
            "uz": "📱 Bukmeker tanlang:",
            "ru": "📱 Выберите букмекера:"
        },
        "invalid_bookmaker": {
            "uz": "❗️Noto‘g‘ri bukmeker. Iltimos, Melbet yoki 1xBet ni tanlang.",
            "ru": "❗️Неверный букмекер. Пожалуйста, выберите Melbet или 1xBet."
        },
        "enter_id": {
            "uz": "🆔 Bukmeker ID raqamingizni kiriting:",
            "ru": "🆔 Введите свой ID от букмекера:"
        },
        "enter_card": {
            "uz": "💳 Karta raqamingizni kiriting:",
            "ru": "💳 Введите номер вашей карты:"
        },
        "enter_amount": {
            "uz": "💰 Summani tanlang yoki kiriting (so‘m):",
            "ru": "💰 Выберите или введите сумму (сум):"
        },
        "amount_number": {
            "uz": "❗️ Iltimos, faqat raqam kiriting.",
            "ru": "❗️ Пожалуйста, введите только число."
        },
        "amount_limit": {
            "uz": "❗️ Minimal 25 000 so‘m, maksimal 5 000 000 so‘m.",
            "ru": "❗️ Минимум 25 000 сум, максимум 5 000 000 сум."
        },
        "confirm_required": {
            "uz": "✅ Pul o‘tkazgan bo‘lsangiz, 'Tasdiqladim ✅' tugmasini bosing.",
            "ru": "✅ Если вы оплатили, нажмите 'Tasdiqladim ✅'."
        },
        "payment_received": {
            "uz": "✅ So‘rovingiz qabul qilindi. Tez orada ko‘rib chiqiladi.",
            "ru": "✅ Ваша заявка принята. Скоро она будет обработана."
        },
        "cancel": {
            "uz": "❌ So‘rov bekor qilindi.",
            "ru": "❌ Запрос отменён."
        },
        "support": {
            "uz": "🛠 Texnik yordam uchun: @YourSupportUsername",
            "ru": "🛠 Техническая поддержка: @YourSupportUsername"
        },
        "approved": {
            "uz": "✅ To‘lov tasdiqlandi!",
            "ru": "✅ Платёж подтверждён!"
        }
    }
    return {key: val.get(lang, "") for key, val in texts.items()}
















