# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdh']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'pdpyras>=4.3.0,<5.0.0',
 'rich>=10.10.0,<11.0.0',
 'textual>=0.1.12,<0.2.0']

entry_points = \
{'console_scripts': ['pdh = pdh.main:main']}

setup_kwargs = {
    'name': 'pdh',
    'version': '0.2.1',
    'description': 'Pagerduty CLI for Humans',
    'long_description': None,
    'author': 'Manuel Bovo',
    'author_email': 'manuel.bovo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
