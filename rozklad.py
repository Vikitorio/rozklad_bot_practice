
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
admin.register_handlers_admin(dp)
async def on_start(_):
    print("Бот Онлайн")
    #await notification_sender()


async def notification_sender():
    while True:
        now = datetime.datetime.now()
        if now.hour == 10:
            await other.send_schedule()
        await asyncio.sleep(3600)

executor.start_polling(dp, skip_updates=True, on_startup=on_start)