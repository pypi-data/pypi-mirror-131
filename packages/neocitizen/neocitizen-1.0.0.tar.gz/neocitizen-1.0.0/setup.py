# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neocitizen']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['neocitizen = neocitizen.cli:cli']}

setup_kwargs = {
    'name': 'neocitizen',
    'version': '1.0.0',
    'description': 'Python client library for Neocities API',
    'long_description': '# neocitizen: Python client library for Neocities API\n\n[![PyPI Version](https://img.shields.io/pypi/v/neocitizen.svg)](https://pypi.org/pypi/neocitizen/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/neocitizen.svg)](https://pypi.org/pypi/neocitizen/)\n[![License](https://img.shields.io/pypi/l/neocitizen.svg)](https://github.com/poyo46/neocitizen/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n[Neocities](https://neocities.org/) is a web hosting service for static pages.\nThis is a library that makes the [Neocities API](https://neocities.org/api) available from the CLI and Python.\n\n## Installation\n\n`neocitizen` is available on PyPI:\n\n```console\n$ pip install neocitizen\n```\n\nYou can also use [poetry](https://python-poetry.org/) to add it to a Python project.\n\n```console\n$ poetry add neocitizen\n```\n\n## CLI Examples\n\n**Upload the directory and check the result**\n\n```\n$ export NEOCITIES_API_KEY=<your api key here>\n$ neocitizen upload --dir=/path/to/dir\n$ neocitizen list\ndir0\ndir0/file00.html\ndir0/file01.html\ndir1\ndir1/dir10\ndir1/dir10/file100.html\ndir1/dir11\ndir1/dir11/file110.html\ndir1/file10.html\ndir1/file11.html\nindex.html\n```\n\n**Download**\n\n```\n$ export NEOCITIES_API_KEY=<your api key here>\n$ neocitizen download /path/to/save\n```\n\n**Detailed usage**\n\n```\n$ neocitizen --help\nUsage: neocitizen [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version        Show the version and exit.\n  --key TEXT       API key. You can also use the environment variable NEOCITIES_API_KEY instead.\n  --username TEXT  User name for authentication. You can also use the environment variable NEOCITIES_USERNAME instead.\n  --password TEXT  Password for authentication. You can also use the environment variable NEOCITIES_PASSWORD instead.\n  -v, --verbose    Verbose output.\n  --help           Show this message and exit.\n\nCommands:\n  delete    Delete the files on your Neocities site.\n  download  Download all the files on your Neocities site.\n  info      Show information about your Neocities site.\n  key       Show API key.\n  list      Show file list your Neocities site.\n  upload    Upload local data to your Neocities site.\n```\n\n## Python Examples\n\n**Code: example.py**\n\n```python:example.py\nfrom neocitizen import NeocitiesApi\n\napi = NeocitiesApi()\nresponse = api.fetch_info()\nfor key, value in response["info"].items():\n    print(f"{key}: {value}")\n\n```\n\n**Run**\n\n```\n$ export NEOCITIES_API_KEY=<your api key here>\n$ python example.py\nsitename: neocli-test\nviews: 268\nhits: 483\ncreated_at: Sun, 05 Dec 2021 12:13:28 -0000\nlast_updated: Sun, 19 Dec 2021 13:37:13 -0000\ndomain: None\ntags: []\nlatest_ipfs_hash: None\n```\n',
    'author': 'poyo46',
    'author_email': 'poyo4rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poyo46/neocitizen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
