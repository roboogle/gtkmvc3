import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter
from gtkmvc import observable
from gtkmvc.support.metaclasses import ObservablePropertyMetaSQL
from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

import gtk
import new

from gtkmvc.support import factories


#cl = (Model.__metaclass__, SQLObject.__metaclass__)
#cl = (Model.__metaclass__, InheritableSQLObject.__metaclass__)
#meta = new.classobj('meta', cl, {'__module__': '__main__', '__doc__': None})
meta = ObservablePropertyMetaSQL

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')


class MetaPerson(Model, InheritableSQLObject):
  __metaclass__ = meta

  def __init__(self, *args, **kargs):
      Model.__init__(self)
      InheritableSQLObject.__init__(self, *args, **kargs)
      return
  pass
MetaPerson.createTable()


# ----------------------------------------------------------------------
class Person(MetaPerson):
  __properties__ = { 'aaa' : 1 }
    
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observable__ = ['fname', 'lname', 'zzz']    
  pass


class PersonCtrl(Controller):
    
  def property_fname_value_change(self, model, old, new):
      print "fname CHANGED!", old, new
      return

  def property_zzz_value_change(self, model, old, new):
      print "zzz CHANGED!", old, new
      return

  def property_aaa_value_change(self, model, old, new):
      print "aaa CHANGED!", old, new
      return
  pass


Person.createTable()
p = Person(fname="John", lname="Doe")
print p

c = PersonCtrl(p)

p.fname = "Ciccio"
print p

p.aaa += 1
p.zzz = 10

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

