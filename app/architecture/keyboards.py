from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать игру'), KeyboardButton(text='Присоединиться к игре')],
                                     [KeyboardButton(text='Сменить никнейм')]],
                           resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')

del_kb = ReplyKeyboardRemove()
start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Погнали в меню!')]], resize_keyboard=True)
ready_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Я готов!')]], resize_keyboard=True)
ready_all_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать игру!')]], resize_keyboard=True)

async def create_keyboard_for_game(users):
    # in_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(user.name)) for user in users]],
    #                                 resize_keyboard=True)

    users_cnt = len(users)
    kb = []

    if users_cnt == 1:
        kb.append([KeyboardButton(text=str(user.name)) for user in users])

    elif users_cnt % 2 == 0:
        for i in range(0, users_cnt, 2):
            kb.append([KeyboardButton(text=str(user.name)) for user in users[i:i + 2]])

    elif users_cnt % 2 == 1:
        kb.append([KeyboardButton(text=str(user.name)) for user in users[:3]])

        for i in range(3, users_cnt, 2):
            kb.append([KeyboardButton(text=str(user.name)) for user in users[i:i + 2]])

    in_game_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return in_game_kb