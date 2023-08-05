# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_tvseries']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.4,<5.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.16,<3.0.0',
 'playwright>=1.17.2,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-tvseries',
    'version': '0.0.2.1',
    'description': '',
    'long_description': '# nonebot-plugin-tvseries\n\n获取美剧\n\n# 安装\n\n## 环境(dockerfile)\n\n```\nENV TZ=Asia/Shanghai\nENV LANG zh_CN.UTF-8\nENV LANGUAGE zh_CN.UTF-8\nENV LC_ALL zh_CN.UTF-8\nENV TZ Asia/Shanghai\nENV DEBIAN_FRONTEND noninteractive\n```\n\n## 本体\n\n`pip install nonebot-plugin-tvseries`\n\n## 依赖\n\n```\napt install -y libzbar0 locales locales-all fonts-noto\nplaywright install chromium && playwright install-deps\n```\n\n# 使用\n\n`美剧` `tvseries`\n\n# 有问题 提pr\n有问题 提pr\n',
    'author': 'kexue',
    'author_email': 'xana278@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
