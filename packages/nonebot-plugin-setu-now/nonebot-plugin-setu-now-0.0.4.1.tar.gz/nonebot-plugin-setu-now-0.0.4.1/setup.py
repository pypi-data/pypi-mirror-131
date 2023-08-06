# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_setu_now']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.0,<1.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.16,<3.0.0',
 'webdav4>=0.9.3,<0.10.0']

setup_kwargs = {
    'name': 'nonebot-plugin-setu-now',
    'version': '0.0.4.1',
    'description': '另一个色图插件',
    'long_description': None,
    'author': 'kexue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
