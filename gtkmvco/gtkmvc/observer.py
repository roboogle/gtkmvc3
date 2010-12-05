#  -------------------------------------------------------------------------
#  Author: Roberto Cavada <cavada@fbk.eu>
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
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.
#  -------------------------------------------------------------------------

from support import decorators, utils, log
from types import MethodType, StringType, FunctionType
from collections import Iterable

import inspect

@decorators.good_decorator_accepting_args
def observes(*args):
    """Use this decorator with methods in observers that are
    intended to be used for notifications. args is an arbitrary
    number of arguments with the names of the observable
    properties to be observed"""

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


# ----------------------------------------------------------------------
class Observer (object):
    """Use this class as base class of all observers"""

    # these are internal
    _CUST_OBS_ = "__custom_observes__"

    @classmethod
    @decorators.good_decorator_accepting_args
    def observes(cls, *args):
        """Use this decorator with methods in observers that are
        intended to be used for notifications. args is an arbitrary
        number of arguments with the names of the observable
        properties to be observed. If empty, the name of the
        property must be equal to the name of the observing
        method."""
        
        @decorators.good_decorator
        def _decorator(_notified):
            # marks the method with observed properties
            _set = getattr(_notified, Observer._CUST_OBS_, set())
            _set |=  set(names)
            setattr(_notified, Observer._CUST_OBS_, _set)
            return _notified        

        # this handle the case of empty args
        if 1 == len(args) and type(args[0]) is FunctionType:
            names = ()
            return _decorator(args[0])

        # this is the case with arguments
        names = args
        return _decorator
    # ----------------------------------------------------------------------
    
    def __init__(self, model=None, spurious=False):
        """
        When parameter spurious is set to False
        (default value) the observer declares that it is not
        interested in receiving value-change notifications when
        property's value does not really change. This happens when a
        property got assigned to a value that is the same it had
        before being assigned.

        A notification was used to be sent to the observer even in
        this particular condition, because spurious (non-changing)
        assignments were used as signals when signals were not
        supported by early version of the framework. The observer
        was in charge of deciding what to do with spurious
        assignments, by checking if the old and new values were
        different at the beginning of the notification code. With
        latest version providing new notification types like
        signals, this requirement seems to be no longer needed, and
        delivering a notification is no longer a sensible
        behaviour.

        This is the reason for providing parameter spurious that
        changes the previous behaviour but keeps availability of a
        possible backward compatible feature.
        """

        self.__accepts_spurious__ = spurious

        # NOTE: In rev. 202 these maps were unified into
        #   __CUST_OBS_MAP only (the map contained pairs (method,
        #   args). However, this broke backward compatibility of code
        #   accessing the map through
        #   get_custom_observing_methods. Now the informatio is split
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
            
            # TODO: fix this code to call add_custom_observing_method

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

    def add_custom_observing_method(self, method, 
                                    prop_name_or_names):
        """Adds a custom osberving method to self. prop_name_or_names
        can be either:
        1. string name of a property which the method observes
        2. a sequence of string names which the given method observes.

        If a sequence of names is passed, then the method will also
        receive the property name among its arguments. Otherwise if a
        string name is passed, the method will not receive the name of
        the property, as the method is assumed to handle only
        notifications for one specific property.

        Multiple methods can be observing the same properties set.
        This method can be used to add observing method dynamically.

        Methods get_custom_observing_methods and
        does_observing_method_receive_prop_name can be used to
        retrieve information about the method later.

        If the given method has already be added before, information
        internally stored in the previous call will be substituted by
        the new call.
        """

        if isinstance(prop_name_or_names, StringType):
            takes_name = False
            prop_names = (prop_name_or_names,)
        else:
            assert isinstance(prop_name_or_names, Iterable), \
                "prop_name_or_names must be either a string or an iterable"
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

    def remove_custom_observing_method(self, method, prop_names):
        """Removes the given method from the observing methods
        set. Removal is performed for the observation of the given
        property names.

        This mthod can be used to revert (even partially) the effects
        of add_custom_observing_method.
        """
        for prop_name in prop_names:
            _set = self.__CUST_OBS_MAP.get(prop_name, set())
            if method in _set: _set.remove(method)
            pass
        
        if method in self.__CUST_OBS_ARGS: del self.__CUST_OBS_ARGS[method]
        return

    def is_custom_observing_method(self, method):
        """Returns True if given method has been previously added as
        observing method."""
        return self.__CUST_OBS_ARGS.has_key(method)
    
    def get_custom_observing_methods(self, prop_name):
        """Given a property name, returns a set of methods, Each
        method is an observing method, either explicitly marked to be
        observable with decorators, or added at runtime. Whether each
        method receive also the name of the property (for
        multi-properties observer methods) can be known by calling
        does_observing_method_receive_prop_name.

        This method is called by models when searching for
        notification methods."""
        return self.__CUST_OBS_MAP.get(prop_name, set())

    def does_observing_method_receive_prop_name(self, method):
        """Returns True iff the given observing method receives also
        the name of the property, i.e. it is a multi-properties
        observing method.
        This method is called by models when dealingsearching for
        notification methods.
        """
        return self.__CUST_OBS_ARGS[method]
    
    pass # end of class

    
        
