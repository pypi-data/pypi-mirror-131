# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['episimlab',
 'episimlab.models',
 'episimlab.partition',
 'episimlab.setup',
 'episimlab.setup.greek',
 'episimlab.utils']

package_data = \
{'': ['*']}

install_requires = \
['dask[distributed]>=2021.4.0,<2022',
 'graphviz>=0.17,<1',
 'matplotlib>=3.4.3,<4',
 'networkx>=2.6.3,<3',
 'xarray-simlab>=0.5.0,<1',
 'xarray>=0.19.0']

setup_kwargs = {
    'name': 'episimlab',
    'version': '2.2.2',
    'description': 'Framework for modular development of compartmental epidemic models',
    'long_description': None,
    'author': 'Ethan Ho',
    'author_email': 'eho@tacc.utexas.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
