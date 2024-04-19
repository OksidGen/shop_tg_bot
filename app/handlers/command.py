from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.database.requests as db

command_router = Router()


@command_router.message(CommandStart())
@command_router.callback_query(F.data == 'main')
async def cmd_start(update: Message | CallbackQuery, bot: Bot):
    chat_id_list = [-1002003944582, -4161920027]
    for chat_id in chat_id_list:
        status = await bot.get_chat_member(chat_id=chat_id, user_id=update.from_user.id)
        if status.status == 'left':
            await update.answer("Подпишись на наши канал и группу для доступа к боту", reply_markup=kb.subscribe)
            return
    await db.create_user(update.from_user.id)
    if type(update) is Message:
        await update.answer("Добро пожаловать в наш интернет магазин WD", reply_markup=kb.main)
        return
    await update.answer(show_alert=False)
    await update.message.answer("Добро пожаловать в наш интернет магазин WD", reply_markup=kb.main, )
