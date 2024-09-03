from app.database.models import async_session
from app.database.models import Base, User, Category, Item, Link
from sqlalchemy import select, update, delete


async def set_user(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))

        if not user:
            session.add(User(tg_id=user_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def get_link():
    async with async_session() as session:
        return await session.scalars(select(Link))
