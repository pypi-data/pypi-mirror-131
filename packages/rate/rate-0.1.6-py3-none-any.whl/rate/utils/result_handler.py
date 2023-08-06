class ResultHandler:
    _skipped_results = set()
    _skipped_results_count = 0
    _computed_results_count = 0
    _total = 0

    def __init__(self, win, lose, draw):
        self.win = win.casefold()
        self.lose = lose.casefold()
        self.draw = draw.casefold()

    def get_result_from_string(self, text):
        self._total += 1
        if text.casefold() == self.win:
            self._computed_results_count += 1
            return 1
        elif text.casefold() == self.lose:
            self._computed_results_count += 1
            return 0
        elif text.casefold() == self.draw:
            self._computed_results_count += 1
            return 0.5
        else:
            self._skipped_results.add(text)
            self._skipped_results_count += 1
            raise ValueError(
                "Invalid result value[{}], supported values are [{}, {}, {}]".format(
                    text, self.win, self.lose, self.draw
                )
            )

    def print_stats(self):
        print(
            "Computed results: {}/{} ({:.2f}%)".format(
                self._computed_results_count,
                self._total,
                self._computed_results_count / self._total * 100,
            )
        )
        print(
            "Skipped results: {}/{} ({:.2f}%)".format(
                self._skipped_results_count,
                self._total,
                self._skipped_results_count / self._total * 100,
            )
        )

    def __del__(self):
        self._total = 0
        self._skipped_results = set()
        self._skipped_results_count = 0
        self._computed_results_count = 0
