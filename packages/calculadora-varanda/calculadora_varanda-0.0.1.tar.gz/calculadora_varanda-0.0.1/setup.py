# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calculadora_varanda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'calculadora-varanda',
    'version': '0.0.1',
    'description': 'Está é uma calculadora mantida pela Codaqui.',
    'long_description': None,
    'author': 'Pedro Varanda',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
