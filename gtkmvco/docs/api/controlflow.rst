How it all works
================

Applications programmers only need this for debugging, but if you want to
contribute to gtkmvc here's a rough outline of how it works.

Pseudocode
----------

::

 class PropertyMeta(type):
     def __init__():
         obs = metaclass.__get_observables_array__(newclass)
         old = newclass.__properties__
 
         for name in obs + old:
             metaclass.__create_prop_accessors__(newclass, name, value)
 
         newclass.__all_observables__ = obs + old + superclass.__all_observables__
 
     def __get_observables_array__():
         for name in newclass.__observables__:
             expand_wildcards
             # assert newclass.value or getter and setter, possibly generic
         
     def __create_prop_accessors__():
         newclass.set_name = eval(metaclass.get_setter_source)
         newclass.name = property(getter, setter)
         newclass.name = metaclass.create_value(default)
 
     def create_value():
         # choose appropriate wrapper and apply it,
         if model:
             value.__add_model__
 
     def get_getter_source():
         NotImplemented
 
 class ObservablePropertyMeta(PropertyMeta):
 
   def get_getter_source():
       # look in class for instance variable or getter function and
       return match
 
   def get_setter_source():
       return """
       as getter, but with in metclass.create_value,
       class.notify_property_value_change and, if class.check_value_change
       class._reset_property_notification
       """
 
 class Observer(object):
 
     __accepts_spurious__ = False
 
     def __init__():
         for method in dir(self):
             for prop_name in getattr(method, __custom_observes__, set):
                 self.__CUST_OBS_MAP[prop_name].add(method)
 
     def get_custom_observing_methods(prop_name):
         return self.__CUST_OBS_MAP
 
 class Model(Observer):
 
     __metaclass__  = ObservablePropertyMeta
 
     __properties__ = {}
     __observables__ = ()
     
     def __init__():
         for name in self.__all_observables__:
             self.register_property
 
     def register_property():
         self.__value_notifications[name] = []
         if isinstance(value, ObsWrapperBase):
             wrapper.__add_model__(self, name)
             self.__instance_notif_before[name] = []
 
     def register_observer():
         for name in metaclass.__all_observables__:
             self.__add_observer_notification
 
     def __add_observer_notification():
         for method in observer.get_custom_observing_methods + \
             methods_matching_naming_schema:
             
             self.__value_notifications[prop_name].append(
                 (implicit_flag, method))
 
     def _reset_property_notification():
         self.__remove_observer_notification
         self.__add_observer_notification
     
     def notify_property_value_change():
         for implicit_flag, method in self.__value_notifications[prop_name]:
             if flag:
                 method()
             else:
                 method(prop_name)

Textual
-------

PropertyMeta.__get_observables_array__ takes the __observables__ of the class to create and expands wildcards. Names have to either exist as a value or getter/setter pair, with fallback to a generic getter/setter.

PropertyMeta.__init__ calls __create_prop_accessors__ on __get_observables_array__ and the class's __properties__, then merges the names with its bases' __all_observables__ set.

__create_prop_accessors__ uses get_g/setter_source and property() to create attributes for the new class, three per observable, and calls the setter with any previous value, wrapping it first. The default g/setter doesn't do anything!

ObservablePropertyMeta overrides get_getter_source to look for getters matching the naming scheme or use an attribute. get_setter_source wraps using the metaclass' create_value and calls the new self's _reset_property_notification and notify_property_value_change.

Observer.__accepts_spurious__ = False

Observer.__CUST_OBS_MAP[prop_name] = set of methods bound to self
Uppercase sic! Populated by __init__ with methods that have a __custom_observes__ attribute which is a set of property names. Accessor get_custom_observing_methods(prop_name)

Model inherits Observer and is created by ObservablePropertyMeta. The constructor calls register_property on self.__all_observables__. This adds their empty lists for their names to dictionaries self.__value_notifications and, for wrappers, self.__instance_notif_before and after. It also calls __add_model__(self, name) of ObsWrapperBase instances.

On registering an observer __add_observer_notification is called for each property. this does the name matching and gets custom methods. It fills the notification lists with tuples of implicit/explicit flag (to decide the number of arguments) and bound method.
