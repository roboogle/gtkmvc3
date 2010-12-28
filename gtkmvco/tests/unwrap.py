import unittest

import _importer
import gtkmvc

class Model(gtkmvc.Model):
    mutable = None
    __observables__ = ("mutable",)

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.mutable = []
        self.called = False
        self.register_observer(self)
        return

    def property_mutable_before_change(self, model, instance, name, args,
        kwargs):
        self.called = True
        return

class ValueChange(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.o = self.m.mutable
        # Replace wrapped property with new instance.
        self.n = self.m.mutable = []
        return

    def testRemove(self):
        self.failIf(self.o.__get_models__())
        return

    def testDisconnect(self):
        self.o.append(1)
        self.failIf(self.m.called)
        return

if __name__ == "__main__":
    unittest.main()
