import _importer

from sqlobject import *
sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

from gtkmvc.model import SQLObjectModel
from gtkmvc import Observer


class Person (SQLObjectModel):
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observable__ = ['?name']    
  pass


class PersonObs (Observer):
    
  def property_fname_value_change(self, model, old, new):
      print "fname CHANGED!", old, new
      return

  def property_lname_value_change(self, model, old, new):
      print "lname CHANGED!", old, new
      return
  pass

Person.createTable()

p = Person(fname="John", lname="Doe")
print p

c = PersonObs(p)

p.fname = "Ciccio"
print p


