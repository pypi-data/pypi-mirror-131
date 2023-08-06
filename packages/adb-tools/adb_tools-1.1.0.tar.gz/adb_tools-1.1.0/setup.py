# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name="adb_tools",
    version="1.1.0",
    author="crystal",
    author_email="zhuhuiping@shizhuang-inc.com",
    description="adb tools",
    packages=["adb_tools", "adb_tools.providers"],
    python_requires=">=3.7",
    long_description_content_type="text/x-rst",
    license='Apache License 2.0',
)