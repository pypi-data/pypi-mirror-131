# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodm']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'pymongo>=3.12.0,<4.0.0']

setup_kwargs = {
    'name': 'mongodm',
    'version': '0.1.5b0',
    'description': 'Simple ODM for MongoDB',
    'long_description': '<h1 align="center">MongoDM</h1>\n\n<p align="center">\n    <em>MongoDM is simple ODM for MongoDB based on Pymongo & Pydantic</em>\n</p>\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n```bash\npip install mongodm\n```\n',
    'author': 'Deni',
    'author_email': 'azureswastika@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azureswastika/mongodm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
