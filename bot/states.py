from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    username = State()
    phone_number = State()
    password = State()


class LoginState(StatesGroup):
    phone_number = State()
    password = State()
