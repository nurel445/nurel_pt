import asyncio
import logging
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()
TOKEN = os.getenv("TOKEN")
WEATHER_API = os.getenv("WEATHER_API")


logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher()



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
    await message.answer(f"Привет, {user_name}! Выбери действие:", reply_markup=get_main_keyboard())



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



@dp.callback_query(lambda c: c.data == "weather")
async def ask_city(callback: types.CallbackQuery):
    await callback.message.answer("Введите название города:")


@dp.message()
async def send_weather(message: types.Message):
    city = message.text
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={city}&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if "error" in data:
        await message.answer("Ошибка: Город не найден!")
        return

    weather = f"🌡 Температура: {data['current']['temp_c']}°C\n🌤 {data['current']['condition']['text']}"
    await message.answer(weather)



@dp.callback_query(lambda c: c.data == "currency")
async def send_currency(callback: types.CallbackQuery):
    url = "https://valuta.kg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()


    soup = BeautifulSoup(html, "html.parser")

    usd_rate_div = soup.find("div", class_="usd-rate")
    if usd_rate_div:
        usd_rate = usd_rate_div.text.strip()
    else:
        usd_rate = "Курс не найден"

    await callback.message.answer(f"💰 Курс USD: {usd_rate} KGS")




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
        "football": "https://example.com/football.jpg",
        "boxing": "https://example.com/boxing.jpg",
        "basketball": "https://example.com/basketball.jpg"
    }
    await callback.message.answer_photo(images[category])



@dp.callback_query(lambda c: c.data == "movies")
async def send_movies(callback: types.CallbackQuery):
    movies_list = "🎬 Фильмы:\n1️⃣ Начало\n2️⃣ Матрица\n3️⃣ Интерстеллар"
    await callback.message.answer(movies_list)



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



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())









