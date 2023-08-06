# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiogh']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'aiogh',
    'version': '0.1.2',
    'description': '',
    'long_description': '# aiogh - an async GitHub API\n\nProject TODO\n',
    'author': 'Kevin Duff',
    'author_email': 'kevinkelduff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/k2bd/aiogh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
