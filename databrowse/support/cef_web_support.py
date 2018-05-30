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
###############################################################################
""" support/dummy_web_support.py - Classes to encapsulate Web/WSGI functionality """

import os
import os.path
import cgi
import platform
from lxml import etree
import databrowse.support


class wsgi_req:
    """ A simple wrapper for the wsgi request """

    environ = []

    def start_response(self, status, headers):
        for header in headers:
            self.response_headers[header[0]] = header[1]
        pass       # start_response function to call before finalization

    filename = None             # name of script that was called
    dirname = None              # name of directory containing script that was called
    unparsed_uri = None         # request URI
    form = None                 # form parameters
    status = None               # Status string
    output = None               # Output string
    response_headers = None     # Dictionary of response headers
    output_done = None          # Flag: Have we generated output yet or not?

    def __init__(self, filename, params):
        """ Load Values from Request """
        fs = None
        os.environ['QUERY_STRING'] = str('&'.join(['%s=%s' % (key, params[key]) for key in params]))
        fs = cgi.FieldStorage(keep_blank_values=1)
        self.form = fs
        # print("Web Support params: %s" % params)
        self.status = [200, "OK"]
        self.response_headers = {}
        self.response_headers['Content-Type'] = 'text/html'
        self.response_headers['Access-Control-Allow-Origin'] = '*'
        self.output_done = False

        if "debug" in self.form:
            self.response_headers["Content-Type"] = "text/plain"    # can switch to "text/plain" for debugging -- add ?debug to end of URL
            # config.req.output=str(config.req.form)+str(config.req.form["debug"])
            pass

        pass

    def return_page(self):
        """ Send Webpage Output """
        #self.response_headers['Content-Length'] = str(len(self.output))
        #self.start_response(self.status, self.response_headers.items())
        #self.output_done = True
        return self.output

    def return_error(self, status=500):
        """ Return Error Message """
        if status == 400:
            self.status = [status, 'Bad Request']
        elif status == 401:
            self.status = [status, 'Unauthorized']
        elif status == 403:
            self.status = [status, 'Forbidden']
        elif status == 404:
            self.status = [status, 'Page Not Found']
        elif status == 405:
            self.status = [status, 'Method Not Allowed']
        elif status == 406:
            self.status = [status, 'Not Acceptable']
        elif status == 500:
            self.status = [status, 'Internal Server Error']
        elif status == 501:
            self.status = [status, 'Not Implemented']
        elif status == 503:
            self.status = [status, 'Service Unavailable']
        else:
            self.status = [status, 'Internal Server Error']

        #self.output_done = True
        self.response_headers = {}
        self.response_headers['Content-Type'] = 'text/html'
        self.response_headers['Content-Length'] = str(len(self.status[1].encode('utf-8')))
        #self.start_response(self.status, self.response_headers.items())
        raise Exception(self.status[1])

    pass


class style_support:
    """ Class containing support functionality for xslt stylesheet compliation """

    _style_dict = {}

    class StyleException(Exception):
        pass

    def __init__(self):
        self._style_dict = {}

    def AddStyle(self, namespace, content):
        if (namespace) in self._style_dict:
            # Check to ensure new value is the same as the current value, otherwise throw error
            if self._style_dict[namespace] != content:
                raise self.StyleException("Multiple stylesheets using the same namespace and mode exist")
        else:
            self._style_dict[namespace] = content
            pass
        pass

    def IsStyleLoaded(self, namespace):
        if (namespace) in self._style_dict:
            return True
        else:
            return False
        pass

    def GetStyle(self):
        stylestring = ""
        for i in self._style_dict:
            stylestring = stylestring + self._style_dict[i]
            pass
        return stylestring

    pass


class menu_support:
    """ Class containing support functionality for xslt stylesheet compliation """

    _menu = []

    class MenuException(Exception):
        pass

    def __init__(self, siteurl, logouturl, username):
        self._menu = []
        topmenu = etree.Element('{http://thermal.cnde.iastate.edu/databrowse}navbar', xmlns="http://www.w3.org/1999/xhtml")
        menuitem = etree.SubElement(topmenu, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
        menulink = etree.SubElement(menuitem, '{http://www.w3.org/1999/xhtml}a', href=siteurl)
        menulink.text = "Databrowse Home"
        # menuitem = etree.SubElement(topmenu, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
        # menulink = etree.SubElement(menuitem, '{http://www.w3.org/1999/xhtml}a', href=logouturl)
        # menulink.text = "Logout " + username
        self.AddMenu(topmenu)

    def AddMenu(self, xml):
        self._menu.append(xml)

    def GetMenu(self):
        menu = etree.XML('<db:navigation xmlns="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse"/>')
        for item in self._menu:
            menu.append(item)
            pass
        pass
        return menu

    pass


class web_support:
    """ Class containing support functionality for web operations """
    req = None                  # request class object
    style = None                # style class object
    menu = None                 # menu class object
    req_filename = None         # requested filename
    webdir = None               # directory containing the requested file
    confstr = None              # string containing optional configuration file
    email_sendmail = None       # email:  sendmail location
    email_admin = None          # email:  admin email for alert reports, etc
    email_from = None           # email:  email address mail should appear from
    administrators = None       # dictionary containing administrator list
    limatix_qautils = None      # Path to limatix-qautils
    qautils = None              # Path to old checklist QAutils
    sitetitle = None            # site title
    shorttitle = None           # abbreviated site title
    remoteuser = None           # Username
    siteurl = None              # URL to site root directory
    resurl = None               # URL to resources directory
    logouturl = None            # URL to logout
    dataroot = None             # Path to root of data directory
    pluginpath = None           # Path to root of plugin directory (default plugins)
    icondbpath = None           # Path to icon db (default support/iconmap.conf)
    hiddenfiledbpath = None     # Path to hidden file list (default support/hiddenfiles.conf)
    directorypluginpath = None  # Path to the directory plugin list (default support/directoryplugins.conf)
    checklistpath = None        # Relative path to checklist directory
    stderr = None               # filehandle to server error log
    seo_urls = None             # Boolean indicating whether SEO URLs are enabled - requires URL rewrites
    debugging = None            # Boolean indicating whether debugging messages should be shown

    def __init__(self, filename, params):
        self.req = wsgi_req(filename, params)
        #self.reqfilename = self.req.filename
        #self.webdir = os.path.dirname(self.reqfilename)
        #self.stderr = environ["wsgi.errors"]
        self.style = style_support()

        # Try to Load Optional Configuration File
        #try:
            #conffile = file(os.path.join(os.path.dirname(self.reqfilename), "web.conf"))
            #self.confstr = conffile.read()
            #conffile.close()
            #exec self.confstr
        #except:
        #    pass

        # Set Default Configuration Options

        self.dataroot = params['dataroot']

        if platform.system() == "Linux":
            self.path = "127.0.0.1/" + params['path']
        else:
            self.path = params['path']

        if self.siteurl is None:
            self.siteurl = params['dataroot']
            pass

        if self.resurl is None:
            self.resurl = os.path.abspath(params['install'] + "/databrowse_wsgi/resources")
            self.resurl = "/".join(self.resurl.split("\\"))
            pass

        if self.webdir is None:
            self.webdir = params['install'] + "/databrowse_wsgi"
            pass

        if self.logouturl is None:
            self.logouturl = "http://localhost/logout"
            pass

        #if not environ["REMOTE_USER"]:
        #    raise Exception("User Not Logged In")
        #else:
        #    self.remoteuser = environ["REMOTE_USER"]

        #if self.pluginpath is None:
        #    self.pluginpath = os.path.join(self.webdir, "plugins")
        #    pass

        if self.icondbpath is None:
            self.icondbpath = os.path.join(os.path.dirname(databrowse.support.__file__), "iconmap.conf")
            pass

        if self.hiddenfiledbpath is None:
            self.hiddenfiledbpath = os.path.join(os.path.dirname(databrowse.support.__file__), "hiddenfiles.conf")
            pass

        if self.directorypluginpath is None:
            self.directorypluginpath = os.path.join(os.path.dirname(databrowse.support.__file__), "directoryplugins.conf")
            pass

        if self.checklistpath is None:
            self.checklistpath = r"/SOPs"

        if self.email_sendmail is None:
            self.email_sendmail = "/usr/lib/sendmail -i"
            pass

        if self.email_admin is None:
            self.email_admin = "scheirer@iastate.edu"
            pass

        if self.email_from is None:
            self.emailfrom = "scheirer@iastate.edu"
            pass

        if self.limatix_qautils is None:
            self.limatix_qautils = r'/Users/nscheirer/Documents/dev/databrowse-utils/limatix-qautils'
            pass

        if self.qautils is None:
            self.qautils = r'/Users/nscheirer/Documents/dev/databrowse-utils/QAutils'
            pass

        if self.administrators is None:
            self.administrators = {"sdh4": "Steve Holland", "tylerl": "Tyler Lesthaeghe", "scheirer": "Nathan Scheirer"}
            pass

        if self.sitetitle is None:
            self.sitetitle = "Databrowse Project Browser"
            pass

        if self.shorttitle is None:
            self.shorttitle = "databrowse"
            pass

        if self.seo_urls is None:
            self.seo_urls = True
            pass

        if self.debugging is None:
            self.debugging = False
            pass

        self.menu = menu_support(self.siteurl, self.logouturl, "")

        assert(self.dataroot is not None)

        pass

    pass
