# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_cea_googlesheet', 'tap_cea_googlesheet.tests']

package_data = \
{'': ['*'], 'tap_cea_googlesheet': ['schemas/*']}

install_requires = \
['google-api-python-client==2.31.0',
 'google-auth-oauthlib==0.4.6',
 'google-auth>=2.3.3,<3.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pylint>=2.12.2,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.3.16,<0.4.0']

entry_points = \
{'console_scripts': ['tap-cea-googlesheet = '
                     'tap_cea_googlesheet.tap:Tapgooglesheet.cli']}

setup_kwargs = {
    'name': 'tap-cea-googlesheet',
    'version': '0.0.3',
    'description': '`tap-cea-googlesheet` is a Singer tap for googlesheet, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Basil',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
