# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cibercca']

package_data = \
{'': ['*'], 'cibercca': ['inventory/*']}

install_requires = \
['PyYAML==6.0',
 'hvac==0.11.2',
 'napalm==3.3.1',
 'nornir==3.2.0',
 'openpyxl==3.0.9',
 'pandas==1.3.4',
 'tabulate==0.8.9',
 'tqdm==4.62.3',
 'ttp==0.8.1',
 'typer==0.4.0']

entry_points = \
{'console_scripts': ['ciberc-ca = cibercca.main:main']}

setup_kwargs = {
    'name': 'cibercca',
    'version': '0.1.0',
    'description': 'CiberC Code Automation - reports excel and json formats',
    'long_description': None,
    'author': 'Rafael Garcia Sagastume',
    'author_email': 'rafael.garcia@ciberc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
