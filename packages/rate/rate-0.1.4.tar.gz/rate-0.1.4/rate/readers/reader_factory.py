import os


class ReaderFactory:
    @staticmethod
    def create_reader(file):
        file_name, file_extension = os.path.splitext(file)
        if file_extension == "csv" or file_extension == ".csv":
            from rate.readers import CsvReader
            return CsvReader(file)
        elif file_extension == "json" or file_extension == ".json":
            from rate.readers import JsonReader
            return JsonReader(file)
        else:
            raise ValueError("Unknown reader type")
