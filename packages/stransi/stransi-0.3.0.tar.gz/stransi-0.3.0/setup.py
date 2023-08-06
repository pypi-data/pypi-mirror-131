# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stransi']

package_data = \
{'': ['*']}

install_requires = \
['ochre>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'stransi',
    'version': '0.3.0',
    'description': 'A lightweight parser for ANSI escape sequences',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/stransi)](https://pypi.org/project/stransi/)\n[![Python package](https://github.com/getcuia/stransi/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/stransi/actions/workflows/python-package.yml)\n[![PyPI - License](https://img.shields.io/pypi/l/stransi)](https://github.com/getcuia/stransi/blob/main/LICENSE)\n\n# [stransi](https://github.com/getcuia/stransi#readme) 🖍️\n\n<div align="center">\n    <img class="hero" src="https://github.com/getcuia/stransi/raw/main/banner.jpg" alt="stransi" width="33%" />\n</div>\n\n> I see a `\\033[1;31m`red`\\033[;39m` door, and I want it painted\n> `\\033[1;30m`black`\\033[;39m`.\n\nstransi is a lightweight parser for\n[ANSI escape code sequences](https://en.wikipedia.org/wiki/ANSI_escape_code). It\nimplements a string-like type that is aware of its own ANSI escape sequences,\nand can be used to parse most of the common escape sequences used in terminal\noutput manipulation.\n\n## Features\n\n-   ✨ [Good support of ANSI escape sequences](FEATURES.md)\n-   🎨 Focus on coloring and styling\n-   🛡️ Unsupported `CSI` escape sequences are emitted as tokens\n-   🏜️ Only one dependency: [ochre](https://github.com/getcuia/ochre)\n-   🐍 Python 3.8+\n\n## Installation\n\n```console\n$ pip install stransi\n```\n\n## Usage\n\n```python\nIn [1]: from stransi import Ansi\n\nIn [2]: text = Ansi(\n   ...:     "I see a \\033[1;31mred\\033[;39m door, "\n   ...:     "and I want it painted \\033[1;30mblack\\033[;39m"\n   ...: )\n\nIn [3]: list(text.escapes())\nOut[3]:\n[\'I see a \',\n Escape(\'\\x1b[1;31m\'),\n \'red\',\n Escape(\'\\x1b[;39m\'),\n \' door, and I want it painted \',\n Escape(\'\\x1b[1;30m\'),\n \'black\',\n Escape(\'\\x1b[;39m\')]\n\nIn [4]: list(text.instructions())\nOut[4]:\n[\'I see a \',\n SetAttribute(attribute=<Attribute.BOLD: 1>),\n SetColor(role=<ColorRole.FOREGROUND: 30>, color=Ansi256(1)),\n \'red\',\n SetAttribute(attribute=<Attribute.NORMAL: 0>),\n SetColor(role=<ColorRole.FOREGROUND: 30>, color=None),\n \' door, and I want it painted \',\n SetAttribute(attribute=<Attribute.BOLD: 1>),\n SetColor(role=<ColorRole.FOREGROUND: 30>, color=Ansi256(0)),\n \'black\',\n SetAttribute(attribute=<Attribute.NORMAL: 0>),\n SetColor(role=<ColorRole.FOREGROUND: 30>, color=None)]\n```\n\n## Credits\n\n[Photo](https://github.com/getcuia/stransi/raw/main/banner.jpg) by\n[Tien Vu Ngoc](https://unsplash.com/@tienvn3012?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)\non\n[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).\n',
    'author': 'Felipe S. S. Schneider',
    'author_email': 'schneider.felipe@posgrad.ufsc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/getcuia/stransi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
