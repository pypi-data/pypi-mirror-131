# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glyles', 'glyles.glycans', 'glyles.grammar']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime>=4.9.3,<5.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pydot>=1.4.2,<2.0.0',
 'rdkit-pypi>=2021.9.2,<2022.0.0']

setup_kwargs = {
    'name': 'glyles',
    'version': '0.0.1',
    'description': 'A tool to convert IUPAC representation of glycans into SMILES strings',
    'long_description': None,
    'author': 'Roman Joeres',
    'author_email': 'Roman.Joeres@helmholtz-hzi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
