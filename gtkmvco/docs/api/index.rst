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

The :mod:`gtkmvc` Module
========================

.. module:: gtkmvc

.. note::
   Nothing in this module is exported by default, you have to prefix identifiers
   with the module name.

.. class:: Model
.. class:: ModelMT
.. class:: TextBufferModel
.. class:: ListStoreModel
.. class:: TreeStoreModel
.. class:: View
.. class:: Controller
.. class:: Observer

   These are shortcuts to classes from other modules. They are documented there.

.. function:: get_version()

   Get the version of the library as imported.

   :rtype: tuple of integers

.. function:: require(version)

   Takes a dotted string or sequence of integers and raises :exc:`AssertionError`
   if it exceeds :func:`get_version`.
