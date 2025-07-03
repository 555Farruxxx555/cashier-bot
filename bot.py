import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from config import BOT_TOKEN
from handlers import start_handlers, population, withdraw, report

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(start_handlers.router)
dp.include_router(population.router)
dp.include_router(withdraw.router)
dp.include_router(report.router)

# ID администратора
ADMIN_ID = 2033317678

# Функция отправки автоотчёта
async def send_daily_report():
    now = datetime.now().strftime("%Y-%m-%d")
    report_text = (
        f"📊 Kunlik hisobot ({now}):\n\n"
        "🔸 To‘lovlar: 6 ta\n"
        "🔸 Yechimlar: 2 ta\n"
        "🔸 Umumiy: 2,300,000 so‘m"
    )
    await bot.send_message(ADMIN_ID, report_text)

async def main():
    # Настраиваем планировщик
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(send_daily_report, trigger="cron", hour=21, minute=0)
    scheduler.start()

    print("🤖 Бот запущен. Ishga tayyor!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








