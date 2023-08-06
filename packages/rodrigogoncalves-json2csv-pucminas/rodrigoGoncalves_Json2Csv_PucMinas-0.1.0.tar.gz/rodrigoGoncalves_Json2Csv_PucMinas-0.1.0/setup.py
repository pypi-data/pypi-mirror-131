# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rodrigogoncalves_json2csv_pucminas']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'rodrigoGoncalves_Json2Csv_PucMinas.converter:converter']}

setup_kwargs = {
    'name': 'rodrigogoncalves-json2csv-pucminas',
    'version': '0.1.0',
    'description': 'Converter Csv2Json for learning purposes',
    'long_description': '',
    'author': 'Rodrigo Pereira Gonçalves',
    'author_email': 'rodrigo.goncalves@engenharia.ufjf.br',
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
