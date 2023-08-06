# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['obelist',
 'obelist.cli',
 'obelist.cli.cmds',
 'obelist.core',
 'obelist.core.handlers']

package_data = \
{'': ['*'], 'obelist': ['data/schemas/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'charset-normalizer>=2.0.7,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'inflection>=0.5.1,<0.6.0',
 'lxml>=4.6.4,<5.0.0',
 'natsort>=8.0.0,<9.0.0',
 'pastel>=0.2.1,<0.3.0',
 'pyjq>=2.5.2,<3.0.0',
 'pyroma>=3.2,<4.0',
 'sh>=1.14.2,<2.0.0',
 'urlextract>=1.4.0,<2.0.0',
 'vulture>=2.3,<3.0',
 'wrapt>=1.13.3,<2.0.0']

entry_points = \
{'console_scripts': ['obelist = obelist.cli.cmds:main']}

setup_kwargs = {
    'name': 'obelist',
    'version': '0.0.0a2',
    'description': 'A CLI tool for generating standard annotations for linting tools, tests, and so on (including support for GitHub Actions)',
    'long_description': '# Obelist\n\n_A CLI tool for generating standard annotations for linting tools, tests, and so on (including support for GitHub Actions)_\n\n[![Build][action-build-img]][action-build]\n\n**Table of contents:**\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [Appendix](#appendix)\n  - [Etymology](#etymology)\n\n## Installation\n\nThe [obelist][pypi-obelist] package is published to [PyPI][pypi].\n\nBecause Obelist is primarily designed to be used as a CLI tool, we recommend that you install the package in an isolated virtual environment using [pipx][pipx], like so:\n\n```console\n$ pipx install obelist\n```\n\nHowever, if you want to install Obelist as a library, you can also install the package using [pip][pip]:\n\n```console\n$ pip install obelist\n```\n\n## Usage\n\nFor basic usage information, run:\n\n```console\n$ obelist\n```\n\nFor more detailed help, run:\n\n```console\n$ obelist --help\n```\n\n## Appendix\n\n### Etymology\n\nThe [obelus] is a typographical mark used to "indicate erroneous or dubious content." The _Oxford English Dictionary_ (OED) defines [obelism] as the "action or practice of marking something as spurious."\n\nObelist, then, serves as both a verbal noun and a play on words: the program\'s output is, essentially, _a list of obeluses_.\n\n[action-build-img]: https://github.com/nomiro/obelist/actions/workflows/build.yaml/badge.svg\n[action-build]: https://github.com/nomiro/obelist/actions/workflows/build.yaml\n[obelism]: https://en.wikipedia.org/wiki/Obelism\n[obelus]: https://en.wikipedia.org/wiki/Obelus\n[pip]: https://pip.pypa.io/en/stable/\n[pipx]: https://pypa.github.io/pipx/\n[pypi-obelist]: https://pypi.org/project/obelist\n[pypi]: https://pypi.org/\n',
    'author': 'Naomi Rose',
    'author_email': '23469+nomiro@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nomiro/obelist',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
