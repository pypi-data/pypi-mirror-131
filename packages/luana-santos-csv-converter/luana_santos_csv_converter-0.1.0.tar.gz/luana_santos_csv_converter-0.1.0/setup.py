# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luana_santos_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.5,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'luana_santos_csv_converter.converter:converter',
                     'json_converter = '
                     'luana_santos_csv_converter.converterj:converterj']}

setup_kwargs = {
    'name': 'luana-santos-csv-converter',
    'version': '0.1.0',
    'description': 'Convert csv to json and vice versa. For learning purposes.',
    'long_description': '# File Converter\n\nCSV to JSON and JSON to CSV converter.\n\n## Introduction\n\nLearning how to deploy a lib on PyPi at PUC using Poetry.\n\n### What this project can do\n\nRead a **csv** file or a **folder** and convert them to **JSON** and vice versa.\nThis project is a program running on terminal, preferably install with pipx:\n\n```bash\npipx install luana_santos_csv_converter\n```\n\nTo use, just type in:\n\n```bash\ncsv_converter --help\n```\n\nOr:\n\n```bash\njson_converter --help\n```',
    'author': 'Luana Santos',
    'author_email': 'luanasilvia.lss@gmail.com',
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
