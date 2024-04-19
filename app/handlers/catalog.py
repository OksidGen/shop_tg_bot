import base64

from aiogram import F, Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.database.requests as db
from app.states import CreateOrderState

catalog_router = Router()


@catalog_router.message(F.text == "Каталог")
@catalog_router.callback_query(F.data.startswith('catalog_'))
async def catalog(update: Message | CallbackQuery, bot: Bot):
    if type(update) is Message:
        await update.answer('Выберите категорию', reply_markup=await kb.list_of_categories(0))
    else:
        await update.answer(show_alert=False)
        offset = int(update.data.split('_')[-1])
        await update.message.edit_text('Выберите категорию', reply_markup=await kb.list_of_categories(int(offset)))


@catalog_router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer(show_alert=False)
    page = int(callback.data.split('_')[-1].split(':')[-1])
    category_id = callback.data.split('_')[-1].split(':')[0]
    await callback.message.edit_text('Выберите подкатегорию',
                                     reply_markup=await kb.list_of_subcategories(category_id, page))


@catalog_router.callback_query(F.data.startswith('subcategory_'))
async def subcategory(callback: CallbackQuery):
    await callback.answer(show_alert=False)
    sub_id = callback.data.split('/')[0].split('_')[-1].split(':')[0]
    page = int(callback.data.split('/')[0].split('_')[-1].split(':')[1])
    category_id = callback.data.split('/')[1].split('_')[-1]
    await callback.message.answer('Выберите товар',
                                  reply_markup=await kb.list_of_items(category_id, sub_id, page,))
    await callback.message.delete()


@catalog_router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer(show_alert=False)
    item_id = callback.data.split('/')[0].split('_')[-1]
    category_id = callback.data.split('/')[1].split('_')[-1]
    _item = await db.get_item(item_id)
    caption = (f'Название: {_item.name}\n\n'
               f'Описание: {_item.description}\n\n'
               f'Цена: {_item.price / 100} ₽')
    if _item.photo is None:
        await callback.message.edit_text(text=caption,
                                         reply_markup=await kb.manage_item(category_id, _item.subcategory,
                                                                           _item.id, _item.name, _item.price))
        return
    _photo_db = await db.get_photo(_item.photo)
    _photo = types.BufferedInputFile(base64.b64decode(_photo_db.photo), f'{item_id}.jpg')
    await callback.message.answer_photo(photo=_photo,
                                        caption=caption,
                                        reply_markup=await kb.manage_item(category_id, _item.subcategory,
                                                                          _item.id, _item.name, _item.price))
    await callback.message.delete()


@catalog_router.callback_query(F.data.startswith('create_order_item_'))
async def create_order_item_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer(show_alert=False)
    item_id = callback.data.split('/')[0].split('_')[-1].split(':')[0]
    item_name = callback.data.split('/')[0].split('_')[-1].split(':')[1]
    item_price = callback.data.split('/')[0].split('_')[-1].split(':')[2]
    subcategory_id = callback.data.split('/')[1].split('_')[-1]
    category_id = callback.data.split('/')[2].split('_')[-1]
    await state.update_data(subcategory_id=subcategory_id,
                            category_id=category_id,
                            item_id=item_id,
                            item_name=item_name,
                            item_price=int(item_price))
    await state.set_state(CreateOrderState.count)
    await callback.message.answer(
        'Введите необходимое количество',
        reply_markup=await kb.simple_keyboard('Назад', f'item_{item_id}/category_{category_id}'))
    await callback.message.delete()


@catalog_router.message(CreateOrderState.count)
async def create_order_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Нужно ввести целое число')
        return
    await state.update_data(count=int(message.text))
    await state.set_state(CreateOrderState.confirm)
    data = await state.get_data()
    await message.answer(f'Товар: {data["item_name"]}\n'
                         f'Цена: {data["item_price"] / 100} ₽\n'
                         f'Количество: {data["count"]}\n'
                         f'Итого: {data["item_price"] * data["count"] / 100} ₽\n\n'
                         f'Вы уверены?',
                         reply_markup=await kb.confirm_create_order(data['category_id'], data['item_id']))


@catalog_router.callback_query(F.data == 'confirm', CreateOrderState.confirm)
async def create_order_success(callback: CallbackQuery, state: FSMContext):
    await callback.answer(show_alert=False)
    data = await state.get_data()
    await db.create_order(callback.from_user.id, data['item_id'], data['count'])
    await callback.message.edit_text(
        f'Товар:{data["item_name"]}\n'
        f'Цена:{data["item_price"] / 100} ₽\n'
        f'Количество:{data["count"]}\n'
        f'Итого:{data["item_price"] * data["count"] / 100} ₽\n\n'
        f'Успешно добавлено',
        reply_markup=await kb.create_order_success(data['category_id'], data['subcategory_id'], ))
    await state.clear()
