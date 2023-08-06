class PlayerFactory:
    @staticmethod
    def create_player(algorithm_name):
        if algorithm_name == "elo":
            from rate.players import EloPlayer
            return EloPlayer()
        elif algorithm_name == "glicko-1":
            from rate.players import Glicko1Player
            return Glicko1Player()
        elif algorithm_name == "glicko-2":
            from rate.players import Glicko2Player
            return Glicko2Player()
        elif algorithm_name == "trueskill":
            from rate.players import TrueSkillPlayer
            return TrueSkillPlayer()
        elif algorithm_name == "ecf":
            from rate.players import ECFPlayer
            return ECFPlayer()
        elif algorithm_name == "dwz":
            from rate.players import DWZPlayer
            return DWZPlayer()
        else:
            raise ValueError("Unknown algorithm name: " + algorithm_name)
