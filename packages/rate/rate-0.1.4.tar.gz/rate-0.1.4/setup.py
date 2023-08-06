# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rate',
 'rate.calculator',
 'rate.gui',
 'rate.match',
 'rate.players',
 'rate.readers',
 'rate.utils',
 'rate.writers']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer==1.0.3',
 'elote>=0.1.0,<0.2.0',
 'glicko2==2.0.0',
 'tqdm>=4.32,<5.0',
 'trueskill>=0.4.5,<0.5.0']

entry_points = \
{'console_scripts': ['rate = rate.main:main']}

setup_kwargs = {
    'name': 'rate',
    'version': '0.1.4',
    'description': 'A simple CLI tool to rate matches in a file.',
    'long_description': '## Rate\nA Cli-tool for rating players from a file.\nSupported Algorithms:\n- [Elo](https://en.wikipedia.org/wiki/Elo_rating_system)\n- [Glicko](https://en.wikipedia.org/wiki/Glicko_rating_system)\n- [Glicko-2](https://en.wikipedia.org/wiki/Glicko-2_rating_system)\n- [TrueSkill](https://en.wikipedia.org/wiki/TrueSkill)\n- [DWZ](https://en.wikipedia.org/wiki/DWZ_rating_system)\n- [ECF](https://en.wikipedia.org/wiki/ECF_grading_system)\n\n## Usage\n```\nrate path/to/file.csv or path/to/file.json\n```\nAnd you will get prompted with interactive options to select:\n- First player key in the file\n- Second player key in the file\n- Result key from the first player perspective in the file\n- Algorithm to use `[all, elo, "glicko-1", "glicko-2", "trueskill", "dwz", "ecf"]`\n- Output Format `[csv, json]`\n- How a win is defined in the file `Example`: `1` or `win` \n- How a loss is defined in the file `Example`: `0` or `loss` \n- How a draw is defined in the file `Example`: `0.5` or `draw` \n## Example\n### matches.csv\n| player1 | player2 | result1 | result2 | date       |\n|---------|---------|---------|---------|------------|\n| John    | Doe     | won     | Lost    | 12-14-2021 |\n| Doe     | John    | Draw    | Draw    | 12-15-2021 |\n| Sam     | John    | Lost    | won     | 12-16-2021 |\n#### examples of generated files in /examples\n### Answers\n- First player key: player1\n- Second player key: player2\n- Result key: result1\n- Algorithm: elo\n- Output Format: csv\n- How a win is defined: won\n- How a loss is defined: Lost\n- How a draw is defined: Draw\n\n## Installation\n```\n$ pip install rate\n$ rate\n```\n### or ###\n```\n$ py -m pip install rate\n$ py -m rate\n```\nYou might need to run it with `winpty` if you are on Windows.\n```winpty py -m rate```\n\n## Contributing\nIt still needs some work.\nPlease feel free to open an issue or pull request.',
    'author': 'blankalmasry',
    'author_email': 'blankhussien@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
