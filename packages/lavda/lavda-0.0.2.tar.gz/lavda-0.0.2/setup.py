# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose :
# author :
# create_time : 2020/7/2 17:21
# update_time : 2020/7/2 17:21
# copyright : Lavector
# ----------------------------------------------
#!/usr/bin/python
# coding:utf-8
from __future__ import print_function
from setuptools import setup, find_packages
import sys
import datetime
import os


version_path = os.path.join(os.getcwd(), *['maxda', "version.py"])
if os.path.exists(version_path):
    version_file = open(version_path)
    cur_version = version_file.readline().strip()
else:
    cur_version = "0.0.2"

setup(
    name="lavda",
    version=cur_version,
    author="lavector data_analysis",
    author_email="hao.jia@lavector.com",
    description="data process and analysis",
    # license="MIT",
    # url="http://gitlab.lavector.com/analysis/maxda-dev.git",
    packages=['lavda'],
    # packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pandas',
        'numpy',
        'xlsxwriter',
        'joblib>=0.14.0',
        'xlrd',
        'pymysql',
        'emoji',
        "sklearn",
        "pyahocorasick",
        "openpyxl",
        "torch>=1.2.0"
    ],
    zip_safe=True,
)


