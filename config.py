import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
JOKE_API_URL = os.getenv("JOKE_API_URL")
