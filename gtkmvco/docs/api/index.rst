.. gktmvc documentation master file, created by
   sphinx-quickstart on Wed Apr 28 11:30:03 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GTK MVC |version| documentation
===============================

.. toctree::
   :maxdepth: 2

   model
   view
   controller
   adapters
   observable
   observer
   support
   metaclasses
   factories
   controlflow

Installation
============

The required dependencies are:

 * Python 2.4.3
 * GTK+ 2.10.4
 * PyGTK 2.10.1

or newer. ::

 setup.py install

The :mod:`gtkmvc` Module
========================

.. module:: gtkmvc

.. note::
   Nothing in this module is exported by default, you have to prefix identifiers
   with the module name.

.. class:: Model
   :noindex:
.. class:: ModelMT
   :noindex:
.. class:: TextBufferModel
   :noindex:
.. class:: ListStoreModel
   :noindex:
.. class:: TreeStoreModel
   :noindex:
.. class:: View
   :noindex:
.. class:: Controller
   :noindex:
.. class:: Observer
   :noindex:

   These are shortcuts to classes from other modules. They are documented there.

.. function:: get_version()

   Get the version of the library as imported.

   :rtype: tuple of integers

.. autofunction:: require(version)
