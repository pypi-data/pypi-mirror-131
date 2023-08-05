# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_lolmatch']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'aiohttp>=3.7.4.post0,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'databases>=0.5.0,<0.6.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.15,<3.0.0',
 'nonebot2>=2.0.0-alpha.15,<3.0.0',
 'playwright>=1.17.0,<2.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-lolmatch',
    'version': '0.1.0',
    'description': '',
    'long_description': '<!-- markdownlint-disable MD033 MD041-->\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot_plugin_lolmatch\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_✨ 一个有关lol比赛信息的插件 ✨_\n<!-- prettier-ignore-end -->\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/nonebot2" alt="license">\n  </a>\n\n## 简介\n\nlolmatch是一个有关于lol比赛信息的插件，你可以用它来获取每天的比赛结果。本人python新手，有bug请提交issue，欢迎pr\n\n## 注意\n\n因为本插件使用了playwright模块，在windows平台使用需要使用猴子补丁,可以参考nonebot官方FQA\n\n使用本插件需要提供定时模块可以使用以下命令安装\n\n```\n    nb plugin install nonebot_plugin_apscheduler\n```\n\n## 使用\n\n        主命令 lol 查看今日比赛信息\n        附带命令 本周 查看本周比赛信息\n        附带命令 详情 [matchID] 查询指定比赛详细信息\n        附带命令 订阅 [tournamentID] 订阅相关系列赛 每晚检查当日结果和第二天赛程\n        附带命令 赛事 查看所有即将进行或正在进行的赛事\n\n## 即刻开始\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_lolmatch\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_lolmatch\n```\n\n### 常见问题\n\n### 教程/实际项目/经验分享\n\n## 许可证\n\n`noneBot_plugin_lolmatch` 采用 `MIT` 协议开源，协议文件参考 [LICENSE](./LICENSE)。\n\n',
    'author': 'Alex Newton',
    'author_email': 'sharenfan222@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Diaosi1111/nonebot_plugin_lolmatch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
