# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['OpenApiLibCore']

package_data = \
{'': ['*']}

install_requires = \
['openapi-core',
 'openapi-spec-validator',
 'prance',
 'requests',
 'robotframework>=4']

setup_kwargs = {
    'name': 'robotframework-openapi-libcore',
    'version': '1.0.0a0',
    'description': 'A Robot Framework library to facilitate library development for OpenAPI / Swagger APIs.',
    'long_description': '---\n---\nModule with core logic to interact with OpenAPI APIs.',
    'author': 'Robin Mackaij',
    'author_email': None,
    'maintainer': 'Robin Mackaij',
    'maintainer_email': None,
    'url': 'https://github.com/MarketSquare/robotframework-openapi-libcore',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
