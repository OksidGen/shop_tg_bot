from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.database.requests as db
from log import log_this


@log_this()
async def list_of_faqs():
    keyboard = InlineKeyboardBuilder()
    faqs = await db.get_faqs_list()
    for faq in faqs:
        keyboard.add(InlineKeyboardButton(text=faq.question, callback_data=f'faq_{faq.id}'))
    keyboard.add(InlineKeyboardButton(text='Задать свой вопрос', callback_data=f'new_question'))
    return keyboard.adjust(1).as_markup()
