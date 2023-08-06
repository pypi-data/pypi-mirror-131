# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcompress']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'dataset>=1.5.2,<2.0.0',
 'gerrychain>=0.2.17,<0.3.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'pcompress',
    'version': '1.1.1',
    'description': 'Experimental, efficient, and performant binary representation of districting plans',
    'long_description': None,
    'author': 'Max Fan',
    'author_email': 'root@max.fan',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/InnovativeInventor/pcompress',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
