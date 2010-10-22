"""
Test should print:
<Person 1 fname='John' mi=None lname='Doe'>
CHANGED fname John Ciccio
<Person 1 fname='Ciccio' mi=None lname='Doe'>
CHANGED aaa 1 2
<Student 2 year='1974' fname='rob' mi=None lname='bibo'>
[<Person 1 fname='Ciccio' mi=None lname='Doe'>,
<Student 2 year='1974' fname='rob' mi=None lname='bibo'>]
"""
import _importer
from gtkmvc import Model, Observer
from gtkmvc.model import SQLObjectModel
from gtkmvc.adapters.basic import Adapter
from gtkmvc import observable
from gtkmvc.support.metaclasses import ObservablePropertyMetaSQL
from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

import gtk
import new

from gtkmvc.support import factories

sqlhub.processConnection = connectionForURI("sqlite:/:memory:")


# ----------------------------------------------------------------------
class Person(SQLObjectModel):
    
  aaa = 1
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observables__ = ['fname', 'lname', 'aaa']

  pass


class PersonObserver(Observer):

  @Observer.observes("fname", "lname", 'aaa')
  def property_value_change(self, model, prop_name, old, new):
      print "CHANGED", prop_name, old, new
      return
  pass

SQLObjectModel.createTable(ifNotExists = True)
Person.createTable()
p = Person(fname="John", lname="Doe")
print p

o = PersonObserver(p)

p.fname = "Ciccio"
print p

p.aaa += 1
# ----------------------------------------------------------------------

class Student (Person):
    year = StringCol()
    pass


Student.createTable()
s = Student(fname="rob", lname="bibo", year="1974")
print s

print list(Person.select())

#class MyMeta (Model.__metaclass__, SQLObject.__metaclass__): pass
#cls = new.classobj('', good_bc, {'__module__': '__main__', '__doc__': None})
#fa = factories.ModelFactory.make([SQLObject])
#print fa

