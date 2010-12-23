A simple application
********************

This section describes the process of creation of a sample
application, from the design with *Glade*, to the integration of views
and code inside the *MVC-O* Infrastructure.

We want to design and implement a simple application constituted by
only one window, containing two string labels. One label shows a text,
while the other shows the number of characters displayed (i.e. the
length of the string) by the first one. There is also a button the
user can press. By pressing the button, the user can change the
displayed text, and of course this action might change also the
displayed text length accordingly. Figure :ref:`EX:f` gives an idea on
how the application should appear.

.. _EX:f:

.. figure:: images/example.png
   :width: 6 cm
   :align: center

   The sample Application

.. _GLEX:

Glade
=====

Figure :ref:`GL:f` shows *Glade* and a project named ``example``.
The sample *GUI* has only one top-level window (named
``window1``).

.. _GL:f:

.. figure:: images/example_glade.png
   :width: 15 cm
   :align: center

   Designing the example by means of *Glade* for GTK2

The *Widget Tree Window* shows the widgets hierarchy. There are
essentially the three main components (one button and two labels),
grouped inside a set of *containers*, which supplies alignments and
resizing capabilities.

On the right side of Figure :ref:`GL:f`, the *Properties Window*
shows that the widget named ``button1`` has signal
``clicked`` associated with function
``on_button1_clicked``. This means that the Controller will
have to supply this function in order to handle the ``click``
event occurring in ``button1``.

Implementation
==============

The implementation is slightly elaborate for this example, because the
goal here is to show how the sample application can be implemented by
using the *MVC-O* Infrastructure.

A basic knowledge of any Object Oriented programming language is
sufficient to understand how this example has been pushed inside the
*MVC-O* framework. On the contrary, a fair knowledge of the Python
language is required in order to understand the code details.

More description section is :doc:`impl`.


View
----

In the example, the View is implemented inside the class
``ExampleView`` shown below. ::

 from gtkmvc import View
 import os.path
 
 GLADE_PATH = "./glade" 
 
 class ExampleView (View):
     """The application view. Contains only the main window1 tree."""
     glade = os.path.join(GLADE_PATH, "example.glade")
     top = "window1"

     def set_msg(self, msg):
        self['label_text'].set_text(msg)
        self['label_text_len'].set_text(str(len(msg)))
        return

     pass # end of class


Class ``ExampleView`` extends the generic ``View``
class, which performs most of the job, as described above.
Class memebers ``glade`` and ``top`` are used instead of
calling ``View`` constructor directly.

Model
-----

Class ``ExampleModel`` is as simple as class
``ExampleView``.  As for ``ExampleView``, it extends a
base class of the *MVC-O* Infrastructure, class ``Model``.  The
state is represented by a set of possible messages, as well as by the
current message index. The current message index is also an
observable property. A couple of methods are supplied in order to
access the state. ::

 from gtkmvc import Model

 class ExampleModel (Model):
     """The model contains a set of messages
     and an observable property that represent the current message
     index"""
 
     # Observable property: code for that is automatically generated
     # by metaclass constructor. The controller will be the observer
     # for this property
     message_index = -1   # -1 is the initial value
     __observables__ = ("message_index",)
 
     def __init__(self):
         Model.__init__(self)
 
         self.messages= ('Initial message',
                         'Another message', 
                         'Another message again',
                         'Model changed again!')
         return
 
     def get_message(self, index): return self.messages[index]
 
     def set_next_message(self):
         # this changes the observable property:
         self.message_index = (self.message_index + 1) % len(self.messages)
         return
 
     pass # end of class



Notice that class instance members are declared to be observable
through the special class variable ``__observables__``,
which is a list of names (string) of the properties that are
observable.

The base class Model belongs to a
meta-class which automatically searches for observable properties and
generates the needed code to handle the notification.  When the value
of variable ``message_index`` changes, all registered
observers will be notified.

.. Note:: 
   It is also possible to use the special class' variable
   ``__properties__``, which is a map of (property, value)
   couples. This variable was used in older versions of *gtkmvc* and
   should be avoided in new code.


Controller
----------

Class ``ExampleController`` contains the *logic* of the
application. The controller handles two signals and the observable
property notification. Signals are the ``destroy`` event,
invoked when the application quits, and the
``on_button1_clicked``, fired when ``button1`` is
pressed. ::

 from gtkmvc import Controller
 from gtk import mainquit

 class ExampleController(Controller):
     """The only one controller. Handles the button clicked signal, and
     notifications about one observable property."""
 
     def __init__(self, model, view):
         """Contructor. model will be accessible via the member 'self.model'.
         View registration is also performed."""
         Controller.__init__(self, model, view)
         return
 
     def register_view(self, view):
         # Connects the exiting signal:
         view.get_top_widget().connect("destroy", mainquit)
         return
 
     # Signal
     def on_button1_clicked(self, button):
         """Handles the signal clicked for button1. Changes the model."""
         self.model.set_next_message()
         return
 
     # Observables notifications
     @Controller.observe("message_index", assign=True)
     def value_change(self, model, name, info):
         """The model is changed and the view must be updated"""
         msg = self.model.get_message(info.new)
         
         self.view.set_msg(msg)
         return    
 
     pass # end of class


The ``destroy`` signal is connected when the View registers itself
inside the controller, by using the method override of
``register_view``.  Method ``on_button1_clicked`` calls a method
inside the model which changes a part of the state inside the
model. Since that part of the state is an observable property, the
associated observer (which is the controller itself) is notified of
the modification, by calling method ``value_change``. This method
updates the view connected to the controller.

