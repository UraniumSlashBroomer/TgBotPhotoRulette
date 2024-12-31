from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from app.architecture.states import *

import app.architecture.keyboards as kb

menu_router = Router()
# Команда меню

@menu_router.message(Command('menu'))
@menu_router.message(F.text == 'Погнали в меню!')
async def cmd_menu(message: Message, state: FSMContext):
    await state.set_state(MenuState.in_menu)
    await message.answer(f'Вы вышли в меню. Выберите действие.', reply_markup=kb.main)