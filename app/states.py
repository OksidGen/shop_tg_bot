from aiogram.fsm.state import StatesGroup, State


class CreateOrderState(StatesGroup):
    category_id = State()
    subcategory_id = State()

    item_id = State()
    item_name = State()
    item_price = State()
    count = State()
    confirm = State()


# class DeliveryState(StatesGroup):
#     address = State()


class NewQuestionState(StatesGroup):
    question = State()


class CreatePayment(StatesGroup):
    orders = State()
    total_amount = State()
