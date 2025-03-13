from aiogram import types, Dispatcher, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from joke_api import get_joke

router = Router()


@router.message()
async def start_command(message: types.Message):
    buttons = [
        [InlineKeyboardButton(text="Картинка", callback_data="image")],
        [InlineKeyboardButton(text="Погода", callback_data="weather")],
        [InlineKeyboardButton(text="Курс валют", callback_data="currency")],
        [InlineKeyboardButton(text="Список фильмов", callback_data="movies")],
        [InlineKeyboardButton(text="Шутка", callback_data="joke")],
        [InlineKeyboardButton(text="Опрос", callback_data="survey")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(f"Привет, {message.from_user.full_name}! Выбери действие:", reply_markup=keyboard)


@router.callback_query()
async def joke_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "joke":
        joke = await get_joke()
        await callback_query.message.answer(joke)
    await callback_query.answer()


@router.callback_query()
async def image_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "image":

        await callback_query.message.answer("Выберите картинку: футбол, бокс или баскетбол?")
    await callback_query.answer()


@router.callback_query()
async def weather_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "weather":

        await callback_query.message.answer("Введите город для получения погоды.")
    await callback_query.answer()


@router.callback_query()
async def currency_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "currency":

        await callback_query.message.answer("Текущий курс валют.")
    await callback_query.answer()


@router.callback_query()
async def movies_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "movies":

        await callback_query.message.answer("Вот список фильмов.")
    await callback_query.answer()


@router.callback_query()
async def survey_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "survey":

        await callback_query.message.answer("Запускаю опрос...")
    await callback_query.answer()


def register_handlers(dp: Dispatcher):
    dp.include_router(router)


