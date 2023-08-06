from __future__ import print_function, unicode_literals

import os
import sys
from os.path import isfile
from rate.calculator import Calculator
from rate.gui import GUI
from rate.readers import ReaderFactory
from rate.utils import ResultHandler
from rate.writers import WriterFactory
from rate.config import supported_algorithms, supported_writers, supported_readers


def generate(reader, player_a, player_b, result_a,
             algorithm_name, output_format,
             result_win, result_loss, result_draw):
    reader.readonly_keys = [player_a, player_b, result_a]
    # create writer
    file = reader.file_name
    file_name, _ = os.path.splitext(file)
    output_file_name = file_name + "_" + algorithm_name + "." + output_format
    writer = WriterFactory.create_writer(output_file_name, headers=["file_name", "rating"])

    # create result handler to handle results according to the user specifications
    result_handler = ResultHandler(result_win, result_loss, result_draw)

    # start calculation
    calculator = Calculator(reader,
                            writer,
                            algorithm_name if algorithm_name != 'all' else supported_algorithms,
                            result_handler)
    calculator.calculate()
    del calculator


def main():
    # example answers
    # answers = {
    #     'player_a': 'fighter1',
    #     'player_b': 'fighter2',
    #     'result_a': 'result1',
    #     'algorithm_name': 'all',
    #     'output_format': 'json',
    #     'result_win': 'Win',
    #     'result_loss': 'loss',
    #     'result_draw': 'Draw',
    # }

    try:
        file = sys.argv[1:][0]
    except IndexError:
        print("Please provide a file name")
        exit(1)
    if not isfile(file):
        print("File does not exist")
        exit(1)
    if file.strip().split(".")[-1] not in supported_readers:
        # print the same without f strings
        print("File format not supported. Supported formats are: " + ", ".join(supported_readers))
        exit(1)

    # create reader
    reader = ReaderFactory.create_reader(file)

    answers = GUI.display(supported_writers, supported_algorithms, keys=reader.keys())
    if answers['algorithm_name'] == 'all':
        for algorithm in supported_algorithms:
            # print with no f strings
            print("Computing " + answers['algorithm_name'] + " ratings...")
            answers["algorithm_name"] = algorithm
            generate(reader, **answers)
            reader.reset()

    else:
        print("Computing " + answers['algorithm_name'] + " ratings...")
        generate(reader, **answers)
    print("Done")


if __name__ == '__main__':
    main()
