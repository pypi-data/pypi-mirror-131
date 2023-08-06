# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['realtime']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses>=0.6,<0.7',
 'python-dateutil>=2.8.1,<3.0.0',
 'websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'realtime',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'None',
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
