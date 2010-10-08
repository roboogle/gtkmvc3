"""
Test should print:
property_mylist_before_change:
<id 1> [] append (10,) {}
property_mylist_before_change:
<id 2> [] append (20,) {}
"""
import _importer
from gtkmvc import Model, Observer

class MyModel (Model):
  mylist = None
  
  __observables__ = ("my*",)

  def __init__(self):
    Model.__init__(self)
    self.mylist = []
    return

  pass # end of class


class MyObserver (Observer):
      
  def property_mylist_before_change(self, model, prop_instance, 
                                    meth_name, args, kwargs):
    print "property_mylist_before_change:"
    print model, prop_instance, meth_name, args, kwargs
    return

  pass # end of class


o = MyObserver()
m1 = MyModel()
m2 = MyModel()
for m in (m1, m2): o.observe_model(m)

m1.mylist.append(10)
m2.mylist.append(20)

    


