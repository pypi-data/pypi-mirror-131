# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trabalho_jeansilva_converter_csv_json']

package_data = \
{'': ['*']}

install_requires = \
['bpython>=0.22.1,<0.23.0', 'click>=8.0.3,<9.0.0', 'path>=16.2.0,<17.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'Trabalho_JeanSilva_Converter_CSV_JSON.converter:converter',
                     'json_converter = '
                     'Trabalho_JeanSilva_Converter_CSV_JSON.converter:converter2']}

setup_kwargs = {
    'name': 'trabalho-jeansilva-converter-csv-json',
    'version': '0.1.5',
    'description': 'Função de converter arquivo csv para json, e json para csv.',
    'long_description': None,
    'author': 'Jean Silva',
    'author_email': 'JeanSilvadSantos@gmail.com',
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
