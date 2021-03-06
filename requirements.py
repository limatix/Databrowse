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
""" requirements.py - Script that determines current system and the required dependencies """

import sys
import os
from pip._internal import main as pipmain


def select_requirements_file():
    """
    Return the path to a requirements file based on some os/arch condition.
    """
    # operating system
    sys_platform = str(sys.platform).lower()
    linux = 'linux' in sys_platform
    windows = 'win32' in sys_platform
    cygwin = 'cygwin' in sys_platform
    solaris = 'sunos' in sys_platform
    macosx = 'darwin' in sys_platform
    posix = 'posix' in os.name.lower()

    # python version
    python_major = sys.version_info[0]
    python_minor = sys.version_info[1]

    if python_major == 2 and python_minor < 7:
        prefix = '26'
    else:
        prefix = ''

    if windows:
        return 'requirements/windows/windows%s.txt' % prefix
    elif macosx:
        return 'requirements/mac/mac%s.txt' % prefix
    elif linux:
        return 'requirements/linux/linux%s.txt' % prefix
    elif cygwin:
        return 'requirements/cygwin/cygwin%s.txt' % prefix
    elif solaris:
        return 'requirements/solaris/solaris%s.txt' % prefix
    elif posix:
        return 'requirements/posix/posix%s.txt' % prefix
    else:
        raise Exception('Unsupported OS/platform')


if __name__ == "__main__":
    f = select_requirements_file()
    pipmain(['install', '-r', f])
