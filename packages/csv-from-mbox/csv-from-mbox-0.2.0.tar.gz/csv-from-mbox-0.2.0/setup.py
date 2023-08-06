# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['main']
entry_points = \
{'console_scripts': ['csv-from-mbox = main:main']}

setup_kwargs = {
    'name': 'csv-from-mbox',
    'version': '0.2.0',
    'description': "Python script for extracting emails contained in the 'from' field of your mailbox from an .mbox file.",
    'long_description': None,
    'author': 'Vsevolod Mineev',
    'author_email': 'vsevolod.mineev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vsevolod-mineev/csv-from-mbox',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
