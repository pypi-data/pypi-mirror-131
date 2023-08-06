# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shuncommands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'gitignore-parser>=0.0.8,<0.0.9', 'pikepdf>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['pdftool = shuncommands.pdftool:ctx',
                     'rmtmp = shuncommands.rmtmp:ctx']}

setup_kwargs = {
    'name': 'shuncommands',
    'version': '1.0.5',
    'description': 'mypaceshun usefull commands',
    'long_description': '[![shuncommand Actions](https://github.com/mypaceshun/shuncommands/actions/workflows/main.yml/badge.svg)](https://github.com/mypaceshun/shuncommands/actions/workflows/main.yml)\n# shuncommands\n\nmy usefull commands\n\n\n# install\n\n```\n$ pip install shuncommands\n```\n\n# install commands\n\n  * rmtmp\n  * pdftool\n\n# rmtmp Usage\n\n```\nUsage: rmtmp [OPTIONS] TARGETDIR\n\n  tmpディレクトリの中身お掃除君\n\n  <TARGETDIR>で指定されたディレクトリの中身をせっせとお掃除してくれるかわいいやつ。\n  自分がよく ~/document/tmp/ とか雑にディレクトリ作ってしまうので、それのお掃除用に生まれた\n\n  <TARGETDIR>/.rmtmpignore のファイルに gitignore と同様の書式でファイルを指定することで、\n  削除対象から明示的に外すことができる。\n\nOptions:\n  -q, --quiet              quiet output\n  --dry-run\n  -d, --day INTEGER RANGE  削除対象となる期日  [default: 3; x>=0]\n  --help                   Show this message and exit.\n```\n\n# pdftool usage\n\n```\nUsage: pdftool [OPTIONS] COMMAND [ARGS]...\n\n  PDF file をあれやこれやしたいがためのコマンド\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  unlock  パスワード付きPDFファイルを、パスワードなしPDFファイルにコピーする\n```\n',
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
