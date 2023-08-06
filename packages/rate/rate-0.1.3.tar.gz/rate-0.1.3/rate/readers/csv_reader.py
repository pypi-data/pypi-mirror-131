import csv

from rate.readers.reader import Reader


class CsvReader(Reader):
    def __init__(self, file_name, columns_indexes: list):
        super().__init__(file_name, columns_indexes)
        self._reader = csv.reader(self.file)
        # skip header line and get keys
        self._keys = self.__next__()

    def next_record(self):
        return next(self)

    def __next__(self):
        raw = next(self._reader)
        return [raw[int(field_index)] for field_index in self.columns_indexes]

    def __iter__(self):
        return self._reader

    def keys(self):
        return self._keys
