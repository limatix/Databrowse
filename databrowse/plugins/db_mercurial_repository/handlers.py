#!/usr/bin/env python
###############################################################################
## Databrowse:  An Extensible Data Management Platform                       ##
## Copyright (C) 2012-2013 Iowa State University                             ##
##                                                                           ##
## This program is free software: you can redistribute it and/or modify      ##
## it under the terms of the GNU General Public License as published by      ##
## the Free Software Foundation, either version 3 of the License, or         ##
## (at your option) any later version.                                       ##
##                                                                           ##
## This program is distributed in the hope that it will be useful,           ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of            ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             ##
## GNU General Public License for more details.                              ##
##                                                                           ##
## You should have received a copy of the GNU General Public License         ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>.     ##
###############################################################################
""" plugins/handlers/dbh_mercurial_repository.py - Mercurial Repository Handler """

import subprocess
import os


def dbh_directory_mercurial(path, contenttype, extension):
    """ Generic Image Directory Handler - Returns directory_image for all directories with more than 50 percent images """
    if contenttype.startswith("inode/directory") or contenttype.startswith("application/x-directory") or contenttype.startswith("directory"):
        if subprocess.call(['/usr/bin/hg', '--cwd', path, '-q', 'stat'], stdout=open(os.devnull), stderr=open(os.devnull)) == 0:
            return "db_mercurial_repository"
        else:
            return False
    else:
        return False