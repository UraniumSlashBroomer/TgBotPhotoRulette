from random import randint

TIME_ROUND = 7 # time round in seconds
MAX_PLAYERS = 10

# Класс пользователя, хранит тг ключ и имя
class User:
    def __init__(self, tg_id, name):
        self.tg_id = tg_id
        self.name = name

# Класс игры, хранит токен, фото, игроков, которые подключены
class Game:
    def __init__(self, token, host):
        self.token = token # token of game
        self.photos = list(list()) # photos [[photo_id, who_sent_it]]
        self.players = dict() # key - tg_id, value - ready or not for a whole game
        self.host = host # host tg_id
        self.round_ready = dict() # key - tg_id, value - ready or not for a round
        self.right_answer = '' # right answer for current round
        self.scores = {} # scores
        self.last_round_scores = {}
        self.round_counter = 0
        self.time_from_last_round = 0

    # Метод добавления игроков, игроков не может быть больше 10
    async def add_player(self, player: User):
        if len(self.players) >= MAX_PLAYERS:
            print(f'Игроков больше 10 в игре {self.token}')
        else:
            self.players[player] = False # Значение - игрок not ready or ready
            self.scores[player] = 0
            self.last_round_scores[player] = 0
            self.round_ready[player] = True
            print(f'игрок добавлен. Игроки в игре: {self.players}')

    # Метод для того, чтобы игрок был ready
    async def player_ready(self, player):
        self.players[player] = True

    async def player_ready_in_round(self, player):
        self.round_ready[player] = True

    async def reset_round_ready(self):
        for player in self.round_ready:
            self.round_ready[player] = False

    # Метод добавления фото
    async def add_photo(self, photo_id, player_id):
        self.photos.append([photo_id, player_id])

    # Метод получения рандомной фотки и удаления ее из сета
    async def get_random_photo(self):
        self.round_counter += 1 # Считаем раунды
        photo_index = randint(0, len(self.photos) - 1)
        photo_data = self.photos[photo_index]
        photo_id = photo_data[0]
        self.right_answer = str(photo_data[1])
        self.photos.remove(photo_data)
        return photo_id, self.right_answer

    async def cache_scores(self):
        self.last_round_scores = self.scores.copy()

    async def update_scores(self, player, time):
        if time <= TIME_ROUND:
            self.scores[player] += int(1000 / (time * 2))



