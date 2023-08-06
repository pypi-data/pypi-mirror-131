# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cicd_example']

package_data = \
{'': ['*']}

install_requires = \
['pytest==6.1.2', 'requests[security]==2.25.1']

setup_kwargs = {
    'name': 'ozo',
    'version': '0.0.1',
    'description': ' ',
    'long_description': None,
    'author': 'Erik Li',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
