import _importer
from gtkmvc import Model, observer
from gtkmvc.model import SQLObjectModel
from gtkmvc.adapters.basic import Adapter
from gtkmvc import observable
from gtkmvc.support.metaclasses import ObservablePropertyMetaSQL
from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

import gtk
import new

from gtkmvc.support import factories

__connection__ = "sqlite:/:memory:"


# ----------------------------------------------------------------------
class Person(SQLObjectModel):
  __properties__ = { 'aaa' : 1 }
    
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observables__ = ['fname', 'lname', 'zzz']    

  pass


class PersonObserver(observer.Observer):

  @observer.observes("fname", "lname", "zzz", 'aaa')
  def property_value_change(self, model, prop_name, old, new):
      print "CHANGED", prop_name, old, new
      return
  pass

Person.createTable()
p = Person(fname="John", lname="Doe")
print p

o = PersonObserver(p)

p.fname = "Ciccio"
print p

p.aaa += 1
p.zzz = 10
# ----------------------------------------------------------------------

#class Student (Person):
#    year = StringCol()
#    pass


#Student.createTable()
#s = Student(fname="rob", lname="bibo", year="1974")
#print s

#print list(Person.select())

#class MyMeta (Model.__metaclass__, SQLObject.__metaclass__): pass
#cls = new.classobj('', good_bc, {'__module__': '__main__', '__doc__': None})
#fa = factories.ModelFactory.make([SQLObject])
#print fa

