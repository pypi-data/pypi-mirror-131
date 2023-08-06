class PlayersContainer:
    def __init__(self):
        self.players = {}

    def add_player(self, name, rating):
        if name in self.players.keys():
            raise ValueError(f"Player {name} already exists")
        self.players[name] = rating

    def get_player(self, name):
        if name not in self.players.keys():
            raise ValueError(f"Player {name} does not exist")
        return self.players[name]

    def update_player(self, key, value):
        if key not in self.players.keys():
            raise ValueError(f"Player {key} does not exist")
        self.players[key] = value

    def update_players(self, players: list[list]):
        for player in players:
            self.update_player(player[0], player[1])

    def find_or_add_player(self, key, value):
        if key not in self.players.keys():
            self.add_player(key, value)
            return value
        else:
            return self.players[key]

    def find_or_add_players(self, players: list[list]):
        updated_players = []

        for player in players:
            player_rating = self.find_or_add_player(player[0], player[1])
            updated_players.append(player_rating)
        return updated_players

    def __del__(self):
        self.players.clear()
        del self.players
