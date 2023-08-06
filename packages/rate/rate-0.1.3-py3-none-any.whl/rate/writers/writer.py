import abc


class Writer(abc.ABC):
    def __init__(self, file_name, keys):
        self.file_name = file_name
        self.file = open(self.file_name, 'w+', encoding='utf-8', newline='')
        self.keys = keys

    @abc.abstractmethod
    def write(self, data):
        pass

    @abc.abstractmethod
    def write_record(self, writable):
        pass

    def write_records(self, data: list):
        for row in data:
            self.write_record(row)

    @property
    @abc.abstractmethod
    def keys(self):
        pass

    @keys.setter
    def keys(self, keys):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    def __del__(self):
        self.close()
