# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bd103', 'bd103.data', 'bd103.ext', 'bd103.shared']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=4.3.1,<5.0.0'], 'ext': ['trio>=0.19.0,<0.20.0']}

setup_kwargs = {
    'name': 'bd103',
    'version': '2.0.0rc1',
    'description': "BD103's Python Package",
    'long_description': "# BD103 Python Package\n\nThese are some utility modules and fun stuff that might make a good dependency. There are some subpackages that has special purposes.\n\n- `bd103.ext`: Contains extensions and plugins to other Python packages\n- `bd103.shared`: Contains modules that are shared between different implementations of BD103's library\n- `bd103.data`: Contains data types for various formats\n\n## Installation\n\n```shell\npython -m pip install -U bd103\n```\n\n## Getting Started\n\nA good idea is too look through the [documentation](https://bd103.github.io/BD103-Python/) to find modules that might pique your interest. A recommended one is the [decorators](https://bd103.github.io/BD103-Python/api/decorators.html) module.\n\n## Contributing\n\nFeel free to submit a PR if you want to contribute to the package. For more information, see [CONTRIBUTING.md](CONTRIBUTING.md).\n",
    'author': 'BD103',
    'author_email': 'dont@stalk.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bd103.github.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
