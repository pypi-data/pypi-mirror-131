# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsw_xarray', 'gsw_xarray.tests']

package_data = \
{'': ['*']}

install_requires = \
['gsw>=3.4.0,<4.0.0', 'xarray>=0.20.2,<0.21.0']

setup_kwargs = {
    'name': 'gsw-xarray',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Barna',
    'author_email': 'abarna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
