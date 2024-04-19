from sqlalchemy import BigInteger, String, ForeignKey, LargeBinary
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger(), primary_key=True, autoincrement=False)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = mapped_column(String(25))


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = mapped_column(String(25))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))


class Photo(Base):
    __tablename__ = 'photos'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    photo = mapped_column(String())


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = mapped_column(String(25))
    description = mapped_column(String(100))
    price = mapped_column(BigInteger())
    photo: Mapped[int] = mapped_column(ForeignKey('photos.id'), nullable=True)
    subcategory: Mapped[int] = mapped_column(ForeignKey('subcategories.id'))


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))
    count: Mapped[int] = mapped_column()


class FAQ(Base):
    __tablename__ = 'faqs'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question = mapped_column(String(100))
    answer = mapped_column(String(1000))
