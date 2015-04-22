import unittest

import _importer
import gtkmvc3

# Despite the name this superclass does not work directly with Observer but
# only in a Model property.
class Custom(gtkmvc3.Observable):
    x = 0

    @gtkmvc3.Observable.observed
    def touch(self):
        self.x += 1

    def reset(self):
        self.x = 5

class Model(gtkmvc3.Model):
    y = None
    __observables__ = ["y"]

    def __init__(self):
        gtkmvc3.Model.__init__(self)

        self.y = Custom()

class Observer(gtkmvc3.Observer):
    def __init__(self, model):
        gtkmvc3.Observer.__init__(self, model)

        self.notified = []

    def property_y_value_change(self, model, old, new):
        self.notified.append(new)
        # Not suppressed.
        new.touch()
        model.y.touch()

    def property_y_after_change(self, model, instance, name, res,
        args, kwargs):
        self.notified.append((instance, name))

class AdHoc(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.c = Observer(self.m)

    def testTouch(self):
        self.m.y.touch()
        self.assertEqual(1, self.m.y.x)
        self.assertEqual([(self.m.y, "touch")], self.c.notified)

    def testAssign(self):
        self.m.y = Custom()
        self.assertEqual(3, len(self.c.notified))

if __name__ == "__main__":
    unittest.main()
