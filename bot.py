import asyncio
import logging
import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from aiogram.fsm.storage.memory import MemoryStorage

from config import WEATHER_API

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())



WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")








survey_questions = [
    "Как вас зовут?",
    "Сколько вам лет?",
    "Какой ваш любимый школьный предмет?",
    "Какой ваш любимый цвет?",
    "Какой ваш любимый фильм?",
    "Какой ваш любимый музыкальный жанр?",
    "Какое ваше любимое блюдо?",
    "Какой ваш любимый город?"
]

user_answers = {}



def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Картинка", callback_data="image")],
        [InlineKeyboardButton(text="🌤 Погода", callback_data="weather")],
        [InlineKeyboardButton(text="💱 Курс валют", callback_data="currency")],
        [InlineKeyboardButton(text="🎬 Список фильмов", callback_data="movies")],
        [InlineKeyboardButton(text="😂 Шутка", callback_data="joke")],
        [InlineKeyboardButton(text="📋 Опрос", callback_data="survey")]
    ])

    return keyboard



@dp.message(Command("start"))
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}! Выберите действие:", reply_markup=get_main_keyboard())



@dp.callback_query(lambda c: c.data == "survey")
async def start_survey(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_answers[user_id] = []
    await callback.message.answer(survey_questions[0])



@dp.message()
async def handle_survey(message: types.Message):
    user_id = message.from_user.id


    if user_id in user_answers and len(user_answers[user_id]) < len(survey_questions):
        user_answers[user_id].append(message.text)

        if len(user_answers[user_id]) < len(survey_questions):
            await message.answer(survey_questions[len(user_answers[user_id])])
        else:

            answers_text = "\n".join(
                [f"{i + 1}. {q}: {a}" for i, (q, a) in enumerate(zip(survey_questions, user_answers[user_id]))])
            await message.answer(f"📝 Ваши ответы:\n{answers_text}")
            del user_answers[user_id]






@dp.callback_query(lambda c: c.data == "joke")
async def send_joke(callback: types.CallbackQuery):
    url = "https://v2.jokeapi.dev/joke/Any"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if data["type"] == "twopart":
        joke = f"{data['setup']}\n\n{data['delivery']}"
    else:
        joke = data["joke"]

    await callback.message.answer(joke)







from aiogram import types

@dp.callback_query(lambda c: c.data == "weather")
async def send_weather(callback: types.CallbackQuery):
    if not WEATHER_API_KEY:
        await callback.message.answer("Ошибка: API ключ не предоставлен!")
        return

    city = "Москва"
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await callback.message.answer(f"Ошибка: Не удалось получить данные о погоде. Статус: {resp.status}")
                    return

                data = await resp.json()

                if "error" in data:
                    await callback.message.answer("Ошибка: Город не найден!")
                    return

                weather = (
                    f"🌡 Температура в {city}: {data['current']['temp_c']}°C\n"
                    f"🌤 {data['current']['condition']['text']}\n"
                    f"💨 Ветер: {data['current']['wind_kph']} км/ч\n"
                    f"💧 Влажность: {data['current']['humidity']}%"
                )
                await callback.message.answer(weather)

    except aiohttp.ClientError as e:
        await callback.message.answer(f"Ошибка сети: {e}")
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {e}")







import aiohttp
from bs4 import BeautifulSoup
from aiogram import types


@dp.callback_query(lambda c: c.data == "currency")
async def fetch_currency(callback: types.CallbackQuery):
    url = "https://valuta.kg/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status != 200:
                await callback.message.answer("Ошибка при запросе курса валют.")
                return

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            tables = soup.find_all("table", class_="kurs-table")
            if len(tables) < 2:
                await callback.message.answer("Не найдена нужная таблица с курсами валют.")
                return

            currency_table = tables[1]
            rows = currency_table.find_all("tr")

            currency_names = ["USD", "EUR", "RUB", "KZT", "CNY", "GBP"]

            currency_info = []
            for i, row in enumerate(rows):
                cols = row.find_all("td")
                if len(cols) == 2 and i < len(currency_names):
                    buy_rate = cols[0].text.strip()
                    sell_rate = cols[1].text.strip()
                    currency_info.append(f"{currency_names[i]}: Покупка {buy_rate} / Продажа {sell_rate}")

            if currency_info:
                await callback.message.answer("\n".join(currency_info))
            else:
                await callback.message.answer("Не удалось извлечь данные о курсах валют.")


@dp.callback_query(lambda c: c.data == "image")
async def send_image_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚽ Футбол", callback_data="image_football")],
        [InlineKeyboardButton(text="🥊 Бокс", callback_data="image_boxing")],
        [InlineKeyboardButton(text="🏀 Баскетбол", callback_data="image_basketball")]
    ])
    await callback.message.answer("Выберите категорию:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith("image_"))
async def send_image(callback: types.CallbackQuery):
    category = callback.data.split("_")[1]

    images = {
        "football": "https://www.iphones.ru/wp-content/uploads/2024/07/vikram-tkv-JO19K0HDDXI-unsplash.jpg",
        "boxing": "https://th.bing.com/th/id/R.99ceabd123a680f9e04f74bdd5b0306b?rik=N2TjUy9GYS65nA&pid=ImgRaw&r=0",
        "basketball": "https://nauchitsya.ru/app/uploads/2021/08/rasstanovka-1-1-768x475.png"
    }

    if category in images:
        await bot.send_photo(callback.message.chat.id, images[category], caption=f"Вот изображение {category.capitalize()}!")
    else:
        await callback.message.answer("Ошибка! Картинка не найдена.")

    await callback.answer()






@dp.callback_query(lambda c: c.data == "movies")
async def send_movies(callback: types.CallbackQuery):
    movies_list = "🎬 Фильмы:\n1️⃣ Начало\n2️⃣ Матрица\n3️⃣ Интерстеллар\n 4 kreed3\n apps"
    await callback.message.answer(movies_list)






async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())









