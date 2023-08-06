import json

from rate.writers.writer import Writer


class JsonWriter(Writer):
    def __init__(self, file_name, keys):
        super().__init__(file_name, keys)
        self._keys = keys
        # write open bracket
        self.file.write('[\n')

    def write(self, data):
        json.dump(data, self.file, indent=2)

    def write_record(self, values):
        if self.file.tell() > 6:
            self.file.write(',\n')
        dict_data = dict(zip(self._keys, values))
        json.dump(dict_data, self.file, indent=2)

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys):
        self._keys = keys

    def close(self):
        # write close bracket
        self.file.write(']')
        self.file.close()
