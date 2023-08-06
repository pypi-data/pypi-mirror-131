# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['research_utils',
 'research_utils.abc',
 'research_utils.argparse',
 'research_utils.argparse.actions',
 'research_utils.decorators',
 'research_utils.sqlite',
 'research_utils.sqlite.typing',
 'research_utils.torch']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'sqlite-utils>=3.6,<4.0']

setup_kwargs = {
    'name': 'research-utils',
    'version': '0.0.3',
    'description': 'some utils for my research',
    'long_description': '# research-utils\n[![Build](https://github.com/r08521610/research-utils/actions/workflows/package-build.yml/badge.svg)](https://github.com/r08521610/research-utils/actions/workflows/package-build.yml)\n[![Publish Package](https://github.com/r08521610/research-utils/actions/workflows/package-publish.yml/badge.svg?branch=main)](https://github.com/r08521610/research-utils/actions/workflows/package-publish.yml)\n[![PyPI version](https://badge.fury.io/py/research-utils.svg)](https://badge.fury.io/py/research-utils)\n',
    'author': 'Rainforest Cheng',
    'author_email': 'r08521610@ntu.edu.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://r08521610.github.io/research-utils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
