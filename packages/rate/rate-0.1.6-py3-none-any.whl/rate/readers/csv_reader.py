import csv

from rate.readers.reader import Reader


class CsvReader(Reader):
    def __init__(self, file_name):
        super().__init__(file_name)
        self._reader = csv.reader(self.file)
        # skip header line and get keys
        self._keys = self._reader.__next__()
        # init readonly keys to None
        self._readonly_keys_indexes = None

    def next_record(self):
        return next(self)

    def __next__(self):
        raw = next(self._reader)
        return [raw[i] for i in self._readonly_keys_indexes]

    def __iter__(self):
        return self._reader

    def keys(self):
        return self._keys

    def reset(self):
        self.file.seek(0)
        self._reader = csv.reader(self.file)
        # skip header line and get keys
        self._keys = self._reader.__next__()
        # init readonly keys to all keys
        self._readonly_keys_indexes = None
