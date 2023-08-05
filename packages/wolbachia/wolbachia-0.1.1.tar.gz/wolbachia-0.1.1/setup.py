# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wolbachia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wolbachia',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'cachora',
    'author_email': 'cachora@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
