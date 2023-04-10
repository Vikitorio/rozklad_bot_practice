from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards.admin_keyboard import main_admin_keyboard
from data_base import users_db
from rozklad_api import ksu_api
from rozklad_parser import rozklad_file
from data_validation import data_validation_admin
import os

admin_keyboard = main_admin_keyboard()
async def news_spam(news_title,news_body,faculty = False,course=False,groupe=False):
    arr =users_db.get_users_id_list(faculty,course,groupe)
    letter = news_title + '\n' + news_body
    for item in arr:
        print(item[0])
        await bot.send_message(item[0], letter)
class FSMAdmin_schedule(StatesGroup):
    user_id_schedule  = State()
    faculty_schedule = State()
    file_schedule = State()
async def start_panel(message : types.Message):
    if users_db.check_admin(message.from_user.id):
        await message.answer("Введіть команду",reply_markup=admin_keyboard.main_panel())
        #await message.reply(message.text)


async def new_schedule(message : types.Message):
        await FSMAdmin_schedule.faculty_schedule.set()
        await message.reply("Вибери факультет",reply_markup=admin_keyboard.faculty_panel())

async def get_faculty(message : types.Message,state: FSMContext):
    if message.text == '/Скасувати' or message.text == 'Скасувати':
        await state.finish()
    else:
        async with state.proxy() as data:
            data['user_id_schedule'] = message.from_user.id
            data['faculty_schedule'] = message.text
            print(data['faculty_schedule'])
            await FSMAdmin_schedule.next()
            await message.reply("Завантажте файл",reply_markup=admin_keyboard.cancel_panel())
async def get_schedue_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['file_schedule'] = message.document.file_id
        data['file_schedule_title'] = message.document.file_name
        file_id = message.document.file_id
        file_name = message.document.file_name
        file_size = message.document.file_size

        # Download the document file from Telegram's servers
        rozklad_file.cleane_the_dir(data["faculty_schedule"])
        directory_path = f'D:/rozklad_bot/Розклади_ексель/{data["faculty_schedule"]}/'
        await message.document.download(directory_path)

        # Create the directory if it doesn't exist

    await state.finish()
    await message.answer('Розклад Завантажено', reply_markup=admin_keyboard.main_panel())



class FSMAdmin_news(StatesGroup):
    user_id_schedule  = State()
    faculty_news = State()
    course_news = State()
    groupe_news = State()
    news_title = State()
    news_body = State()

async def send_news(message: types.Message):
    await FSMAdmin_news.faculty_news.set()
    await message.reply("Вибери факультет", reply_markup=admin_keyboard.faculty_panel(1))
async def get_faculty_news(message : types.Message,state: FSMContext):
    if message.text == '/Скасувати' or message.text == 'Скасувати':
        await state.finish()
    elif data_validation_admin.check_faculty(message.text):
        async with state.proxy() as data:
            if message.text == "Всім":
                data['user_id_news'] = message.from_user.id
                data['faculty_news'] = False
                data['course_news'] = False
                data['groupe_news'] = False
                await FSMAdmin_news.news_title.set()
                await message.reply("Введіть заголовок", reply_markup=ReplyKeyboardRemove())
            else:
                data['user_id_news'] = message.from_user.id
                data['faculty_news'] = message.text
                print(data['faculty_news'])
                await FSMAdmin_news.next()
                await message.reply("Виберіть курс",reply_markup=admin_keyboard.group_course(1))
async def get_course_news(message : types.Message,state: FSMContext):
    if message.text == '/Скасувати' or message.text == 'Скасувати':
        await state.finish()
    elif data_validation_admin.check_course(message.text):
        async with state.proxy() as data:
            if message.text == "Всім":
                data['course_news'] = False
                data['groupe_news'] = False
                await FSMAdmin_news.news_title.set()
                await message.reply("Введіть заголовок", reply_markup=ReplyKeyboardRemove())
            else:
                data['course_news'] = message.text
                await FSMAdmin_news.next()
                await message.reply("Виберіть групу",reply_markup=admin_keyboard.get_groups_panel(data['faculty_news'],1))
async def get_groupe_news(message : types.Message,state: FSMContext):
    if data_validation_admin.check_groupe(message.text):
        if message.text == '/Скасувати' or message.text == 'Скасувати':
            await state.finish()
        else:
            async with state.proxy() as data:
                if message.text == "Всім":
                    data['groupe_news'] = False
                    await FSMAdmin_news.news_title.set()

                else:
                    data['groupe_news'] = message.text
                    await FSMAdmin_news.next()
                    await message.reply("Введіть заголовок",reply_markup=admin_keyboard.cancel_panel())
async def get_news_title(message : types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['news_title'] = message.text
        await FSMAdmin_news.next()
        await message.reply("Введіть основний текст новини", reply_markup=admin_keyboard.cancel_panel())
async def get_news_body(message : types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['news_body'] = message.text
        await news_spam( data['news_title'], data['news_body'], data['faculty_news'],data['course_news'],data['groupe_news'])
        await state.finish()
        await message.reply("Новина відправлена",reply_markup=admin_keyboard.main_panel())

async def cansel_admin(message : types.Message,state: FSMContext):
    await state.finish()
    await message.reply('Операція скасована', reply_markup=admin_keyboard.main_panel())


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cansel_admin, commands=['Скасувати_Операцію'],state="*")
    dp.register_message_handler(start_panel ,commands=['dev'])
    dp.register_message_handler(new_schedule, commands=['Додати_Розклад'])
    dp.register_message_handler(get_faculty, state=FSMAdmin_schedule.faculty_schedule)
    dp.register_message_handler(get_schedue_file,content_types=['document'], state=FSMAdmin_schedule.file_schedule)

    dp.register_message_handler(send_news, commands=['Відправити_Новину'])
    dp.register_message_handler(get_faculty_news,  state=FSMAdmin_news.faculty_news)
    dp.register_message_handler(get_course_news, state=FSMAdmin_news.course_news)
    dp.register_message_handler(get_groupe_news, state=FSMAdmin_news.groupe_news)
    dp.register_message_handler(get_news_title, state=FSMAdmin_news.news_title)
    dp.register_message_handler(get_news_body, state=FSMAdmin_news.news_body)