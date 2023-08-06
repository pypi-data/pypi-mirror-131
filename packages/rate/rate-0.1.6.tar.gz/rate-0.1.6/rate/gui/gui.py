from PyInquirer import prompt


class GUI:

    @staticmethod
    def questions(supported_writers, supported_algorithms, keys):
        questions = [
            {
                'type': 'list',
                'name': 'player_a',
                'message': 'First Player Key',
                'choices': keys,
                'validate': lambda value: value.strip().isdigit() or 'Please enter a valid number.'

            },
            {
                'type': 'list',
                'name': 'player_b',
                'message': 'Second Player Key:',
                'choices': keys,

                'validate': lambda value: value.strip().isdigit() or 'Please enter a valid number.'

            },
            {
                'type': 'list',
                'name': 'result_a',
                'message': 'Result from the first player perspective:',
                'choices': keys,
                'validate': lambda value: value.strip().isdigit() or 'Please enter a valid number.'

            },
            {
                'type': 'list',
                'name': 'algorithm_name',
                'message': 'Algorithm you want to use to rate the matches:',
                'choices': ['all'] + supported_algorithms,

            },
            {
                'type': 'list',
                'name': 'output_format',
                'message': 'Output format:',
                'choices': supported_writers,
            },
            {
                'type': 'input',
                'name': 'result_win',
                'message': 'Result for a win:(how would a win is typed in the result column)',
                'validate': lambda value: value.strip() != '' or 'Please enter a valid answer.'
            },
            {
                'type': 'input',
                'name': 'result_loss',
                'message': 'Result for a loss:(how would a loss is typed in the result column)',
                'validate': lambda value: value.strip() != '' or 'Please enter a valid answer.'

            },
            {
                'type': 'input',
                'name': 'result_draw',
                'message': 'Result for a draw:(how would a win is typed in the result column)',
                'validate': lambda value: value.strip() != '' or 'Please enter a valid answer.'
            },
        ]
        return questions

    @staticmethod
    def display(supported_writers, supported_algorithms, keys):
        return prompt(GUI.questions(supported_writers, supported_algorithms, keys))
