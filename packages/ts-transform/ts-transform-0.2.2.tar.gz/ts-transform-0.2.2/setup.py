# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ts_transform', 'ts_transform.core']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0', 'scikit-learn>=0.24.2,<0.25.0']

setup_kwargs = {
    'name': 'ts-transform',
    'version': '0.2.2',
    'description': 'Timeseries transforms',
    'long_description': None,
    'author': 'Adam Hendel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
