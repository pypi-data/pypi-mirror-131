from elote import ECFCompetitor

from rate.players.player import Player


class ECFPlayer(Player):
    _rating_class = ECFCompetitor

    def __init__(self):
        self._rating_object = ECFPlayer._rating_class()

    @property
    def rating(self):
        return self._rating_object.rating

    def play(self, opponent: 'ECFPlayer', result):
        if result == 1:
            self._rating_object.beat(opponent._rating_object)
        elif result == 0.5:
            self._rating_object.tied(opponent._rating_object)
        elif result == 0:
            self._rating_object.lost_to(opponent._rating_object)
        return self, opponent
