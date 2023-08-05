from rate.players.player import Player
from glicko2 import Player as GlickoPlayer


class Glicko2Player(Player):
    _rating_class = GlickoPlayer

    def __init__(self, rating_initial=1500):
        self._rating_object = Glicko2Player._rating_class(rating_initial)

    @property
    def rating(self):
        return self._rating_object.rating

    def play(self, opponent: 'Glicko2Player', result):
        o = opponent._rating_object
        if result == 1:
            self._rating_object.update_player([o.getRating()], [o.getRd()], [1])
            o.update_player([self._rating_object.getRating()], [self._rating_object.getRd()], [0])
        elif result == 0.5:
            self._rating_object.update_player([o.getRating()], [o.getRd()], [0.5])
            o.update_player([self._rating_object.getRating()], [self._rating_object.getRd()], [0.5])
        elif result == 0:
            self._rating_object.update_player([o.getRating()], [o.getRd()], [0])
            o.update_player([self._rating_object.getRating()], [self._rating_object.getRd()], [1])
        return self, opponent
