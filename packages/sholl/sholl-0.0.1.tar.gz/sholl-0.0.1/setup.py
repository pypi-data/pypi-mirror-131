# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sholl', 'sholl.test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sholl',
    'version': '0.0.1',
    'description': 'Generate Hombrew formulas for your python projects',
    'long_description': None,
    'author': 'jeremynac',
    'author_email': 'jeremynac@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
