# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_export_openapi']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pydantic>=1.8.2,<2.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['fastapi-export-openapi = '
                     'fastapi_export_openapi.main:app']}

setup_kwargs = {
    'name': 'fastapi-export-openapi',
    'version': '0.1.2',
    'description': 'GitHub Action to export OpenAPI schema from FastAPI apps.',
    'long_description': None,
    'author': 'Andrew Hoetker',
    'author_email': 'andrew@hoetker.engineer',
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
