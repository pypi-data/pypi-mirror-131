#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

version = "0.1.2"
long_description = "解析podfile和批量修改组件版本号"
setuptools.setup(
    name="iosci",
    version=version,
    author="lichanghong",
    author_email="1211054926@qq.com",
    description="T解析podfile和批量修改组件版本号.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hehuoya.com",
    install_requires=[
        'requests'
    ],
    packages=setuptools.find_packages(exclude=("iosci")),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ),
    exclude_package_data={'': ["iosci/test.py", "iosci/xcode/a.py","iosci/xcode/b.py"]}
)