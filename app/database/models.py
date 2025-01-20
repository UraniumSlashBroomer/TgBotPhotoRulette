from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import String
from sqlalchemy import BigInteger

# from dotenv import load_dotenv
# from os import getenv

# for T-SQL

# load_dotenv()
# server = getenv('server')
# database_name = getenv('database_name')
# driver = getenv('driver')
# database_connection = f'mssql+aioodbc://@{server}/{database_name}?driver={driver}'

# SQLite
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine, class_=AsyncSession)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nickname = mapped_column(String(20))



async def async_main():
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
        print('Подключение к БД произошло успешно.')