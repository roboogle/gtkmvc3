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

        self.__CUST_OBS_MAP = {}

        # searches all custom observer methods: (method-name, method, property-names)        
        processed_props = set() # tracks already processed properties
        for cls in inspect.getmro(type(self)):
            meths = [ (name, meth, getattr(meth, Observer._CUST_OBS_))
                      for name, meth in cls.__dict__.iteritems()
                      if inspect.isfunction(meth) and hasattr(meth, Observer._CUST_OBS_)]

            # props processed in this class. This is used to avoid
            # processing the same props in base classes.
            cls_processed_props = set() 
            
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
                        self.__CUST_OBS_MAP[name].add((geattr(self, name), 0))
                        cls_processed_props.add(name)
                        pass
                    pass
                else: 
                    if 1 == len(pnames): args = 0
                    else: args = 1
                    for prop_name in pnames:
                        if prop_name not in processed_props:
                            if not self.__CUST_OBS_MAP.has_key(prop_name):
                                self.__CUST_OBS_MAP[prop_name] = set()
                                pass
                            # (method-name, does_it_take_name)
                            self.__CUST_OBS_MAP[prop_name].add((getattr(self, name), args))
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

    def get_custom_observing_methods(self, prop_name):
        """Given a property name, returns a set of pairs (method,
        num-of-additional-args). Each method in the pair has one
        equivalent menthod in the mro explicitly marked to be
        observables of the given property. num-of-additional-args
        is the number of additional arguments which the method
        receives (can be 0 or 1) if receives also the name of the
        property (used for multi-properties).  This method is
        called by models when searching for notification methods."""
        return self.__CUST_OBS_MAP.get(prop_name, set())
    
    pass # end of class

    
        
