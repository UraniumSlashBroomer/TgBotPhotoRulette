from app.architecture.classes import *

# key - token, value - game
games: dict[str, Game] = {}
# key - tg_id, value - user
users: dict[int, User] = {}

async def add_user(tg_id: int, user: User):
    users[tg_id] = user

async def add_game(token: str, game: Game):
    games[token] = game

async def get_game(token: str):
    if token not in games:
        return 0
    else:
        return games[token]

async def delete_game(token: str):
    if token in games:
        games.pop(token)
        print(f'игра {token} завершилась.')
        print(f'текущие игры после удаления: {games}')

async def get_user(tg_id: int):
    return users[tg_id]



