# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aidkit_client', 'aidkit_client.endpoints', 'aidkit_client.resources']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0', 'tabulate>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'aidkit-client',
    'version': '0.1.0',
    'description': 'aidkit for your CI/CD and j-notebooks.',
    'long_description': '![aidkit](https://www.neurocat.ai/wp-content/uploads/2018/11/addkit-hori.png)\n\naidkit is an MLOps platform that allows you to assess and defend against threads\nand vulnerabilities of AI models before they deploy to production.\naidkit-client is a companion python client library to seamlessly integrate with\naidkit in python projects.\n',
    'author': 'neurocat GmbH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
