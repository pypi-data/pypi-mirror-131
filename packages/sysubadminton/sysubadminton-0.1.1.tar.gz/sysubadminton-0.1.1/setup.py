#!/usr/bin/env python

from setuptools import setup

setup(
    name='sysubadminton',
    version='0.1.1',
    python_requires='>=3.6.0',
    author='SYSUBad',
    author_email='sysu@bad.com',
    url='https://gist.github.com/834e635e82739ee23d1450357f4fcc6e',
    description='用于中山大学珠海校区羽毛球场的预定',
    long_description='''

# 说明

此脚本专用于**中山大学珠海校区羽毛球场**的预定，理论上更改文件中的部分参数可实现预定其他场地，请自行测试

# 使用步骤

## 下载代码

```shell
git clone https://gist.github.com/834e635e82739ee23d1450357f4fcc6e.git ./badminton
```

或者[下载压缩包](https://gist.github.com/SYSUgym/834e635e82739ee23d1450357f4fcc6e/archive/master.zip)

## 安装环境

需要 `python >= 3.6`，同时需要 `requests, BeautifulSoup4` 软件包。

```shell
cd ./badminton
python -m pip install -r requirements.txt
```

## 修改配置文件

打开 `config.ini`，填入想要的配置，以及用户名和密码

```ini
[badminton]
; 下面写入希望预定的场地，按顺序进行预定，如 1, 2, 3
stock_name = 7, 8, 6, 9, 4, 3, 2, 1, 5

; 下面写入需要预定的时间，按顺序进行预定，如希望预定 16-17, 17-18 时，写入 16, 17
stock_time = 19, 20, 18, 17

; 下面写入预定的日期，如 2020-12-04，留空为程序运行日期的后天（T+2），通常留空即可
stock_date =

; 下面写入预定的顺序，如果优先满足场地，即尽可能订同一场地的不同时间段，则输入 name
; 如果优先满足时间，即尽可能订同一时间段的不同场地，则输入 time
first = name

; 下面写入每个时间段需要的场地数，默认不限制
stock_number = 99

netid =
password =
```

## 运行脚本

```shell
python badminton.py
```

验证码识别顺利的话即可自动登录，到时间订场。

PS. 此脚本目测可以实现晚上打开，早上自动订场，Linux 下可配合 `screen` 使用。如果对验证码自动识别放心的话，可以设置定时任务运行。
''',
    long_description_content_type="text/markdown",
    packages=['sysubadminton'],
    install_requires=['requests', 'beautifulsoup4'],
)
