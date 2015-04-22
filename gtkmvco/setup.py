#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author: Ionutz Borcoman <borco@go.ro>
#
# ----------------------------------------------------------------------

try:
    from setuptools import setup

except:
    from distutils.core import setup
    pass

from gtkmvc3 import get_version


setup(name="python-gtkmvc3",
      version=".".join(map(str, get_version())), 
      description="Model-View-Controller and Observer patterns "\
                  "for developing pygtk-based applications",
      author="Roberto Cavada",
      author_email="roboogle@gmail.com",
      license="LGPL",
      url="https://github.com/roboogle/gtkmvc3/",
      packages=['gtkmvc3', 'gtkmvc3.support', 'gtkmvc3.adapters', 'gtkmvc3.progen'],
      package_data={'gtkmvc3.progen': ['progen.glade']},
      scripts=['scripts/gtkmvc3-progen'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: GTK Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          ],
      
     )
