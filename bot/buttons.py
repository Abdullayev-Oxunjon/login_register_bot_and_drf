from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def register_button():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text="👤  Ro'yxatdan o'tish")
    rkm.add(btn)
    return rkm


def login_button():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text="👤  Tizimga kirish")
    rkm.add(btn)
    return rkm


