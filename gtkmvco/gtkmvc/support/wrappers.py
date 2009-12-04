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


import new


# ----------------------------------------------------------------------
class ObsWrapperBase (object):
    """
    This class is a base class wrapper for user-defined classes and
    containers like lists, maps, signals, etc.
    """
    
    def __init__(self):

        # all model instances owning self (can be multiple due to
        # inheritance). Each element of the set is a pair (model,
        # property-name)
        self.__models = set()
        return

    def __add_model__(self, model, prop_name):
        """Registers the given model to hold the wrapper among its
        properties, within a property whose name is given as well"""
        
        self.__models.add((model, prop_name))
        return

    def __get_models__(self): return self.__models

    def _notify_method_before(self, instance, name, args, kwargs):
        for m,n in self.__get_models__():
            m.notify_method_before_change(n, instance, name,
                                          args, kwargs)
            pass
        return

    def _notify_method_after(self, instance, name, res_val, args, kwargs):
        for m,n in self.__get_models__():
            m.notify_method_after_change(n, instance, name, res_val,
                                         args, kwargs)
            pass
        return
    
    pass # end of class
    

# ----------------------------------------------------------------------
class ObsWrapper (ObsWrapperBase):
    """
    Base class for wrappers, like user-classes and sequences. 
    """

    def __init__(self, obj, method_names):
        ObsWrapperBase.__init__(self)
        
        self._obj = obj
        self.__doc__ = obj.__doc__

        for name in method_names:
            if hasattr(self._obj, name):
                src = self.__get_wrapper_code(name)
                exec src
                
                code = eval("%s.func_code" % name)
                func = new.function(code, globals())
                meth = new.instancemethod(func, self, type(self).__name__)
                setattr(self, name, meth)
                pass
            pass

        return
   
    def __get_wrapper_code(self, name):
        return """def %(name)s(self, *args, **kwargs):
 self._notify_method_before(self._obj, "%(name)s", args, kwargs)
 res = self._obj.%(name)s(*args, **kwargs)
 self._notify_method_after(self._obj, "%(name)s", res, args, kwargs)
 return res""" % {'name' : name}

    # For all fall backs
    def __getattr__(self, name): return getattr(self._obj, name)
    def __repr__(self): return self._obj.__repr__()
    def __str__(self): return self._obj.__str__()
    
    pass #end of class


# ----------------------------------------------------------------------
class ObsSeqWrapper (ObsWrapper):
    def __init__(self, obj, method_names):
        ObsWrapper.__init__(self, obj, method_names)
        
        for _m in "lt le eq ne gt ge len iter".split():
            meth = "__%s__" % _m
            assert hasattr(self._obj, meth), "Not found method %s in %s" % (meth, str(type(self._obj)))
            setattr(self.__class__, meth, getattr(self._obj, meth))
            pass
        return

    def __setitem__(self, key, val):        
        self._notify_method_before(self._obj, "__setitem__", (key,val), {})
        res = self._obj.__setitem__(key, val)
        self._notify_method_after(self._obj, "__setitem__", res, (key,val), {})
        return res

    def __delitem__(self, key):
        self._notify_method_before(self._obj, "__delitem__", (key,), {})
        res = self._obj.__delitem__(key)
        self._notify_method_after(self._obj, "__delitem__", res, (key,), {})
        return res

    def __getitem__(self, key):
        return self._obj.__getitem__(key)
    
    pass #end of class


# ----------------------------------------------------------------------
class ObsMapWrapper (ObsSeqWrapper):
    def __init__(self, m):
        methods = ("clear", "pop", "popitem", "update",
                   "setdefault")
        ObsSeqWrapper.__init__(self, m, methods)
        return
    pass #end of class


# ----------------------------------------------------------------------
class ObsListWrapper (ObsSeqWrapper):
    def __init__(self, l):
        methods = ("append", "extend", "insert",
                   "pop", "remove", "reverse", "sort")
        ObsSeqWrapper.__init__(self, l, methods)

        for _m in "add mul".split():
            meth = "__%s__" % _m
            assert hasattr(self._obj, meth), "Not found method %s in %s" % (meth, str(type(self._obj)))
            setattr(self.__class__, meth, getattr(self._obj, meth))
            pass        
        return

    def __radd__(self, other): return other.__add__(self._obj)
    def __rmul__(self, other): return self._obj.__mul__(other)
    
    pass #end of class



# ----------------------------------------------------------------------
class ObsUserClassWrapper (ObsWrapper):
    def __init__(self, user_class_instance, obs_method_names):
        ObsWrapper.__init__(self, user_class_instance, obs_method_names)
        return
    pass #end of class



