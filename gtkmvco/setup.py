#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

from distutils.core import setup

setup(name="python-gtkmvc",
      version="1.0.0",
      description="Model-View-Controller and Observer patterns "\
                  "for PyGTK2",
      author="Roberto Cavada",
      author_email="cavada@irst.itc.it",
      license="LGPL",
      url="http://pygtkmvc.sourceforge.net/",
      packages=['gtkmvc', 'gtkmvc.support'],
     )
