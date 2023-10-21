from aiogram.dispatcher.filters.state import StatesGroup, State


class LoginState(StatesGroup):
    phone_number = State()
    password = State()


class ShowUserState(StatesGroup):
    id = State()


class AddUserState(StatesGroup):
    id = State()
    score = State()


class UpdateGradeState(StatesGroup):
    id = State()
    score = State()
