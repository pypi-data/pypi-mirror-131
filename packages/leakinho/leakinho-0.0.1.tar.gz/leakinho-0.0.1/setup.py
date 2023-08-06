# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leakinho']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'leakinho',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Thúlio Costa',
    'author_email': 'thulio@thuliocosta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
