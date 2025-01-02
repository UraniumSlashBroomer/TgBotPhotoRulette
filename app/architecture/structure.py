from app.architecture.classes import *

# key - token, value - game
games: dict[str, Game] = {}

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



