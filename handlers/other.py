from aiogram import types
from create_bot import dp, bot
import multiprocessing
import datetime
from data_base import users_db
from rozklad_api import ksu_api
import time

async def send_schedule():
    print('rrrrrr')
    id_arr = users_db.get_notification_list()
    print(id_arr)
    if id_arr:
        for item in id_arr:
            print(item)
            await bot.send_message(item, ksu_api.get_rozklad_api(item))
            users_db.update_notification_day(item)



