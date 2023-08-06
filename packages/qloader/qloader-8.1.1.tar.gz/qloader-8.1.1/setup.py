# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qloader']

package_data = \
{'': ['*']}

install_requires = \
['imagehash>=4.1.0,<5.0.0',
 'pillow>=8.1.1,<9.0.0',
 'requests>=2.23.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'qloader',
    'version': '8.1.1',
    'description': 'Gather results from some search engine',
    'long_description': None,
    'author': 'tasker',
    'author_email': 'tasker@ialcloud.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
