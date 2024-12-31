from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def update_nickname(tg_id, new_nickname):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        user.nickname = new_nickname
        await session.commit()

async def get_nickname(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

    return user.nickname
