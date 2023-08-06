# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kbackground']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.2',
 'numpy>=1.21.4,<2.0.0',
 'patsy>=0.5.2,<0.6.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'kbackground',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Christina Hedges',
    'author_email': 'christina.l.hedges@nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
