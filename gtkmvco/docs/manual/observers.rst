=========
Observers
=========

If OPs live into ``Models``, ``Observers`` are the objects which are
interested in being notified when an OP gets changed. An Observer
observes one or more Models.

Observer registration
---------------------

Registration is the mechanism which observers make model known about
them. 

There are a few methods which can be used when registering observers into models.

.. method:: Observer.__init__(model=None, spurious=False)
 
   Class constructor

   :param model: is optional ``Model`` to observe.
   :param spurious: when ``True`` make the interested in receiving
   	  	    spurious notifications, i.e. when an obxserved OP
   	  	    is assigned with the same value it got before the
   	  	    assignment.

.. method::  Observer.observe_model(model)

   Observes the given model among the others already observed.

   :param model: the Model instance to observe.

.. method::  Observer.relieve_model(model)

   Stops observing the given model which was being previously observed.

   :param model: the Model instance to relieve.

Since it is common to observe one model, the class constructor provide
the possibility to specify it.


:TODO:  Fix all the following text

FROM OPS TYPES
--------------

*Mutable sequential types* and *User classes* are also supported by
the *Observer* pattern of *gtkmvc*, but the name of the notified
method in the controller has to be changed accordingly.  The idea is
to provide two methods to be notified:

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

CONTINUING OLD DOC
------------------

This means that you may use the property in this way: ::

 m = MyModel()
 print m.name  # prints 'Rob'
 m.name = 'Roberto' # changes the property value

What's missing is now an observer, to be notified when the property
changes. To create an observer, derive your class from base class
``gtkmvc.Observer``. ::

 from gtkmvc import Observer
 
 class AnObserver (Observer):
 
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

 from gtkmvc import Observer
 
 class AnObserver (Observer):
 
   @Observer.observes('name', ...)
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

