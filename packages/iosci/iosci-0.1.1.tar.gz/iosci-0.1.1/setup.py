#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

version = "0.1.1"
long_description = "描述"
setuptools.setup(
    name="iosci",
    version=version,
    author="lichanghong",
    author_email="1211054926@qq.com",
    description="This is the SDK for example.",
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
    exclude_package_data={'': ["example-pkg/test.py", "example-pkg/config.txt"]}
)