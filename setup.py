# -*- coding: utf-8 -*-

from distutils.core import setup

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
    license = "LGPL",
    url="https://github.com/LEMS/pylems",
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: Scientific/Engineering']
)



