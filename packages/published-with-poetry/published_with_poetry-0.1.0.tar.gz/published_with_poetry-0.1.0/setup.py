# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['published_with_poetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'published-with-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Hosam Almoghraby',
    'author_email': 'hosam.moghraby@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
