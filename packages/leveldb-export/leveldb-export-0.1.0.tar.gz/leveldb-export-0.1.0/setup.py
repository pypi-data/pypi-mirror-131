# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leveldb_export']

package_data = \
{'': ['*']}

install_requires = \
['appengine-python-standard>=0.3.1,<0.4.0',
 'google-crc32c>=1.1.2,<2.0.0',
 'protobuf>=3.15.8,<4.0.0']

setup_kwargs = {
    'name': 'leveldb-export',
    'version': '0.1.0',
    'description': 'Package to export documents from LevelDB export (for instance Firestore).',
    'long_description': None,
    'author': 'Joël Luijmes',
    'author_email': 'me@joell.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
