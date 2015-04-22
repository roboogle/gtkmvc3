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



# ----------------------------------------------------------------------
# In this example the use of observable properties is shown.  Here the
# property we want to observe is an already existing instance of a
# class that we do _not_ want to change to add support for the
# observer pattern.  Given that instance, we want the obsevers to be
# notified when one or more instance methods are executed, but without
# modifying the class instance itself. To reach our goal, as soon as the
# instance is stored into the model as an observable class, we 'wrap' it
# into a tuple of 3 elements, as shown in this simple example
# ----------------------------------------------------------------------

import _importer
from gtkmvc3 import Model, Observer

# ----------------------------------------------------------------------
class ExistingClass (object):
    """This is an already existing class whose code is not intended to
    be changed. Instead, when instantiated into the model, it is
    declared in a particular manner, so that the model can recognise
    it and wrap it in order to monitor it"""
    
    def __init__(self): self.val = 0 

    def change(self): self.val += 1

    pass #end of class


# ----------------------------------------------------------------------
class MyModel (Model):

    obj = (ExistingClass, ExistingClass(), ('change',))
    __observables__ = ["obj"]

    pass # end of class


# ----------------------------------------------------------------------
class MyObserver (Observer):
    def __init__(self, model):
        Observer.__init__(self, model)
        return

    # notification
    @Observer.observe("obj", assign=True, before=True, after=True)
    def obj_change(self, model, prop_name, info):
        if "assign" in info:            
            print prop_name, "changed!"
        elif "before" in info:
            print prop_name, "before change!", info.instance, \
                  info.method_name, info.args, info.kwargs
        else:
            assert "after" in info
            print prop_name, "before change!", info.instance, \
                  info.method_name, info.result, info.args, info.kwargs
            pass            
        return

    pass # end of class


# Look at what happens to the observer
if __name__ == "__main__":
    m = MyModel()
    c = MyObserver(m)
    m.obj.change()
    pass

# ----------------------------------------------------------------------

