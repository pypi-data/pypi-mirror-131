# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tablefill']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.14.0,<9.0.0', 'typer>=0.4.0,<0.5.0', 'xlrd==1.2.0', 'xlutils==2.0.0']

entry_points = \
{'console_scripts': ['fill = tablefill.cli:app']}

setup_kwargs = {
    'name': 'tablefill',
    'version': '0.1.2',
    'description': 'Excel模板数据填充,快速应对Web项目数据导入',
    'long_description': '# 背景\n在测试Web后台管理系统项目时，导入数据是个高频出现的功能,[tablefill](https://github.com/zy7y/tablefill)主要完成根据配置文件对模板进行填充数据\n\n# 使用\n**安装**\n```shell\npip install tablefill\n```\n**配置列数据类型**\n```json5\n[\n  {\n    "type": "faker", // 可选值 faker(默认值,可不写type这个字段)、input 会直接读取var 的值 由自己设置\n    "func": "name", // 对应的是 Faker 生成虚拟数据的那些方法名 https://faker.readthedocs.io/en/master/providers.html\n    "var": null, // 没有参数时可以不写该字段, 当type 为faker时 这部分会被作为func 对应函数名的入参\n    "varFirst": "前", // 如果不需要可以不写该字段, 会在 var 这个 参数 前面 加上 内容\n    "varEnd": "后" // 如果不需要可以不写该字段, 会在 var 这个 参数 后面 加上 内容\n  }\n]\n```\n**api参考[faker](https://faker.readthedocs.io/en/stable/providers.html)**\nphone_number: 生成手机号\nrandom_element: 列表中随机元素\nname: 随机名称\nssn: 身份证号\ndate: 随机日期\n\n\n*示例*\n```json\n[\n  {\n    "type": "input",\n    "var": "这列我输入"\n  },\n  {\n    "func": "phone_number"\n  },\n  {\n    "func": "random_int",\n    "var": {\n      "min": 10,\n      "max": 21\n    },\n    "varFirst": "编号",\n    "varEnd": "班"\n  },\n  {\n    "func": "random_element",\n    "var": {\n      "elements": ["小学", "高中", "初中"],\n    }\n  }\n]\n```\n**导入模板文件**\n> 需要是xlsx/xls文件\n[![4h3G3F.md.png](https://z3.ax1x.com/2021/09/29/4h3G3F.md.png)](https://imgtu.com/i/4h3G3F)\n\n**执行命令**\n```shell\n# --num 可选参数 默认 10条 ，这里就是30条\nfill generate 配置文件 模板文件 生成文件名 --num 30 \n\nfill generate "E:\\coding\\tablefill\\examples\\demo.json" "E:\\coding\\tablefill\\examples\\demo.xlsx"  demo.xls\n```\n\n**填充数据后的文件**\n[![4h8FbR.md.png](https://z3.ax1x.com/2021/09/29/4h8FbR.md.png)](https://imgtu.com/i/4h8FbR)\n\n**help**\n```shell\nfill --help\n```\n\n',
    'author': '柒意',
    'author_email': '396667207@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitee.com/zy7y/tablefill',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
