#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation file  for  billmanager ticket alerting.
"""
from setuptools import setup


setup(
    name='ticketsbill5',
    version='0.2',
    packages=['ticketsbill5'],
    install_requires=['bs4', 'requests', 'urllib3'],
    entry_points={'console_scripts': ['ticketsbill5 = ticketsbill5.main:main']},
    url='nope',
    license='GPLv2+',
    author='Kirill Shilov',
    author_email='ktk@ktkd.ru',
    description='Provide notification about new tickets in billmanager 5'
)
