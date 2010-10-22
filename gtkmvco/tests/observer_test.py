"""
Test should print:
obj after change: <id 1> change None (<id 1>,) {}
obj value changed from: <id 1> to: <id 2>
obj after change: <id 2> change None (<id 2>,) {}
obj after change: <id 2> change None (<id 2>,) {}
"""
import _importer

from gtkmvc import Model
from gtkmvc import Observer
from gtkmvc import Observable

# ----------------------------------------------------------------------
class AdHocClass (Observable):
    def __init__(self):
        Observable.__init__(self)
        self.val = 0

    # this way the method is declared as 'observed':
    @Observable.observed 
    def change(self): self.val += 1

    # this is NOT observed:
    def is_val(self, val): return self.val == val

    pass #end of class

# ----------------------------------------------------------------------
class MyModel (Model):
    obj = AdHocClass()
    __observables__ = ("obj",)

    def __init__(self):
        Model.__init__(self)
        return    

    pass # end of class

# ----------------------------------------------------------------------
class MyObserver (Observer):
    def __init__(self, model):
        Observer.__init__(self, model)
        return

    def property_obj_value_change(self, model, old, new):
        print "obj value changed from:", old, "to:", new 
        new.change() # XXX
        model.obj.change() # XXX
        return

    def property_obj_after_change(self, model, instance, name, res,
                                  args, kwargs):
        print "obj after change:", instance, name, res, args, kwargs
        return

    pass

# Look at what happens to the observer
if __name__ == "__main__":
    m = MyModel()
    c = MyObserver(m)
    m.obj.change()
    m.obj = AdHocClass() # XXX
    pass

