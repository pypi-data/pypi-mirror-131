# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioherepy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'aioherepy',
    'version': '0.1.0',
    'description': 'Asynchronous Python library that provides a simple interface to the HERE APIs.',
    'long_description': '# aioherepy\nAsynchronous Python library that provides a simple interface to the HERE APIs.\n',
    'author': 'Abdullah Selek',
    'author_email': 'abdullahselek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abdullahselek/aioherepy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
