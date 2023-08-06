class ReaderFactory:
    @staticmethod
    def create_reader(extension_type, file_path, relevant_columns_indexes):
        if extension_type == "csv" or extension_type == ".csv":
            from rate.readers import CsvReader
            return CsvReader(file_path, relevant_columns_indexes)
        elif extension_type == "json" or extension_type == ".json":
            from rate.readers import JsonReader
            return JsonReader(file_path, relevant_columns_indexes)
        else:
            raise ValueError("Unknown reader type")
