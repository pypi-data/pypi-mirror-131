# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack_migrate']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.7.5,<2.0.0', 'fastack>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'fastack-migrate',
    'version': '0.1.0',
    'description': 'WIP',
    'long_description': None,
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
