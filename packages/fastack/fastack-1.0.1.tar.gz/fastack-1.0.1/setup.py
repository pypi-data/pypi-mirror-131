# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack',
 'fastack.plugins',
 'fastack.plugins.aioredis',
 'fastack.plugins.mongoengine',
 'fastack.plugins.sqlmodel',
 'fastack.templates.app',
 'fastack.templates.app.commands',
 'fastack.templates.app.controllers',
 'fastack.templates.app.controllers.dummy',
 'fastack.templates.app.plugins',
 'fastack.templates.app.settings']

package_data = \
{'': ['*'], 'fastack': ['templates/*']}

install_requires = \
['fastapi>=0.70.1,<0.71.0',
 'typer[all]>=0.4.0,<0.5.0',
 'uvicorn>=0.16.0,<0.17.0']

extras_require = \
{'nosql': ['mongoengine>=0.23.1,<0.24.0'],
 'redis': ['aioredis>=2.0.0,<3.0.0'],
 'sql': ['sqlmodel>=0.0.5,<0.0.6', 'alembic>=1.7.5,<2.0.0']}

entry_points = \
{'console_scripts': ['fastack = fastack.cli:fastack']}

setup_kwargs = {
    'name': 'fastack',
    'version': '1.0.1',
    'description': 'Fastack is a blah blah blah framework!!!',
    'long_description': None,
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
