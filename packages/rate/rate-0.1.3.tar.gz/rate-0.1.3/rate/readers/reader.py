import abc


class Reader:
    _extension = None

    def __init__(self, file_name, columns_indexes: list):
        self.file_name = file_name
        self.file = open(file_name, 'r', encoding='utf-8')
        self.columns_indexes = columns_indexes

    @abc.abstractmethod
    def next_record(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def keys(self) -> list:
        pass

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()
