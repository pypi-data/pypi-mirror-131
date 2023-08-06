# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_picsbank']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'aiohttp>=3.7.4.post0,<4.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.15,<3.0.0',
 'nonebot2>=2.0.0-alpha.15,<3.0.0',
 'numpy>=1.21.4,<2.0.0',
 'opencv-python>=4.5.4,<5.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-picsbank',
    'version': '0.1.3',
    'description': '',
    'long_description': '<!-- markdownlint-disable MD033 MD041-->\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot_plugin_picsbank\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_✨ 一个根据图片回答的插件 ✨_\n<!-- prettier-ignore-end -->\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">\n    <img src="https://img.shields.io/github/license/nonebot/nonebot2" alt="license">\n  </a>\n\n## 简介\n\npicsbank是一个根据群友发送的图片做出相应回答的插件，灵感来源于workbank\n\n## 使用\n\n    pb添加[全局][匹配率x][sidxxxx]发(你要应答的图片)答[你要应答的文字]\n\npb添加 : 指令，添加一个词条\n\n[全局] : 可选参数，用于指定添加的响应是否针对本群\n\n[匹配率x] : 用于指定图片的误差大小，默认为5.默认使用的是插值哈希算法生成64位哈希指纹，计算汉明距离，匹配率x指汉明距离大小。对于.gif只匹配第一帧图像。\n\n[sidxxxx] : xxxx替换为你想使用的标记,可以用来删除词条。不提供时默认为响应句子。\n\n[应答的文字] : 图片匹配成功时返回的句子。\n\n    pb删除 [图片][sidxxxx]\n\n[pb删除] : 删除指令\n\n[图片] : 要针对的图片,与sid二选一。\n\n[sidxxxx] : 要删除词条的sid,与图片二选一。\n\n    pb删除词库\n\n    pb删除全局词库\n\n    pb删除全部词库\n\n## 即刻开始\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_picsbank\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_picsbank\n```\n\n### 常见问题\n\n### 教程/实际项目/经验分享\n\n## 许可证\n\n`noneBot_plugin_picsbank` 采用 `MIT` 协议开源，协议文件参考 [LICENSE](./LICENSE)。\n\n',
    'author': 'Alex Newton',
    'author_email': 'sharenfan222@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Diaosi1111/nonebot_plugin_picsbank',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
