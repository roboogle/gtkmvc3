"""
Test should print:
name changed from Roberto to Cavada
age changed from 0 to 1
age changed from 10 to 11
name changed from Roberto to Cavada2
days changed from 12 to 17
days changed from 17 to 22
"""
# MyModel.py
import _importer
import gtkmvc

class MyModelBase (gtkmvc.Model):
    name = "Roberto"
    age = 0
    __observables__ = ["name", "age" ] 
    pass # end of class

class MyModelDer1 (MyModelBase):
    age = 10
    __observables__ = ["age", "days" ] 

    __val = 12
    def get_days_value(self): return self.__val
    def set_days_value(self, val):self.__val = val
    
    pass # end of class

class MyModelDer2 (MyModelDer1):
    #days = 1000
    #__observables__ = [ "days", "pippo" ]

    #def get_days_value(self): return self.__val
    #def set_days_value(self, val):self.__val = val

    pass # end of class


class MyObserver (gtkmvc.Observer):
    def property_name_value_change(self, model, old, new):
        print "name changed from %s to %s" % (old, new)
        return

    def property_age_value_change(self, model, old, new):
        print "age changed from %d to %d" % (old, new)
        return

    def property_days_value_change(self, model, old, new):
        print "days changed from %d to %d" % (old, new)
        return

    pass # end of class

    
    

# main.py
m1 = MyModelBase()
m2 = MyModelDer1()
o1 = MyObserver(m1)
o2 = MyObserver(m2)

m1.name = "Cavada"
m1.age += 1
m2.age += 1 
m2.name = "Cavada2"
m2.days += 5
m2.days += 5
