# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fliswarm']

package_data = \
{'': ['*'], 'fliswarm': ['etc/*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'daemonocle>=1.0.2,<2.0.0',
 'docker>=5.0.0,<6.0.0',
 'sdss-clu>=1.0.0,<2.0.0',
 'sdsstools>=0.4.0']

entry_points = \
{'console_scripts': ['fliswarm = fliswarm.__main__:main']}

setup_kwargs = {
    'name': 'sdss-fliswarm',
    'version': '0.2.0',
    'description': 'A tool to create and manage Docker instances of flicamera',
    'long_description': "# fliswarm\n\n![Versions](https://img.shields.io/badge/python->3.8-blue)\n[![Documentation Status](https://readthedocs.org/projects/sdss-fliswarm/badge/?version=latest)](https://sdss-fliswarm.readthedocs.io/en/latest/?badge=latest)\n[![Build](https://img.shields.io/github/workflow/status/sdss/fliswarm/Test)](https://github.com/sdss/fliswarm/actions)\n[![codecov](https://codecov.io/gh/sdss/fliswarm/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/fliswarm)\n\nA tool to create and manage Docker instances of [flicamera](https://github.org/sdss/flicamera).\n\n## Installation\n\nYou can install ``fliswarm`` by doing\n\n```console\npip install sdss-fliswarm\n```\n\nTo build from source, use\n\n```console\ngit clone git@github.com:sdss/fliswarm\ncd fliswarm\npip install .\n```\n\n## Development\n\n`fliswarm` uses [poetry](http://poetry.eustace.io/) for dependency management and packaging. To work with an editable install it's recommended that you setup `poetry` and install `fliswarm` in a virtual environment by doing\n\n```console\npoetry install\n```\n\nPip does not support editable installs with PEP-517 yet. That means that running `pip install -e .` will fail because `poetry` doesn't use a `setup.py` file. As a workaround, you can use the `create_setup.py` file to generate a temporary `setup.py` file. To install `fliswarm` in editable mode without `poetry`, do\n\n```console\npip install poetry\npython create_setup.py\npip install -e .\n```\n",
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdss/fliswarm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
