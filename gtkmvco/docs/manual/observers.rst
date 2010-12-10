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

Value
	When the value of an OP is changed, meaning that the OP is
	assigned with a different value.

Instance 
	 When an object instance is changed internally. For example an
	 element is added to a list, or a method modifying the
	 instance is called.


.. _Observer_vcn:

Value Change Notifications
^^^^^^^^^^^^^^^^^^^^^^^^^^

Value notifications sent to methods whose propotype is: 

.. method:: Observer.method_name(model, [pname,] old, new)

   :param model: is the observed Model instance containing the OP
                 which got changed.
   :param pname: is the name of the OP which got changed. It has to be
   	  	         specified when the method receives notifications for
   	  	         multiple OPs.
   :param old: is the old value the OP had before being changed.
   :param new: is the current value the OP is assigned to.
   
How are methods receiving value change notifications bound to OPs?

1. **Statically** with decorator ``Observer.observes``::
    
    from gtkmvc import Observer    
    class MyObserver (Observer):
      @Observer.observes
      def prop1(self, model, old, new):
          # this is called when OP 'prop1' is changed
          return

      @Observer.observes('prop1', 'prop2')
      def multiple_notifications(self, model, pname, old, new):
          # this is called when 'prop1' or 'prop2' are changed
          return

   Notice in this case the difference between the two cases
   (with/without arguments passed to the decorators). Also notice that
   an OP can be bound to multiple notifications, like ``prop1`` in the
   example.

#. **Statically** with a naming convention, by naming the notification
   method ``property_<pname>_value_change`` (*deprecated*)::

    from gtkmvc import Observer    
    class MyObserver (Observer):

      def property_prop1_value_change(self, model, old, new):
          # this is called when OP 'prop1' is changed
          return

      def property_prop2_value_change(self, model, old, new):
          # this is called when OP 'prop2' is changed
          return
   		
   In this case each notification method has to be bound to one
   specific OP only.
   
#. **Dynamically** with method ``Observer.add_observing_method``.
   This is useful when the definition of the observer class happens
   dynamically (e.g. in generated *proxies*), or when the OPs to be
   observed are not known at static time. ::

    from gtkmvc import Observer    
    class MyObserver (Observer):

      def __init__(self, m):
          Observer.__init__(self, m)
          self.add_observing_method(self.prop1_change, "prop1")
          self.add_observing_method(self.multiple_notifications, ("prop1", "prop2"))
          return

      def prop1_change(self, model, old, new):
          # this is called when OP 'prop1' is changed
          return

      def multiple_notifications(self, model, pname, old, new):
          # this is called when OPs 'prop1' or 'prop2' are changed
          return
   
   Notice the difference between the two cases, with
   ``prop1_change`` not receiving the OP name as it is a notification
   method for a specific OP, while ``multiple_notifications``
   receiving the OP name. The difference is imposed when calling
   ``add_observing_method``.


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

Similarly to :ref:`_Observer_vcn`, there are different ways a method
in ``Observer`` can be declared to be a instance change notification
method:

1. **Statically** with decorator ``Observer.observes``::

    from gtkmvc import Observer    
    class MyObserver (Observer):
      @Observer.observes
      def prop1_before(self, model, instance, mname, args, kwargs):
          # this is called before OP 'prop1' is changed by calling a changing method 
          return

      @Observer.observes('prop1', 'prop2')
      def multiple_notifications_before(self, model, pname, instance, mname, args, kwargs):
          # this is called before 'prop1' or 'prop2' are changed by calling a changing method
          return

      @Observer.observes
      def prop4_after(self, model, instance, mname, res, args, kwargs):
          # this is called after OP 'prop4' is changed by calling a changing method 
          return

      @Observer.observes('prop2', 'prop4')
      def multiple_notifications_after(self, model, pname, instance, mname, res, args, kwargs):
          # this is called after 'prop2' or 'prop4' are changed by calling a changing method 
          return

   Again, notice that an OP's change can be notified to multiple
   methods in the same observer.

#. **Statically** with a naming convention, by naming the
   notification methods ``property_<pname>_before_change`` and
   ``property_<pname>_after_change`` (*deprecated*)::

    from gtkmvc import Observer    
    class MyObserver (Observer):

      def property_prop1_before_change(self, model, instance, mname, args, kwargs):
          # this is called immediatelly before 'prop1' is changed by a method call
          return

      def property_prop2_after_change(self, model, instance, mname, res, args, kwargs):
          # this is called immediatelly after 'prop2' is changed by a method call
          return
   		
   In this case each notification method has to be bound to one
   specific OP only.

#. **Dynamically** with method ``Observer.add_observing_method``.
   Exactly like in the case of value change, but the notification
   methods have different prototypes::

    from gtkmvc import Observer    
    class MyObserver (Observer):

      def __init__(self, m):
          Observer.__init__(self, m)
          self.add_observing_method(self.before_prop1_gets_changed, "prop1")
          self.add_observing_method(self.multiple_after_change, ("prop1", "prop2"))
          return

      def before_prop1_gets_changed(self, model, instance, mname, args, kwargs):
          # this is called immediatelly before 'prop1' is changed by a method call
          return

      def multiple_after_change(self, model, pname, instance, mname, res, args, kwargs):
          # this is called immediatelly after 'prop1' or 'prop2'
          # are changed by a method call. pname carries the name of
          # the property which has been changed.
          return


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

