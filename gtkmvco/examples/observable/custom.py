#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2006-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.

import _importer

from gtkmvc3 import Model
from gtkmvc3 import Observer
from gtkmvc3 import Observable
from gtkmvc3.observable import Signal

class AdHocClass (Observable):

    """This is a class that is thought to be integrated into the
    observer pattern. It is declared to be 'observable' and the
    methods which we are interested in monitoring are decorated
    accordingly"""

    def __init__(self): 
        Observable.__init__(self)
        self.val = 0
        return

    @Observable.observed # this way the method is declared as 'observed'
    def change(self): self.val += 1
    pass #end of class


class MyModel (Model):

    a_value = 1
    a_value2 = 1
    a_signal = Signal()
    a_class = AdHocClass()

    __observables__ = ("a_*",)

    pass # end of class

class MyObserver (Observer):
    _for_test = 0 # this is acounter to count the notifications

    @Observer.observe("a_value", assign=True)
    @Observer.observe("a_value2", assign=True)
    @Observer.observe("pippo", assign=True)
    def observer_for_value(self, model, prop_name, info):
        print "observer_for_value", model, prop_name, info
        self._for_test += 1
        return

    # multiple observes work!
    @Observer.observe("a_value", assign=True)
    @Observer.observe("a_value2", assign=True)
    def observer_for_value2(self, model, prop_name, info):
        print "observer_for_value2", model, prop_name, info
        self._for_test += 1
        return
        
    @Observer.observe("a_signal", signal=True)
    def observer_for_signal(self, model, prop_name, info):
        print "observer_for_signal", model, prop_name, info
        self._for_test += 1
        return

    @Observer.observe("a_signal", signal=True)
    def observer_for_signal2(self, model, prop_name, info):
        print "observer_for_signal2", model, prop_name, info
        self._for_test += 1
        return
    
    @Observer.observe("a_class", before=True)
    def observer_for_method_before(self, model, prop_name, info):
        print "observer_for_method_before", model, prop_name, info
        self._for_test += 1
        return

    @Observer.observe("a_class", after=True)
    def observer_for_method_after(self, model, prop_name, info):
        print "observer_for_method_after", model, prop_name, info
        self._for_test += 1
        return
    
    def property_a_value_value_change(self, model, old, new):
        print "property_a_value_change_value", model, old, new
        self._for_test += 1
        return

    def property_a_signal_signal_emit(self, model, arg):
        print "property_a_signal_emit", model, arg
        self._for_test += 1
        return
    
    def property_a_class_before_change(self, model,
                                       instance, meth_name, args, kwargs):
        print "property_a_class_before_change", model,\
            instance, meth_name, args, kwargs
        self._for_test += 1
        return

    def property_a_class_after_change(self, model,
                                      instance, meth_name, res, args, kwargs):
        print "property_a_class_after_change", model,\
            instance, meth_name, res, args, kwargs
        self._for_test += 1
        return
    
    pass # end of class

m = MyModel()
o = MyObserver(m)

m.a_value += 1
m.a_value2 += 2
m.a_signal.emit()
m.a_signal.emit("ciao")
m.a_class.change()

# this is for testing
old = o._for_test 
assert o._for_test == 15

o.relieve_model(m)

m.a_value += 1
m.a_value2 += 2
m.a_signal.emit()
m.a_signal.emit("ciao2")
m.a_class.change()

# this is for testing
assert o._for_test == old
