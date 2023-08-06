# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['colorie']
setup_kwargs = {
    'name': 'colorie',
    'version': '0.1.0',
    'description': 'ANSII Color formatting for output in terminal',
    'long_description': None,
    'author': 'Ovsyanka83',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ovsyanka83/colorie',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
