#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='k0napi',  # 项目的名称,pip3 install get-time
    version='0.0.2',  # 项目版本
    author='SuzuBucket',  # 项目作者
    author_email='root@k-0n.org', # 作者email
    url='https://github.com/',  # 项目代码仓库
    description='k-0n bf1 api sdk', # 项目描述
    packages=['konBfApi'],  # 包名
    install_requires=["httpx[http2] == 0.21.1"],
)
