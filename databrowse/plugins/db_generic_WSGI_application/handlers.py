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
""" plugins/handlers/dbh_wsgi.py - Generic WSGI Handler """

import os.path


def dbh_wsgi(path, contenttype, extension, roottag, nsurl):
    """ Generic WSGI Handler - Returns wsgi_generic for all wsgi files """
    if extension.lower() == "wsgi" and os.path.basename(path) != "monthly_rpt.wsgi":
        return "db_generic_WSGI_application"
    else:
        return False
