from aiogram import types, Dispatcher
from create_bot import dp, bot

async def echo_send(message : types.Message):
    await message.answer(message.text)
    #await meassage.reply(message.text)

def register_handlers_client(dp : Dispatcher):
    dp.register_massage_handler(echo_send)