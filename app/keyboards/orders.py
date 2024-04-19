from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from log import log_this

create_payment = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить', callback_data=f'payment')],
        [InlineKeyboardButton(text='Назад', callback_data=f'orders')],
    ]
)


@log_this()
async def list_of_orders(orders):
    keyboard = InlineKeyboardBuilder()
    _sum = 0
    for order, item in orders:
        _sum += item.price * order.count
        keyboard.add(InlineKeyboardButton(
            text=f'{item.name} - {order.count} шт. - {item.price * order.count / 100} ₽',
            callback_data=f'order_{order.id}'))
    # keyboard.add(InlineKeyboardButton(text='Перейти к адресу доставки', callback_data=f'delivery'))
    keyboard.add(InlineKeyboardButton(text='Очистить корзину', callback_data=f'delete_all_orders'))
    keyboard.add(InlineKeyboardButton(text=f'Оплатить {_sum / 100} ₽', callback_data=f'payment'))
    return keyboard.adjust(1).as_markup()


@log_this()
async def manage_order(order_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Удалить', callback_data=f'delete_order_{order_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'orders'))
    return keyboard.adjust(1).as_markup()
