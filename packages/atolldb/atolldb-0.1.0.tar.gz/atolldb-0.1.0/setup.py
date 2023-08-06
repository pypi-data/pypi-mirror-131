# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atolldb', 'atolldb.parsing']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'biopython>=1.79,<2.0',
 'cachetools>=4.2.4,<5.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'loguru>=0.5.3,<0.6.0',
 'lxml>=4.7.1,<5.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'numpy>=1.21.5,<2.0.0',
 'path>=16.2.0,<17.0.0',
 'peewee>=3.14.8,<4.0.0',
 'plumbum>=1.7.1,<2.0.0',
 'python-slugify>=5.0.2,<6.0.0',
 'requests>=2.26.0,<3.0.0',
 'retrying>=1.3.3,<2.0.0',
 'tables>=3.6.1,<4.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'uplink>=0.9.4,<0.10.0',
 'watchdog>=2.1.6,<3.0.0']

setup_kwargs = {
    'name': 'atolldb',
    'version': '0.1.0',
    'description': 'Atoll is a project that aim to gather heterogeneous sources of genomic island (GI) sequences and return them in an unified interface.',
    'long_description': None,
    'author': 'A.Bioteau, N. Cellier',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
