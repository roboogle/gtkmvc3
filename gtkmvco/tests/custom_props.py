import unittest

import _importer

import gtkmvc

class Model(gtkmvc.Model):
    __observables__ = ['old', 'new', 'generic']

    def __init__(self, pre=None, post=None):
        self.calls = []
        gtkmvc.Model.__init__(self)
        self.calls.append('init')

    def get_old_value(self):
        self.calls.append('old')
        return 1

    @gtkmvc.Model.getter
    def new(self):
        self.calls.append('new')
        return 2

    def get__value(self, key):
        self.calls.append(key)
        return 3
    
class Initialization(unittest.TestCase):
    def testOrder(self):
        m = Model()
        # 1.99.1
        self.assertEqual(['init'], m.calls)

if __name__ == "__main__":
    unittest.main()
