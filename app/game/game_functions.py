from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from time import time

import app.architecture.keyboards as kb
from app.architecture.structure import get_game, delete_game


# Функция для отправки всем очков после завершения раунда
async def print_scores(message: Message, state: FSMContext, game):
    scores = game.scores
    msg = ''
    last_round_scores = sorted(game.last_round_scores.items(), key=lambda item: item[1], reverse=True)
    if game.photos:
        arrows = '🟢🔻⚪️'
        for place, (player, score) in enumerate(sorted(scores.items(), key=lambda item: item[1], reverse=True)):
            for place_2, (player_2, _) in enumerate(last_round_scores):
                if player_2 == player and place < place_2:
                    msg += f'{arrows[0]} {place + 1}. {player.name}: {score}\n'
                    break
                elif player_2 == player and place > place_2:
                    msg += f'{arrows[1]} {place + 1}. {player.name}: {score}\n'
                elif player_2 == player and place == place_2:
                    msg += f'{arrows[2]} {place + 1}. {player.name}: {score}\n'
    else:
        places_smiles = '🥇🥈🥉🎖'
        for place, (player, score) in enumerate(sorted(scores.items(), key=lambda item: item[1], reverse=True)):
            if place >= 3:
                msg += f'{places_smiles[-1]} {place + 1}. {player.name}: {score}\n'
            else:
                msg += f'{places_smiles[place]} {place + 1}. {player.name}: {score}\n'
    await echo_all(message, state, msg, True)


# Функция для отправки сообщений всем, кто в игре
async def echo_all(message: Message, state: FSMContext, msg: str, with_user_who_triggered: bool):
    data = await state.get_data()
    game = await get_game(data['token'])
    for player in game.players:
        if player.tg_id == message.from_user.id and with_user_who_triggered:
            await message.bot.send_message(player.tg_id, msg)
        else:
            await message.bot.send_message(player.tg_id, msg)

# Проверка, все ли готовы начинать раунд
async def round_ready(message: Message, state: FSMContext):
    data = await state.get_data()
    game = await get_game(data['token'])
    for value in game.round_ready.values():
        if not value:
            return False

    return True

# Логика игры
async def game_running(message: Message, state: FSMContext):
    data = await state.get_data()
    game = await get_game(data['token'])
    player = data['current_user']
    await game.player_ready_in_round(player)
    keyboard = await kb.create_keyboard_for_game(game.players)
    ready = await round_ready(message, state)

    # Если фото остались и все игроки готовы, начинаем следующий раунд
    if game.photos and ready:
        if game.round_counter != 0:
            await print_scores(message, state, game)

        await game.reset_round_ready()
        photo_id, _ = await game.get_random_photo()

        for player in game.players:
                await message.bot.send_photo(player.tg_id, photo_id)
                await message.bot.send_message(player.tg_id, 'Чье это фото?', reply_markup=keyboard)
        game.time_from_last_round = time() # Фиксируем время начала раунда
        await game.cache_scores() # Сейвим скор с последнего раунда для обозначения, кто поднялся, а кто опустился
    elif game.photos and not ready: # Если фото остались, но не все ответили - даем знать пользователю
        await message.answer(f'Дождитесь, пока другие игроки сделают свой выбор...')
    elif not game.photos and not ready: # Если фото нет, но не все ответили - даем знать пользователю
        await message.answer(f'Игра завершилась, ждите результатов...')
    elif ready: # Когда последний игрок сделает свой выбор на последней фотке - завершаем игру
        await echo_all(message, state, 'Игра завершилась. Результаты:', True)
        await print_scores(message, state, game)
        await echo_all(message, state, 'Выйдите в меню. /menu', True)
        # Завершаем игру (удаляем ее из памяти) и не забываем вывести очки
        await delete_game(data['token'])

    # if not game.photos:
    #     await state.set_state(GameState.game_ended)