import abc


class Player(abc.ABC):
    @property
    @abc.abstractmethod
    def _rating_class(self) -> object:
        pass

    @abc.abstractmethod
    def rating(self) -> int:
        pass

    @abc.abstractmethod
    def play(self, opponent: 'Player', result):
        pass
