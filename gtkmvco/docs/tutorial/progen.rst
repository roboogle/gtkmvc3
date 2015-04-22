.. include:: common.rst 

Generating a standard project from scratch
==========================================

Since version 1.2.0 a little application called *gtkmvc3-progen*
is available to help setting up from scratch a new application based
on |gtkmvc3|. *gtkmvc3-progen* is available both as a command-line
program and as a GUI application. 

.. figure:: images/progen.png
   :width: 12cm
   
   *gtkmvc3-progen* GUI at work

By the way, the source code of *gtkmvc3-progen* is simple and can
be exploted to learn more about gtkmvc3-based applications. A model
carries out all the work, and a controller/view pair provides the
GUI if needed.

*gtkmvc3-progen* can be executed either locally from the script
directory, or can be executed as any other program if |gtkmvc3| has
been officially installed on the hosting system.

From the local script directory: ::

 $> python gtkmvc3-progen name=hello author="Roberto Cavada" gui=no
 
If |gtkmvc3| was installed: ::

 $> gtkmvc3-progen name=hello author="Roberto Cavada" gui=no

"name=hello" is an example of setting of a property that customizes the
way *gtkmvc3-progen* works. See the user manual for a full list. 

A new directory called ``hello`` will be created in the current
directory (as property *destdir* is "." by default. 

Let us run now the resulting application skeleton. ::

 $> cd hello
 $> ls
 hello.py  resources  src
 
 $> python hello.py


.. figure:: images/hello.png
   :width: 8cm
   
   The skeletal hello application
