#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='dutool',
    version='0.0.3',
    keywords='dutool',
    description='a library for revang developer',
    license='MIT License',
    url='https://github.com/revang/dutool',
    author='revang',
    author_email='revang.alternative@foxmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'you-get>=0.4.1555',
        'ffmpy>=0.3.0',
    ],
)
