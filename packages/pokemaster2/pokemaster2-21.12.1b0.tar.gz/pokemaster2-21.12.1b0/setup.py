# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pokemaster2', 'pokemaster2.db']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'click>=8.0.3,<9.0.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'loguru>=0.5.3,<0.6.0',
 'peewee>=3.14.8,<4.0.0']

entry_points = \
{'console_scripts': ['pokemaster2 = pokemaster2.cli:main']}

setup_kwargs = {
    'name': 'pokemaster2',
    'version': '21.12.1b0',
    'description': 'Get Real, Living™ Pokémon in Python',
    'long_description': '\n# Pokemaster2\n\n\n<div align="center">\n\n[![PyPI - Version](https://img.shields.io/pypi/v/pokemaster2.svg)](https://pypi.python.org/pypi/pokemaster2)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pokemaster2.svg)](https://pypi.python.org/pypi/pokemaster2)\n[![Tests](https://github.com/kipyin/pokemaster2/workflows/tests/badge.svg)](https://github.com/kipyin/pokemaster2/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/kipyin/pokemaster2/branch/main/graph/badge.svg)](https://codecov.io/gh/kipyin/pokemaster2)\n[![Read the Docs](https://readthedocs.org/projects/pokemaster2/badge/)](https://pokemaster2.readthedocs.io/)\n[![PyPI - License](https://img.shields.io/pypi/l/pokemaster2.svg)](https://pypi.python.org/pypi/pokemaster2)\n\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)\n\n</div>\n\n\nGet Real, Living™ Pokémon in Python\n\n\n* GitHub repo: <https://github.com/kipyin/pokemaster2.git>\n* Documentation: <https://pokemaster2.readthedocs.io>\n* Free software: MIT\n\n\n## Features\n\nCurrently, there is not much you can do with `pokemaster`, but more features are actively being added!\n\n* Load pokemon data from csv to a sqlite database.\n\n## Quickstart\n\nTODO\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n',
    'author': 'Kip Yin',
    'author_email': '28321392+kipyin@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kipyin/pokemaster2',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
