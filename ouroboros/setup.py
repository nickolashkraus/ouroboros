#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Nickolas Kraus",
    author_email='NickHKraus@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Ouroboros simplifies AWS Lambda function deployments.",
    install_requires=requirements,
    license="MIT license",
    long_description='',
    include_package_data=True,
    keywords='ouroboros',
    name='ouroboros',
    packages=find_packages(include=['ouroboros']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/NickolasHKraus/ouroboros',
    version='0.1.0',
    zip_safe=False,
)
