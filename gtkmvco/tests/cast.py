import unittest

import _importer
import gtkmvc3

TYPES = [int, float, str]
VALUES = [t(1) for t in TYPES]

class AdaptTypes(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(0, gtkmvc3.support.utils.cast_value('', int))

    def testCast(self):
        for t in TYPES:
            for v in VALUES:
                r = gtkmvc3.support.utils.cast_value(v, t)
                self.assertEqual(t, type(r))
                if t == type(v):
                    self.assertEqual(v, r)
        return

if __name__ == "__main__":
    unittest.main()
