#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

APP_NAME = 'rug'
VERSION = '0.0.1'

setup(
    name=APP_NAME,
    version=VERSION,
    description='An static site generator for mysqlf.',
    long_description=open('README.md').read(),
    author='Kosei Moriyama',
    author_email='cou929@gmail.com',
    url='https://github.com/cou929/rug',
    packages=['rug'],
    license='MIT License',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    entry_points={
        'console_scripts': [
            'rug = rug.cli:dispatch',
            ],
        },
    )
