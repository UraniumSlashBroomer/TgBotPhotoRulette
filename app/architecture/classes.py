from random import randint

TIME_ROUND = 7 # time round in seconds
MAX_PLAYERS = 10

# Класс пользователя, хранит тг ключ и имя
class User:
    def __init__(self, tg_id, name):
        self.tg_id = tg_id
        self.name = name

    def __hash__(self):
        return hash(self.tg_id)

    def __eq__(self, other):
        return self.tg_id == other.tg_id


# Класс игры, хранит токен, фото, игроков, которые подключены
class Game:
    def __init__(self, token, host):
        self.token = token # token of game
        self.photos = list(list()) # photos [[photo_id, who_sent_it]]
        self.players = list() # key - User
        self.host = host # host tg_id
        self.round_ready = dict() # key - User, value - ready or not for start the game and a round
        self.right_answer = '' # right answer for current round
        self.scores = {} # scores
        self.last_round_scores = {} # cache last round scores
        self.game_started = False
        self.time_from_last_round = 0

    # Метод добавления игроков
    async def add_player(self, player: User):
        if self.game_started:
            return 'Эта игра уже идет, вы не можете присоединяться к идущим играм.'
        if len(self.players) >= MAX_PLAYERS:
            return 'В игре максимальное количество игроков. Присоединитесь к другой игре.'
        else:
            self.players.append(player)
            self.scores[player] = 0
            self.last_round_scores[player] = 0
            self.round_ready[player] = False
            print(f'игрок добавлен. Игроки в игре: {self.players}')

        return ''

    async def delete_player(self, player: User):
        self.players.remove(player)

    async def player_ready(self, player):
        self.round_ready[player] = True

    async def reset_round_ready(self):
        for player in self.round_ready:
            self.round_ready[player] = False

    # Метод добавления фото
    async def add_photo(self, photo_id, player_id):
        self.photos.append([photo_id, player_id])

    # Метод получения случайной фотки и удаления ее из сета
    async def get_random_photo(self):
        photo_index = randint(0, len(self.photos) - 1)
        photo_data = self.photos[photo_index]
        photo_id = photo_data[0]
        self.right_answer = str(photo_data[1])
        self.photos.remove(photo_data)
        return photo_id, self.right_answer

    async def cache_scores(self):
        self.last_round_scores = self.scores.copy()

    async def update_scores(self, player, time):
        potential_score = int(1000 / (time * 2))
        if time <= TIME_ROUND:
            if potential_score > 1000:
                self.scores[player] += 1000
            elif potential_score > 0:
                self.scores[player] += potential_score

    async def are_players_here(self):
        if self.players:
            return True

        return False




