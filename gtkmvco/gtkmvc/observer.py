#  -------------------------------------------------------------------------
#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2006 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.
#  -------------------------------------------------------------------------

from support import decorators, utils, log

import inspect
import types

@decorators.good_decorator_accepting_args
def observes(*args):
    """
    Decorate a method in an :class:`Observer` subclass as a notification.
    Takes one to many property names as strings. If any of them changes
    in a model we observe, the method is called. If multiple names were given
    the method will be passed the name of the property that changed.

       .. versionadded:: 1.99.0

       .. deprecated:: 1.99.1
          Use :meth:`Observer.observes` instead.
    """

    @decorators.good_decorator
    def _decorator(_notified):
        # marks the method with observed properties
        _set = getattr(_notified, Observer._CUST_OBS_, set())
        _set |=  set(args)
        setattr(_notified, Observer._CUST_OBS_, _set)
        return _notified

    log.logger.warning("Decorator observer.observers is deprecated:"
                       "use Observer.observes instead")
    return _decorator
# ----------------------------------------------------------------------


# private metaclass, used to force read-only class-level properties.
class __NTinfo_mc__ (type):
    NT_AUTO  = property(lambda cls: 0) # for internal use only
    NT_VALUE  = property(lambda cls: 1)
    NT_BEFORE = property(lambda cls: 2)
    NT_AFTER  = property(lambda cls: 4)
    NT_SIGNAL = property(lambda cls: 8)
    pass # end of metaclass


class NTInfo (dict):
    """Notification Type of observers' notification methods.

    This class is used:

    1. As class when defining notificaion methods in observers, as it
       contains the constants for notification types.

    2. As class instance as parameter when a notification methods is
       called in observers.


    Notification Type Constants
    ===========================

    Class `NTInfo` exports these notification type constants:
    
    NT_VALUE: For value-change notification types. 
    NT_BEFORE: For before-method-call notification types.
    NT_AFTER: For after-method-call notification types.
    NT_SIGNAL: For signal-emit notification types.

    
    Instance content
    ================

    Instances of class `NTInfo` will be received as the last argument
    (`info`) of any notification method::

      def notification_method(self, model, name, info)

    NTInfo is a dictionary (with some particular behaviour added),
    containing some information which is independent on the
    notification type, and some other information wich depends on the
    notification type.


    Common to all types
    -------------------

    For all notification types, NTInfo contains:

      model : the model containing the observable property triggering
              the notification. model is also passed as first argument
              of the notification method.

      name : the name of the observable property triggering the
             notification. name is also passed as second argument of
             the notification method.

      type : The value identifying the type of the notification
             method. This is generally one value among NT_VALUE,
             NT_BEFORE, NT_AFTER and NT_SIGNAL, but more generally it
             can be also a bitwise combination of these values.
  
    There are further information depending on the specific
    notification type:

    For NT_VALUE
    ------------

      old : the value that the observable property had before being
            changed.

      new : the new value that the observable property has been
            changed to.


    For NT_BEFORE
    -------------

      instance : the object instance which the method that is being
                 called belongs to.

      method_name : the name of the method that is being called. 

      args : tuple of the arguments of the method that is being called. 

      kwargs: dictionary of the keyword arguments of the method that
              is being called.


    For NT_AFTER
    ------------

      instance : the object instance which the method that has been 
                 called belongs to.

      method_name : the name of the method that has been called. 

      args : tuple of the arguments of the method that has been called. 

      kwargs: dictionary of the keyword arguments of the method that
              has been called.
      
      result : the value returned by the method which has been called. 
 
    For NT_SIGNAL
    -------------

      arg : the argument which was optionally specified when invoking
            emit() on the signal observable property.
  
    Type queries
    ============

    As already told, the type carried by a NTInfo instance can be
    accessed through attribute `type`, to be matched type constants
    available in class `NTInfo`, possibly with bit masks.  However,
    class `NTInfo` provides also predicates to query for type, like
    methods `is_value`, `is_before`, etc.

       .. versionadded:: 1.99.1

    """

    __metaclass__ = _NTinfo_mc
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        # if not already set, sets the default type
        if 'type' not in self: self['type'] = NTInfo.NT_VALUE
        return

    def __getattr__(self, name): return self[name]

    def is_value(self): 
        return self['type'] & NTInfo.NT_VALUE != 0

    def is_before(self): 
        return self['type'] & NTInfo.NT_BEFORE != 0

    def is_after(self): 
        return self['type'] & NTInfo.NT_AFTER != 0

    def is_signal(self): 
        return self['type'] & NTInfo.NT_AFTER != 0
    
    pass # end of class
    

# ----------------------------------------------------------------------
class Observer (object):
    """
    .. note::

       Most methods in this class are used internally by the framework.
       Do not override them in subclasses.
    """

    # these are internal
    _CUST_OBS_ = "__custom_observes__"

    @classmethod
    @decorators.good_decorator_accepting_args
    def observes(cls, *args, **kwargs):
        """
        Decorate a method as a notification. Takes an arbitrary number
        of property names as strings. If none are given, the name of
        the method is used. If a given property changes in a model we
        observe, the method is called.

        Keyword argument 'type' can be used to specify the type of the
        notification. Values for type are type constants in class
        `NTInfo`.  Values for `type` can be combined for declaring
        notifications which can receive notification of several
        types. If `type` is not specified, the default value is
        `NTInfo.NT_VALUE`.

           .. versionadded:: 1.99.1
        """
        
        @decorators.good_decorator
        def _decorator(_notified):
            # marks the method with observed properties
            _set = getattr(_notified, Observer._CUST_OBS_, set())
            _set |=  set(names)
            setattr(_notified, Observer._CUST_OBS_, _set)
            return _notified        

        # this handle the case of empty args
        if 1 == len(args) and type(args[0]) is types.FunctionType:
            names = ()
            return _decorator(args[0])

        # this is the case with arguments
        names = args
        return _decorator
    # ----------------------------------------------------------------------
    
    def __init__(self, model=None, spurious=False):
        """
        *model* is passed to :meth:`observe_model` if given.
        
        *spurious* indicates interest to be notified even when
        the value hasn't changed, like for: ::

         model.prop = model.prop

        .. versionadded:: 1.2.0
           Before that observers had to filter out spurious
           notifications themselves, as if the default was `True`. With
           :class:`~gtkmvc.observable.Signal` support this is no longer
           necessary.
        """

        self.__accepts_spurious__ = spurious

        # NOTE: In rev. 202 these maps were unified into
        #   __CUST_OBS_MAP only (the map contained pairs (method,
        #   args). However, this broke backward compatibility of code
        #   accessing the map through
        #   get_observing_methods. Now the informatio is split
        #   and the original information restored. To access the
        #   additional information (number of additional arguments
        #   required by observing methods) use the newly added methods.

        # Private maps: do not change/access them directly, use
        # methods to access them:
        self.__CUST_OBS_MAP = {} # prop name --> set of observing methods
        self.__CUST_OBS_ARGS = {} # observing method --> flag 

        processed_props = set() # tracks already processed properties

        # searches all custom observer methods
        for cls in inspect.getmro(type(self)):
            # list of (method-name, method-object, list-of-properties-the-method-observes)
            meths = [ (name, meth, getattr(meth, Observer._CUST_OBS_))
                      for name, meth in cls.__dict__.iteritems()
                      if inspect.isfunction(meth) and hasattr(meth, Observer._CUST_OBS_)]

            # props processed in this class. This is used to avoid
            # processing the same props in base classes.
            cls_processed_props = set() 
            
            # TODO: fix this code to call add_observing_method

            # since this is traversed top-bottom in the mro, the
            # first found match is the one to care
            for name, meth, pnames in meths:
                if 0 == len(pnames):
                    # no args were specified in the decorator. In this
                    # case the method does not take the prop name among
                    # its arguments, and the property name is taken
                    # from the method name.
                    if name not in processed_props:
                        if not self.__CUST_OBS_MAP.has_key(name):
                            self.__CUST_OBS_MAP[name] = set()
                            pass
                        _me = getattr(self, name)
                        self.__CUST_OBS_MAP[name].add(_me)
                        
                        # first hit matters
                        if not self.__CUST_OBS_ARGS.has_key(_me):
                            self.__CUST_OBS_ARGS[_me] = False # no additional args
                            pass
                        cls_processed_props.add(name)
                        pass
                    pass
                else: 
                    takes_arg = 1 < len(pnames)
                    for prop_name in pnames:
                        if prop_name not in processed_props:
                            if not self.__CUST_OBS_MAP.has_key(prop_name):
                                self.__CUST_OBS_MAP[prop_name] = set()
                                pass
                            _me = getattr(self, name)
                            self.__CUST_OBS_MAP[prop_name].add(_me)

                            # first hit matters
                            if not self.__CUST_OBS_ARGS.has_key(_me):
                                self.__CUST_OBS_ARGS[_me] = takes_arg
                                pass
                            
                            cls_processed_props.add(prop_name)
                            pass
                        pass
                    pass
                pass 
            
            # accumulates props processed in this class
            processed_props |= cls_processed_props
            pass # end of loop over classes in the mro

        if model: self.observe_model(model)
        return
    
    def observe_model(self, model):
        """
        Call :meth:`~gtkmvc.model.Model.register_observer` on *model*.
        """
        return model.register_observer(self)

    def relieve_model(self, model):
        """
        Call :meth:`~gtkmvc.model.Model.unregister_observer` on *model*.
        """
        return model.unregister_observer(self)
    
    def accepts_spurious_change(self):
        """
        Are we interested in spurious notifications?

        :rtype: bool
        """
        return self.__accepts_spurious__

    def add_observing_method(self, method, 
                             prop_name_or_names):
        """
        Add notifications at runtime.
        
        *method* is a callable bound to `self`.
        
        *prop_name_or_names* can be a string or a sequence of strings.
        In the latter case the name of the property that changed will be
        passed to the method during notifications.
        
        Multiple calls may add different methods for the same names as well as
        additional names for the same method. However, the signature of the
        method is always determined by the last call. ::

         def observes_one_property(self, model, old, new)

         def observes_multiple(self, model, prop_name, old, new)

        .. note::

           Dynamic methods only work if you add/remove them before starting
           to observe a model.
        """

        if isinstance(prop_name_or_names, types.StringType):
            takes_name = False
            prop_names = (prop_name_or_names,)
        else:
            try:
                iter(prop_name_or_names)
            except TypeError:
                raise AssertionError("prop_name_or_names must be either a"
                    " string or an iterable")
            takes_name = True
            prop_names = prop_name_or_names
            pass
                          
        for prop_name in prop_names:
            if not self.__CUST_OBS_MAP.has_key(prop_name):
                self.__CUST_OBS_MAP[prop_name] = set()
                pass
            self.__CUST_OBS_MAP[prop_name].add(method)
            pass
        self.__CUST_OBS_ARGS[method] = takes_name
        return

    def remove_observing_method(self, method, prop_names):
        """
        Remove dynamic notifications.
        
        *method* a callable that was registered with 
        :meth:`add_observing_method` or :meth:`observes`.
        
        *prop_names* a sequence of strings. This need not correspond to any
        one `add` call.

        .. note::

           This can revert the effects of a decorator at runtime. Don't.
        """
        for prop_name in prop_names:
            _set = self.__CUST_OBS_MAP.get(prop_name, set())
            if method in _set: _set.remove(method)
            pass
        
        if method in self.__CUST_OBS_ARGS: del self.__CUST_OBS_ARGS[method]
        return

    def is_observing_method(self, method):
        """
        Returns `True` if the given method was previously added as an
        observing method, either dynamically or via decorator.
        """
        return self.__CUST_OBS_ARGS.has_key(method)
    
    def get_observing_methods(self, prop_name):
        """
        Return a possibly empty set of callables registered with
        :meth:`add_observing_method` or :meth:`observes` for *prop_name*.

        .. versionadded:: 1.99.1
           Replaces :meth:`get_custom_observing_methods`.
        """
        return self.__CUST_OBS_MAP.get(prop_name, set())

    # this is done to keep backward compatibility
    get_custom_observing_methods = get_observing_methods

    def does_observing_method_receive_prop_name(self, method):
        """
        Will the method be passed the name of the property that changed on
        notification? This additional argument is meant for methods that are
        registered for more than one property.
        
        *method* a callable that was registered with
        :meth:`add_observing_method` or :meth:`observes`.
        
        :rtype: bool
        """
        return self.__CUST_OBS_ARGS[method]
    
    pass # end of class

    
        
