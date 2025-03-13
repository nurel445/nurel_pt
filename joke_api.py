import aiohttp
from config import JOKE_API_URL

async def get_joke():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{JOKE_API_URL}/Any") as response:
            if response.status == 200:
                data = await response.json()
                if data["type"] == "single":
                    return data["joke"]
                else:
                    return f"{data['setup']}\n{data['delivery']}"
            return "Ошибка: не удалось получить шутку"
