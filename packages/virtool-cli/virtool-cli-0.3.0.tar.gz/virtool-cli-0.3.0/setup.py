# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtool_cli']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>0.5.0',
 'aiohttp==3.6.2',
 'aiojobs==0.2.2',
 'arrow==0.16.0',
 'biopython>=1.79,<2.0',
 'click>=8.0.3,<9.0.0',
 'pytest-asyncio>=0.16.0,<0.17.0',
 'pytest-mock>=3.6.1,<4.0.0',
 'rich>=7.0.0,<8.0.0']

entry_points = \
{'console_scripts': ['virtool = virtool_cli.run:cli']}

setup_kwargs = {
    'name': 'virtool-cli',
    'version': '0.3.0',
    'description': 'CLI Tool for working with Virtool data',
    'long_description': None,
    'author': 'Ian Boyes',
    'author_email': 'igboyes@gmail.com',
    'maintainer': 'Ian Boyes',
    'maintainer_email': 'igboyes@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
