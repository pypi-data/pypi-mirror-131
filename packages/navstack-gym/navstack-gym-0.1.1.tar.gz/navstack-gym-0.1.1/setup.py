# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['navstack_gym']

package_data = \
{'': ['*']}

install_requires = \
['descartes>=1.1.0,<2.0.0',
 'gym>=0.21.0,<0.22.0',
 'matplotlib>=3.5.0,<4.0.0',
 'nav-sim-modules>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'navstack-gym',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Reona Sato',
    'author_email': 'www.shinderu.www@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
