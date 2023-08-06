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
    'version': '0.1.1',
    'description': 'Package to export documents from LevelDB export (for instance Firestore).',
    'long_description': '# LevelDB Export\n\nThis package allows to export documents from a LevelDB file. For instance it can be used to extract documents from a previously created Firestore export. Note, this package is a fork from [labbots/firestore-export-json](https://github.com/labbots/firestore-export-json). This fork is different in:\n\n1. Makes it an installable package. The original is designed to run as a script.\n2. Solves some parsing issues regarding arrays.\n\n\n## Installation\n\nInstall the package from pypi.\n\n```bash\npip install leveldb-export\n```\n\n## Example\n\nUse the function `parse_leveldb_documents` to parse documents from a LevelDB / Firestore dump. As input either:\n\n- Use path to file\n- Use open file handle\n\nFor example\n\n```python\n>>> from leveldb_export import parse_leveldb_documents\n>>> docs = list(parse_leveldb_documents("./firestore/export-0"))\n>>> print(f"Got {len(docs)} documents")\nGot 288 documents\n```\n',
    'author': 'Joël Luijmes',
    'author_email': 'me@joell.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joelluijmes/leveldb-export',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
