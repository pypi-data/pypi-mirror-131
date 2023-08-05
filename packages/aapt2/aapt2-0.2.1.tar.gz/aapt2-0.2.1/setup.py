# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aapt2']

package_data = \
{'': ['*'], 'aapt2': ['bin/Darwin/*', 'bin/Linux/*', 'bin/Windows/*']}

setup_kwargs = {
    'name': 'aapt2',
    'version': '0.2.1',
    'description': 'Android Asset Packaging Tool 2 for Python3',
    'long_description': None,
    'author': 'Trevor Wang',
    'author_email': 'trevor.wang@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trevorwang/aapt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
