import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from app.database.models import async_main
from app.routers import reg_router, menu_router, game_router

from dotenv import load_dotenv
from os import getenv

load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='menu', description='Меню'),
        BotCommand(command='set_nickname', description='Установить никнейм')
        ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(reg_router)
    dp.include_router(menu_router)
    dp.include_router(game_router)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')


