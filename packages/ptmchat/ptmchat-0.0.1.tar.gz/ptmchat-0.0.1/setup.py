#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@File        :  setup.py
@Project     :  ptmchat_develop
@Contact     :  yangshansong
@License     :  (C)Copyright 2021-2022, Hisense
@Description :  None

@Modify Time        @Author         @Version        @Description
------------        -------         --------        ------------
2021/12/6 11:30     yangshansong    1.0             None
"""

import os
import setuptools

DIR = os.path.dirname(__file__)
REQUIREMENTS = os.path.join(DIR, "requirements.txt")

with open(REQUIREMENTS) as f:
    reqs = f.read()

setuptools.setup(
    name="ptmchat",
    version="0.0.1",
    description="pretrained ernie model based retrieval open domain chatting",
    url="http://10.18.203.116/dialog/python-aispeech-ptmchat-api",
    author="hisense",
    license="Apache License 2.0",
    packages=setuptools.find_packages(),
    install_requires=reqs.strip().split("\n"),
    entry_points={
        'console_scripts': ['ptmchat=ptmchat_develop.ptmchat_entry:main'],
    }
)
