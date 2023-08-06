# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['veiled']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'cryptography>=36.0.1,<37.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['veil = veiled.cli:run']}

setup_kwargs = {
    'name': 'veiled',
    'version': '0.2.1',
    'description': 'A very thin CLI wrapper around cryptography.fernet:Fernet',
    'long_description': 'veiled\n======\nA very thin CLI wrapper around `cryptography.fernet:Fernet` for symmetric encryption.\n\nI made this to use in CI things, so I can keep encrypted secrets in my git repositories,\nand have my build agents decrypt them using a centralized key.\n\n',
    'author': 'Vasili Syrakis',
    'author_email': 'cetanu@gmail.com',
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
