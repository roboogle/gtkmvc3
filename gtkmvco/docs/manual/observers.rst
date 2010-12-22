.. _Observers:

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

Since it is common to observe one model, the class constructor provides
the possibility to specify it.


Change Notifications
--------------------

When an OP gets changed, notifications are sent by the framework to
observer's methods. As we see in previous chapter, changes can happen
at:

Assignment
	When the value of an OP is changed, meaning that the OP is
	assigned with a value.

Instance 
	 When an object instance is changed internally. For example an
	 element is added to a list, or a method modifying the
	 instance is called.


.. _Observer_vcn:

Change Notification Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Independently on the notification type, the prototype of notification
methods in observers is always:

.. method:: Observer.method_name(model, prop_name, info)

   :param model: is the observed Model instance containing the OP
                 which got changed

   :param prop_name: is the name of the OP which got changed.

   :param info: a dictionary whose content depends on the notification
                type (namely *assign*, *before* method call, *after* method
                call and *signal*).

How is an observer's method declared to be *notification* method for
an OP? It is possible to declare notification methods *statically* or
*dynamically*.

1. **Statically** with decorator ``@Observer.observe``. For example::

    from gtkmvc import Observer
    class MyObserver (Observer):

      @Observer.observe('prop1', assign=True)
      @Observer.observe('prop2', assign=True, signal=True)
      def notifications(self, model, prop_name, info):
          # this is called when 'prop1' or 'prop2' are assigned
          # and also when 'prop2.emit()' is called
          return

      @Observer.observe('prop1', assign=True)
      def other_notification(self, model, prop_name, info):
          # this is called when 'prop1' is assigned
          return

   Notice that an OP can be bound to multiple notifications, like
   ``prop1`` in the example. Also notice that the type of the
   notification (assign, signal, etc.) is declared by means of keyword
   arguments flags. We are discussing types and keyword arguments
   later in this section.

2. **Dynamically** with method ``Observer.observe``. For example::

    from gtkmvc import Observer
    class MyObserver (Observer):

      def __init__(self):
         Observer.__init__(self)

         self.observe(self.notification, "prop1", assign=True)
         self.observe(self.notification, "prop2", assign=True, signal=True)
         return

      def notification(self, model, prop_name, info):
          # ...
          return

   As you can see, `Observer.observe` can be used both as decorator
   and instance method to declare notifications. When used dynamically
   (as instance method), the only difference is that it takes as first
   argument the method to declare as notification.


The parameter `info:NTInfo`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We anticipated that parameter `info` of change notification is a
dictionary whose content depends on the notification type. Actually
:py:obj:`info` is an instance of class :py:class:`NTInfo` 
(**N**\ otification **T**\ ype **Info**\ rmation).

:py:class:`NTInfo` derives from :py:class:`dict` type, but offers the
possibility to access to its values by accessing keys as attributes::

    # ...
    info['key'] = 20 # access with key
    info.key += 1 # access with attribute
    print info.key # 21

When defining a notification method, e.g. statically with decorator::

    @Observer.observe('prop2', assign=True, signal=True, foo="a-value-for-foo")
    def notifications(self, model, prop_name, info):
        # ...
        return 

Instance :py:obj:`info` in method notification will contain all
keyword arguments and associated values which were specified at
declaration time::

    @Observer.observe('prop2', assign=True, signal=True, foo="a-value-for-foo")
    def notifications(self, model, prop_name, info):
        print info['assign'] # True
        print info.signal    # True
        print info.foo       # "a-value-for-foo"
        return

Notification types
------------------

The type of the notification method is decided at declaration time, by
using specific flags as keyword arguments. Later in the notification
method, parameter :py:obj:`info` will carry specific information which
depend on the notification type. Here all the supported types are
discussed in details.

Assign Notifications
^^^^^^^^^^^^^^^^^^^^

Keyword flag: :py:obj:`assign` set to :py:const:`True`.

:py:obj:`info` content:

   :model: is the observed Model instance containing the OP
                 which got changed.
   :prop_name: is the name of the OP which got changed. It has to be
   	  	         specified when the method receives notifications for
   	  	         multiple OPs.
   :old: is the old value the OP had before being changed.
   :new: is the current value the OP is assigned to.
   

Instance Change Notifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In section :ref:`OPtypes` mutable instances were used as OP in
models. When a mutable instance gets changed, notifications are made
within observers, **before** and/or **after** the method changing the
OP is called.

A notification method which is called *before* a change has the following prototype in a
class deriving from ``Observer``:

.. method:: before_method_call(model, [pname,] instance, mname, args, kwargs)
 
   This it the notification called when a mutable instance is being
   changed, right before the call execution.

   :param model: is the ``Model`` instance containing the mutable
                 instance OP.
   :param pname: is the name of the OP which got changed. It has to be
   	  	specified when the method receives notifications for
   	  	multiple OPs.
   :param instance: is the mutable instance which is being changed.
   :param mname: is the name of the instance's method which is being
                called to change the instance.
   :param args: List of arguments to the instance's method which is 
                being called. 
   :param kwargs: Keywords arguments to the instance's method which is 
                being called. 

A notification method which is called *after* a change has the
following prototype in a class deriving from ``Observer``:

.. method:: after_method_call(model, [pname,] instance, mname, res, args, kwargs)
 
   This it the notification called when a mutable instance is being
   changed, right before the call execution.

   :param model: is the ``Model`` instance containing the mutable
                 instance OP.
   :param pname: is the name of the OP which got changed. It has to be
   	  	specified when the method receives notifications for
   	  	multiple OPs.
   :param instance: is the mutable instance which has been changed.
   :param mname: is the name of the instance's method which has been called
                to change the instance.
   :param res: value returned by the instance's method which has been called
                to change the instance.
   :param args: List of arguments to the instance's method which has 
                been called. 
   :param kwargs: Keywords arguments to the instance's method which has
                been called. 


Of course, it is not needed to define both *before* and *after*
notification methods in the observer class, as only the actually
defined/declared methods will be called.


Examples
--------

:TODO: This subsection has to be extended largely

You may use the property in this way: ::

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

