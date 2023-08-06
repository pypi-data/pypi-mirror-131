# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['OlivOS', 'OlivOS.middlewares', 'OlivOS.middlewares.onebot']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0a13,<3.0.0', 'nonebot2>=2.0.0a13,<3.0.0']

setup_kwargs = {
    'name': 'olivos.nb2',
    'version': '0.1.1',
    'description': 'Load OlivOS plugin in NoneBot2',
    'long_description': '# OlivOS.nb2\n\n[NoneBot2](https://github.com/nonebot/nonebot2) 的 [OlivOS](https://github.com/OlivOS-Team/OlivOS) 兼容层插件\n\n[![License](https://img.shields.io/github/license/j1g5awi/OlivOS.nb2)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a13+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/OlivOS.nb2.svg)\n\n### 安装\n\n#### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```\nnb plugin install OlivOS.nb2\n```\n\n- 使用 poetry\n\n```\npoetry add OlivOS.nb2\n```\n\n- 使用 pip\n\n```\npip install OlivOS.nb2\n```\n\n#### 从 GitHub 安装（不推荐）\n\n```\npip install git+https://github.com/j1g5awi/OlivOS.nb2.git\n```\n\n### 使用\n\n目前只有 CQHTTP(OneBot) 平台的被动消息兼容层，其他平台待添加。\n\nOlivOS 插件请放入`./data/OlivOs/app/`。\n',
    'author': 'jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
