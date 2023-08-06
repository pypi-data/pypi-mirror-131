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
 'rich>=10.10.0,<11.0.0']

entry_points = \
{'console_scripts': ['pdh = pdh.main:main']}

setup_kwargs = {
    'name': 'pdh',
    'version': '0.2.3',
    'description': 'Pagerduty CLI for Humans',
    'long_description': '# PDH - PagerDuty CLI for humans\n\n![Build Image](https://github.com/mbovo/pdh/actions/workflows/build-image.yml/badge.svg)\n\nSee [docs](./docs)\n\n## Usage\n\nFirst of all you need to configure `pdh` to talk with PagerDuty APIs:\n\n```bash\npdh config\n```\n\nWill ask you for 3 settings:\n\n- `apiky` is the API key from the user\'s profile page on pagerduty\n- `email` your pagerduty email\n- `uid` the userID of your account (you can read it from the link address when clicking on "My Profile")\n\nSettings are persisted to `~/.config/pdh.yaml`\n\n### Listing incidents assigned to self\n\n```bash\npdh inc ls\n```\n\n### Auto ACK incoming incidents\n\nWatch for new incidents every 10s and automatically set them to Acknowledged\n\n```bash\npdh inc ls --watch --new --ack --timeout 10\n```\n\n### List all HIGH priority incidents periodically\n\nList incidents asssigned to all users every 5s\n\n```bash\npdh inc ls --high --everything --watch --timeout 5\n```\n\n### Resolve specific incidents\n\n```bash\npdh inc resolve INCID0001 INCID0024 INCID0023\n```\n\n## Resolve all incidents related to `Backups`\n\n```bash\npdh inc ls --resolve --regexp ".*Backup.*"\n```\n\n## Requirements\n\n- [Taskfile](https://taskfile.dev)\n- Python >=3.9\n- Docker\n\n## Contributing\n\nFirst of all you need to setup the dev environment, using Taskfile:\n\n```bash\ntask setup\n```\n\nThis will create a python virtualenv and install `pre-commit` and `poetry` in your system if you lack them.\n',
    'author': 'Manuel Bovo',
    'author_email': 'manuel.bovo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbovo/pdh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
