# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gbstats', 'gbstats.bayesian', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'toml>=0.10.2,<0.11.0'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'gbstats',
    'version': '0.2.1',
    'description': 'Stats engine for GrowthBook, the open source A/B testing platform.',
    'long_description': '# GrowthBook Stats\n\nThe stats engine for GrowthBook, the open source A/B testing platform.\n\n## Installation\n\n```\npip install gbstats\n```\n\n## Usage\n\n```python\nimport gbstats\n```\n',
    'author': 'Jeremy Dorn',
    'author_email': 'jeremy@growthbook.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/growthbook/growthbook/packages/stats',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
