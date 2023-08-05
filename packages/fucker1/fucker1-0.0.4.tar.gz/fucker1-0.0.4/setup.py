#!/usr/bin/env python
# coding: utf-8

# from setuptools import setup
import setuptools
setuptools.setup(
    name='fucker1', # 项目的名称,pip3 install get-time
    version='0.0.4', # 项目版本
    author='黄民航', # 项目作者
    author_email='gmhesat@gmail.com', # 作者email
    # url='https://github.com/Coxhuang/get_time', # 项目代码仓库
    # description='获取任意时间/获取当前的时间戳/时间转时间戳/时间戳转时间', # 项目描述
    packages=setuptools.find_packages(),
    # packages=['get_time'], # 包名
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'

)
