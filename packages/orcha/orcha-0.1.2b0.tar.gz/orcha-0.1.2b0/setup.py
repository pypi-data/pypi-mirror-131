# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orcha',
 'orcha.bin',
 'orcha.exceptions',
 'orcha.handlers',
 'orcha.interfaces',
 'orcha.lib',
 'orcha.plugins',
 'orcha.utils']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'python-daemon>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'orcha',
    'version': '0.1.2b0',
    'description': 'System handler and orchestrator of multiple environments',
    'long_description': None,
    'author': 'Javier Alonso',
    'author_email': 'jalonso@teldat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
