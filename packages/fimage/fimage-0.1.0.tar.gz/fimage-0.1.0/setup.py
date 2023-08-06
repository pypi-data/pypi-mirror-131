# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fimage']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'fimage',
    'version': '0.1.0',
    'description': 'A Python module to create and apply filters to images.',
    'long_description': '# FImage\n\nA Python module to create and apply filters to images.',
    'author': 'Jordan Jimenez',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jordandjp/fimage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
