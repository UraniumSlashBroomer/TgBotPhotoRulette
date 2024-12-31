from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import String

from dotenv import load_dotenv
from os import getenv

load_dotenv()
server = getenv('server')
database_name = getenv('database_name')
driver = getenv('driver')
database_connection = f'mssql+aioodbc://@{server}/{database_name}?driver={driver}'

engine = create_async_engine(database_connection)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    nickname = mapped_column(String(20))



async def async_main():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
        print('Подключение завершено, должна создаться таблица и БД.')