# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['assert_typecheck']

package_data = \
{'': ['*']}

install_requires = \
['ast-compat>=0.10.1,<0.11.0', 'mypy>=0.800']

setup_kwargs = {
    'name': 'assert-typecheck',
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
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
