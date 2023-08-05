#!/usr/bin/env python

from setuptools import setup

setup(
    name='sysubadminton',
    version='0.1.0',
    author='SYSUBad',
    author_email='sysu@bad.com',
    url='https://gist.github.com/834e635e82739ee23d1450357f4fcc6e',
    description='用于中山大学珠海校区羽毛球场的预定',
    packages=['sysubadminton'],
    install_requires=['requests', 'beautifulsoup4'],
)
