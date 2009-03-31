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
    
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observables__ = ['fname', 'lname', ]    

  pass


class PersonObserver(observer.Observer):

  @observer.observes("fname", "lname", )
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

# ----------------------------------------------------------------------
