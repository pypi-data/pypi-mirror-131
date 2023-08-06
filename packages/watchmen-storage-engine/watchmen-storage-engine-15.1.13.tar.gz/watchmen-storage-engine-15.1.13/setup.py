# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage',
 'storage.common',
 'storage.common.utils',
 'storage.mongo',
 'storage.mysql',
 'storage.oracle',
 'storage.storage',
 'storage.storage.exception',
 'storage.storage.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.27,<2.0.0',
 'arrow>=1.1.0,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'watchmen-boot>=15.1.11,<16.0.0']

setup_kwargs = {
    'name': 'watchmen-storage-engine',
    'version': '15.1.13',
    'description': '',
    'long_description': None,
    'author': 'luke0623',
    'author_email': 'luke0623@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
