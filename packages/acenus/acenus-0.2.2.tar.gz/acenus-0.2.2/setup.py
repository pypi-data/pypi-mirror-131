# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acenus']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'acenus',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'tsarbas',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
