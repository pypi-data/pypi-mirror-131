# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dajapy']

package_data = \
{'': ['*']}

install_requires = \
['SudachiDict-core>=20210802.post1,<20210803', 'SudachiPy>=0.6.2,<0.7.0']

setup_kwargs = {
    'name': 'dajapy',
    'version': '0.1.0',
    'description': '日本語のダジャレを判定するPythonパッケージ',
    'long_description': None,
    'author': 'fujitako03',
    'author_email': 'okome.osakana.oniku@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fujitako03',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
