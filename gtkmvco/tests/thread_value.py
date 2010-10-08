"""
Test should print:
Changed  <id 1> 0 10
"""
import _importer
from gtkmvc import ModelMT, Observer

class MyModel (ModelMT):

    test = 0
    __observables__ = ("test",)

    def __init__(self):
        ModelMT.__init__(self)
        return
    pass


class MyObserver (Observer):
    def __init__(self, m):
        Observer.__init__(self, m)
        return

    def property_test_value_change(self, model, old, new):
        print "Changed ", model, old, new
        return
    pass

m = MyModel()
o = MyObserver(m)

m.test = 10
    
