"""
Test should print:
<Person 1 fname='John' mi=None lname='Doe'>
fname CHANGED! John Ciccio
<Person 1 fname='Ciccio' mi=None lname='Doe'>
"""
import _importer

from sqlobject import *
sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

from gtkmvc.model import SQLObjectModel
from gtkmvc import Observer


class Person (SQLObjectModel):
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

  __observables__ = ['?name']
  pass


class PersonObs (Observer):
    
  def property_fname_value_change(self, model, old, new):
      print "fname CHANGED!", old, new
      return

  def property_lname_value_change(self, model, old, new):
      print "lname CHANGED!", old, new
      return
  pass

SQLObjectModel.createTables(ifNotExists=True)

p = Person(fname="John", lname="Doe")
print p

c = PersonObs(p)

p.fname = "Ciccio"
print p


