import os

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, LabeledPrice, ShippingQuery, PreCheckoutQuery

import app.keyboards as kb
import app.database.requests as db
from app.utils import write_order_info_to_csv

orders_router = Router()
yookassa_token = os.getenv('YOOKASSA_TOKEN')
# yookassa_shop_id = os.getenv('YOOKASSA_SHOP_ID')


@orders_router.message(F.text == 'Корзина')
@orders_router.callback_query(F.data == 'orders')
async def orders(update: Message | CallbackQuery):
    _orders = await db.get_orders_list(update.from_user.id)
    if len(_orders) == 0:
        if type(update) is Message:
            await update.answer('Корзина пуста...',
                                reply_markup=await kb.simple_keyboard('Вперед за новыми покупками', 'catalog_0'))
        else:
            await update.answer(show_alert=False)
            await update.message.edit_text(
                'Корзина пуста...',
                reply_markup=await kb.simple_keyboard('Вперед за новыми покупками', 'catalog_0'))
        return
    if type(update) is Message:
        await update.answer('Товары в корзине', reply_markup=await kb.list_of_orders(_orders))
    else:
        await update.answer(show_alert=False)
        await update.message.edit_text('Товары в корзине', reply_markup=await kb.list_of_orders(_orders))


@orders_router.callback_query(F.data.startswith('order_'))
async def order(callback: CallbackQuery):
    await callback.answer(show_alert=False)
    order_id = callback.data.split('_')[-1]
    _order, _item = await db.get_order(order_id)
    await callback.message.edit_text(
        text=f'Заказ: {_item.name}\nЦена: {_item.price / 100} ₽\nКоличество: {_order.count}\n\n'
             f'Итого: {_item.price * _order.count / 100} ₽',
        reply_markup=await kb.manage_order(order_id))


@orders_router.callback_query(F.data.startswith('delete_order_'))
async def delete_order(callback: CallbackQuery):
    await callback.answer(show_alert=False)
    order_id = callback.data.split('_')[-1]
    await db.delete_order(order_id)
    await orders(callback)


@orders_router.callback_query(F.data == 'delete_all_orders')
async def delete_all_orders(callback: CallbackQuery):
    await callback.answer(show_alert=False)
    await db.delete_all_orders(callback.from_user.id)
    await orders(callback)


# @orders_router.callback_query(F.data == 'delivery')
# async def delivery(callback: CallbackQuery, state: FSMContext):
#     await callback.answer(show_alert=False)
#     await state.set_state(DeliveryState.address)
#     await callback.message.edit_text('Напишите ваш адрес для доставки',
#                                      reply_markup=await kb.simple_keyboard('Назад', 'orders'))
# 
# 
# @orders_router.message(DeliveryState.address)
# async def delivery_address(message: Message, state: FSMContext):
#     await state.update_data(address=message.text)
#     data = await state.get_data()
#     await message.answer('Адрес доставки записан, оплатите заказ', reply_markup=kb.create_payment)
#     await state.clear()


@orders_router.callback_query(F.data == 'payment')
async def payment(callback: CallbackQuery):
    await callback.answer(show_alert=False)

    async def prepare_payment():
        _payload_items = []
        _prices = []
        _orders_items = await db.get_orders_list(callback.from_user.id)
        for _order, _item in _orders_items:
            _payload_items.append(f'{_item.id}:{_item.price}:{_order.count}')
            _prices.append(LabeledPrice(
                label=f'{_item.name} x {_order.count} ',
                amount=_item.price * _order.count))
        _payload = '_'.join(_payload_items)
        return _payload, _prices

    payload, prices = await prepare_payment()
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title='Покупка в магазине WD',
        description="Оплата корзины в интернет магазине WD",
        provider_token=yookassa_token,
        payload=payload,
        currency='RUB',
        prices=prices,
        start_parameter='shop_wd_bot',
        provider_data=None,
        need_name=True,
        need_phone_number=True,
        need_email=False,
        need_shipping_address=True,
        is_flexible=False,
        disable_notification=True,
        protect_content=True,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=60
    )


@orders_router.shipping_query()
async def process_shipping_query(shipping_query: ShippingQuery):
    await shipping_query.answer(ok=True)


@orders_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@orders_router.message(F.successful_payment)
async def success_payment(message: Message):
    _payment_id = message.successful_payment.telegram_payment_charge_id
    _user_id = message.from_user.id
    _user_phone = message.successful_payment.order_info.phone_number
    _orders = message.successful_payment.invoice_payload.split('_')
    _shipping_address = message.successful_payment.order_info.shipping_address
    _total_price = message.successful_payment.total_amount / 100
    await write_order_info_to_csv([_payment_id, _user_id, _user_phone, _shipping_address, _total_price, _orders])
    await db.delete_all_orders(_user_id)
    await message.answer('Оплата прошла успешно.\nСпасибо за покупку!',
                         reply_markup=await kb.simple_keyboard('Вперед за новыми покупками', 'catalog'))
