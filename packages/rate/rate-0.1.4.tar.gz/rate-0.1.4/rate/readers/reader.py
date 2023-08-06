import abc


class Reader:
    _extension = None

    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, 'r', encoding='utf-8')
        self._readonly_keys_indexes = []

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

    @property
    def readonly_keys(self):
        a = []
        for i in range(len(self.keys())):
            if i in self._readonly_keys_indexes:
                a.append(self.keys()[i])
        return a

    @readonly_keys.setter
    def readonly_keys(self, keys: list):
        self._readonly_keys_indexes = []
        for key in keys:
            if key in self.keys():
                self._readonly_keys_indexes.append(self.keys().index(key))

    @abc.abstractmethod
    def reset(self):
        pass

    def __del__(self):
        self.close()
