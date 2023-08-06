#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='dutool',
    version='0.0.1',
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
        'requests>=2.19.1',
        # 'pycrypto>=2.6.1',
        # 'xmltodict>=0.11.0'
    ],
)
