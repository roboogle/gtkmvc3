.. pygtkmvc documentation master file, created by sphinx-quickstart on Mon Mar 23 18:58:19 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
gtkmvc in 30 minutes
====================

This document presents gtkmvc for those that are in hurry, or for
curious people who want to have a quick overview of gtkmvc features
and capabilities.


.. warning:: 
 This document is not complete. For a complete information refer to
 the User Manual and to the Tutorial, both coming along with gtkmvc.

 It is assumed you already know *Python*, *pygtk* and have some
 experience with *design issues*. 
 However, here you will find a short introduction
 presenting the main actors that are going to play a role into an
 GUI application based on gtkmvc. 


------------
Introduction
------------

What is gtkmvc, and what it does
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

gtkmvc is a think framework for developing GUI applications with
Python and the pygtk toolkit.

1. It helps you to organize the source code of your application.
2. It provides some support for making views out glade files.
3. It separates the data/logic of your application (the *model*) from the presentation layer (the *view*).
4. It tries to be as much transparent as possible wrt your application. 

Some terminology
~~~~~~~~~~~~~~~~

**Model**
        Contains the logic of the application, the data that are
        independent on the GUI.
        For example, in a *music player*:

        * The list of the mp3 file names.
        * The methods for playing the files in the list.
        * The methods for contacting a server in the Internet for
          downloading some new music file.

**Observer**
        It is an entity interested in observing some parts of one or
        more Models. Observers are used to react to certain changes in
        models without creating explicit dependencies or links with them.

**Observable Property**
        It is an attribute of the Model, that is supposed to be
        *observable* by one or more observers connected to the model.
        For example:

        * The property ``current_mp3_file`` that is the currently
          played mp3 file name.
        * The property ``current_perc`` holding the % of the mp3 file
          that is being played.

**View**
        Contains a set of widgets, and the methods for
        manipulating them. The set of widgets can be build out of a
        *glade* file. E.g:

        * A method for making a bunch of widgets visible/unvisible
        * A method for making the view appearing in same manner under
          some circumstances.

**Controller**
        It is a particular kind of observer, connected to one model
        and to one or more views. It contains the GUI logic, and all
        handlers for GUI signals. E.g.

        * A method for making the model play selected file when the
          ``play`` button is clicked.
        * The code that makes a progress bar advance in the view
          as the music file is played by the model. 

**Adapter**
        Adapts the content of one widget (or a set of widgets) into
        the view with one observable property into the model. An
        adapter keeps the content of an observable property
        up-to-dated with the content of a widget, and
        viceversa. Adapters live into the controllers. 
        E.g.

        * An adapter that bounds property ``current_perc`` with a
          progress bar widget into the view.


.. note:: 
 All these entities are now presented more in details.   
          
-----
Views
-----

A view is a class that is intended to be a container for widgets. ::

 import gtk
 from gtkmvc import View

 class MyView (View):
    glade = "view_glade_file.glade"
    top = "name_of_top_level_widget"

    def __init__(self):
        View.__init__(self)
        
        # possible construction of manual widgets
        self['name_of_new_label'] = gtk.Label("A label manually constructed!")
        self['some_container_in_glade_file'].pack_start(self['name_of_new_label'])

        # possible setup of all widgets
        # ...
        return

    def set_sentitivity(self, flag):
        for wid in (self[x] for x in ('widget1', 'widget2', )):
            wid.set_sensitive(flag)
            pass
        return

    pass # end of class

Your view is derived from base class ``gtkmvc.View`` that offers
several services:

1. Attributes ``glade`` that is used to tell the view which glade file
   its widgets are taken from.
2. Attributes ``top`` that is used to tell which is the widget name in
   the glade file tree to be taken as the root widget. It is also
   possible to specify a list of names to pick a set of trees.
3. The view instance can be used a container (a dictionary) of
   widgets, both for accessing named widgets in glade files, and for
   creating new widgets manually.

Views can be decomposed into a hierarchy of views. For example::

 import gtk
 from gtkmvc import View

 class MySuperView (View):
    glade = "view1.glade"
    top = "view1_top_widget"

    def __init__(self):
        View.__init__(self)

        self.subview = MySubView()

        # connects the subview to a widget in the containing view
        self['some_container'].add(self.subview.get_top_widget())
        return
    pass # end of class
 
 class MySubView (View):
    def __init__(self):
        View.__init__(self, glade="view2.glade", top="view2_top_widget")
        # setting of sub view...
        return
    pass # end of class

As you can see:

1. It is possible to construct a hierarchy of views to deal with view
   composition.
2. Subviews can be connected to known containers widgets, like in the
   example.
3. Class View provides the method ``get_top_widget`` that returns the
   View's top level widget.
4. Both attributes ``glade`` and ``top`` can be overridden or
   substituted by View's constructor equivalent parameters. 

    
==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

