# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['svcmangle']

package_data = \
{'': ['*']}

install_requires = \
['pywin32==302']

entry_points = \
{'console_scripts': ['svcm = svcmangle.cli:main']}

setup_kwargs = {
    'name': 'svcmangle',
    'version': '0.1.7',
    'description': 'Query and control Windows services.',
    'long_description': 'Query and control Windows services.\n\nProvides a simple CLI for basic service management.\n',
    'author': 'dustin',
    'author_email': 'dustin.wyatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmwyatt/svcmangle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
