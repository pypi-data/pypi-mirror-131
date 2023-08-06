import json

from rate.readers.reader import Reader


class JsonReader(Reader):
    def __init__(self, file_name):
        super().__init__(file_name)
        data = json.load(self.file)
        self._keys = list(data[0].keys())
        # init readonly keys to all keys
        self.readonly_keys = self._keys
        self._reader = (i for i in data)

    def next_record(self) -> dict:
        return next(self)

    def __next__(self):
        raw = next(self._reader)
        # return list of values for readonly keys from dict raw
        return [raw[key] for key in self.readonly_keys]

    def __iter__(self):
        return self._reader

    def keys(self) -> list:
        return self._keys

    def close(self):
        self.file.close()

    def reset(self):
        self.file.seek(0)
        data = json.load(self.file)
        self._reader = (i for i in data)
