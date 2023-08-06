# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['main']
entry_points = \
{'console_scripts': ['csv-from-mbox = main:main']}

setup_kwargs = {
    'name': 'csv-from-mbox',
    'version': '0.4.5',
    'description': "Python script for extracting emails contained in the 'from' field of your mailbox from an .mbox file.",
    'long_description': "# Python script to extract emails from an .mbox file.\n\nPython script for extracting emails contained in the 'from' field of your mailbox from an .mbox file. Install the package using `pip install`, run the script, paste the input directory, paste the output directory -> done.\n\nAll the emails that contain one of the following are filtered out: noreply, no-reply, do-not-reply, do_not_reply.\n\n# How to use:\nTo install `csv-from-mbox` using `pip install`:\n```\npip install csv-from-mbox\n```\n\nTo execute the script enter:\n```\ncsv-from-mbox\n```\nYou'll be prompted to specify the `input path`, for example to use an .mbox file in your current directory named mail.mbox, you would paste:\n```\n./mail.mbox\n```\nYou'll be prompted to specify the `output path`, for example to output the .csv file into your current directory and name it emails.csv, you would paste:\n```\n./emails.csv\n```\nThank you and have fun!",
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
