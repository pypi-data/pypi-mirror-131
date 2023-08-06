# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_planetscale', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>3.0.0,<4.1', 'mysqlclient>=2.1.0,<3.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0',
         'ipython'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'django-planetscale',
    'version': '0.2.3',
    'description': 'A Django database backend for PlanetScale.',
    'long_description': '# Django PlanetScale\n\n\n[![pypi](https://img.shields.io/pypi/v/django-planetscale.svg)](https://pypi.org/project/django-planetscale/)\n[![python](https://img.shields.io/pypi/pyversions/django-planetscale.svg)](https://pypi.org/project/django-planetscale/)\n[![Build Status](https://github.com/birdcar/django-planetscale/actions/workflows/dev.yml/badge.svg)](https://github.com/birdcar/django-planetscale/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/birdcar/django-planetscale/branch/main/graphs/badge.svg)](https://codecov.io/github/birdcar/django-planetscale)\n\n\n\nA Django database backend for PlanetScale\n\n* GitHub: <https://github.com/birdcar/django-planetscale>\n* PyPI: <https://pypi.org/project/django-planetscale/>\n* Free software: GPL-3.0-only\n\n## Features\n\n* Enables you to use PlanetScale with your Django app\n* Avoids you having to rewrite your model code to set the kwarg `db_constraint=False` on every relationship you model.\n* Subclasses the existing MySQL database backend using the documented process, ensuring compatibility with all versions of Django.\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Nick Cannariato',
    'author_email': 'devrel@birdcar.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/birdcar/django-planetscale',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
