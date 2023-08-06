# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'gitignore-parser>=0.0.8,<0.0.9', 'pikepdf>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['pdftool = src.pdftool:ctx', 'rmtmp = src.rmtmp:ctx']}

setup_kwargs = {
    'name': 'shuncommands',
    'version': '1.0.2',
    'description': 'mypaceshun usefull commands',
    'long_description': '# shuncommands\nmy usefull commands\n\n# install\n\n```\n$ pip install --user git+https://github.com/mypaceshun/shuncommands\n```\n',
    'author': 'KAWAI Shun',
    'author_email': 'mypaceshun@gmail.com',
    'maintainer': 'KAWAI Shun',
    'maintainer_email': 'mypaceshun@gmail.com',
    'url': 'https://github.com/mypaceshun/shuncommands',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
