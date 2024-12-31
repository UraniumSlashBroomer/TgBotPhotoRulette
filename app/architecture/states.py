from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class RegisterState(StatesGroup):
    nickname = State()

class MenuState(StatesGroup):
    in_menu = State()

class GameState(StatesGroup):
    connecting_to_game = State()
    adding_photos = State()
    ready = State()
    all_ready = State()
    game_running = State()
    game_ended = State()