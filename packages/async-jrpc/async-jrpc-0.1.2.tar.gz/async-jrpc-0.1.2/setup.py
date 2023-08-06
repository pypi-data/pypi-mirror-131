# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpc']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'async-jrpc',
    'version': '0.1.2',
    'description': 'JSON RPC via HTTP client, backed with httpx.',
    'long_description': None,
    'author': 'yallxe',
    'author_email': '82591945+yallxe@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
