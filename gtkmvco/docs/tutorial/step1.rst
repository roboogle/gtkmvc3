
.. _step1:

########################
A short tutorial: Step 1
########################

.. include:: common.rst

.. Important::

   All the code presented here can be found in the distributed examples.

The example in few words
========================
The sample application must provide a single window, with a label
showing the value of a numeric counter. The window contains also a
button, which increments the counter by one every time it is pressed.

.. figure:: images/appl.png
   :width: 4cm

   How the mini-application looks like


Since this tutorial must fit into few pages, the example is extremely
simple.


The framework
=============
The implementation of this example is split into three *distinct*
parts. First, the |gui| is constructed from a |glade| file. Second,
the |gui| is constructed *by hand*, by creating and connecting
manually all widgets. Third, adapters are applied to make the code
much easier.

Hand-made view is mainly presented to make this tutorial more
complete, but the readers should keep in mind that they are going to
adopt |glade| most of the times, or a mixture of them, where many
parts come from one or more glade files, and some others are built
manually only when it comes handly.

The |gtkmvc3| framework provides three well-distinguishable levels, to
allow the pure-glade parts to go into the View side, and all the
remaining parts that would be put in the |vc| part, to go either in
the Controller part, or in the View part, depending on how much close
to the |gui| stuff are.

For example, all the widgets signal handlers must go in the Controller
side, whereas the code that sets some attributes of a specific widget
might live either in the Controller or in the View, depending on how
much those attributes are bounded to the application logic.

The more some code depends on the logic of the application, the
farther it lives from the View side. If some code depends only on the
logic without any relation with the |gui| stuff, it must live in the
Model.


The implementation glade-based
==============================

The model
---------
The model is represented by class ``MyModel``, derived from
class ``gtkmvc3.Model``, provided by the framework.

The class ``MyModel`` contains a numeric member called ``counter``.
Since we are interested in monitoring and show any change of this
counter, we declare it as an *observable property*. ::

 from gtkmvc3 import Model

 class MyModel (Model):
     counter = 0
     __observables__ = ('counter',)

Names in ``__observables__`` can contain wilcards, see the user manual
for further information.


The glade-based view
--------------------
|glade| while editing the example is depicted in figure
:ref:`glade-figure`. The names for the main window, the label and the
button are significant, and signal clicked of the button has been
associated with a function called ``on_button_clicked``.

.. _glade-figure:

.. figure:: images/glade.png
   :width: 18cm

   Glade at work

The result is saved in file ``step1.ui``.

The view is represented by class ``MyView``, that derives from class
``gtkmvc3.View``. The class ``gtkmvc3.View`` can be thought as a
dictionary that holds a set of widgets, and allows for accessing
contained widgets through their names. ::

 from gtkmvc3 import View
 class MyView (View):
    builder = "step1.ui"

    def set_text(self, text):
        self['label'].set_text(text)

The name of the |glade| file can be passed with member ``builder``.


The controller
--------------

The controller is the only part of the |mvc| which knows the model and
the view instances which it is linked to. These are accessible via
members ``self.model`` and ``self.view`` respectively. ::

 # This is file ctrl_glade.py
 from gtkmvc3 import Controller
 from gi.repository import Gtk

 class MyController (Controller):
     def register_view(self, view):
         # initializes the text of label:
         self.view.set_text("%d" % self.model.counter)

     # signals:
     def on_main_window_delete_event(self, w, e):
         Gtk.main_quit()
         return False

     def on_button_clicked(self, button):
         self.model.counter += 1  # changes the model

     # observable properties:
     @Controller.observe("counter", assign=True)
     def counter_change(self, model, prop_name, info):
         self.view.set_text("%d" % info.new)
         print("Property '%s' changed value from %d to %d" \
   	       % (prop_name, info.old, info.new))

See the in the main code below how the ``MyController`` gets
instantiated.

Method ``register_view`` is called by the framework to to connect
signals and initialize the |gui| side that depends on the application
logic. In the example, the text label is initialized to the initial
value of the counter.

Method ``on_button_clicked`` is called when the user clicks the
button. The corresponding signal is automatically connected to this
method when class ``MyView`` registers itself within the controller.

A ``gtkmvc3.Controller`` is also a ``gtkmvc3.Observer``, and decorator
`@Controller.observe` makes method ``counter_change`` being called
when observable property ``counter`` in the connected model is
assigned. The model containing the property, the name of the property,
and a structure carrying other information (e.g. the old and new
value) are passed to this method. Notice that the model is passed
since the controller might be an observer for more than one model,
even different from the model it is directly connected to in the |mvc|
chain.


The main code
-------------
Main code is pretty trivial: ::

 # This is file main_glade.py
 from gi.repository import Gtk
 from model import MyModel
 from ctrl_glade import MyController
 from view_glade import MyView

 m = MyModel()
 v = MyView()
 c = MyController(m, c)

 Gtk.main()

A triple MVC is created, and main loop is started.


The implementation without glade
================================

The model
---------
The model does not depend on the controller+view sides, so it is
exactly the same as for the implementation glade-based.

The view
--------
Using manually constructed views is slightly less intuitive that using
glade-based views, since the architecture of the view-side |gtkmvc3|
is mainly designed to be used with glade files. ::

 # This is file view_no_glade.py
 from gtkmvc3.view import View
 from gi.repository import Gtk

 class MyViewNoGlade (View):

    def __init__(self):

        # The view here is not constructed from a glade file.
        View.__init__(self)

        # The set of widgets:
        w = Gtk.Window()
        h = Gtk.VBox()
        l = Gtk.Label()
        b = Gtk.Button("Press")
        h.add(b)
        h.add(l)
        w.add(h)
        w.show_all()

        # We add all widgets we are interested in retrieving later in
        # the view, by giving them a name. Suppose you need access
        # only to the main window, label and button.  Widgets are
        # added like in a map:
        self['main_window'] = w
        self['label'] = l
        self['button'] = b

    def set_text(self, text):
        self['label'].set_text(text)

The entire work is carried out by the View's constructor which can
be exploited to manually construct all the widgets set.

Following lines are used to build the widgets set, and to associate a
few of them with string names (only those that will have to accessed
later).

Notice that here |glade| file has not been used at all. Nevertheless,
a mixed solution where |glade| file(s) and manually constructed
widgets sets is fully supported, and indeed it is frequent to be used
in real world.


The controller
--------------
The controller is the same that has been used for the glade-based
version, a part from a further signal connection that is performed to
connect the button "``clicked``" event to class method
``self.on_button_clicked``. For this reason, class
``MyControllerNoGLade`` is derived from class
``MyController`` to reduce typing. ::

 # This is file ctrl_no_glade.py
 from ctrl_glade import MyController

 class MyControllerNoGlade (MyController):
    def register_view(self, view):
        MyController.register_view(self, view)

        # connects manually the signals:
        self.view['button'].connect('clicked', self.on_button_clicked)
        self.view['main_window'].connect('delete-event', self.on_main_window_delete_event)


The main code
-------------
Like previous version, main code for manually built view is very
short: ::

 # This is file main_no_glade.py
 from gi.repository import Gtk
 from model import MyModel
 from ctrl_no_glade import MyControllerNoGlade
 from view_no_glade import MyViewNoGlade

 m = MyModel()
 v = MyViewNoGlade()
 c = MyControllerNoGlade(m,v)
 Gtk.main()


Multiple views, one model
=========================
This example shows the powerful of the |obs|.

Here both the glade-based and manually built versions are being run at
the same time, with a single instance of class ``MyModel``
shared between those two versions. The execution of this example
results in two windows being displayed; by clicking the button of one
of them, the counter is incremented, and the labels in both of them
are updated. ::

 # This is file main_mixed.py
 from gi.repository import Gtk
 from model import MyModel
 from ctrl_no_glade import MyControllerNoGlade
 from ctrl_glade import MyController
 from view_no_glade import MyViewNoGlade
 from view_glade import MyView

 m = MyModel()
 v1 = MyViewNoGlade()
 c1 = MyControllerNoGlade(m,v1)
 v2 =  MyView()
 c2 = MyController(m,v2)
 Gtk.main()


Using Adapters
==============
Adapters largely contribute to make the code
simpler and so to reduce development costs and efforts.

Adapters *adapt* some part of the model to some part of the view. In a
simple version, one adapter makes one property (possibly observable)
into the model communicate autonomously with a single widget into the
view, and viceversa. See the user manual for full info.

We want to have an adapter to handle coordination between property
``counter`` and the label. Model and View remain unchanged. It is the
Controller that can be simplified as follows: ::

 # This is file ctrl_glade_adap.py
 from gtkmvc3 import Controller
 from gi.repository import Gtk

 class MyControllerAdap (Controller):

    def register_adapters(self):
        self.adapt("counter", "label")

    # signals:
    def on_main_window_delete_event(self, w, e):
        Gtk.main_quit()
        return False

    def on_button_clicked(self, button):
        self.model.counter += 1  # changes the model

Controller method ``register_adapters`` is called by the
framework when adapters can be instantiated. The controller is no
longer interested in observing property ``counter`` and to
initialize the value shown in the label, as these activities are now
transparently carried out by the adapter.

Notice that if editable widget like a text entry were used instead
of a label, the adapter would also have taken care about changes of
the text entry reporting them to the property.


Advanced use of Adapters
------------------------

Now suppose you wanted to apply some customization to the way the
label shows the property's value. Method ``register_adapters`` might
had been: ::

    from gtkmvc3 import adapters
    def register_adapters(self):
        a = adapters.Adapter(self.model, "counter")
        a.connect_widget(self.view['label'],
             setter=lambda w,v:
               w.set_markup("<big>Counter=<b>%02d</b></big>" % v))
        self.adapt(a)

.. figure:: images/adap.png
   :width: 4cm

   Customized adapter at work

Here an adapter is created explicitly, and parameter ``setter`` is
used to custom the functional block that is in charge of writing to
the widget.

There are several types of adapters that can be used, depending on the
property type and the widget type they adapt. Adapters offer a very
straight and simple default support, but they can be largely
customized when needs get more advanced. See the user manual for
further information.


What's next?
============

Are you ready for a jump ahead? Go to the :ref:`second part<step2>` of this
tutorial.
