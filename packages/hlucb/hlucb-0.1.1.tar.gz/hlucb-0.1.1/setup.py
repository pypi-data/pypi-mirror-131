# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlucb', 'hlucb._cli', 'hlucb._ranking']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hlucb = hlucb._cli.main:run']}

setup_kwargs = {
    'name': 'hlucb',
    'version': '0.1.1',
    'description': 'Hamming-LUCB algorithm implementation',
    'long_description': '# Hamming-LUCB\n\nThis package is an implementation of the paper [Approximate ranking from pairwise comparisons](http://proceedings.mlr.press/v84/heckel18a.html).\n\n`Heckel, R., Simchowitz, M., Ramchandran, K., & Wainwright, M. (2018, March). Approximate ranking from pairwise comparisons. In International Conference on Artificial Intelligence and Statistics (pp. 1057-1066). PMLR.`¡\n',
    'author': 'Chris Gregory',
    'author_email': 'christopher.b.gregory@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gregorybchris/hlucb',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
