#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from setuptools import find_packages, setup


def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(
    name='papago',
    version='2.0.0',
    description='Unofficial Naver Papago Translate API for Python',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/hy040504/papago',
    author='hy040504',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False,
    test_suite='tests',
)
