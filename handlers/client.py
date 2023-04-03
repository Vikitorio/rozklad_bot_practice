from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import main_keyboard
from data_base import users_db
keyboard = main_keyboard()

class FSMAdmin(StatesGroup):
    user_id = State()
    faculty = State()
    course = State()
    groupe = State()

async def start_key(message : types.Message):
    await message.answer("Доброго дня",reply_markup=keyboard.rozklad_panel())
    #await message.reply(message.text)

async def reg_start(message : types.Message):
    await FSMAdmin.faculty.set()
    await message.reply("Вибери свій факультет",reply_markup=keyboard.faculty_panel())

async def get_faculty(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['faculty'] = message.text
    await FSMAdmin.next()
    await message.reply("Тепер введи курс",reply_markup=keyboard.group_course())
async def get_course(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
    await FSMAdmin.next()
    await message.reply('Тепер введи групу',reply_markup=keyboard.get_groups_panel(data['faculty'],int(data['course'])))
async def get_groupe(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FSMAdmin.next()
    async with state.proxy() as data:
        await users_db.db_add_user(state)
        await message.answer('Ваші данні збережено',reply_markup=keyboard.rozklad_panel())
        await message.answer(f'Ваша група {data["group"]}')
    await state.finish()


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_key ,commands=['start'])
    dp.register_message_handler(reg_start, commands=['Отримати_Розклад'], state=None)
    dp.register_message_handler(get_faculty, state=FSMAdmin.faculty)
    dp.register_message_handler(get_course, state=FSMAdmin.course)
    dp.register_message_handler(get_groupe, state=FSMAdmin.groupe)