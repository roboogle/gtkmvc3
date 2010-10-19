Details of implementation
=========================

This section presents some details regarding the implementation of the
*MVC-O* framework in Python.

Models, Views and Controllers in detail
---------------------------------------

The *MVC-O* framework essentially supplies three base classes which
implement respectively a View, a Model and a Controller. Developers
have to derive custom classes from the base classes set, adding the
implementation which depends on the application semantics.

Model base class
   Supplies servicing for:

   * Fully automatic Observable Properties 

   * Automatic broadcast notification when observable properties
     change.

   * Transparent notifications to observers running in the *PyGTK*
     loop, even when sent by models running from other threads.

View base class
   Supplies servicing for:

   * Automatic widgets tree registration. Input can be a set of root
     widgets stored inside a *Glade* File, or a completely customized widgets
     hierarchies.
   * Automatic signals connection to methods supplied by the
     associated Controller(s).
   * Widget retrieval inside the set of hierarchy. Widget can be
     accessed by using the name they have been defined from within
     *Glade*, at design time, or that have been specified when creating
     widgets by hand.
   * Support for custom widgets declared in *Glade* files.

Controller base class
   Supplies servicing for:

   * Automatic registration as observers of the associated Model.
   * Easy access to the associated Model and View for any derived
     class.
   * Construction of columns and renderers of
     ``gtk.TreeView`` widgets.
   * Instantiation of *adapters*.


.. _MODELS:

Models
------

Models must be used to hold the *data* or *logic* of the
application. They can be connected to observers (like Controllers) by
a mechanism detailed by section :ref:`OPD`.  It is important to note
that apart from during the registration phase, the model does not know
that there exists a set observers connected to it.

All the code strictly related to the data of the application (i.e. not
related to any view of those data) will live in the model class. 

There exist several model classes that users can derive their own
classes:

gtkmvc.Model
   Standard model class. The derived class does not
   multiple-derive from gobject classes, and there are not methods in
   the class that run from threads different from the *PyGTK* main loop
   thread. This is the base model class most likely users will derive
   their own models.
 
gtkmvc.ModelMT
   Multi-threading model used as the previous
   class Model, but to be used in all cases when the *PyGTK* main loop
   runs in a thread that is different from the thread running the
   model. This is the typical case of a model that needs to perform
   asynchronous operations that requires much time to complete, and
   that can be ran on a different thread making the *GUI* still
   responsive to the user actions. When the model's thread changes an
   observable property, corresponding notifications will be
   transparently delivered to the observers through their own thread.
 
gtkmvc.TreeStoreModel
   To be used as a base model class that
   derives both from ``Model`` and ``gtk.TreeStore``.
 
gtkmvc.TreeStoreModelMT
   To be used as a base model class that
   derives both from ``ModelMT`` and ``gtk.TreeStore``.
 
gtkmvc.ListStoreModel
   To be used as a base model class that
   derives both from ``Model`` and ``gtk.ListStore``.
 
gtkmvc.ListStoreModelMT
   To be used as a base model class that
   derives both from ``ModelMT`` and ``gtk.ListStore``. 
 
gtkmvc.TextBufferModel
   To be used as a base model class that
   derives both from ``Model`` and ``gtk.TextBuffer``.
 
gtkmvc.TextBufferModelMT
   To be used as a base model class that
   derives both from ``ModelMT`` and ``gtk.TextBuffer``.



Controllers
-----------

User's controllers must derive from this class.  A controller is
always associated with one model, that the controller can monitor and
modify. At the other side the controller can control a View.  Two
members called ``model`` and ``view`` hold the
corresponding instances.

The controller holds all the code that lives between data in model and
the data-presentation in the view. For example the controller will
read a property value from the model, and will send that value to the
view, to visualize it.  If the property in the model is an Observable
Property that the Controller is interested in monitoring, than when
somebody will change the property, the controller will be notified and
will update the view.


Model registration
^^^^^^^^^^^^^^^^^^

By default, a controller is also an Observer (see below) of the
corresponding Model, even when there is nothing to observe, or when
the controller is interested in observing nothing within the model.

Registration occurs automatically. If the observation is not wanted,
the derived controller can call method ``unregister_model``
from the instance constructor, to unregister itself.


.. _VR:D:

View registration
^^^^^^^^^^^^^^^^^

View registration (see View class, below) occurs upon Controller
construction. An important method of the class Controller that user
can override is ``register_view``, that the Controller will
call during View's registration. This can be used to connect custom
signals to widgets of the view, or to perform some initialization
that can be performed only when model, controller and view are
actually connected.  ``register_view`` gets the view
instance that is performing its registration within the
controller. See section :ref:`VR:EX` for an example of how this
mechanism may be exploited effectively.

Views
-----

User's views derive from base class ``gtkmvc.View``, that is
the only part specific for the *PyGTK* graphic toolkit.

A View is associated to a set of widgets. In general, this set
can be organized as a set of trees of widgets. Each tree can be
optionally be generated by using the *Glade* application 
(see section :ref:`GLEX`). 


Constructor
^^^^^^^^^^^

The View constructor is quite much complicated: ::

 def __init__(self, glade=None, top=None, parent=None)


glade
   can be either a string or a list of strings. In
   any case each provided string represents the file name of a *Glade*
   file. Typically each glade file contains a tree of (named) widgets.
    
   When not given (of ``None``) a corresponding class member
   called ``glade`` is checked. If also ``self.glade``
   is ``None`` it means that there is no *Glade* file and the
   widgets will have to be constructed manually.
  
top
   can be a string or a list of strings.  Each string
   provided is associated to the parameter ``glade`` content,
   and represent the name of the widget in the widgets tree
   hierarchy to be considered as top level. This lets the user to
   select single parts of the glade trees passed through parameter
   ``glade``.
 
   When not given (of ``None``) a corresponding class member
   called ``top`` is checked. If also ``self.top`` is
   ``None`` it means that the root widget name of the given
   *Glade* file will be taken as the name for the top level widget.

parent
   is the view instance to be considered parent of
   self. This can be used in special cases to construct hiearchical
   views. Generally this parameter is None or not given.

.. _VIEW:MANUAL:

A widgets container
^^^^^^^^^^^^^^^^^^^

The ``View`` class can also be considered a map, that
associates widget names to the corresponding widget objects. If file
``test.glade`` contains a Button that you called
``start_button`` from within *Glade*, you can create the view
and use it as follows: ::

 from gtkmvc import View
 
 class MyView (View):
   glade = 'test.glade'
   pass 
 
 m = MyModel()
 v = MyView()
 c = MyController(m, v)
 
 v['start_button'] # this returns a gtk.Button object


Instead of using only *Glade* files, sometimes the derived views create
a set of widgets on the fly. If these widgets must be accessed later,
they can be associated simply by (continuing the code above): ::

 v['vbox_widget'] = gtk.VBox()
 ...

The creation on the fly of new widgets should be performed within
the derived view cosntructor: ::


 from gtkmvc import View
 
 class MyView (View):
   def __init__(self, ):
     View.__init__(self, 'test.glade')
 
     self['vbox_widget'] = gtk.VBox()
     ...
     return
 
   pass 



Another important mechanism provided by the class View is the signals
auto-connection. By using *Glade* users can associate to widget's
signals functions and methods to be called when associated events
happen.  When performs the registration, the View searches inside the
corresponding Controller instance for methods to associate with
signals, and all methods found are automatically connected.


Custom widgets support
^^^^^^^^^^^^^^^^^^^^^^

A basic support for Custom widgets is provided since version 1.0.1.
Designers can specify custom widgets within a *Glade* file, and for
each custom widget they may specify a function name to be called to
build it. The specified function will be searched and invoked among
the ``View`` methods when the instance is
created. ``View``'s method for custom widget creation
has prototype: ::

 def func_name(self, str1, str2, int1, int2)

Creation functions are expected to return a widget object.

.. _VR:EX:

An example about View Registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A typical example of exploitation of the view registration mechanism
is the setup of a ``gtk.TreeView`` chain: construction of
``TreeView``, ``TreeViewColumn``,
``CellRenderers``, connection to the ``TreeModel``, etc.
As *Glade* does not provide a full support for these widgets, and as
the ``TreeModel`` lives in the model-side of the application,
their construction cannot occur within the View, but must be performed
within the Controller, that knows both the view and model sides. The
right time when this construction has to occur is the view
registration.

The idea is to have a ``TreeView`` showing an integer and a
string in two separated columns from a ``gtk.ListStore``.

Now suppose you created a project in *Glade* that contains a window,
some menus and other accessories, and a ``TreeView`` whose
properties are set in *Glade* in a comfortable manner (see figure
:ref:`fig:VR`).

.. _fig:VR:

.. figure:: images/treeview.png
   :width: 12 cm
   :align: center

   Designing a ``TreeView`` by means of *Glade*

In the example, the ``TreeView`` has been called
``tv_main``, and after View creation the widget will be
available with that name. ::

 from gtkmvc import View
 
 class MyView (View):
   def __init__(self):
     View.__init__(self, 'test.glade')
     #...
     return
   pass 


The ``ListStore`` is of course not contained in the view, but
it is created and stored in the Model. If the model had to be also a
``ListStore`` (i.e.  derived from it) ``MyModel`` had to
derive from ``gtkmvc.ListStoreModel`` instead of
``Model``. To keep things easier, Has--A relationship is
chosen. ::

 from gtkmvc import Model
 import gtk
 import gobject
 
 class MyModel (Model):
   def __init__(self):
     Model.__init__(self)
 
     self.list = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
     return
   pass 

The controller has the responsibility of connecting the
``TreeView`` and the ``ListStore``, and it creates
columns and renderers as well. Construction must occur after View has
been created. More precisely, the ideal time is during
view-registration. ::

 from gtkmvc import Controller
 import gtk

 class MyCtrl (Controller):
 
   def register_view(self, view):
     tv = self.view['tv_main']    
     tv.set_model(self.model.list) # sets the model
 
     # creates the columns
     cell = gtk.CellRendererText()
     col = gtk.TreeViewColumn('Int', cell, text=0)
     tv.append_column(col)
 
     cell = gtk.CellRendererText()
     col = gtk.TreeViewColumn('String', cell, text=1)
     tv.append_column(col)
 
     # registers any treeview-related signals...
     return
 
   pass # end of class 


.. _OPD:

Observable Properties in details
--------------------------------

The mechanism of the Observable Properties (*OP*) is fully automatic,
since its management is carried out by the base class
``Model``.

Basically the user derives from class ``Model`` (or the others
listed in section :ref:`MODELS`). 

Properties are listed as class variables with default values, and
to declare which variables in the model are also observable,
special class variable __observables__ can be used. 

__observables__ is a tuple (or a list) of names of class variables that are
observable. Names can contain wilcards like ``*`` to match
any sequence of characters, ``?`` to match one single
character, etc. See module ``fnmatch`` in *Python* library
for other information about possible use of wilcards in
names. Important to say that if wilcards are used, names starting
with a double underscore ``__`` will be not matched.

It is also possible for the user to add a class variable called
__properties__. This variable must be a map, whose elements' keys are names
of properties, and the associated values are the initial
values. Using __properties__ is complementary to the use of __observables__, but it
is now deprecated and should be avoided in new code.

For example, suppose you want to create an *OP* called ``name`` 
initially associated to the string value "Rob": ::

 from gtkmvc import Model
 
 class MyModel (Model):
   name = 'Rob'
   __observables__ = ("name",)
 
   def __init__(self):
     Model.__init__(self)
     # ...
     return
 
   pass # end of class


This is another example showing the usage of wilcards in names: ::

 from gtkmvc import Model
 
 class MyModelWithWilcards (Model):
   firstname = 'Rob'
   secondname = 'Mario'
   surname = 'Cavada'
   energy = 0.2 # needs holidays!
   entropy = 1.0
   enology = "good science"
 
   __observables__ = ("*name", "en????y")
   pass # end of class


In the example, all properties but ``energy`` are declared
to be observable.

Old-style (deprecated) observable properties declaration that makes
use of special variable __properties__ is shown here. This example is shown
only for completeness and should be not used anymore in new code. ::

 from gtkmvc import Model
 
 class MyModelDeprecated (Model):
 
  __properties__ = { 
     'name' : 'Rob',
   }
   pass # end of class



By using a specific meta-class, property ``name`` will be
automatically added, as well as all the code to handle it.

This means that you may use the property in this way: ::

 m = MyModel()
 print m.name  # prints 'Rob'
 m.name = 'Roberto' # changes the property value

What's missing is now an observer, to be notified when the property
changes. To create an observer, derive your class from base class
``gtkmvc.Observer``. ::

 from gtkmvc import observer
 
 class AnObserver (observer.Observer):
   def __init__(self, model):
     Observer.__init__(self, model)
 
     # ...
     return
 
   def property_name_value_change(self, model, old, new):
     print "Property name changed from '%s' to '%s"' % (old, new)
     return
 
   pass # end of class


The Observer constructor gets an instance of a Model, and registers the
class instance itself to the given model, to become an observer of
that model instance.

To receive notifications for the property ``name``, the
observer must define a method called
``property_name_value_change`` that when is automatically
called will get the instance of the model containing the changed
property, and the property's old and new values.

Instead of using an implicit naming convention for the notification
methods, is also possible to declare that a method within the observer
is interested in receiving notifications for a bunch of properties: ::

 from gtkmvc import observer
 
 class AnObserver (observer.Observer):
 
   @observer.observes('name', ...)
   def an_observing_method(self, model, prop_name, old, new):
     print "Property '%s' changed from '%s' to '%s"' % (prop_name, old, new)
     return
 
   pass # end of class


Of course the explicit observing method will receive the name of the
property it is changed as now it can observe multiple properties. 

As already mentioned, when used in combination with the *MVC* pattern,
Controllers are also Observers of their models.

Here follows an example of usage: ::

 m = MyModel()
 o = AnObserver(m)
 
 print m.name  # prints 'Rob'
 m.name = 'Roberto' # changes the property value, o is notified


Things so far are easy enough, but they get a bit complicated when you
derive custom models from other custom models.  For example, what
happens to *OP* if you derive a new model class from the class
``MyModel``?

In this case the behavior of the *OP* trusty follows the typical Object
Oriented rules:

* Any *OP* in base class are inherited by derived classes.
* Derived class can override any *OP* in base classes.
* If multiple base classes defines the same *OP*, only the
  first *OP* will be accessible from the derived class.

For example: ::

 from gtkmvc import Model

 class Test1 (Model):
     prop1 = 1
     __observables__ = ("prop1", )
 
     def __init__(self):
         Model.__init__(self)
 
         # this class is an observer of its own properties:
         self.register_observer(self) 
         return
     
     def property_prop1_value_change(self, model, old, new):
         print "prop1 changed from '%s' to '%s'" % (old, new)
         return
     pass # end of class
 
 class Test2 (Test1):    
     prop2 = 2
     prop1 = 3
     __observables__ = ("prop?",)
     
     def __init__(self):
         Test1.__init__(self)
         
         # also this class is an observer of itself:
         self.register_observer(self)
         return
     
     def property_prop2_value_change(self, model, old, new):
         print "prop2 changed from '%s' to '%s'" % (old, new)
         return
     pass
 
 # test code:
 t1 = Test1()
 t2 = Test2()
 
 t2.prop2 = 20
 t2.prop1 = 30
 t1.prop1 = 10


When executed, this script generates this output: ::

 prop2 changed from '2' to '20'
 prop1 changed from '3' to '30'
 prop1 changed from '1' to '10'

As you can see, ``t2.prop1`` overrides the *OP* ``prop1``
defined in Test1 (they have different initial values).  Test2 could
also override method ``property_prop1_value_change``: ::

 class Test2 (Test1):
   # ... copy from previous definition, and add:
    
   def property_prop1_value_change(self, model, old, new):
     print "Test2: prop1 changed from '%s' to '%s'" % (old, new)
     return   
 
   pass

As you expect, the output in this case would be:

 prop2 changed from '2' to '20'
 Test2: prop1 changed from '3' to '30'
 prop1 changed from '1' to '10'


.. _KOBS:DET:

Types of Observable Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In section :ref:`KOBS` we anticipated that there exist several types
of *OP*. In the examples so far we have seen only *value* *OPs*,
meaning that observers will be notified of any change of *value*
assigned to the corresponding *OP*. What would happen if the value of
the property would be a complex object like a list, or a user-defined
class, and the object would change internally?

For example: ::

 from gtkmvc import Model

 class MyModel (Model):
     prop1 = [1,2,3]
     __observables__ = ("prop1",)
 
     def __init__(self):
         Model.__init__(self)
         ...
         return
     pass # end of class
 
 m = MyModel()
 m.prop1.append(4)
 m.prop1[1] = 5


Last two lines of the previous example actually change the *OP*
internally, that is different from *assigning* a new value to the
property like in ``m.prop1 = [5,4,3,2]`` that would trigger a value
notifications like those seen in previous examples.  Similar problem
is found when the property is assigned to a class instance, and then a
method that change the instance is called.

*Mutable sequential types* and *User classes* are also
supported by the *Observer* pattern of *gtkmvc*, but the name of the notified
method in the controller has to be changed accordingly.
The idea is to provide two methods to be notified:

property_``name``_before_change
   That is called
   immediately *before* a method that changes the instance is
   called on the *OP* called ``name``.
property_``name``_after_change
   That is called
   immediately *after* a method that changes the instance is
   called on the *OP* called ``name``.

Of course, it is not needed to define both of the two methods in the
observer class, as only the actually defined methods will be called. 

The signature of these methods is: ::

 def property_<name>_before_change(self, model, instance, name,
                                   args, kwargs)
 
 def property_<name>_after_change(self, model, instance, name, 
                                  res, args, kwargs)

self
   The Observer class instance defining the method.
model
   The Model instance containing the *OP* called
    ``<name>`` that is being changed.
instance
   The object instance that is assigned to the *OP* called
   ``<name>``.
name
   The name of the method that is being called. This
   is different from ``<name>`` that is the name of the *OP*
   contained in the model. 
res
   (Only for *after* notification) the value returned by
   the method *name* that has been called on the *OP*
   *instance*.
args
   List of arguments of the method *name*.
kwargs
   Map of keyword arguments of the method *name*.

As it can be noticed, the only difference between these two method
signatures is the parameter *res* that is obviously available only
for notification method *after*.

The framework *MVC-O* provides a full support for python mutable
sequences like *lists* and *maps*. For example: ::


 from gtkmvc import Model, Observer
 
 # ----------------------------------------------------------------------
 class MyModel (Model): 
     myint = 0
     mylist = []
     mymap = {}
     __observables__ = ("my*", )
 
     pass # end of class
 
 # ----------------------------------------------------------------------
 class MyObserver (Observer):
 
     # notifications
 
     def property_myint_value_change(self, model, old, new):
         print "myint changed"
         return
 
     def property_mylist_value_change(self, model, old, new):
         print "mylist changed"
         return
 
     def property_mylist_before_change(self, model, instance, name,
                                       args, kwargs):
         print "mylist before change:", instance, name, args, kwargs
         return
 
     def property_mylist_after_change(self, model, instance, name, res,
                                      args, kwargs):
         print "mylist after change:", instance, name, res, args, kwargs
         return
 
     # for mymap value_change and before_change are not provided!
     def property_mymap_after_change(self, model, instance, name, res,
                                     args, kwargs):
         print "mymap after change:", instance, name, res, args, kwargs
         return
 
     pass # end of class
 
 
 # Look at what happens to the observer
 if __name__ == "__main__":
 
     m = MyModel()
     c = MyObserver(m)
 
     # changes the int:
     m.myint = 20
 
     # changes the list:
     m.mylist = [1,2]             # calls value_change
     m.mylist.append(10)     
     m.mylist[0] = m.mylist[0]+1
 
     # changes the map:
     m.mymap["hello"] = 30
     m.mymap.update({'bye' : 50})
     del m.mymap["hello"]
     pass
 
After the execution, this is the program output: ::
 
 myint changed
 mylist changed
 mylist before change: [1, 2] append (10,) {}
 mylist after change: [1, 2, 10] append None (10,) {}
 mylist before change: [1, 2, 10] __setitem__ (0, 2) {}
 mylist after change: [2, 2, 10] None __setitem__ (0, 2) {}
 mymap after change: {'hello': 30} None __setitem__ ('hello', 30) {}
 mymap after change: {'bye': 50, 'hello': 30} update None ({'bye': 50},) {}
 mymap after change: {'bye': 50} None __delitem__ ('hello',) {}

This covers those cases where you have your *OPs* holding mutable
sequence values. What if the value is a user-defined class instance?
The notification mechanism is the same: when a method ``M``
that changes internally the instance is called, Observer's methods
*before* and *after* will be called. However, how can the user
declare that method ``M`` *does changes* the instance?
Two mechanism are provided by the framework:

* For already existing classes and class instances. In this cases
  the declaration occurs when the instance is assigned to the *OP* in
  the model.
* For ad-hoc and new classes. In this case the method will be
  *declared* as *Observable* at the class level, through a
  special *decorator* provided by the framework. This is the
  preferable manner. 

Examples for new classes: ::

 from gtkmvc import Model
 from gtkmvc import Observer
 from gtkmvc import observable
 
 # ----------------------------------------------------------------------
 class AdHocClass (observable.Observable):
     def __init__(self): self.val = 0
 
     # this way the method is declared as 'observed':
     @observable.observed 
     def change(self): self.val += 1
 
     # this is NOT observed:
     def is_val(self, val): return self.val == val
 
     pass #end of class
 
 # ----------------------------------------------------------------------
 class MyModel (Model):
     obj = AdHocClass()
     __observables__ = ("obj",)
 
     pass # end of class
 
 # ----------------------------------------------------------------------
 class MyObserver (Observer):
 
     def property_obj_value_change(self, model, old, new):
         print "obj value changed from:", old, "to:", new 
         return
 
     def property_obj_after_change(self, model, instance, name, res,
                                   args, kwargs):
         print "obj after change:", instance, name, res, args, kwargs
         return
 
     pass
 
 # Look at what happens to the observer
 if __name__ == "__main__":
     m = MyModel()
     c = MyObserver(m)
     m.obj.change()
     m.obj = None
     pass
 
The execution prints out (slightly modified for the sake of
readability):
 
 obj after change: <__main__.AdHocClass object at 0xb7d91e8c> 
 change None (<__main__.AdHocClass object at 0xb7d91e8c>,) {}
 
 obj value changed 
 from: <__main__.AdHocClass object at 0xb7d91e8c> to: None

As you can see, declaring a class as *observable* is as simple as
deriving from ``gtkmvc.observable.Observable`` and decorating
those class methods that must be observed with the decorator 
``gtkmvc.observable.observe`` (decorators are supported by
Python version 2.4 and later only). 


What if the user class cannot be easy changed, or only an instance of
the class is available as *OP* value? In this case declaration of the
methods to be observed can be done at time of declaration of the
corresponding *OP*. In this case the *value* to be assigned to the
*OP* must be a triple ``(class, instance, method_names>``, where:

class
   Is the ``class`` of the object to be observed.
instance
   Is the object to be observed.
method_names
   Is a tuple of strings, representing the method
   names of the instance to be observed.

For example: ::

 from gtkmvc import Model
 
 #----------------------------------------------------------------------
 # This is a class the used cannot/don't want to change
 class HolyClass (object):    
     def __init__(self): self.val = 0 
     def change(self): self.val += 1
     pass #end of class
 
 
 # ----------------------------------------------------------------------
 class MyModel (Model):
     obj = (HolyClass, HolyClass(), ('change',))
     __observables__ = ("obj",)
 
     pass # end of class
 


Finally, *OP* can hold special values that are *signals* that can be
used to notify observers that certain events occurred. 

To declare an *OP* as a signal, the value of the *OP* must be
``gtkmvc.observable.Signal()``. To notify an event, the model
can then invoke method ``emit`` of the *OP*. The observers will
be notified by calling method
``property_<name>_signal_emit`` that will also receive any
parameter passed to the ``emit`` method. For example: ::

 from gtkmvc import Model
 from gtkmvc import Observer
 from gtkmvc import observable
 
 # ----------------------------------------------------------------------
 class MyModel (Model):
     sgn = observable.Signal()
     __observables__ = ("sgn",)
 
     pass
 
 # ----------------------------------------------------------------------
 class MyObserver (Observer):
 
     # notification
     def property_sgn_signal_emit(self, model, args, kwargs):
         print "Signal:", model, args, kwargs
         return
 
     pass # end of class
 
 # Look at what happens to the observer
 if __name__ == "__main__":
     m = MyModel()
     c = MyObserver(m)
     m.sgn.emit() # we emit a signal
     m.sgn.emit("hello!", key=10) # with arguments
     pass
 
The execution of this example will produce:
 
 Signal: <__main__.MyModel object at 0xb7de564c> () {}
 Signal: <__main__.MyModel object at 0xb7de564c> ('hello!',) {'key': 10}


In the ``examples``, there are several examples that show how
different types of *OPs* can be used. Of course all available types can
be used in all available kind of model classes, with or without
multi-threading support.

  
Special members for Observable Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Classes derived from Model, that exports *OPs*, have several special
members. Advanced users might be interested in overriding some of them,
but in general they should be considered as private members. They are
explained here for the sake of completeness.

__observables__
   A class (static) member that lists property
   names. This must be provided as either a tuple or a list by the
   user. Wilcards in names can be used to match property names, but
   properties with names starting with a double underscore
   ``_,_`` will be not matched.

__properties__
   (Deprecated, do not use anymore) A dictionary mapping
   observable properties names and their initial value. This
   variable has been substituted by __observables__. 
 
__derived_properties__
   (Deprecated) Automatically generated static member
   that maps the *OPs* exported by all base classes. This does not
   contain *OPs* that the class overrides.
 
``_prop_*property_name*``
   This is an
   auto-generated variable holding the property value. For example,
   a property called ``x`` will generate a variable called
   ``_prop_x``.
 
``get_prop_*property_name*``
   This public method
   is the getter for the property. It is automatically generated only
   if the user does not define one. This means that the user can change
   the behavior of it by defining their own method.  For example, for
   property ``x`` the method is ``get_prop_x``.  This
   method gets only self and returns the corresponding property value.
 
``set_prop_*property_name*``
   This public method
   is customizable like 
   ``get_prop_<property_name>``.  This does not return
   anything, and gets self and the value to be assigned to the
   property. The default auto-generated code also calls method
   ``gtkmvc.Model.notify_property_change`` to notify the
   change to all registered observers.
 


For further details about this topic see meta-classes ``PropertyMeta``
and ``ObservablePropertyMeta`` from package ``support``.


