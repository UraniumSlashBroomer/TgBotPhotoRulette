from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать игру'), KeyboardButton(text='Присоединиться к игре')],
                                     [KeyboardButton(text='Сменить никнейм')]],
                           resize_keyboard=True, input_field_placeholder='Выберите пункт меню...')

del_kb = ReplyKeyboardRemove()
start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Погнали в меню!')]], resize_keyboard=True)
ready_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Я готов!')]], resize_keyboard=True)
ready_all_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать игру!')]], resize_keyboard=True)
async def create_keyboard_for_game(users):
    in_game_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(user.name)) for user in users]],
                                    resize_keyboard=True)
    return in_game_kb