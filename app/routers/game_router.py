from aiogram import F, Router
from aiogram.filters import Command
from aiogram.enums import ParseMode

from app.database.requests import get_nickname
from app.architecture.states import *
from app.game.game_functions import *

from app.architecture.classes import User, Game
from app.architecture.structure import add_game, get_game

import app.architecture.keyboards as kb
import uuid

game_router = Router()

# Команда создания игры
@game_router.message(F.text == 'Создать игру', MenuState.in_menu)
async def cmd_create_game(message: Message, state: FSMContext):
    await message.answer('Создается токен игры...')
    token = uuid.uuid4().hex
    user_id = message.from_user.id
    await state.update_data(token=token)

    await add_game(token=token,
                   game=Game(token=token, host=user_id))

    game = await get_game(token)

    nickname = await get_nickname(user_id)
    current_user = User(user_id, nickname)
    await game.add_player(current_user)
    await state.update_data(current_user=current_user)

    print(f'Игра создана успешно! \nИгра: {token} \nИгроки: {game.players}')
    print(f'Зашел игрок {user_id}\nhost: {game.host}')
    await message.answer('Игра создана. Скопируйте токен нажатием из следующего сообщения и отправьте друзьям:', reply_markup=kb.del_kb)
    await message.answer(text=f'`\n{token}\n`', parse_mode=ParseMode.MARKDOWN)
    await message.answer('Отправьте (сколько угодно) фото для игры.\nКогда добавите все фото, используйте команду /ready' + \
                             ' или нажмите на соответствующую клавишу на клавиатуре', reply_markup=kb.ready_kb)

    await state.set_state(GameState.adding_photos)

# Команда присоединения к игре
@game_router.message(F.text == 'Присоединиться к игре', MenuState.in_menu)
async def cmd_join_to_game_1(message: Message, state: FSMContext):
    await message.answer('Введите токен игры: ',  reply_markup=kb.del_kb)
    await state.set_state(GameState.connecting_to_game)

# Команда для присоединения к игре после ввода токена
@game_router.message(GameState.connecting_to_game)
async def cmd_join_to_game_2(message: Message, state: FSMContext):
    token = message.text
    user_id = message.from_user.id
    if await get_game(token):
        game = await get_game(token)
        nickname = await get_nickname(user_id)
        current_user = User(user_id, nickname)
        msg = await game.add_player(current_user)
        if not msg:
            await state.update_data(current_user=current_user)

            await message.answer('Подключение произошло успешно!')
            await message.answer('Отправьте (сколько угодно) фото для игры.\nКогда добавите все фото, используйте команду /ready' + \
                                 ' или нажмите на соответствующую клавишу на клавиатуре', reply_markup=kb.ready_kb)
            await state.set_state(GameState.adding_photos)
            await state.update_data(token=token)
            await echo_all(message, state, f'Зашел игрок {nickname}! Всего игроков в игре: {len(game.players)}', True)
        else:
            await message.answer(msg)
    else:
        await message.answer('Такого токена не существует. Введите другой токен.')

# Добавление фоток (перед началом игры)
@game_router.message(F.photo, GameState.adding_photos)
async def add_photos(message: Message, state: FSMContext):
    data = await state.get_data()
    game = await get_game(data['token'])
    player = data['current_user']
    await game.add_photo(message.photo[-1].file_id, player.name)

# Игрок готов начинать игру
@game_router.message(F.text == 'Я готов!', GameState.adding_photos)
@game_router.message(Command('ready'), GameState.adding_photos)
async def ready_with_photos(message: Message, state: FSMContext):
    data = await state.get_data()
    game = await get_game(data['token'])
    current_user = data['current_user']
    await game.player_ready(current_user)
    await message.answer('Вы готовы.', reply_markup=kb.del_kb)

    ready_to_start = await round_ready(message, state)

    counter = 0
    for user in game.players:
        counter += game.round_ready[user]

    if ready_to_start:
        await echo_all(message, state, f'Все готовы! Хост может запустить игру', True)
        await message.bot.send_message(game.host, f'Вы хост. Используйте команду /all_ready, чтобы запустить игру', reply_markup=kb.ready_all_kb)
    else:
        await echo_all(message, state, f'Количество готовых игроков: {counter} из {len(game.players)}', False)

    if current_user.tg_id == game.host:
        await state.set_state(GameState.all_ready)
    else:
        await state.set_state(GameState.ready)

    print(f'ID фотографий в игре: {game.photos}')

# Это функция старта игры для хоста
@game_router.message(F.text == 'Начать игру!', GameState.all_ready)
@game_router.message(Command('all_ready'), GameState.all_ready)
async def cmd_host_ready(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(GameState.ready)
    await echo_all(message, state, 'Игра началась!', True)

    await game_running(message, state)

# Это функция срабатывает, когда игрок играет (пишет свой вариант)
@game_router.message(GameState.ready)
async def cmd_ready(message: Message, state: FSMContext):
    data = await state.get_data()
    game = await get_game(data['token'])
    player = data['current_user']
    end = time() # Игрок написал свой вариант
    if game and game.game_started:
        if message.text == game.right_answer:
            await message.answer('Вы ответили верно!')
            await game.update_scores(player, end - game.time_from_last_round) # Обновляем очки если игрок ответил правильно
        else:
            await message.answer(f'Вы ошиблись.. это фото игрока {game.right_answer}!')
        await game_running(message, state)
    elif not game:
        await state.set_state(GameState.game_ended)