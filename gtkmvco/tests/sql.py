import os
import tempfile
import unittest

try:
    from sqlobject import *

    import _importer
    from gtkmvc.model import SQLObjectModel
    from gtkmvc import Observer

    class Person(SQLObjectModel):
        aaa = 1
        fname = StringCol()
        lname = StringCol()
        __observables__ = ["?name", "aaa"]
        pass
    
    class Student(Person):
        year = StringCol()
        pass
    
    class Trigger(Observer):
        def property_fname_value_change(self, model, old, new):
            self.fname = old, new
            return
        
        @Observer.observe("lname", assign=True)
        @Observer.observe("aaa", assign=True)
        def property_value_change(self, model, prop_name, info):
            setattr(self, prop_name, (info.old, info.new))
            return
        pass
    

    class SQLite(unittest.TestCase):
        def setUp(self):
            self.temp = tempfile.mkdtemp()
            self.file = os.path.join(self.temp, "db")
            sqlhub.processConnection = connectionForURI("sqlite:%s" % self.file)
            SQLObjectModel.createTables(ifNotExists=True)
            return
        
        def tearDown(self):
            os.unlink(self.file)
            os.rmdir(self.temp)
            return
        
        def testContructor(self):
            p = Person(fname="John", lname="Doe")
            self.assertEqual("John", p.fname)
            return
        
        def testNotification(self):
            p = Person(fname="John", lname="Doe")
            t = Trigger(p)
            p.fname = "Ciccio"
            self.assertEqual("Ciccio", p.fname)
            self.assertEqual(("John", "Ciccio"), t.fname)
            return
        
        def testRegression(self):
            p = Person(fname="John", lname="Doe")
            t = Trigger(p)
            p.aaa += 1
            self.assertEqual(2, p.aaa)
            self.assertEqual((1, 2), t.aaa)
            return
        
        def testInheritance(self):
            s = Student(fname="rob", lname="bibo", year="1974")
            self.assertEqual("rob", s.fname)
            self.assertEqual("1974", s.year)
            l = list(Person.select())
            self.assert_(s is l[0])
            return
        pass
    pass

except ImportError:
    class SQLImport(unittest.TestCase):
        def testImport(self):
            self.fail("sqlobject not installed.")
            return
        pass
    pass

if __name__ == "__main__":
    unittest.main()
        
