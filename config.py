import os
from dotenv import load_dotenv

load_dotenv()

# Bot
TOKEN = os.getenv('BOT_TOKEN')
PAYMENT_TOKEN = os.getenv('BOT_TG_PAYMENT_TOKEN')

# DB
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_PORT = os.getenv('DB_PORT')

# General Bot Info
ADMIN = [os.getenv('BOT_ADMIN')]
BOT_NICKNAME = os.getenv('BOT_NICKNAME')
CHANNELS = [
    [os.getenv('BOT_CHANNEL_NAME'), os.getenv('BOT_CHANNEL_ID'), os.getenv('BOT_CHANNEL_LINK')]
]
