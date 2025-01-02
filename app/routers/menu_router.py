from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.architecture.states import *
from app.architecture.classes import MAX_PLAYERS, TIME_ROUND
from app.game.game_functions import leave

import app.architecture.keyboards as kb

menu_router = Router()
# Команда меню

@menu_router.message(Command('menu'))
@menu_router.message(F.text == 'Погнали в меню!')
async def cmd_menu(message: Message, state: FSMContext):
    await leave(message, state)
    await state.clear()
    await state.set_state(MenuState.in_menu)
    await message.answer(f'Вы вышли в меню. Выберите действие.\n\n/help - ознакомиться с ботом', reply_markup=kb.main)

@menu_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это бот для игры в фото-рулетку.\n\nСоздайте игру или присоединитесь к ней. ' + \
                         'Токен для подключения можно узнать у того, кто создал игру.\n' + \
                         'Перед началом игры отправьте любое количество фотографий, и нажмите кнопку "Готов".\n' + \
                         'Во время игры бот будет присылать вам случайную фотографию из всех, которые отправили игроки. ' + \
                         'Те, кто угадал, чья это фотография — получает очки, если успел по времени. ' + \
                         'Те, кто НЕ угадал, ничего не получают.\n\n' + \
                         'Вот стандартные (текущие) настройки игры:\n\n' + \
                         f'Максимальное кол-во игроков: {MAX_PLAYERS} человек\n' + \
                         f'Максимальное кол-во фотографий в игре: на данный момент ограничений нет\n' + \
                         f'Время, после которого очки не выдаются: {TIME_ROUND} секунд')

    await message.answer('Вы можете выйти из игры в любой момент введя /menu.\nЕсли все игроки выйдут из игры до ' + \
                         'ее окончания - токен будет недействителен.\nПрисоединиться к уже идущей игре невозможно.')
    await message.answer('Вот команды, которые есть у бота:\n/help - посмотреть команды бота\n' + \
                         '/start - запустить бота заново\n/menu - вернуться в меню\n' + \
                         '/set_nickname - сменить никнейм')
