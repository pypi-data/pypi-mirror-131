# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ericabrandao_puc_csv_converter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ericabrandao-puc-csv-converter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
