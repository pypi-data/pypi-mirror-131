# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['loghelper']

package_data = \
{'': ['*']}

extras_require = \
{'concurrent': ['concurrent-log>=1.0,<2.0'],
 'flask': ['Flask>=2.0,<3.0'],
 'json': ['python-json-logger>=2.0,<3.0']}

setup_kwargs = {
    'name': 'loghelper',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'ITXiaoPang',
    'author_email': 'itxiaopang.djh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
