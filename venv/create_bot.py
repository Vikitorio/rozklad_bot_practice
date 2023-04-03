from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
#bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token='6225855539:AAEFQYAgU7TEQEdu3_AS2u0mOK2dnovDsBk')
dp = Dispatcher(bot, storage=storage)
