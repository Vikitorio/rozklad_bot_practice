import os
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards import main_keyboard
from data_base import users_db
from rozklad_api import ksu_api
from rozklad_parser.rozklad_file import get_file
from data_validation import data_validation_client
keyboard = main_keyboard()

class FSMAdmin(StatesGroup):
    user_id = State()
    faculty = State()
    course = State()
    groupe = State()

async def start_key(message : types.Message):
    await message.answer("Введіть команду",reply_markup=keyboard.rozklad_panel())
    #await message.reply(message.text)
async def options(message : types.Message):
    await message.answer("Налаштування", reply_markup=keyboard.options_panel())
async def notification_options(message : types.Message):
    await message.answer("Виберіть тип чи ввімкнути нагадування", reply_markup=keyboard.notification_panel())
async def news_options(message : types.Message):
    await message.answer("Виберіть тип чи ввімкнути отримування новин інституту", reply_markup=keyboard.news_panel())
async def set_notification_button(message : types.Message):
    if users_db.check_user(message.from_user.id):
        users_db.set_notification(message.from_user.id,'8')
        await message.answer("Нагадування ввімкнено, ви будете отримувати розклад о 8:00", reply_markup=keyboard.rozklad_panel())
    else:
        await message.answer("Ви не зареєстровані")

async def remove_notification_button(message: types.Message):
    if users_db.check_user(message.from_user.id):
        users_db.remove_notification(message.from_user.id)
        await message.answer("Нагадування вимкнено", reply_markup=keyboard.rozklad_panel())
    else:
        await message.answer("Ви не зареєстровані")

async def set_news_button(message : types.Message):
    if users_db.check_user(message.from_user.id):
        users_db.set_news(message.from_user.id)
        await message.answer("Отримання новин ввімкнено", reply_markup=keyboard.rozklad_panel())
    else:
        await message.answer("Ви не зареєстровані")

async def remove_news_button(message: types.Message):
    if users_db.check_user(message.from_user.id):
        users_db.remove_news(message.from_user.id)
        await message.answer("Отримання новин вимкнено", reply_markup=keyboard.rozklad_panel())
    else:
        await message.answer("Ви не зареєстровані")
async def delete_user(message : types.Message):
    await users_db.delete_user(message.from_user.id)
    await message.answer('Ваші данні видалено, зареєструйтесь знову')
    await start_key(message)
async def rozklad_request(message : types.Message):
    print(users_db.check_user(message.from_user.id))
    if users_db.check_user(message.from_user.id) == []:
        await FSMAdmin.faculty.set()
        await message.reply("Спочатку треба зареєструватися\nВибери свій факультет",reply_markup=keyboard.faculty_panel())
    else:
        await message.answer('Розклад на сьогодні')
        arr = (ksu_api.get_rozklad_api(users_db.get_user_groupe(message.from_user.id)))
        for item in arr:
            try:
                await message.answer(item)
            except:
                continue

async def rozklad_file_request(message : types.Message):
    if users_db.check_user(message.from_user.id):
        file_path = get_file(users_db.get_faculty(message.from_user.id))
        document = types.InputFile(file_path)
        await bot.send_document(message.chat.id, document, caption='Розклад')
    else:
        await FSMAdmin.faculty.set()
        await message.reply("Спочатку треба зареєструватися\nВибери свій факультет", reply_markup=keyboard.faculty_panel())
async def get_faculty(message : types.Message, state: FSMContext):
    if message.text == '/Скасувати' or message.text == 'Скасувати':
        await state.finish()
        await message.answer("Введіть команду", reply_markup=keyboard.rozklad_panel())
    elif data_validation_client.check_faculty(message.text):
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['faculty'] = message.text
        await FSMAdmin.next()
        await message.reply("Тепер введи курс",reply_markup=keyboard.group_course())
async def get_course(message : types.Message, state: FSMContext):
    if message.text == '/Скасувати' or message.text == 'Скасувати':
        await state.finish()
        await message.answer("Введіть команду", reply_markup=keyboard.rozklad_panel())
    elif data_validation_client.check_course(message.text):
        async with state.proxy() as data:
            if message.text == '1-магістр':
                data['course'] = 5
            elif message.text == '2-магістр':
                data['course'] = 6
            else:
                data['course'] = message.text
        await FSMAdmin.next()
        await message.reply('Тепер введи групу',reply_markup=keyboard.get_groups_panel(data['faculty'],int(data['course'])))
async def get_groupe(message : types.Message, state: FSMContext):
    if message.text == '/Скасувати' or message.text == 'Скасувати':
        await state.finish()
        await message.answer("Введіть команду", reply_markup=keyboard.rozklad_panel())
    elif data_validation_client.check_groupe(message.text):
        async with state.proxy() as data:
            data['group'] = message.text
        await FSMAdmin.next()
        async with state.proxy() as data:
            await users_db.db_add_user(state)
            await message.answer('Ваші данні збережено',reply_markup=keyboard.rozklad_panel())
        await state.finish()
async def cancel_reg(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        print('відміна')
        await state.finish()
        await message.reply('Операція скасована', reply_markup=keyboard.rozklad_panel())


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_key ,commands=['start'])
    dp.register_message_handler(start_key, commands=['Головне_меню'])
    dp.register_message_handler(rozklad_file_request, commands=['Отримати_Файл_Розкладу'])
    dp.register_message_handler(options, commands=['Налаштування'])
    dp.register_message_handler(notification_options, commands=['Нагадування'])
    dp.register_message_handler(news_options, commands=['Новини'])
    dp.register_message_handler(set_notification_button, commands=['Встановити_Нагадування'])
    dp.register_message_handler(remove_notification_button, commands=['Прибрати_Нагадування'])
    dp.register_message_handler(set_news_button, commands=['Отримувати_Новини'])
    dp.register_message_handler(remove_news_button, commands=['Не_Отримувати_Новини'])
    dp.register_message_handler(delete_user, commands=['Змінити_групу'])
    dp.register_message_handler(start_key, commands=['Головне_меню'])
    dp.register_message_handler(rozklad_request, commands=['Отримати_Розклад'], state=None)
    dp.register_message_handler(get_faculty, state=FSMAdmin.faculty)
    dp.register_message_handler(get_course, state=FSMAdmin.course)
    dp.register_message_handler(get_groupe, state=FSMAdmin.groupe)
    dp.register_message_handler(cancel_reg, commands=['Скасувати'], state="*")
    dp.register_message_handler(cancel_reg,Text(equals='Скасувати', ignore_case=True), commands=['Скасувати'])
