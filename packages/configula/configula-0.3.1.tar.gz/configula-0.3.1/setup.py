# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configula']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'configula',
    'version': '0.3.1',
    'description': 'Merges configuration from toml file and environment variables',
    'long_description': None,
    'author': 'Eugen Ciur',
    'author_email': 'eugen@papermerge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
