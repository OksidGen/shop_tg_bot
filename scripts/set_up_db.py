import base64

from app.database.models import Base, Photo, User, FAQ, Category, Subcategory, Item


def prepare_data():
    # with open('images/test_photo1.jpg', 'rb') as photo:
    #     binary_data = photo.read()
    #     _photo1 = base64.b64encode(binary_data).decode('utf-8')
    # 
    # with open('images/test_photo2.jpg', 'rb') as photo:
    #     binary_data = photo.read()
    #     _photo2 = base64.b64encode(binary_data).decode('utf-8')

    # photos = [
    #     Photo(photo=_photo1),
    #     Photo(photo=_photo2),
    # ]
    users = [
        User(tg_id=428755740)
    ]
    faqs = [
        FAQ(question='q1', answer='a1'),
        FAQ(question='q2', answer='a2'),
        FAQ(question='q3', answer='a3'),
    ]
    categories = [
        Category(name='c1'),
        Category(name='c2'),
        Category(name='c3'),
    ]
    subcategories = [
        Subcategory(name='s1', category=1),
        Subcategory(name='s2', category=1),
        Subcategory(name='s3', category=2),
        Subcategory(name='s4', category=2),
        Subcategory(name='s5', category=2),
        Subcategory(name='s6', category=3),
        Subcategory(name='s7', category=3),
        Subcategory(name='s8', category=3),
        Subcategory(name='s9', category=3),
    ]
    items = [
        Item(name='i1', description='d1', price=100, subcategory=1,),
        Item(name='i2', description='d2', price=100, subcategory=1, ),
        Item(name='i3', description='d3', price=100, subcategory=2, ),
        Item(name='i4', description='d4', price=100, subcategory=2, ),
        Item(name='i5', description='d5', price=100, subcategory=3, ),
        Item(name='i6', description='d6', price=100, subcategory=3, ),
        Item(name='i7', description='d7', price=100, subcategory=4, ),
        Item(name='i8', description='d8', price=100, subcategory=4, ),
        Item(name='i9', description='d9', price=100, subcategory=5, ),
        Item(name='i10', description='d10', price=100, subcategory=5, ),
        Item(name='i11', description='d11', price=100, subcategory=6, ),
        Item(name='i12', description='d12', price=100, subcategory=6, ),
        Item(name='i13', description='d13', price=100, subcategory=7, ),
        Item(name='i14', description='d14', price=100, subcategory=7, ),
        Item(name='i15', description='d15', price=100, subcategory=8, ),
        Item(name='i16', description='d16', price=100, subcategory=8, ),
        Item(name='i17', description='d17', price=100, subcategory=9, ),
        Item(name='i18', description='d18', price=100, subcategory=9, ),
    ]

    _data = [users, faqs, categories, subcategories, items]
    return _data


async def drop_and_create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def fill_tables(async_session):
    data = prepare_data()
    async with async_session() as session:
        for table in data:
            session.add_all(table)
            await session.commit()
