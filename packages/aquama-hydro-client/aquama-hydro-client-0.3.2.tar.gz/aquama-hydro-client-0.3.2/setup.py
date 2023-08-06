# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aquama_hydro_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'aquama-hydro-client',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Sébastien Gendre',
    'author_email': 'sgendre@aquama.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
