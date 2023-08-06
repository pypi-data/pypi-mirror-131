# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ntn_torch',
 'ntn_torch.rl',
 'ntn_torch.rl.common',
 'ntn_torch.rl.ntn_reinforce']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0',
 'stable-baselines3[extra]>=1.3.0,<2.0.0',
 'torch>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'ntn-torch',
    'version': '0.2.2',
    'description': 'ntn_torch is a library to build n-tuple neural network models using the framework of pytorch',
    'long_description': None,
    'author': 'Rafael F. Katopodis',
    'author_email': 'rafaelkatopodis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.11',
}


setup(**setup_kwargs)
