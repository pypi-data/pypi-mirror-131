# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicholima_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'nicholima_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'nicholima-csv-converter',
    'version': '0.1.1',
    'description': 'Converter csv to json.',
    'long_description': "CSV to JSON converter.\n\n\n\n## Introduction\n\nTeaching how to deploy a lib on Pypi at PUC using Poetry\n\n\n\n\n\n### What this project can do\n\nRead a **csv** file or a **folder** with csv's and convert them to **JSON**\nThis project is a program running on terminal, preferably install with pipx:\n\n\n\n\n\n```\npipx install nicholima-csv-converter\n```\nTo use, just type in:\n\n```bash\ncsv_converter --help\n```\n\nOr:\n\n```bash\njson_converter --help\n```",
    'author': 'Nicholas Lima',
    'author_email': 'nicho.lima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
