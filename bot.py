import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import register_handlers
from database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция запуска бота
async def main():
    await init_db()  # Инициализация базы данных
    register_handlers(dp)  # Регистрация обработчиков
    await bot.delete_webhook(drop_pending_updates=True)  # Удаление старых обновлений
    await dp.start_polling(bot)  # Запуск бота

if __name__ == "__main__":
    asyncio.run(main())







