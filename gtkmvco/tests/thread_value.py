import _importer
from gtkmvc import ModelMT, Observer

class MyModel (ModelMT):

    __properties__ = { 'test' : 0 }

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
    
