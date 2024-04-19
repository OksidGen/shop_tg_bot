import os

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.requests as db
from log import log_this

limit = int(os.getenv('LIMIT'))


def pagination(count: int, page: int, need_back: bool, back_data: str | None, callback_data: str):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text='<', callback_data=callback_data.format(page=page - 1)))
    if need_back:
        buttons.append(InlineKeyboardButton(text='Назад', callback_data=back_data))
    if page < count // limit:
        buttons.append(InlineKeyboardButton(text='>', callback_data=callback_data.format(page=page + 1)))
    return buttons


@log_this()
async def list_of_categories(page=0):
    keyboard = InlineKeyboardBuilder()
    all_categories, count = await db.get_categories_list(offset=page * limit, limit=limit)
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}:0'))
    keyboard.adjust(1)
    keyboard.row(
        *pagination(
            count=count,
            page=page,
            need_back=False,
            back_data=None,
            callback_data='catalog_{page}'),
        width=2
    )
    return keyboard.as_markup()


@log_this()
async def list_of_subcategories(category_id, page=0):
    keyboard = InlineKeyboardBuilder()
    all_subcategories, count = await db.get_subcategories_list(category_id, offset=page * limit, limit=limit)
    for subcategory in all_subcategories:
        keyboard.add(InlineKeyboardButton(text=f'{subcategory.name}',
                                          callback_data=f'subcategory_{subcategory.id}:0/category_{category_id}'))
    keyboard.adjust(1)
    keyboard.row(
        *pagination(
            count=count,
            page=page,
            need_back=True,
            back_data=f'catalog_0',
            callback_data=f'category_{category_id}:'+'{page}'
        ),
        width=3
    )
    return keyboard.as_markup()


@log_this()
async def list_of_items(category_id, subcategory_id, page=0):
    keyboard = InlineKeyboardBuilder()
    all_items, count = await db.get_items_list(subcategory_id, offset=page * limit, limit=limit)
    for item in all_items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item.name} - {item.price / 100} ₽',
            callback_data=f'item_{item.id}/category_{category_id}'))
    keyboard.adjust(1)
    keyboard.row(
        *pagination(
            count=count,
            page=page,
            need_back=True,
            back_data=f'category_{category_id}:0',
            callback_data=f'subcategory_{subcategory_id}:'+'{page}'+f'/category_{category_id}'
        ),
        width=3
    )
    return keyboard.as_markup()


@log_this()
async def manage_item(category_id, subcategory_id, item_id, item_name, price):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text='Добавить в корзину',
        callback_data=f'create_order_item_{item_id}:{item_name}:{price}/subcategory_{subcategory_id}/category_{category_id}'))
    keyboard.add(
        InlineKeyboardButton(text='Назад', callback_data=f'subcategory_{subcategory_id}:0/category_{category_id}'))
    return keyboard.adjust(1).as_markup()


@log_this()
async def confirm_create_order(category_id, item_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Подвердить', callback_data='confirm'))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data=f'item_{item_id}/category_{category_id}'))
    return keyboard.adjust(1).as_markup()


@log_this()
async def create_order_success(category_id, subcategory_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Перейти в корзину', callback_data=f'orders'))
    keyboard.add(InlineKeyboardButton(text='Назад к покупкам',
                                      callback_data=f'subcategory_{subcategory_id}:0/category_{category_id}'))
    return keyboard.adjust(1).as_markup()
