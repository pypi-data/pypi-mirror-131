# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wolproxypycli']

package_data = \
{'': ['*']}

install_requires = \
['pretty-errors>=1.2.25,<2.0.0',
 'rich>=10.16.1,<11.0.0',
 'typer>=0.4.0,<0.5.0',
 'wakeonlan>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['wolproxypycli = wolproxypycli.main:run']}

setup_kwargs = {
    'name': 'wolproxypycli',
    'version': '0.1.0',
    'description': 'A PyPI module and Typer (CLI) app for sending Wake-On-LAN packets',
    'long_description': None,
    'author': 'Fabio Calefato',
    'author_email': 'fabio.calefato@uniba.it',
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
