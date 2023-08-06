import csv

from rate.writers.writer import Writer


class CsvWriter(Writer):
    _writer = None

    def __init__(self, file_name, keys: list):
        super().__init__(file_name, keys)
        self._writer = csv.writer(self.file)
        self._keys = keys
        # for csv file, we need to write the keys first as the first row
        self._writer.writerow(keys)

    def write_record(self, line: list):
        self._writer.writerow(line)

    def write(self, data):
        self.write_record(data)

    def write_header(self, header: list):
        self._writer.writerow(','.join(header) + '\n')

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys: list):
        self._keys = keys

    def close(self):
        self.file.close()
