import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from log import log_this

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Корзина')],
        [KeyboardButton(text='FAQ')]],
    resize_keyboard=True,
    input_field_placeholder='Главное меню')


@log_this()
async def simple_keyboard(text, callback_data):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    return keyboard.adjust(1).as_markup()

telegram_channel_link = os.getenv('TELEGRAM_CHANNEL_LINK')
telegram_group_link = os.getenv('TELEGRAM_GROUP_LINK')


subscribe = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Канал', url=telegram_channel_link)],
        [InlineKeyboardButton(text='Группа', url=telegram_group_link)],
        [InlineKeyboardButton(text='Я подписался', callback_data='main')]
    ]
)
