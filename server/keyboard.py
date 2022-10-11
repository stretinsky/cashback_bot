
from typing import Dict
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

def get_back_keyboard():
    back = InlineKeyboardButton('Назад', callback_data='back')
    return InlineKeyboardMarkup(row_width=1).add(back)

def get_main_kb():
    one = InlineKeyboardButton('1️⃣', callback_data='one')
    two = InlineKeyboardButton('2️⃣', callback_data='two')
    three = InlineKeyboardButton('3️⃣', callback_data='three')
    return InlineKeyboardMarkup(row_width=3).add(one, two, three)

def get_apply_kb(user_id, username):
    ok = InlineKeyboardButton('✅', callback_data=f"ok_{user_id}")
    cancel = InlineKeyboardButton('❌', callback_data=f"cancel_{user_id}")
    user = InlineKeyboardButton(f"@{username}", url=f"t.me/{username}")
    return InlineKeyboardMarkup(row_width=2).add(ok, cancel, user)