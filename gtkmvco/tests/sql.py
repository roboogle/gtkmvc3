import _importer
from gtkmvc import Model
import new
from sqlobject import *

cl = (Model.__metaclass__, SQLObject.__metaclass__)
meta = new.classobj('meta', cl, {'__module__': '__main__', '__doc__': None})

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

class MetaPerson(SQLObject, Model):
  __metaclass__ = meta
  pass
  
class Person(MetaPerson):
  fname = StringCol()
  mi = StringCol(length=1, default=None)
  lname = StringCol()

Person.createTable()
p = Person(fname="John", lname="Doe")
print p
