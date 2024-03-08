import logging
from aiogram import executor
from create_bot import dp, scheduler, bot

# from datetime import datetime, timedelta

logging.basicConfig(filename='bot_logs.log', encoding='utf-8', level=logging.DEBUG)


async def on_startup(_):
    print("BOT Online!")


from handlers import user, admin, guide

# other.register_handlers_other(dp)
guide.register_handlers_guide(dp)
user.register_handlers_user(dp)
admin.register_handlers_admin(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
