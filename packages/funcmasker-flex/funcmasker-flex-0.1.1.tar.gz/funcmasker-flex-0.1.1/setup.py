# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funcmasker_flex']

package_data = \
{'': ['*']}

install_requires = \
['batchgenerators==0.21',
 'matplotlib>=3.5.1,<4.0.0',
 'nnunet-inference-on-cpu-and-gpu==1.6.6',
 'snakebids==0.4.0',
 'snakemake>=6.12.3,<7.0.0']

entry_points = \
{'console_scripts': ['funcmasker-flex = funcmasker_flex.run:main']}

setup_kwargs = {
    'name': 'funcmasker-flex',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Ali Khan',
    'author_email': 'alik@robarts.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
