from typing import Union

from rate.match import Match
from rate.players import PlayerFactory
from rate.players import PlayersContainer
from rate.readers import Reader
from rate.writers import Writer
from rate.utils import ResultHandler


class Calculator:
    def __init__(self, reader: Reader, writer: Writer, algorithm_name: Union[str, list],
                 result_handler: ResultHandler):
        self.reader = reader
        self.writer = writer
        self.algorithm_name = algorithm_name
        self.result_handler = result_handler
        self.players_container = PlayersContainer()

    def calculate(self):
        while True:
            try:
                # read next line if exists
                player1, player2, result_for_player1 = self.reader.next_record()

                # get player ratings from container
                p1, p2 = self.players_container.find_or_add_players([
                    [player1, PlayerFactory.create_player(self.algorithm_name)],
                    [player2, PlayerFactory.create_player(self.algorithm_name)]
                ])

                # get result in terms of 1, 0 or 0.5, if text is not recognized, skip it
                try:
                    result = self.result_handler.get_result_from_string(result_for_player1)
                except ValueError as error_message:
                    print(error_message)
                    continue

                # compute new ratings
                p1_updated, p2_updated = Match.create(p1, p2, result)

                # update players container
                self.players_container.update_players([[player1, p1_updated], [player2, p2_updated]])

                # write new ratings
                self.writer.write_records([
                    [player1, str(p1_updated.rating)],
                    [player2, str(p2_updated.rating)],
                ])
            except StopIteration:
                self.result_handler.print_stats()
                break

    def __del__(self):
        del self.reader
        del self.writer
        del self.players_container
        del self.result_handler
