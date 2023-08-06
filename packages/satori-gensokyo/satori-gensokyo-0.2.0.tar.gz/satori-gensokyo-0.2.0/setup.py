# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satori_gensokyo']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'tomlkit>=0.7.2,<0.8.0']

entry_points = \
{'console_scripts': ['satori = satori_gensokyo.satori:main']}

setup_kwargs = {
    'name': 'satori-gensokyo',
    'version': '0.2.0',
    'description': 'Gensokyo style spellcard fight generator',
    'long_description': None,
    'author': 'Ravenclaw-OIer',
    'author_email': 'lilywhite2005@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
