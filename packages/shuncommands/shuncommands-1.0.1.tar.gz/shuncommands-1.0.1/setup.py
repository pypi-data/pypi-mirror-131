# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'gitignore-parser>=0.0.8,<0.0.9',
 'pikepdf>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['pdftool = src.pdftool:ctx', 'rmtmp = src.rmtmp:ctx']}

setup_kwargs = {
    'name': 'shuncommands',
    'version': '1.0.1',
    'description': 'my usefull commands',
    'long_description': None,
    'author': 'KAWAI Shun',
    'author_email': 'shun@osstech.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
