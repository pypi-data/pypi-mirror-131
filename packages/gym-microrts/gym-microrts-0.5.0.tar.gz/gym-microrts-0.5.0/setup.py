# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_microrts', 'gym_microrts.envs']

package_data = \
{'': ['*'],
 'gym_microrts': ['microrts/*',
                  'microrts/lib/bots/*',
                  'microrts/maps/*',
                  'microrts/maps/10x10/*',
                  'microrts/maps/12x12/*',
                  'microrts/maps/16x16/*',
                  'microrts/maps/24x24/*',
                  'microrts/maps/4x4/*',
                  'microrts/maps/6x6/*',
                  'microrts/maps/8x8/*',
                  'microrts/maps/BroodWar/*']}

install_requires = \
['JPype1>=1.3.0,<2.0.0', 'gym>=0.21.0,<0.22.0', 'peewee>=3.14.8,<4.0.0']

extras_require = \
{'cleanrl': ['cleanrl[cloud]==0.5.0.dev6'], 'spyder': ['spyder>=5.1.5,<6.0.0']}

setup_kwargs = {
    'name': 'gym-microrts',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Costa Huang',
    'author_email': 'costa.huang@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
