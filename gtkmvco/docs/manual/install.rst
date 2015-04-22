Installation
************

Dependencies
------------

The required dependencies are:

 * Python 2.4.3
 * GTK+ 2.10.4
 * PyGTK 2.10.1

or newer.


Installation
------------

You can install *gtkmvc3* from source files, with the provided standard
:file:`setup.py` based on :mod:`distutils`::

 $> python setup.py install

Alternatively, Windows users may use the binary installer, and
GNU/Linux users may check if their distribution offers packages for an
easy installation. For example under `Ubuntu Linux 10.10` *Maverick
Meerkat*::

  $> apt-cache search gtkmvc3
  python-gtkmvc3 - model-view-controller (MVC) implementation for pygtk
  python-gtkmvc3-doc - gtkmvc3 documentation, tutorial and examples

However, make sure that you are using the latest available version. 


Use without installing
----------------------

*gtkmvc3* is designed to work also without being installed, so it is
possible to keep it locally. A typical directory tree of an
application based on *gtkmvc3* may be::

  top-level
     |
     |-------- main.py, setup.py, ...
     | 
     |-------- resources
     |             |------ bin 
     |             |------ glade
     |             |------ images
     |             |------ ...
     |             +------ external         <---- sys.path contains this
     |                        |--- ...
     |                        +--- gtkmvc3   <---- PUT IT HERE!
     |-------- src
     |          |------ models
     |          |------ views
     |          |------ controllers
     |          +------ ...
     |
     +-------- ...

By prepending `external` to :mod:`sys.path`, *gtkmvc3* will be found as
if it was installed regularly.

Section :doc:`progen` presents a little utility to build a project
based on *gtkmvc3* from scratch. `progen` generates a structure similar
to this, if you decide to distribute *gtkmvc3* along with your
application.


Distribution of your application
--------------------------------

If you want, you can distribute *gtkmvc3* along with your application,
for example as depicted above. This helps to minimize the dependencies
of your application.


License and Copyright
---------------------

*gtkmvc3* is `Free Software <http://www.fsf.org/>`_ distributed under
the `GNU LESSER GENERAL PUBLIC LICENSE
<http://www.gnu.org/licenses/lgpl-2.1.html>`_ (LGPL) version 2 or later
at your choice.

You can distribute your application in any form (even binaries only)
and for any purpose (even commercial). However if you have modified
any file of *gtkmvc3*, you will have to distribute the source files of
your modified version of *gtkmvc3*. For any detail refer to the LGPL
License Terms.

Copyright (C) 2010-2015 by Roberto Cavada <roboogle AT gmail.com>.
