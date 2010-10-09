import unittest

import _importer
import gtkmvc

class Custom(list):
    def __len__(self): return 1

class Model(gtkmvc.Model):
    standard = None
    custom = None
    # Order matters.
    __observables__ = ("standard", "custom")

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.standard = []
        self.custom = Custom()
        return

class SpecialMethod(unittest.TestCase):
    def setUp(self): self.m = Model()
        
    def testWhichMethod(self):
        self.assertEqual(1, len(self.m.custom))
        self.assertEqual(0, len(self.m.standard))
        return

if __name__ == "__main__":
    unittest.main()
