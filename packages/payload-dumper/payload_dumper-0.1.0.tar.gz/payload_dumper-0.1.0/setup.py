# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['payload_dumper']

package_data = \
{'': ['*']}

install_requires = \
['bsdiff4>=1.2.1,<2.0.0', 'enlighten>=1.10.2,<2.0.0', 'protobuf>=3.19.1,<4.0.0']

entry_points = \
{'console_scripts': ['payload_dumper = payload_dumper:dumper.main']}

setup_kwargs = {
    'name': 'payload-dumper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rasmus Moorats',
    'author_email': 'xx@nns.ee',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
