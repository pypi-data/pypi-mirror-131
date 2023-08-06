# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['floxcore', 'floxcore.utils']

package_data = \
{'': ['*']}

install_requires = \
['anyconfig>=0.10,<0.11',
 'click>=7.1,<8.0',
 'lazy-load>=0.8.2,<0.9.0',
 'loguru>=0.5,<0.6',
 'plumbum>=1.7,<2.0',
 'python-box>=5.3,<6.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.58,<5.0',
 'wasabi>=0.9,<0.10']

setup_kwargs = {
    'name': 'flox-core',
    'version': '0.1.1',
    'description': 'Core library for flox',
    'long_description': None,
    'author': 'Michal Przytulski',
    'author_email': 'michal@przytulski.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
