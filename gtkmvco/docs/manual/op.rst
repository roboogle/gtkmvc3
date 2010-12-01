.. _OPD:

Observable Properties
*********************

Observable Properties (*OP*) is a powerful mechanism which
implement the *Observer Pattern*.

The mechanism which allows a part of the data contained in models
to be observed by entities called *Observers*. It is fully
automatic, as its management is carried out transparently by the
base class ``Model``.

Here a quick example is shown here, later all details are
presented. ::

 from gtkmvc import Model, Observer 
 # ----------------------------
 class MyModel (Model):
    name = "Roberto"
    __observables__ = ("name",)
    pass # end of class
 # ----------------------------
 class MyObserver (Observer):
    @Observer.observes
    def name(self, model, old, new):
        print "'name' changed from", old, "to", new
        return
    pass # end of class
 # ----------------------------
 m = MyModel()
 o = MyObserver(m)
 m.name = "Tobias"


In models, OPs are declared explicitly, and in observers we define
methods which will be called when OPs are changed. In the example,
when ``m.name`` is changed in the last line, method
``MyObserver.name`` is called automatically to notify the observer.

Controllers are also observers, so the OP pattern clicks well with
the MVC pattern.

If the example looks smooth and easy, the topic is much more
complex. OPs can be *concrete* or *logical*, and can be values
(like in the previous example), or complex objects like containers
or user's classes. All these differences add complexity which will
be described in details in the following sections.

.. include:: op_concrete.rst
.. include:: op_logical.rst
.. include:: op_types.rst