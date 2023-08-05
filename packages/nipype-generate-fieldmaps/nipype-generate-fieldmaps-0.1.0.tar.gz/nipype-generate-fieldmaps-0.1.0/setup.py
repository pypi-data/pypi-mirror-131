# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nipype_generate_fieldmaps']
install_requires = \
['nibabel>=3.0.0,<4.0.0', 'nipype>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'nipype-generate-fieldmaps',
    'version': '0.1.0',
    'description': 'Nipype workflow to generate fieldmaps from EPI acquisitions with differing phase-encoding directions',
    'long_description': None,
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
