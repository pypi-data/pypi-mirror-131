# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['watchmen',
 'watchmen.boot',
 'watchmen.boot.cache',
 'watchmen.boot.config',
 'watchmen.boot.constants',
 'watchmen.boot.constants.database',
 'watchmen.boot.guid',
 'watchmen.boot.guid.storage',
 'watchmen.boot.guid.storage.mongo',
 'watchmen.boot.guid.storage.mysql',
 'watchmen.boot.guid.storage.oracle',
 'watchmen.boot.logging',
 'watchmen.boot.model',
 'watchmen.boot.storage',
 'watchmen.boot.storage.model',
 'watchmen.boot.storage.mongo',
 'watchmen.boot.storage.mysql',
 'watchmen.boot.storage.oracle',
 'watchmen.boot.storage.utility',
 'watchmen.boot.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.27,<2.0.0',
 'arrow>=1.1.0,<2.0.0',
 'cacheout>=0.13.1,<0.14.0',
 'cx-Oracle>=8.2.1,<9.0.0',
 'mysqlclient>=2.1.0,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pymongo>=3.11.4,<4.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'watchmen-boot',
    'version': '15.1.9',
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
