# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rafa_puc_ia_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'rafa_puc_ia_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'rafa-puc-ia-csv-converter',
    'version': '0.1.0',
    'description': 'Convert csv to Json. For learning purposes.',
    'long_description': '',
    'author': 'Rafael Henrique',
    'author_email': 'cerbellus@gmsil.com',
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
