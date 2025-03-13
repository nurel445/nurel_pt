import aiosqlite

DB_NAME = "bot_database.db"

# Создание таблицы, если её нет
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS survey (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                name TEXT,
                age INTEGER,
                favorite_subject TEXT,
                favorite_color TEXT,
                favorite_movie TEXT,
                custom1 TEXT,
                custom2 TEXT,
                custom3 TEXT
            )
        """)
        await db.commit()

# Функция сохранения ответов пользователя в БД
async def save_survey(user_id, username, answers):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO survey (user_id, username, name, age, favorite_subject, favorite_color, favorite_movie, custom1, custom2, custom3)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, *answers))
        await db.commit()

# Функция получения результатов опроса
async def get_survey_results():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM survey") as cursor:
            return await cursor.fetchall()
