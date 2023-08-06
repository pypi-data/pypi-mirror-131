# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beebole',
 'beebole.interfaces',
 'beebole.interfaces.entities',
 'beebole.interfaces.responses',
 'beebole.services']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'beebole',
    'version': '1.0.0',
    'description': 'A python wrapper around the beebole API',
    'long_description': None,
    'author': 'Dogeek',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
