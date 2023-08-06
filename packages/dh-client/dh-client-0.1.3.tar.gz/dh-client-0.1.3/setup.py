# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dh_client', 'dh_client.entities']

package_data = \
{'': ['*']}

install_requires = \
['acryl-datahub>=0.8.17,<0.9.0']

setup_kwargs = {
    'name': 'dh-client',
    'version': '0.1.3',
    'description': 'A high level python client for datahub.',
    'long_description': None,
    'author': 'Netdata Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
