# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saezo_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.30.1,<8.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'saezo_csv_converter.converter:converterTocsv',
                     'json_converter = '
                     'saezo_csv_converter.converter:converterTocsv']}

setup_kwargs = {
    'name': 'saezo-csv-converter',
    'version': '0.1.3',
    'description': 'Trabalho de Python - PUC - Turma DS',
    'long_description': '',
    'author': 'ozeas santos',
    'author_email': 'ozeassantos@saezo.com.br',
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
