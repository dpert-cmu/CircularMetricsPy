# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['params', 'utils']
install_requires = \
['ipywidgets',
 'numpy',
 'pandas',
 'json',
 'IPython',
 'ipykernel']

setup_kwargs = {
    'name': 'CircularMetricsPy',
    'version': '1.0.0',
    'description': "A Jupyter notebook-based interface to the Ellen MacArthur Foundation's Circulytics framework",
    'author': 'Daniel Pert',
    'author_email': 'dpert@andrew.cmu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)