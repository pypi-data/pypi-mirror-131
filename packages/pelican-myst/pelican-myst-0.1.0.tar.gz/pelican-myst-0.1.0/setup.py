# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican_myst']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'markdown-it-py[plugins,linkify]>=2.0.0,<3.0.0',
 'pelican>=4.0,<5.0']

extras_require = \
{'lint': ['black>=21.9b0,<22.0', 'flake8', 'isort>=5.9.3,<6.0.0'],
 'test': ['pyquery>=1.4.3,<2.0.0',
          'pytest>=6.2.5,<7.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'pytest-pythonpath>=0.7.3,<0.8.0',
          'pytest-sugar>=0.9.4,<0.10.0']}

setup_kwargs = {
    'name': 'pelican-myst',
    'version': '0.1.0',
    'description': 'A Pelican Myst reader',
    'long_description': None,
    'author': 'Axel H.',
    'author_email': 'noirbizarre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
