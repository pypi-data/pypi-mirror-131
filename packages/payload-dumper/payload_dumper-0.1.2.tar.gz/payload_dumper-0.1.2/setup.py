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
    'version': '0.1.2',
    'description': "Dump partitions from Android's payload.bin",
    'long_description': '# payload dumper\n\nDumps the `payload.bin` image found in Android update images.\n\n## Installation\n\n### Requirements\n\n- Python3\n- pip\n\n### Install using pip\n\n```sh\npip install --user payload_dumper\n```\n\n## Usage\n\n### Dumping the entirety of `payload.bin`\n\n```\npayload_dumper payload.bin\n```\n\n### Dumping specific partitions\n\nUse a comma-separated list of partitions to dump:\n```\npayload_dumper --partitions boot,dtbo,vendor\n```\n\n### Patching older image with OTA\n\nAssuming the old partitions are in a directory named `old/`:\n```\npayload_dumper --diff payload.bin\n```\n',
    'author': 'Rasmus Moorats',
    'author_email': 'xx@nns.ee',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnsee/payload-dumper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
