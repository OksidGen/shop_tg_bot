import sqlalchemy.exc
from sqlalchemy import select, delete, func

from app.database.engine import async_session
from app.database.models import Category, Subcategory, Item, Order, User, FAQ, Photo


async def get_categories_list(offset=0, limit=5):
    async with async_session() as session:
        count = await session.scalar(select(func.count(Category.id)))
        result = await session.scalars(select(Category).offset(offset).limit(limit))
        return result, count


async def get_subcategories_list(category_id, offset=0, limit=5):
    async with async_session() as session:
        count = await session.scalar(select(func.count(Subcategory.id)).where(Subcategory.category == int(category_id)))
        result = await session.scalars(
            select(Subcategory)
            .where(Subcategory.category == int(category_id))
            .offset(offset)
            .limit(limit))
        return result, count


async def get_items_list(subcategory_id, offset=0, limit=5):
    async with async_session() as session:
        count = await session.scalar(select(func.count(Item.id)).where(Item.subcategory == int(subcategory_id)))
        result = await session.execute(
            select(Item.id, Item.name, Item.price)
            .where(Item.subcategory == int(subcategory_id))
            .offset(offset)
            .limit(limit)
        )
        return result.fetchall(), count


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == int(item_id)))


async def create_order(user_id, item_id, count):
    async with async_session() as session:
        order = Order(user=user_id, item=int(item_id), count=count)
        session.add(order)
        await session.commit()


async def get_orders_list(user_id):
    async with async_session() as session:
        query = (
            select(Order, Item)
            .where(Order.user == int(user_id))
            .join(Item, Item.id == Order.item)
        )
        result = await session.execute(query)
        return result.fetchall()


async def get_order(order_id):
    async with async_session() as session:
        query = (
            select(Order, Item)
            .where(Order.id == int(order_id))
            .join(Item, Item.id == Order.item)
        )
        result = await session.execute(query)
        return result.fetchone()


async def delete_order(order_id):
    async with async_session() as session:
        await session.execute(delete(Order).where(Order.id == int(order_id)))
        await session.commit()


async def delete_all_orders(user_id):
    async with async_session() as session:
        await session.execute(delete(Order).where(Order.user == int(user_id)))
        await session.commit()


async def create_user(user_id):
    async with async_session() as session:
        try:
            session.add(User(tg_id=user_id))
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass


async def get_faqs_list():
    async with async_session() as session:
        result = await session.execute(select(FAQ.id, FAQ.question))
        return result.fetchall()


async def get_faq(faq_id):
    async with async_session() as session:
        return await session.scalar(select(FAQ).where(FAQ.id == int(faq_id)))


async def get_photo(photo_id):
    async with async_session() as session:
        return await session.scalar(select(Photo).where(Photo.id == int(photo_id)))
