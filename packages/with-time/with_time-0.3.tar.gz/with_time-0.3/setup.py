#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="with_time",
    version="0.3",
    description="Measuring and managing of time through context-managers and decorators.",
    long_description=open("README.rst").read().strip(),
    author="Ilya Sukhanov",
    author_email="ilya@sukhanov.net",
    url="https://github.com/IlyaSukhanov/with-time",
    packages=[
        "with_time",
    ],
    package_dir={"with_time": "with_time"},
    include_package_data=True,
    install_requires=[],
    extras_require={
        "testing": [
            "pip~=20.3",
            "flake8",
            "tox",
            "coverage",
            "pytest",
            "pyflakes",
            "pytest-cov",
            "bandit",
            "black~=21.5b1",
            "isort",
            "wheel",
            "twine",
            "rstcheck",
        ],
    },
    license="MIT license",
    zip_safe=False,
    keywords="with_time",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
)
