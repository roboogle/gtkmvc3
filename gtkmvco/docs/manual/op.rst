.. _OP_top:

Observable Properties
*********************

Observable Properties (*OP*) is a powerful mechanism which
implement the *Observer Pattern*.

The mechanism which allows a part of the data contained in models
to be observed by entities called *Observers*. It is fully
automatic, as its management is carried out transparently by the
base class ``Model``.

:Note: This section mainly focuses on OP in *Models*. The use of
       `Observer` here is anticipated only for examples. The section
       :ref:`Observers` presents full details about them.


Here a quick example is shown here, later all details are
presented. ::

 from gtkmvc3 import Model, Observer 
 # ----------------------------
 class MyModel (Model):
    name = "Roberto"
    __observables__ = ("name",)
    pass # end of class
 # ----------------------------
 class MyObserver (Observer):
    @Observer.observe("name", assign=True)
    def notification(self, model, name, info):
        print "'name' changed from", info.old, "to", info.new
        return
    pass # end of class
 # ----------------------------
 m = MyModel()
 o = MyObserver(m)
 m.name = "Tobias"


In models, OPs are declared explicitly, and in observers we define
methods which will be called when OPs are changed. In the example,
when ``m.name`` is changed in the last line, method
``MyObserver.notification`` is called automatically to notify the
observer. All details about observers will be presented in section
:ref:`Observers`, in particular about what `assign=True` means. 

Controllers are also observers, so the OP pattern clicks well with
the MVC pattern.

If the example looks smooth and relatively easy, the topic is much
more complex. OPs can be *concrete* or *logical*, and can be values
(like in the previous example), or complex objects like containers or
user's classes. All these differences add complexity which will be
described in details in the following sections.

.. _OPconc:
.. include:: op_concrete.rst

.. _OPlog:
.. include:: op_logical.rst

.. _OPtypes:
.. include:: op_types.rst

.. _OPconstr:
.. include:: op_constr.rst

.. include:: op_special.rst

