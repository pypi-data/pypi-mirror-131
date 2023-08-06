# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_lambda_utils',
 'aws_lambda_utils.events',
 'aws_lambda_utils.events.api_gateway',
 'aws_lambda_utils.events.api_gateway.http_proxy',
 'aws_lambda_utils.events.api_gateway.http_proxy.v2',
 'aws_lambda_utils.interfaces',
 'aws_lambda_utils.sns']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs[essential,sns]>=1.20.8,<2.0.0',
 'boto3>=1.20.7,<2.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'aws-lambda-utils-python',
    'version': '2.0.3',
    'description': '',
    'long_description': None,
    'author': 'nichmorgan-loft',
    'author_email': 'nich.morgan@loft.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
