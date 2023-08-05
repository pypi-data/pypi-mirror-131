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
                f"Invalid result value[{text}], supported values are [{self.win}, {self.lose}, {self.draw}]"
            )

    def print_stats(self):
        print(f"Computed results: {{'{self.win}', '{self.lose}', '{self.draw}'}}")
        print(f"Skipped unknown results: {self._skipped_results}")
        print(f"Computed {self._computed_results_count}/{self._total} results")
        print(f"Skipped {self._skipped_results_count}/{self._total} results")
        print(f"Total: {self._total}")

    def __del__(self):
        self._total = 0
        self._skipped_results = set()
        self._skipped_results_count = 0
        self._computed_results_count = 0
