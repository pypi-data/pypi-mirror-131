# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esetinspect']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0', 'httpx>=0.21.1,<0.22.0', 'pyhumps>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'esetinspect',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Donny Maasland',
    'author_email': 'donny@unauthorizedaccess.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
