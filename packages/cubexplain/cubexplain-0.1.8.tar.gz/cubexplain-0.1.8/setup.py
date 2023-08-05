# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cubexplain']

package_data = \
{'': ['*']}

install_requires = \
['atoti[sql]',
 'certifi',
 'pandas',
 'requests>=2.26.0,<3.0.0',
 'watchdog>=2.1.6,<3.0.0']

entry_points = \
{'console_scripts': ['cubexplain = cubexplain.commande_line:main']}

setup_kwargs = {
    'name': 'cubexplain',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
