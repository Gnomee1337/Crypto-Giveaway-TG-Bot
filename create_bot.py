from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.db import Database
from config import TOKEN, ADMIN
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

# DB
db = Database()