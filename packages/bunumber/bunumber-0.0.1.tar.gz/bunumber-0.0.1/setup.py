# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bunumber']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bunumber',
    'version': '0.0.1',
    'description': 'number by digit and letter',
    'long_description': '\ufeffa simple number module',
    'author': 'ahamidp',
    'author_email': 'ahamidp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
