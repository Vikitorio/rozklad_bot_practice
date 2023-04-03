
from aiogram.utils import executor
from create_bot import dp
from handlers import client, other
from data_base import users_db

users_db.db_init()
client.register_handlers_client(dp)
async def on_start(_):
    print("Бот Онлайн")






executor.start_polling(dp, skip_updates=True, on_startup=on_start)