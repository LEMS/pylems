# -*- coding: utf-8 -*-

from setuptools import setup

long_description = open("README.md").read()

import lems
version = lems.__version__

setup(
    name = "PyLEMS",
    version = version,
    packages = ['lems','lems.base','lems.model','lems.parser','lems.sim', 'lems.dlems'],
    scripts=['pylems'],
    author = "PyLEMS authors and contributors",
    author_email = "gautham@lisphacker.org, p.gleeson@gmail.com",
    description = "A Python library for working with the Low Entropy Model Specification language (LEMS)",
    long_description = long_description,
    long_description_content_type="text/markdown",
    install_requires=['lxml','typing'],
    license = "LGPL",
    url="https://github.com/LEMS/pylems",
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering']
)
