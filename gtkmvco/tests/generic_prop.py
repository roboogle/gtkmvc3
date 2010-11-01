import unittest

import _importer

import gtkmvc

class Generic(gtkmvc.Model):
    __observables__ = ["one", "two"]

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.real = {}

    def get__value(self, key):
        return self.real.get(key, None)

    def set__value(self, key, value):
        self.real[key] = value

class Trigger(gtkmvc.Observer):
    def property_value_change(self, model, prop_name, old, new):
        setattr(self, prop_name, (old, new))

    def get_custom_observing_methods(self, prop_name):
        if prop_name in Generic.__observables__:
            return set([self.property_value_change])
        else:
            return set()

class Hack(unittest.TestCase):
    def testAccess(self):
        m = Generic()
        self.assertEqual(None, m.one)
        m.one = 1
        self.assertEqual(1, m.one)

    def testNotification(self):
        m = Generic()
        t = Trigger(m)
        m.two = 1
        self.assertEqual((None, 1), t.two)

if __name__ == "__main__":
    unittest.main()
