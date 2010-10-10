import unittest

import _importer
import gtkmvc

class Dummy(gtkmvc.Model):
    mock = None
    __observables__ = ("mock",)

TYPES = [int, float, str, unicode]
VALUES = [t(1) for t in TYPES]

class AdaptTypes(unittest.TestCase):
    def setUp(self): self.a = gtkmvc.adapters.Adapter(Dummy(), "mock")
        
    def testCast(self):
        for t in TYPES:
            for v in VALUES:
                r = self.a._cast_value(v, t)
                self.assertEqual(t, type(r))
                if t == type(v):
                    self.assertEqual(v, r)
        return

if __name__ == "__main__":
    unittest.main()
