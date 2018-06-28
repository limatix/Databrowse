#!/usr/bin/env python
###############################################################################
## Databrowse:  An Extensible Data Management Platform                       ##
## Copyright (C) 2012-2016 Iowa State University Research Foundation, Inc.   ##
## All rights reserved.                                                      ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions are    ##
## met:                                                                      ##
##   1. Redistributions of source code must retain the above copyright       ##
##      notice, this list of conditions and the following disclaimer.        ##
##   2. Redistributions in binary form must reproduce the above copyright    ##
##      notice, this list of conditions and the following disclaimer in the  ##
##      documentation and/or other materials provided with the distribution. ##
##   3. Neither the name of the copyright holder nor the names of its        ##
##      contributors may be used to endorse or promote products derived from ##
##      this software without specific prior written permission.             ##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS       ##
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED ##
## TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A           ##
## PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER ##
## OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,  ##
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,       ##
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR        ##
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    ##
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      ##
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        ##
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              ##
##                                                                           ##
## This material is based on work supported by the Air Force Research        ##
## Laboratory under Contract #FA8650-10-D-5210, Task Order #023 and          ##
## performed at Iowa State University.                                       ##
##                                                                           ##
## DISTRIBUTION A.  Approved for public release:  distribution unlimited;    ##
## 19 Aug 2016; 88ABW-2016-4051.                                             ##
##                                                                           ##
## This material is based on work supported by NASA under Contract           ##
## NNX16CL31C and performed by Iowa State University as a subcontractor      ##
## to TRI Austin.                                                            ##
##                                                                           ##
## Approved for public release by TRI Austin: distribution unlimited;        ##
## 01 June 2018; by Carl W. Magnuson (NDE Division Director).                ##
###############################################################################
""" setup.py - Main Install Script """

import sys
import os
import requirements as r
import platform
from shutil import copyfile
from setuptools import setup, find_packages, Distribution
from setuptools.command.install import install

# Collect all databrowse static files required for CEFDatabrowse
search_dirs = [('databrowse_wsgi', []), ('cefdatabrowse', [])]
for search_dir in range(0, len(search_dirs)):
    for dir, subdir, files in os.walk(search_dirs[search_dir][0]):
        for file in files:
            if dir not in dict(search_dirs):
                search_dirs.append((dir, []))
            idx = [search_dirs.index(tupl) for tupl in search_dirs if tupl[0] == dir][0]
            search_dirs[idx][1].append(os.path.join(dir, file))


def readfile(filename):
    """ Utility Function to Read the Readme File """
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


# Determine platform specific requirements
with open(r.select_requirements_file(), 'r') as f:
    reqs = f.read().splitlines()


setup(
    name="databrowse",
    author="Tyler Lesthaeghe/Nathan Scheirer",
    author_email="tylerl@iastate.edu/scheirer@iastate.edu",
    description="An Extensible Data Management Platform",
    keywords="databrowse data management",
    url="http://limatix.org",
    version='0.8.0',
    packages=find_packages(exclude=['databrowse_wsgi', 'tests', 'test_*']),
    package_data={'': ['*.conf', '*.xml', '.databrowse']},
    data_files=search_dirs,
    license="BSD-3",
    long_description=readfile('README.md'),
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=reqs,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: CEF Client",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: JavaScript",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'databrowse = cefdatabrowse.cefdatabrowse:main'
        ]
    }
)


class OnlyGetScriptPath(install):
    def run(self):
        self.distribution.install_scripts = self.install_scripts
        db_base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(db_base, 'databrowse.bat'), 'wb') as bat:
            bat.writelines(['@echo off \r\n',
                            '{} %* \r\n'.format(os.path.join(self.distribution.install_scripts, "databrowse.exe"))])

        execdir = raw_input("Enter execution directory: ")
        copyfile(os.path.join(db_base, 'databrowse.bat'), os.path.join(execdir, 'databrowse.bat'))


def get_setuptools_script_dir():
    dist = Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
    dist.dry_run = True  # not sure if necessary, but to be safe
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return dist.install_scripts


if platform.system() == "Windows":
    get_setuptools_script_dir()
