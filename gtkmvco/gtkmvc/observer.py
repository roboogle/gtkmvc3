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
import collections


class NTInfo (dict):
    """Notification Type of observers' notification methods.

    This class is a dictionary-like object used:

    1. As class when defining notification methods in observers, as it
       contains the flags identifying the notification types.

    2. As class instance as parameter when a notification methods is
       called in observers.


    Notification Type Flags
    =======================
    
    Notification methods are declared either statically with decorator
    `@Observer.observe` or dynamically calling the (same) method
    `Observer.observe(...)`. In both cases the type of the
    notification is defined by setting to `True` some flags. Flags can
    be set in any combination for multi-type notification
    methods. Flags are:

      `assign` : For notifications issued when OPs are assigned.
      `before` : For notifications called before a modifying method is
                 called.
      `after`  : For notifications called after a modifying method is
                 called.
      `signal` : For notifications called when a signal is emitted.

    
    Instance content
    ================

    Instances of class `NTInfo` will be received as the last argument
    (`info`) of any notification method::

      def notification_method(self, model, name, info)

    NTInfo is a dictionary (with some particular behaviour added)
    containing some information which is independent on the
    notification type, and some other information wich depends on the
    notification type.


    Common to all types
    -------------------

    For all notification types, NTInfo contains:

      model : the model containing the observable property triggering
              the notification. `model` is also passed as first
              argument of the notification method.

      prop_name : the name of the observable property triggering the
                  notification. `name` is also passed as second
                  argument of the notification method.
      
    Furthermore, any keyword argument not listed here is copied
    without modification into `info`.

    There are further information depending on the specific
    notification type:

    For Assign-type
    ---------------
      assign : flag set to `True`
      
      old : the value that the observable property had before being
            changed.

      new : the new value that the observable property has been
            changed to.


    For Before method call type
    ---------------------------
      before : flag set to `True`

      instance : the object instance which the method that is being
                 called belongs to.

      method_name : the name of the method that is being called. 

      args : tuple of the arguments of the method that is being called. 

      kwargs: dictionary of the keyword arguments of the method that
              is being called.


    For After method call type
    ---------------------------
      after : flag set to `True`

      instance : the object instance which the method that has been 
                 called belongs to.

      method_name : the name of the method that has been called. 

      args : tuple of the arguments of the method that has been called. 

      kwargs: dictionary of the keyword arguments of the method that
              has been called.
      
      result : the value returned by the method which has been called. 
 
    For Signal-type
    ---------------
      signal : flag set to `True`
    
      arg : the argument which was optionally specified when invoking
            emit() on the signal observable property.
  
    Information access
    ==================

    The information carried by a NTInfo instance passed to a
    notification method can be retrieved using the instance as a
    dictionary, or accessing directly to the information as an
    attribute of the instance. For example::
       
       # This is a multi-type notification
       @Observer.observe("op1", assign=True, hello="Ciao")
       @Observer.observe("op2", after=True, before=True)
       def notify_me(self, model, name, info):
           assert info["model"] == model # access as dict key
           assert info.prop_name == name # access as attribute

           if "assign" in info:
              assert info.old == info["old"]
              assert "hello" in info and "ciao" == info.hello
              print "Assign from", info.old, "to", info.new
           else:
              assert "before" in info or "after" in info
              assert "hello" not in info
              print "Method name=", info.method_name
              if "after" in info: print "Method returned", info.result              
              pass
              
           return   

    As already told, the type carried by a NTInfo instance can be
    accessed through boolean flags `assign`, `before`, `after` and
    `signal`. Furthermore, any other information specified at
    declaration time (keyword argument 'hello' in the previous
    example) will be accessible in the corresponding notification
    method.

       .. versionadded:: 1.99.1

    """

    # At least one of the keys in this set is required when constructing
    __ONE_REQUESTED = frozenset("assign before after signal".split())
    __ALL_REQUESTED = frozenset("model prop_name".split())

    def __init__(self, _type, *args, **kwargs):
        """_type is a sting in (assign before after signal) which
        identifies the type."""
        
        dict.__init__(self, *args, **kwargs)
        
        # checks the content provided by the user        
        if not (_type in self and self[_type]):
            raise KeyError("flag '%s' must be set in given arguments" % _type)

        # all requested are provided by the framework, not the user
        assert all((x in self for x in NTInfo.__ALL_REQUESTED))

        # now removes all type-flags not related to _type
        for flag in NTInfo.__ONE_REQUESTED:
            if flag != _type and flag in self: del self[flag]
            pass
        
        return

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError: 
            raise AttributeError("NTInfo object has no attribute '%s'.\n"
                                 "Existing attributes are: %s" % (name, str(self)))
        pass

    pass # end of class NTInfo
# ----------------------------------------------------------------------
    


@decorators.good_decorator_accepting_args
def observes(*args):
    """
    Decorate a method in an :class:`Observer` subclass as a notification.
    Takes one to many property names as strings. If any of them changes
    in a model we observe, the method is called. The name of the property 
    will be passed to the method. 

    The decorated method has to have one of these prototypes:

      def value_notify(self, model, name, old, new)
      def before_notify(self, model, name, instance, method_name, args, kwargs)
      def after_notify(self, model, name, instance, method_name, res, args, kwargs)
      def signal_notify(self, model, name, arg)

       .. versionadded:: 1.99.0

       .. deprecated:: 1.99.1
          Use :meth:`Observer.observe` instead, which offers more features.
    """

    @decorators.good_decorator
    def _decorator(_notified):
        # marks the method with observed properties
        _list = getattr(_notified, Observer._CUST_OBS_, list())        

        # here the notificaion type is inferred out of the number of
        # arguments of the notification method. This is not
        # particularly robust.
        margs, mvarargs, _, _ = inspect.getargspec(_notified)
        mnumargs = len(margs)
        if not mvarargs:
            args_to_type = { 4 : 'signal',
                             5 : 'assign',
                             7 : 'before',
                             8 : 'after', 
                             }
            try : 
                type_kw = args_to_type[mnumargs]
                # warning: flag _old_style_call is used this as
                # deprecated call mechanism like in
                # <property_<name>_...
                _list += [(arg, dict({type_kw : True, 
                                      'old_style_call' : True}))
                          for arg in args]
                setattr(_notified, Observer._CUST_OBS_, _list)

            except KeyError:
                log.logger.warn("Ignoring notification %s: wrong number of"
                                " arguments (given %d, expected in (%s))", 
                                _notified.__name__, mnumargs, 
                                ",".join(map(str, args_to_type)))
                pass
        else:
            log.logger.warn("Ignoring notification %s: variable arguments"
                            " prevent type inference", _notified.__name__)
            pass
        return _notified

    # checks arguments
    if 0 == len(args): 
        raise TypeError("decorator observe() takes one of more arguments (0 given)")
    if any(type(arg) != str for arg in args):
        raise TypeError("decorator observe() takes only strings as arguments")    

    log.logger.warning("Decorator observer.observers is deprecated:"
                       "use Observer.observe instead")
    return _decorator
# ----------------------------------------------------------------------


class Observer (object):
    """
    .. note::

       Most methods in this class are used internally by the
       framework.  Do not override them in subclasses.
    """

    # this is internal
    _CUST_OBS_ = "__custom_observes__"
    # ----------------------------------------------------------------------   


    @classmethod
    @decorators.good_decorator_accepting_args
    def observe(cls, *args, **kwargs):
        """
        If used as decorator, decorates a method as a notification
        method. If called, declares dynamically a new notification
        methods.

        Used as decorator
        =================
        Takes one string (the property name), and at least one boolean
        keyword argument identifying the types of the
        notification. The keyword argument has to be set to True in
        the set `{assign, before, after, signal}`.

        If other keyword arguments are provided, they will be found in
        the dictionary passed to the notification method.

        The decorator can be used multiple times to define
        notification methods which has to be called for multiple
        observable properties.

        Used dynamically
        ================
        To declare dynamically that a method is a notification method,
        `Observer.observe` has to be called specifying the method as
        first argument (not counting Observer `self`). The remaining
        arguments are the property name and keyword arguments like
        described in the use as decorator.

           .. versionadded:: 1.99.1
        """
        
        @decorators.good_decorator
        def _decorator(_notified):
            # marks the method with observed properties
            _list = getattr(_notified, Observer._CUST_OBS_, list())
            _list.append((name, kwargs))
            setattr(_notified, Observer._CUST_OBS_, _list)
            return _notified 

        # handles arguments
        if args and isinstance(args[0], cls):
            # used as instance method, for declaring notifications
            # dynamically
            if len(args) != 3: 
                raise TypeError("observe() takes exactly three arguments"
                                " when called (%d given)" % len(args))
            
            self = args[0]
            notified = args[1]
            name = args[2]            

            assert isinstance(self, Observer), "Method Observer.observe " \
                "must be called with an Observer instance as first argument"
            if not isinstance(notified, collections.Callable):
                raise TypeError("Second argument of observe() must be a callable")
            if type(name) != str: 
                raise TypeError("Third argument of observe() must be a string")
            
            # fills the internal structures
            if not self.__CUST_OBS_KWARGS.has_key(notified):
                if not self.__CUST_OBS_MAP.has_key(name):
                    self.__CUST_OBS_MAP[name] = set()
                    pass
                self.__CUST_OBS_MAP[name].add(notified)
                self.__CUST_OBS_KWARGS[notified] = kwargs
                pass            
            
            return None

        # used statically as decorator
        if len(args) != 1: 
            raise TypeError("observe() takes exactly one argument when used"
                            " as decorator (%d given)" % len(args))
        name = args[0]
        if type(name) != str: 
            raise TypeError("First argument of observe() must be a string")
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

        # --------------------------------------------------------- #
        # This turns the decorator 'observe' an instance method
        def __observe(*args, **kwargs): self.__original_observe(self, *args, **kwargs)
        __observe.__name__ = self.observe.__name__
        __observe.__doc__ = self.observe.__doc__
        self.__original_observe = self.observe
        self.observe = __observe
        # --------------------------------------------------------- #

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
        self.__CUST_OBS_KWARGS = {} # observing method --> flag 

        processed_props = set() # tracks already processed properties

        # searches all custom observer methods
        for cls in inspect.getmro(type(self)):
            # list of (method-name, method-object, list of (prop-name, kwargs))
            meths = [ (name, meth, getattr(meth, Observer._CUST_OBS_))
                      for name, meth in cls.__dict__.iteritems()
                      if (inspect.isfunction(meth) and 
                          hasattr(meth, Observer._CUST_OBS_)) ]

            # props processed in this class. This is used to avoid
            # processing the same props in base classes.
            cls_processed_props = set() 
            
            # since this is traversed top-bottom in the mro, the
            # first found match is the one to care
            for name, meth, pnames_ka in meths:
                for pname, ka in pnames_ka:
                    if pname not in processed_props:
                        if not self.__CUST_OBS_MAP.has_key(pname):
                            self.__CUST_OBS_MAP[pname] = set()
                            pass
                        _me = getattr(self, name) # the most top avail method 
                        self.__CUST_OBS_MAP[pname].add(_me)

                        # first hit matters
                        if not self.__CUST_OBS_KWARGS.has_key(_me):
                            self.__CUST_OBS_KWARGS[_me] = ka
                            pass
                            
                        cls_processed_props.add(pname)
                        pass
                    pass
                pass 
            
            # accumulates props processed in this class
            processed_props |= cls_processed_props
            pass # end of loop over classes in the mro

        if model: self.observe_model(model)
        return   
    
    def observe_model(self, model):
        """Starts observing the given model"""
        return model.register_observer(self)

    def relieve_model(self, model):
        """Stops observing the given model"""
        return model.unregister_observer(self)
    
    def accepts_spurious_change(self):
        """
        Returns True if this observer is interested in receiving
        spurious value changes. This is queried by the model when
        notifying a value change."""
        return self.__accepts_spurious__

    def get_observing_methods(self, prop_name):
        """
        Return a possibly empty set of callables registered with
        :meth:`observe` for *prop_name*.
        
        .. versionadded:: 1.99.1
        Replaces :meth:`get_custom_observing_methods`.
        """
        return self.__CUST_OBS_MAP.get(prop_name, set())

    # this is done to keep backward compatibility
    get_custom_observing_methods = get_observing_methods
    
    def get_observing_method_kwargs(self, method):
        """
        Returns the keyword arguments which were specified when
        declaring a notification method, either statically of
        synamically with :meth:`Observer.observe`.

        *method* a callable that was registered with
        :meth:`observes`.
        
        :rtype: dict
        """
        return self.__CUST_OBS_KWARGS[method]
    

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
        
        if method in self.__CUST_OBS_KWARGS: del self.__CUST_OBS_KWARGS[method]
        return

    def is_observing_method(self, method):
        """
        Returns `True` if the given method was previously added as an
        observing method, either dynamically or via decorator.
        """
        return method in self.__CUST_OBS_KWARGS

    pass # end of class
# ----------------------------------------------------------------------
