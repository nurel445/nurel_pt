import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

WEATHER_API = os.getenv("WEATHER_API")

DB_PATH = "database.sqlite"


DEFAULT_JOKE_CATEGORIES = ["Programming", "Misc", "Pun", "Spooky"]

CURRENCY_API_URL = "https://valuta.kg/api/rates"


DEBUG = True


if not TOKEN:
    raise ValueError("❌ Ошибка: Токен не найден! Проверь .env файл.")




