import os

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.database.requests as db
from app.states import NewQuestionState

faqs_router = Router()
admin_id = os.getenv('TELEGRAM_ADMIN_ID')


@faqs_router.message(F.text == 'FAQ')
@faqs_router.callback_query(F.data == 'faq')
async def faq(update: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if type(update) is Message:
        await update.answer('FAQ', reply_markup=await kb.list_of_faqs())
    else:
        await update.answer(show_alert=False)
        await update.message.edit_text('FAQ', reply_markup=await kb.list_of_faqs())


@faqs_router.callback_query(F.data.startswith('faq_'))
async def faq(callback: CallbackQuery):
    await callback.answer(show_alert=False)
    faq_id = callback.data.split('_')[-1]
    faq = await db.get_faq(faq_id)
    await callback.message.edit_text(f'{faq.question}\n'
                                     f'{faq.answer}',
                                     reply_markup=await kb.simple_keyboard('Назад', 'faq'))


@faqs_router.callback_query(F.data == 'new_question')
async def create_new_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer(show_alert=False)
    await state.set_state(NewQuestionState.question)
    await callback.message.edit_text('Задайте свой вопрос',
                                     reply_markup=await kb.simple_keyboard('Назад', 'faq'))


@faqs_router.message(NewQuestionState.question)
async def get_new_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(question=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=admin_id,
                           text=f'User: @{message.from_user.username}\n'
                                f'Question: {data["question"]}')
    await message.answer('Ваш вопрос принят, с вами свяжется менеджер в личных сообщениях')
    await state.clear()
