#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read().replace('\r\n', '\n')


setup(
    name='async-westjr',
    version='0.0.1',
    license='Unlicense',
    description='Handling of train operation information of JR West, a railroad company in Japan',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='midorichaan',
    author_email='furandorusukaret.jp@gmail.com',
    url='https://github.com/midorichaan/async-westjr',
    install_requires=['aiohttp'],
    packages=find_packages(),
    keywords='async-westjr'
)
