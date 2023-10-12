import logging
import os
import re

import django
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, CommandStart
from aiogram.types import ReplyKeyboardRemove

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "root.settings")  # Replace with your Django project's settings module
django.setup()

from bot.api import register_user_to_api, login_user_to_api
from bot.buttons import login_button, register_button
from bot.states import RegisterState, LoginState
from root.settings import API_TOKEN

BOT_TOKEN = API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(CommandStart())
async def echo(message: types.Message):
    await message.answer(text=f"Assalomu alaykum {message.from_user.full_name}",
                         reply_markup=register_button())


# -----------------------------------------------------------------------------------------------------
# ----------------------------------------------   REGISTER DEPARTMENT   -------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

@dp.message_handler(Text(equals="👤  Ro'yxatdan o'tish"))
async def register_func(message: types.Message, state: FSMContext):
    await message.answer("Xush kelibsiz! Iltimos, quyidagi ma'lumotlarni kiriting.")
    await message.answer(text="<b>Ism-familyangizni kiriting  </b>")
    await RegisterState.username.set()


@dp.message_handler(state=RegisterState.username)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_text = message.text
        USERNAME = re.match('^[a-zA-Z\s.,?!\'"]*$', user_text)
        if USERNAME:
            data['username'] = user_text
            await message.answer(text="<b>Telefon raqamingizni kiriting  </b>")
            await RegisterState.next()
        else:
            await message.answer(text="<b>Ism-familyani kiritishda xatolik bor</b>")


@dp.message_handler(state=RegisterState.phone_number)
async def add_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        phone_number = message.text.strip()  # Remove leading/trailing spaces
        if re.match(r'^\+998\d{9}$', phone_number):
            data['phone_number'] = phone_number
            await message.answer(text="<b>Password kiriting\n"
                                      "Passwordingiz 8 ta belgidan iborat bo'lsin !</b>",
                                 reply_markup=ReplyKeyboardRemove())
            await RegisterState.next()
        else:
            await message.reply(
                "<b>Noto'g'ri telefon raqam formati. Iltimos, to'g'ri formatda kiriting, masalan: +998913333321</b>")


@dp.message_handler(state=RegisterState.password)
async def add_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        password = message.text
        if len(password) != 8:
            await message.answer(text="<b>Passwordni kiritishda xatolik bor ! \n"
                                      "Iltimos qayta kiriting !</b>")
        else:
            data['password'] = password
            username = data['username']
            phone_number = data['phone_number']

            response = register_user_to_api(username, phone_number, data['password'])

            if response.status_code == 201:
                await message.answer(text="<b>Ma'lumotlar muvaffaqiyatli saqlandi !</b>",
                                     reply_markup=login_button())
                await state.finish()
                # await state.finish()

            else:
                print(response.status_code)
                await message.answer(text="<b>Ma'lumotlarni saqlashda xatolik yuz berdi !</b>")


# -----------------------------------------------------------------------------------------------------
# ----------------------------------------------   REGISTER DEPARTMENT   -------------------------------------------------------
# -----------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------
# ----------------------------------------------   LOGIN DEPARTMENT   -------------------------------------------------------
# -----------------------------------------------------------------------------------------------------


@dp.message_handler(Text(equals="👤  Tizimga kirish"))
async def request_phone_number(message: types.Message):
    await message.answer("Tizimga kirish uchun telefon raqamingizni kiriting:")
    await LoginState.phone_number.set()


@dp.message_handler(state=LoginState.phone_number)
async def request_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        phone_number = message.text.strip()
        if not re.match(r'^\+998\d{9}$', phone_number):
            await message.answer(
                "Noto'g'ri telefon raqam formati. Iltimos, to'g'ri formatda kiriting, masalan: +998913333321")
            return

        data['phone_number'] = phone_number
        await message.answer("Passwordni kiriting:")
        await LoginState.password.set()


@dp.message_handler(state=LoginState.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        password = message.text.strip()
        if len(password) != 8:
            await message.answer("Passwordni kiritishda xatolik bor! Passwordingiz 8 ta belgidan iborat bo'lsin.")
            return

        data['password'] = password
        # Send the phone number and password to your API for authentication
        response = login_user_to_api(data['phone_number'], data['password'])

        if response.status_code == 200:
            # Successful login, you can implement your logic here
            await message.answer("Muvaffaqiyatli login")

        else:
            # Authentication failed
            await message.answer("Noto'g'ri telefon raqam yoki parol.")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
