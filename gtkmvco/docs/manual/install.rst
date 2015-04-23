Installation
************

Dependencies
------------

The required dependencies are:

 * Python 2.6+ or Python 3.1 or later
 * GTK+ 3
 * gobject-introspection

See `The Python GTK+ 3 Tutorial
<https://python-gtk-3-tutorial.readthedocs.org/en/latest/install.html>`_
for more information

To use it, you can either use locally without installing it
(preferable), or install it.


Use without installing
----------------------

*gtkmvc3* is designed to work without being installed, so it is
possible to keep it locally. This is indeed the preferable solution,
as it avoid adding an addition dependency of your application, and
allows to use the latest available version of *gtkmvc3*.

A typical directory tree of an application based on *gtkmvc3* may be::

  top-level
     |
     |-------- main.py, setup.py, ...
     |
     |-------- resources
     |             |------ bin
     |             |------ ui
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


Installation
------------

You can install *gtkmvc3* from source files, with the provided standard
:file:`setup.py` based on :mod:`distutils`::

 $> python setup.py install

Alternatively, Windows users may use the binary installer, and
GNU/Linux users may check if their distribution offers packages for an
easy installation (`python-gtkmvc3`).

However, make sure that you are using the latest available version.

.. attention:: Package `python-gtkmvc` is the old version of gtkmvc3,
   as it supports GTK2 and pygtk.


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
