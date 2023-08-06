class WriterFactory:
    @staticmethod
    def create_writer(output_file_name, headers):
        if output_file_name.endswith('.csv'):
            from rate.writers import CsvWriter
            return CsvWriter(output_file_name, headers)
        elif output_file_name.endswith('.json'):
            from rate.writers import JsonWriter
            return JsonWriter(output_file_name, headers)
