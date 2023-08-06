#!/usr/bin/env python
# -*- coding: utf-8 -*-

# specclassify, A Python package for multi- or hyperspectral image classification.
#
# Copyright (C) 2019-2021
# - Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences Potsdam,
#   Germany (https://www.gfz-potsdam.de/)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version = {}
with open("specclassify/version.py") as version_file:
    exec(version_file.read(), version)

requirements = ['numpy', 'tqdm', 'matplotlib', 'scikit-learn', 'geoarray>=0.15.0', 'py_tools_ds>=0.18.0']

setup_requirements = []

test_requirements = ['pytest', 'pytest-cov', 'pytest-reporter-hmtl1', 'dill', 'urlchecker']

setup(
    author="Daniel Scheffler",
    author_email='daniel.scheffler@gfz-potsdam.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python package for multi- or hyperspectral image classification.",
    install_requires=requirements,
    license="Apache-2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['specclassify', 'remote sensing', 'multispectral', 'hyperspectral', 'image classification'],
    name='specclassify',
    packages=find_packages(exclude=['tests*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://git.gfz-potsdam.de/geomultisens/specclassify',
    version=version['__version__'],
    zip_safe=False,
)
