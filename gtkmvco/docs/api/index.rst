.. gktmvc documentation master file, created by
   sphinx-quickstart on Wed Apr 28 11:30:03 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GTK MVC |version| Library Reference
===================================

.. sectionauthor:: Tobias Weber

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

.. automodule:: gtkmvc

.. autofunction:: get_version()

.. autofunction:: require(version)
