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
2. Subviews  can be connected to known containers widgets into the
   containing view, like in the example.
3. Class View provides the method ``get_top_widget`` that returns the
   View's top level widget.
4. Both attributes ``glade`` and ``top`` can be overridden or
   substituted by View's constructor equivalent parameters. 


------
Models
------

A model is a class that is intended to contain the application's
logic. A model contains data and methods, and a subset of the data can be
declared to be *observable*. ::

 from gtkmvc import Model
 class MyModel (Model):
    data1 = 10
    data2 = "a string"
    data3 = "a list of strings".split()

    __observables__ = ("data1", "data3")

    pass # end of class

A model must derive from ``gtkmvc.Model`` [#fn1]_ which derives from
``Observer`` as models may be interested in observing themself and
other models (see *Observers* below).

*Observable Properties* are declared through the special attribute
``__observables__`` which is a sequence of string names.

In the example class attributes ``data1`` and ``data3`` are declared
to be observable properties. Names in ``__observables__`` can contain
wilcards [#fn2]_ and all attributes in the class not beginning with a
double underscore ``__`` will be checked for matching. For example
``__observables__ = ("data?",)`` would match ``data1``, ``data2`` and
``data3``.

Observable Properties
~~~~~~~~~~~~~~~~~~~~~

Observable properties live into models and can be assigned to several
types of values, included lists, maps, and user defined classes.  For
all details about the observable properties, see the User Manual for
the details.

1. Value Properties
"""""""""""""""""""
*Value Properties* are intended to hold values which when are
*re-assigned* observers are notified. ::

 from gtkmvc import Model
 class MyModel (Model):
    data1 = 5
    data2 = [1,2,3]
    data3 = {}
    data4 = SomeClass()
    __observables__ = ("data?", )
    pass # end of class

 m = MyModel()
 # here the properties are re-assigned
 m.data1 += 15  
 m.data2 = [4,5,6]
 m.data3 = { "key" : "value" }
 m.data4 = SomeOtherClass() 

Every time a value property gets reassigned, observers observing it
will be notified.

2. Mutable containers
"""""""""""""""""""""
When the value of an observable property is a mutable object, like a
sequence or a map, observers may be interested in being notified when
a method is called on the object itself::

 # here the object contents are changed:
 m.data2.append(7)
 m.data3['key2'] = "value for key2"
 

3. Mutable class instances
""""""""""""""""""""""""""
Properties can be instances of mutable classes. Like for containers
objects, observers may be interested in being notified when a method
changing the object is called::

 # here the object contents are changed:
 m.data4.some_method_changing_the_instance()

Of course it is needed to declare method
``SomeOtherClass.some_method_changing_the_instance`` to be
observable. For example::

 from gtkmvc.model import Model, observable
 class SomeOtherClass (observable.Observable):
    """This is a class that is thought to be integrated into the
    observer pattern. It is declared to be 'observable' and the
    methods which we are interested in monitoring are decorated
    accordingly"""

    val = 0

    @observable.observed # this way the method is declared as 'observed'
    def change(self): self.val += 1

    pass #end of class

Observable properties derive from class ``Observable`` and methods
that change the content of the instance can be declared by using the
``observed`` decorator like in the example. 

Ok, but what if my class is already existing? It is less natural, but
gtkmvc supports observable properties of already existing classes'
instances::

 from gtkmvc import Model, Observer

 class ExistingClass (object):
    """This is an already existing class whose code is not intended to
    be changed. Instead, when instantiated into the model, it is
    declared in a particular manner, so that the model can recognise
    it and wrap it in order to monitor it"""
    
    val = 0 

    def change(self): self.val += 1
    pass #end of class


 class MyModel (Model):

    obj = (ExistingClass, ExistingClass(), ('change',))
    __observables__ = ["obj"]

    pass # end of class

The triplet must contain the name of the class, the instance, and a
list naming the methods whose calls can be observed by observers. 

4. Signals
""""""""""
Sometimes the models want to communicate to observers that *events*
occurred. For this ``Signal`` can be used as property value::

 from gtkmvc import Model, observable
 class MyModel (Model):
    sgn = observable.Signal()
    __observables__ = ("sgn",)
    pass

 m = MyModel()
 m.sgn.emit()
 m.sgn.emit("A value can also be passed here")


---------
Observers
---------

An observer is a class that is interested in being notified when some
observable properties into one or models it observes got changed.
For example::

 from gtkmvc import Observer
 class MyObserver (Observer):
        
    def property_data1_value_change(self, model, old, new):
        print "Property data1 changed from %d to %d"
        return

    def property_data3_after_change(self, model, instance, name, res, args, kwargs):
        print "data3 after change:", instance, name, res
        return
    pass # end of class

Methods in the observer that are intended to receive notifications use
a *naming convention*. Here you can see two different types of
notifications:

1. Value change notification.
2. List modifications.

Here is how the model and the observer can be connected/unconnected::

 m = MyModel()
 o = MyObserver()
 o.observe_model(m)
 # ...
 o.relieve_model(m)

``Observer`` constructor optionally takes a model that it registers
into::

 m = MyModel()
 o = MyObserver(m)
 # ...
 o.relieve_model(m)

Now let's try to modify the assigned value to a property::
 
 m.data1 += 1
 print ">>> Here m.data is", m.data1

 m.data3.append("Roberto")
 m.data3[0] = "gtkmvc"
 m.data3[1] = "improves your life"
 
The execution ot this example produces the following output::

 Property data1 changed from 10 to 11
 >>> Here m.data is 11
 data3 after change: ['a', 'list', 'of', 'strings', 'Roberto'] append None
 data3 after change: ['gtkmvc', 'list', 'of', 'strings', 'Roberto'] __setitem__ None
 data3 after change: ['gtkmvc', 'improves your life', 'of', 'strings', 'Roberto'] __setitem__ None

Of course an observer is not limited to observe one model::

 m1 = MyModel()
 o = MyObserver(m1) # o observes m1
 m2 = AnotherModel()
 o.observe_model(m2) # o observes also m2 now

It is usual to see models observing other models, like siblings or
sub-models in model hierarchies. For this reason class ``Model``
derives from class ``Observer``::

 m3 = AnotherModel()
 m3.observe_model(m2) # m3 observes m2


-----------
Controllers
-----------

Controllers are the most complex structures that are intended to:

1. Contain the GUI logics.
2. Connect one model and one or more views, without making them know.
3. Observe the model they are connected to.
4. Provide handlers for gtk signals (declared in the views connected to it)
5. Setting up widgets that depend on the model. For example setting up
   of ``gtk.TreeView`` whose ``gtk.TreeModel`` lives within the model. 
6. Setting up :ref:`adapters`


.. _adapters:

--------
Adapters
--------


.. rubric:: Footnotes

.. [#fn1] Or any class derived from ``gtkmvc.Model``, see the User
.. [#fn2] See Python module 
   `fnmatch <http://docs.python.org/library/fnmatch.html>`_ 
   for information about accepted wilcards


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

