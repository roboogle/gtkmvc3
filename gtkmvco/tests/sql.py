import os
import tempfile
import unittest

from sqlobject import *

import _importer

from gtkmvc.model import SQLObjectModel
from gtkmvc import Observer

class Person(SQLObjectModel):
    aaa = 1
    fname = StringCol()
    lname = StringCol()
    __observables__ = ["?name", "aaa"]

class Student(Person):
    year = StringCol()

class Trigger(Observer):
    def property_fname_value_change(self, model, old, new):
        self.fname = old, new

    @Observer.observes("lname", "aaa")
    def property_value_change(self, model, prop_name, old, new):
        setattr(self, prop_name, (old, new))

class SQLite(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.mkdtemp()
        self.file = os.path.join(self.temp, "db")
        sqlhub.processConnection = connectionForURI("sqlite:%s" % self.file)
        SQLObjectModel.createTables(ifNotExists=True)

    def tearDown(self):
        os.unlink(self.file)
        os.rmdir(self.temp)

    def testContructor(self):
        p = Person(fname="John", lname="Doe")
        self.assertEqual("John", p.fname)

    def testNotification(self):
        p = Person(fname="John", lname="Doe")
        t = Trigger(p)
        p.fname = "Ciccio"
        self.assertEqual("Ciccio", p.fname)
        self.assertEqual(("John", "Ciccio"), t.fname)

    def testRegression(self):
        p = Person(fname="John", lname="Doe")
        t = Trigger(p)
        p.aaa += 1
        self.assertEqual(2, p.aaa)
        self.assertEqual((1, 2), t.aaa)

    def testInheritance(self):
        s = Student(fname="rob", lname="bibo", year="1974")
        self.assertEqual("rob", s.fname)
        self.assertEqual("1974", s.year)
        l = list(Person.select())
        self.assert_(s is l[0])

if __name__ == "__main__":
    unittest.main()
