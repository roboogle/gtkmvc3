=============================
Logical Observable Properties
=============================

*Logical* OPs are properties whose values are not necessarily
stored in the model, but which are read and written by a pair of
getter/setter methods.

This make logical OPs ideal for:

* Values calculated out of other OPs (which can be either logical
  or concrete).
* Values living outside the model, like e.g. in a database, or in a
  remote server.

Logical OPs are declared like concrete OPs, but no correspoding
attributes have to appear in the class. Their name have to appear
only within the special member ``__observables__``. 
For example: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto" 
    
    __observables__ = ("name", "happiness")
    pass # end of class
 # ----------------------------

In the example, ``name`` is a concrete property, whereas
``happiness`` is a logical property, as no corresponding attribute
exists in class ``MyModel``.


.. Note:: 
   Notice that names of logical OPs occurring within the
   special member ``__observables__`` cannot contain wildcards like
   concrete properties.

   The reasons for this limitation is obvious, as wildcards
   can be used to match only class attributes.)

However, a logical OP's value is taken from a getter method, and
for a read/write OP the values are stored through a setter
method. Defining a getter is mandatory, while defining a setter is
required only for writable logical OPs.

getter/setter methods can be defined by exploiting decorators, or
by exploiting a naming convention.


Use of decorators for defining getters and/or setters
-----------------------------------------------------

Decorators ``@Model.getter`` and ``@Model.setter`` can be used for
defining logical OPs getter and setter respectively. The syntax and
semantics are very similar to the python ``@property`` 
decorator. 

E.g. for logical OP ``happiness`` in the previous example: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto" 
   
    __observables__ = ("name", "happiness")

    _a_value = 1.0 # support for happiness
    @Model.getter
    def happiness(self): return self._a_value

    @Model.setter
    def happiness(self, value): self._a_value = max(1.0, value)

    pass # end of class
 # ----------------------------


It is possible to define getter/setter methods which serve multiple
logical OPs.
For example: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto" 
   
    __observables__ = ("name", "happiness", "energy")

    _a_value = 1.0 # support for happiness
    @Model.getter("happiness", "energy")
    def a_getter_for_several_ops(self, name): 
      if "energy" == name: return 0.1 # constantly need holidays!
      return self._a_value

    @Model.setter
    def happiness(self, value): self._a_value = max(1.0, value)

    pass # end of class
 # ----------------------------

In the example, the decorator ``@Model.getter`` is used with
arguments, which have to be the string names of all properties
which have to be handled by the decorated method. The method (the
getter in this case) will receive the name of the property along
with its other arguments.

Use of wildcards is allowed in decorators names, and will match all
logical OPs not exactly matched by other decorators. It is an error
condition if multiple matches are found when matching logical OPs
specified with wildcards. For example this is perfectly legal: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto" 
    
    __observables__ = ("name", "energy", "entropy", "enology")

    @Model.getter
    def energy(self): return 0.1  # constantly need holidays!

    @Model.getter("enology")
    def getter1(self, name): return "good science!"

    @Model.getter("en*") # matches only remaining 'entropy'
    def getter2(self, name): 
      assert "entropy" == name
      return 0
    
    @Model.setter("*") # matches "energy", "entropy", "enology"
    def happiness(self, name, value): 
        print "setter for", name, value
        ...
        return


    pass # end of class
 # ----------------------------


However, this example is not legal: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    
    __observables__ = ("energy", "entropy", "enology")

    @Model.getter("en*") # matches energy, entropy, and enology
    def getter1(self, name): ...

    @Model.getter("*") # matches energy, entropy, and enology
    def getter2(self, name): ...

    pass # end of class
 # ----------------------------

The example does not work as ambiguity is found when resolving
wilcards.


Use of naming convention for defining getters and/or setters
------------------------------------------------------------

In some cases, the use of decorators for defining getters/setters
can be a limitation. For example, when the model is built
dynamically, like when generating proxy classes.

In these and other cases, the framework supports a *naming
convention* which can be used to define implicitly getters and/or
setters for logical OPs. 

The naming convention applies to Model's method names which are
implicitly declared as getters or setters.

* `get_<prop_name>_value(self)`: A specific getter for OP `<prop_name>`.
* `set_<prop_name>_value(self, value)`: A specific setter for OP `<prop_name>`.
* `get__value(self, name)`: A generic getter receiving the name of
  the property to be get.
* `set__value(self, name, value)`: A generic setter receiving the name of
  the property to be set.

As you see getters/setters can be either *specific* or
*generic*. In the former case, the getter/setter is specific for
one OP. In the latter case, getter/setter is general and will
receive the name of the property.

Generic getter/setter will not be called for OPs which have
specific getter/setter defined. For example: ::
 
 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    __observables__ = ("energy", "entropy", "enology")

    def get_energy_value(self): return 0.1  # constantly need holidays!

    # getter for entropy and enology only, as energy has a specific getter
    def get__value(self, name): ...

    # setter for all properties
    def set_value(self, name, value): ...

    pass # end of class
 # ----------------------------

The first example we presented for decorators could be rewritten
as: ::

 from gtkmvc import Model
 # ----------------------------
 class MyModel (Model):
    name = "Roberto" 
    
    __observables__ = ("name", "energy", "entropy", "enology")

    def get_energy_value(self): return 0.1  # constantly need holidays!

    def get_enology_value(self): return "good science!"

    def get__value(self, name): 
      assert "entropy" == name
      return 0
    
    def set__value(self, name, value): 
        print "setter for", name, value
        ...
        return

    pass # end of class
 # ----------------------------

Of course, since in naming conventions names *matters*, some names
in the example had to be adapted.
