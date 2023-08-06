# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['veiled']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.1,<37.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['veil = veil.cli:run']}

setup_kwargs = {
    'name': 'veiled',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vasili Syrakis',
    'author_email': 'vsyrakis@atlassian.com',
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
