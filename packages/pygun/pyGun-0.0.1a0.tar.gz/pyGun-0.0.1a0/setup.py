# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygun']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pygun',
    'version': '0.0.1a0',
    'description': 'Gun',
    'long_description': None,
    'author': 'n2k3',
    'author_email': 'n2k3@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
