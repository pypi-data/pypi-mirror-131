# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awslambdalocal']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.19.2,<0.20.0']

setup_kwargs = {
    'name': 'awslambdalocal',
    'version': '1.0.2',
    'description': 'A tool to simulate running an AWS Lambda locally',
    'long_description': None,
    'author': 'Miqueias BRS',
    'author_email': 'miqueias@capybaracode.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
