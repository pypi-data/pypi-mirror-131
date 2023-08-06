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
{'console_scripts': ['rate = rate.main:init']}

setup_kwargs = {
    'name': 'rate',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'blankalmasry',
    'author_email': 'blankhussien@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
