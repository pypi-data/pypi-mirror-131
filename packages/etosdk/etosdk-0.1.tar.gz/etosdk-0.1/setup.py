# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eto',
 'eto.connectors',
 'eto.internal',
 'eto.internal.api',
 'eto.internal.apis',
 'eto.internal.model',
 'eto.internal.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0',
 'rikai>=0.0.13,<0.0.14',
 'urllib3>=1.26.7,<2.0.0']

setup_kwargs = {
    'name': 'etosdk',
    'version': '0.1',
    'description': 'Eto Labs python SDK',
    'long_description': None,
    'author': 'Eto Devs',
    'author_email': 'devs@eto.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
