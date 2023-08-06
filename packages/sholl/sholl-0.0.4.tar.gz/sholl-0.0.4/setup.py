# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sholl']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sholl = sholl.sholl:main']}

setup_kwargs = {
    'name': 'sholl',
    'version': '0.0.4',
    'description': 'Generate Hombrew formulas for your python projects',
    'long_description': None,
    'author': 'jeremynac',
    'author_email': 'jeremynac@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
