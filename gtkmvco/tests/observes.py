"""
"""

import _importer
from gtkmvc import Model, Observer
import unittest

# ----------------------------------------------------------------------
class Person(Model):
  aaa = 1
  fname = "rob"
  lname = "cav"
  __observables__ = ['fname', 'lname', 'aaa']
  pass
# ----------------------------------------------------------------------

class Student (Person):
    pass
# ----------------------------------------------------------------------

class PersonObserver(Observer):
  _map = {}
    
  @Observer.observe("fname", assign=True)
  @Observer.observe("lname", assign=True)
  @Observer.observe("aaa", assign=True)
  def property_value_change(self, model, prop_name, info):
      self._map[prop_name] = (info.old, info.new)
      return
  pass
# ----------------------------------------------------------------------


class ObservesTest(unittest.TestCase):
    def setUp(self): 
        self.o = PersonObserver()
        return
        
    def test_base(self):
        p = Person()
        self.o.observe_model(p)
        
        props = "fname lname aaa".split()
        old = []
        for prop in props: old.append(getattr(p, prop))
        new = [ "v1", "v2", old[2]+1 ]

        for prop, val in zip(props, new): setattr(p, prop, val)

        for prop, pair in zip(props, zip(old, new)):
            # checks that the changes were notified
            self.assertEqual(self.o._map[prop], pair)
            pass
        
        return

    def test_der(self):
        s = Student()
        self.o.observe_model(s)
        
        props = "fname lname aaa".split()
        old = []
        for prop in props: old.append(getattr(s, prop))
        new = [ "v1", "v2", old[2]+1 ]

        for prop, val in zip(props, new): setattr(s, prop, val)

        for prop, pair in zip(props, zip(old, new)):
            # checks that the changes were notified
            self.assertEqual(self.o._map[prop], pair)
            pass
        
        return

    pass


if __name__ == "__main__":
    unittest.main()
