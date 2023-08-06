# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['watchmen_boot',
 'watchmen_boot.cache',
 'watchmen_boot.config',
 'watchmen_boot.constants',
 'watchmen_boot.constants.database',
 'watchmen_boot.guid',
 'watchmen_boot.guid.storage',
 'watchmen_boot.guid.storage.mongo',
 'watchmen_boot.guid.storage.mysql',
 'watchmen_boot.guid.storage.oracle',
 'watchmen_boot.logging',
 'watchmen_boot.model',
 'watchmen_boot.storage',
 'watchmen_boot.storage.model',
 'watchmen_boot.storage.mongo',
 'watchmen_boot.storage.mysql',
 'watchmen_boot.storage.oracle',
 'watchmen_boot.storage.utility',
 'watchmen_boot.utils']

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
 'python-dotenv>=0.19.2,<0.20.0',
 'python-json-logger>=2.0.2,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'watchmen-boot',
    'version': '15.2.2',
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
