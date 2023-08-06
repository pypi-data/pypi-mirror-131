# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_converter_01']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = csv_converter_01.converter:converter']}

setup_kwargs = {
    'name': 'csv-converter-01',
    'version': '0.2.0',
    'description': 'Convert CSV to JSON',
    'long_description': 'Convert a CSV file to JSON and from JSON to CSV\n\nParameter:\n\n--input", "-i", default="./"\n--output", "-o", default="./"\n--delimiter", "-d", default=","\n--prefix, -prefix\n',
    'author': 'Rogerio Segura Perez',
    'author_email': 'rogeriosperez@gmail.com',
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
