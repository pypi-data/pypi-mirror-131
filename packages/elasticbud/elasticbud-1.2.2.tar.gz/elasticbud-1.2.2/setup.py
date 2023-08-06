# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elasticbud']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch-dsl',
 'elasticsearch[async]',
 'pytest-asyncio',
 'pytest-depends',
 'tenacity']

setup_kwargs = {
    'name': 'elasticbud',
    'version': '1.2.2',
    'description': 'Wrappers for writing concise Elasticsearch-integrated python APIs.',
    'long_description': None,
    'author': 'tasker',
    'author_email': 'tasker@ialcloud.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
