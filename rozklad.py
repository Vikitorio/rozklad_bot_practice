
from aiogram.utils import executor
from create_bot import dp
from handlers import client,admin, other
from data_base import users_db
import datetime
import time
import asyncio
from datetime import date, timedelta

users_db.db_init()
client.register_handlers_client(dp)
admin.register_handlers_client(dp)
async def on_start(_):
    print("Бот Онлайн")
    """await asyncio.gather(
        check_time_and_send()
    )"""

"""async def check_time_and_send():
    while True:
        now = datetime.datetime.now()
        if now.hour == 10:  # Change this to the desired hour
            await other.send_schedule()
        await asyncio.sleep(3600)"""

executor.start_polling(dp, skip_updates=True, on_startup=on_start)