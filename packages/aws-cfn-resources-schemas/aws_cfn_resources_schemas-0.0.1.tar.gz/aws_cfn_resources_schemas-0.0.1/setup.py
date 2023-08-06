# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_cfn_resources_schemas']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aws-cfn-resources-schemas',
    'version': '0.0.1',
    'description': 'AWS CFN Resources JSON Schema definitions',
    'long_description': '=========================\nAWS CFN Resources Schemas\n=========================\n\nAWS CFN Resources JSON Schema definitions\n\n\nDISCLAIMER: Although this library is licensed under MLP-2.0, the JSON schemas are provided and owned by Amazon Web Services.\nAvailable to download from `AWS Official site - CloudFormation resource provider schemas`_\n\n\nFeatures\n--------\n\n* Contains the JSON Schema definition of AWS CloudFormation resources from public registry.\n* Easy resource-type to definition retrieval.\n\n\n.. _AWS Official site - CloudFormation resource provider schemas: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-type-schemas.html\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
