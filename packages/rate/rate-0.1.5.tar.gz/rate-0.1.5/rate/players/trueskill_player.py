from trueskill import Rating, rate_1vs1

from rate.players.player import Player


class TrueSkillPlayer(Player):
    _rating_class = Rating

    def __init__(self):
        self._rating_object = TrueSkillPlayer._rating_class()

    @property
    def rating(self):
        return self._rating_object.mu

    def play(self, opponent: 'TrueSkillPlayer', result):

        if result == 1:
            self._rating_object, opponent._rating_object = rate_1vs1(self._rating_object, opponent._rating_object)
        elif result == 0.5:
            self._rating_object, opponent._rating_object = rate_1vs1(self._rating_object, opponent._rating_object, drawn=True)
        elif result == 0:
            opponent._rating_object, self._rating_object = rate_1vs1(opponent._rating_object, self._rating_object)

        return self, opponent
