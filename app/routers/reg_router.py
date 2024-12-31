from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.database.requests import set_user, update_nickname, get_nickname
from app.architecture.states import *
from app.routers.menu_router import cmd_menu
import app.architecture.keyboards as kb

reg_router = Router()

# Команда старта бота
@reg_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(MenuState.in_menu)
    user_id = message.from_user.id
    await set_user(user_id) # Добавляем юзера в БД
    nickname = await get_nickname(user_id)
    if not nickname:
        await message.answer(f'Привет!\nЯ бот, в котором можно поиграть в фото-рулетку.')
        await set_nickname(message, state)
    else:
        await message.answer(f'Привет!\nЯ бот, в котором можно поиграть в фото-рулетку.', reply_markup=kb.start_kb)

@reg_router.message(F.text == 'Сменить никнейм', MenuState.in_menu)
@reg_router.message(Command('set_nickname'), MenuState.in_menu)
async def set_nickname(message: Message, state: FSMContext):
    user_id = message.from_user.id
    old_nickname = await get_nickname(user_id)
    if old_nickname:
        await message.answer(f'Ваш старый ник: {old_nickname}', reply_markup=kb.del_kb)
        await message.answer(f'Введите новый ник: ')
    else:
        await message.answer(f'У вас еще не установлен никнейм.')
        await message.answer(f'Напишите его, под ним вас будут видеть другие игроки')

    await state.set_state(RegisterState.nickname)

@reg_router.message(RegisterState.nickname)
async def save_nickname(message: Message, state: FSMContext):
    user_id = message.from_user.id
    nickname = message.text
    if nickname[0] == '/':
        await message.answer(f'Недопустимый никнейм.')
        await set_nickname(message, state)
    else:
        await state.clear()
        await update_nickname(user_id, nickname)
        await message.answer(f'Вы теперь {nickname}!')

        await state.set_state(MenuState.in_menu)
        await cmd_menu(message, state)

