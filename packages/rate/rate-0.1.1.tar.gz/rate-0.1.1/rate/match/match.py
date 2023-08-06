from rate.players.player import Player


class Match:
    @staticmethod
    def create(player_a: Player, player_b: Player, result_a) -> tuple[Player, Player]:
        player_a, player_b = player_a.play(player_b, result_a)
        return player_a, player_b
