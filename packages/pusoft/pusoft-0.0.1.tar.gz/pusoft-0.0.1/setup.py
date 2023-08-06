#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pusoft',
    version='0.0.1',
    author='pumpkin_1001',
    author_email='2752349525@qq.com',
    url='https://github.com/pumkin1001/PuDatabase/',
    description=u'PUSoft Tools',
    packages=['pusoft'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pudatabase=pusoft.pudatabase:cmd'
        ]
    }
)