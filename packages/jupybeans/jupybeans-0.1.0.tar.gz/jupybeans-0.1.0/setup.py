# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jupybeans']
install_requires = \
['jupyter>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'jupybeans',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gordon Bean',
    'author_email': 'gbean@cs.byu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
