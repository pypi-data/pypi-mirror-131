# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covcheck', 'covcheck._cli', 'covcheck._parsing']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'mypy>=0.920,<0.921',
 'pylint>=2.12.2,<3.0.0',
 'pyproject-flake8>=0.0.1-alpha.2,<0.0.2',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-forked>=1.4.0,<2.0.0',
 'pytest-xdist>=2.5.0,<3.0.0',
 'pytest>=6.2.5,<7.0.0',
 'types-setuptools>=57.4.4,<58.0.0',
 'yapf>=0.31.0,<0.32.0']

entry_points = \
{'console_scripts': ['covcheck = covcheck._cli.main:run']}

setup_kwargs = {
    'name': 'covcheck',
    'version': '0.1.0',
    'description': 'Code coverage validation',
    'long_description': '# covcheck\n\nCommand-line tool for code coverage validation.\n\n`covcheck` is intented to be used in conjunction with [coverage.py](https://coverage.readthedocs.io/), which already has support for `pytest`, `unittest`, and `nosetest`. All you have to do is point `covcheck` to the `coverage.xml` file produced when running your tests.\n\n## Installation\n\n```bash\n$ pip install coverage\n$ pip install covcheck\n```\n\n## Usage\n\n### 1. Produce a `coverage.xml` file while running your tests:\n\n```bash\n# pytest\n$ coverage run --branch -m pytest ...\n$ coverage xml\n\n# unittest\n$ coverage run --branch -m unittest ...\n$ coverage xml\n\n# nosetest\n$ coverage run --branch -m nose ...\n$ coverage xml\n```\n\n### 2. Validate that line and branch coverage meet the provided thresholds:\n\n```bash\n$ covcheck coverage.xml --line 96 --branch --84\n```\n',
    'author': 'Hume AI Dev',
    'author_email': 'dev@hume.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HumeAI/covcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
