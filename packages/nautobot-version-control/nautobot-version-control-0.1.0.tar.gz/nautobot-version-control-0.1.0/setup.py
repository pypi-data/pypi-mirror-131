# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_version_control',
 'nautobot_version_control.api',
 'nautobot_version_control.dynamic',
 'nautobot_version_control.graphql',
 'nautobot_version_control.management.commands',
 'nautobot_version_control.migrations']

package_data = \
{'': ['*'],
 'nautobot_version_control': ['templates/nautobot_version_control/*',
                              'templates/nautobot_version_control/pull_request/*']}

install_requires = \
['mysqlclient>=2.0.3,<3.0.0', 'nautobot>=1.2.0b1,<1.3.0']

setup_kwargs = {
    'name': 'nautobot-version-control',
    'version': '0.1.0',
    'description': 'Nautobot Version Control',
    'long_description': None,
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
