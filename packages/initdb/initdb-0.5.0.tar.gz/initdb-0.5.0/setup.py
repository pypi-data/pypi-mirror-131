# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['initdb']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'initdb',
    'version': '0.5.0',
    'description': 'Creates a user and database owned by that user',
    'long_description': None,
    'author': 'Eugen Ciur',
    'author_email': 'eugen@papermerge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
