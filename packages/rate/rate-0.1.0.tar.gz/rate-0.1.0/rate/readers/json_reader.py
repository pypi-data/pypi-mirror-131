import json

from rate.readers.reader import Reader


class JsonReader(Reader):
    def __init__(self, file_name, columns_indexes: list):
        super().__init__(file_name, columns_indexes)
        data = json.load(self.file)
        self._keys = list(data[0].keys())
        self._reader = (i for i in data)
        self.requested_columns = [self._keys[int(i)] for i in self.columns_indexes]

    def next_record(self):
        return next(self)

    def __next__(self):
        raw = next(self._reader)
        return [raw[i] for i in self.requested_columns]

    def __iter__(self):
        return self._reader

    def keys(self) -> list:
        return self._keys

    def close(self):
        self.file.close()
