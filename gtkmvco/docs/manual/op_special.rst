=========================================
Special members for Observable Properties
=========================================

Classes derived from Model, that exports *OPs*, have several special
members. Advanced users might be interested in overriding some of them,
but in general they should be considered as private members. They are
explained here for the sake of completeness.

``__observables__``
   A class (static) member that lists property
   names. This must be provided as either a tuple or a list by the
   user. Wilcards in names can be used to match property names, but
   properties with names starting with a double underscore
   ``__`` will be not matched.

``__properties__``
   (Deprecated, do not use anymore) A dictionary mapping
   observable properties names and their initial value. This
   variable has been substituted by __observables__. 
 
``__derived_properties__``
   (Deprecated) Automatically generated static member
   that maps the *OPs* exported by all base classes. This does not
   contain *OPs* that the class overrides.
 
``_prop_<property_name>``
   This is an
   auto-generated variable holding the property value. For example,
   a property called ``x`` will generate a variable called
   ``_prop_x``.
 
``get_prop_<property_name>``
   This public method
   is the getter for the property. It is automatically generated only
   if the user does not define one. This means that the user can change
   the behavior of it by defining their own method.  For example, for
   property ``x`` the method is ``get_prop_x``.  This
   method gets only self and returns the corresponding property value.
 
``set_prop_<property_name>``
   This public method
   is customizable like 
   ``get_prop_<property_name>``.  This does not return
   anything, and gets self and the value to be assigned to the
   property. The default auto-generated code also calls method
   ``gtkmvc3.Model.notify_property_change`` to notify the
   change to all registered observers.
 

For further details about this topic see meta-classes ``PropertyMeta``
and ``ObservablePropertyMeta`` from package ``support``.
