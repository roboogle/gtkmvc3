# Submitted by Christian Spoer <spoer@gmx.de>
# Adapted by RC to use unittest

import _importer
from gtkmvc import Model, Observer
import unittest

class MyModel (Model):
  mylist = [1,2]
  __observables__ = ("mylist",)

  def my_len(self): return len(self.mylist) # it was TypeError
  pass

class SpecialMethod(unittest.TestCase):
    def setUp(self): self.m = MyModel()
        
    def testLen(self): self.assertEqual(2, self.m.my_len())
    pass

if __name__ == "__main__":
    unittest.main()
