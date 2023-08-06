# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apirunner',
 'apirunner.app',
 'apirunner.app.routers',
 'apirunner.builtin',
 'apirunner.ext',
 'apirunner.ext.har2case',
 'apirunner.ext.locust',
 'apirunner.ext.uploader']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'jinja2>=2.10.3,<3.0.0',
 'jmespath>=0.9.5,<0.10.0',
 'loguru>=0.4.1,<0.5.0',
 'pydantic>=1.4,<2.0',
 'pytest-html>=2.1.1,<3.0.0',
 'pytest>=5.4.2,<6.0.0',
 'pyyaml>=5.1.2,<6.0.0',
 'requests>=2.22.0,<3.0.0',
 'sentry-sdk>=0.14.4,<0.15.0']

extras_require = \
{'allure': ['allure-pytest>=2.8.16,<3.0.0'],
 'locust': ['locust>=1.0.3,<2.0.0'],
 'upload': ['requests-toolbelt>=0.9.1,<0.10.0', 'filetype>=1.0.7,<2.0.0']}

entry_points = \
{'console_scripts': ['har2case = apirunner.cli:main_har2case_alias',
                     'hmake = apirunner.cli:main_make_alias',
                     'hrun = apirunner.cli:main_hrun_alias',
                     'httprunner = apirunner.cli:main',
                     'locusts = apirunner.ext.locust:main_locusts']}

setup_kwargs = {
    'name': 'apirunner',
    'version': '1.1.0',
    'description': 'One-stop solution for HTTP(S) testing.',
    'long_description': '# httprunners\n\n#### 介绍\n基于httprunner3.1.4框架进行二次开发，优化相关功能与一些小的缺陷。\n\n#### 软件架构\n软件架构说明\n\n\n#### 安装教程\n\n1.  xxxx\n2.  xxxx\n3.  xxxx\n\n#### 使用说明\n\n1.  xxxx\n2.  xxxx\n3.  xxxx\n\n#### 参与贡献\n\n1.  Fork 本仓库\n2.  新建 Feat_xxx 分支\n3.  提交代码\n4.  新建 Pull Request\n\n\n#### 特技\n\n1.  使用 Readme\\_XXX.md 来支持不同的语言，例如 Readme\\_en.md, Readme\\_zh.md\n2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)\n3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目\n4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目\n5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)\n6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)\n\npoetry 打包推送\npoetry build\npoetry publish',
    'author': 'ylfeng',
    'author_email': '835393537@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
