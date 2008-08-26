#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

from distutils.core import setup

setup(name="python-gtkmvc",
      version="1.2.2",
      description="Model-View-Controller and Observer patterns "\
                  "for PyGTK2",
      author="Roberto Cavada",
      author_email="cavada@fbk.eu",
      license="LGPL",
      url="http://pygtkmvc.sourceforge.net/",
      packages=['gtkmvc', 'gtkmvc.support', 'gtkmvc.adapters', 'gtkmvc.progen'],
      package_data={'gtkmvc.progen': ['progen.glade']},
      scripts=['scripts/gtkmvc-progen'],
     )
