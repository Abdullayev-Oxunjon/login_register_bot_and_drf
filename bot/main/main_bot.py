import logging
import os
import re

import django
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove

from bot.main.api import login_user_to_api, get_student_by_id, add_grade_student, update_grade_in_server
from bot.main.buttons import login_button, main_menu_cancel, inline_student_button, inner_back_button, \
    get_student, my_account
from bot.main.states import LoginState, ShowUserState, AddUserState, UpdateGradeState

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE",
                      value="root.settings")  # Django loyihangiz sozlamalari moduli bilan almashtiring
django.setup()

from root.settings import API_TOKEN

BOT_TOKEN = API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(text=f"Assalomu alaykum {message.from_user.full_name}")

    await message.answer_photo(
        photo="https://images.pexels.com/photos/1558690/pexels-photo-1558690.jpeg?auto=compress&cs=tinysrgb&w=1600",
        reply_markup=login_button())


@dp.callback_query_handler()
async def check_buttons(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "about_bot":
        await callback.message.answer_photo(
            photo="https://images.pexels.com/photos/8566470/pexels-photo-8566470.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            caption="Bizning bot orqali siz o'zingizning baholaringizni va bundan tashqari"
                    "guruhingizdagi o'quvchilar baholarini ko'rib borishingiz mumkin !",
            reply_markup=main_menu_cancel())

    elif callback.data == "login":
        await callback.message.answer(text="<b>Tizimga kirish uchun telefon raqamingizni kiriting ! \n"
                                           "</b>")
        await LoginState.phone_number.set()

    elif callback.data == "cancel":
        # mana shu jarayonda yana start commandi qayta ishga tushiriladi !
        await bot_start(message=callback.message, state=state)
        await state.finish()
    elif callback.data == "back_button":
        await callback.message.answer_photo(
            photo="https://img.freepik.com/free-vector/college-or-university-students-group-young-happy-people"
                  "-standing-isolated-on-white-background_575670-66.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696896000&semt=ais",
            reply_markup=inline_student_button())
        await state.finish()

    elif callback.data == "back_inner":
        await callback.message.answer_photo(
            photo="https://img.freepik.com/free-vector/college-or-university-students-group-young-happy-people"
                  "-standing-isolated-on-white-background_575670-66.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696896000&semt=ais",
            reply_markup=inline_student_button())
        await state.finish()

    elif callback.data == "all_students":
        await callback.message.answer_photo(
            photo="https://img.freepik.com/free-vector/college-or-university-students-group-young-happy-people"
                  "-standing-isolated-on-white-background_575670-66.jpg?size=626&ext=jpg&ga=GA1.1.1413502914.1696896000&semt=ais",
            reply_markup=get_student(1)
        )
        await ShowUserState.id.set()
    elif callback.data == "add_student":
        await callback.message.answer(text="Qaysi id ga tegishli studentlar baho kiritmoqchisiz ?\n"
                                           "<b><em> ID raqamni kiriting </em></b>")
        await AddUserState.id.set()

    elif callback.data == "update_student":
        await callback.message.answer(text="Qaysi studentni tahrirlamaoqchisiz\n"
                                           "<b>ID raqamni kiriting  : </b>")
        await UpdateGradeState.next()


@dp.message_handler(lambda message: message.text.isdigit(), state=UpdateGradeState.id)
async def process_student_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['person_id'] = int(message.text)
        student_id = int(message.text)
        student = get_student_by_id(person_id=student_id)
        if student:
            data['student_id'] = student_id
            await message.answer("Iltimos, talaba uchun bahoni yangilang:")
            await UpdateGradeState.score.set()
        else:
            await message.answer(text="Bu id tegishli student yo'q\n"
                                      "<b>Iltimos qayta kiriting </b>")


@dp.message_handler(state=UpdateGradeState.score)
async def process_score(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score'] = float(message.text)

    # Yangi baho qiymatini serverga yuborish
    success = update_grade_in_server(data['person_id'], data['score'])

    if success:
        await message.answer(
            f"<b>{data['person_id']}- id ga tegishli studentning bahosi {data['score']} bahoga yangilandi </b>")
    else:
        await message.answer(f"Bahoni yangilashda xatolik yuz berdi. Iltimos  qayta urinib ko'ring.")


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

        response = login_user_to_api(data['phone_number'], data['password'])
        if response.status_code == 200:
            user_info = response.json()  # JSON javobni o'qish
            is_teacher = user_info.get('is_teacher', False)  # Agar "is_teacher" mavjud bo'lsa olish, aks holda False
            if is_teacher:
                await message.reply("<b>Siz teacher ekansiz !\n\nMuvaffaqiyatli login</b>",
                                    reply_markup=my_account())

            else:
                await message.reply("<b>Siz student ekansiz!</b>",
                                    reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.reply(
                "Noto'g'ri telefon raqam yoki parol.\n<b><em>Iltimos telefon raqam va passwordingizni qayta kiriting!</em></b>")
            await LoginState.phone_number.set()


@dp.message_handler(Text(equals="👤 My account"))
async def check_user(message: types.Message):
    await message.answer(text="Mavjud studentlar",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(
        photo="https://images.pexels.com/photos/1558690/pexels-photo-1558690.jpeg?auto=compress&cs=tinysrgb&w=1600",
        reply_markup=inline_student_button())


@dp.callback_query_handler(lambda callback: callback.data.isdigit() or callback.data == "back_button",
                           state=ShowUserState.id)
async def get_item(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "back_button":
        await callback.message.answer("Back button clicked.")
        await bot_start(message=callback.message, state=state)
        await state.finish()

    else:
        student_id = int(callback.data)
        student = get_student_by_id(person_id=student_id)
        if "score" in student and student['score']:
            await callback.message.answer_photo(
                photo="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg",
                caption=
                f"\n\n\n\n\n\n<b><em>Student Name: {student['fullname']}\n"
                f"Student Phone Number: {student['phone_number']}\n"
                f"Student Group : {student['group']} group\n"
                f"Student grade : {student['score']}</em></b>",
                reply_markup=inner_back_button()
            )
            await state.finish()
        else:
            await callback.message.answer_photo(
                photo="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg",
                caption=
                f"\n\n\n\n\n\n<b><em>Student Name: {student['fullname']}\n"
                f"Student Phone Number: {student['phone_number']}\n"
                f"Student Group : {student['group']} group</em></b>",
                reply_markup=inner_back_button()
            )
            await state.finish()


@dp.message_handler(lambda message: message.text.isdigit(), state=AddUserState.id)
async def process_student_grade(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        student_id = int(message.text)
        student = get_student_by_id(person_id=student_id)
        if student:
            data['student_id'] = student_id
            await message.answer("Iltimos, talaba uchun bahoni kiriting:")
            await AddUserState.score.set()
        else:
            await message.answer(text="Bu id tegishli student yo'q\n"
                                      "<b>Iltimos qayta kiriting </b>")


@dp.message_handler(lambda message: message.text.replace(".", "").isdigit(), state=AddUserState.score)
async def process_student_score(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score'] = float(message.text)

    if 'student_id' in data:
        response = add_grade_student(data['student_id'], data['score'])

        if response.status_code == 201:
            await message.answer(f"Baho {data['score']} student uchun saqlandi.")
            await message.answer_photo(
                photo="https://images.pexels.com/photos/1558690/pexels-photo-1558690.jpeg?auto=compress&cs=tinysrgb&w=1600",
                reply_markup=inline_student_button())

        else:
            await message.answer("Bahoni saqlashda xatolik yuz berdi. Iltimos keyinroq qayta urinib ko'ring.")
    else:
        await message.answer("Iltimos, talaba ID ni kiritib chiqing.")

    await state.finish()


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
