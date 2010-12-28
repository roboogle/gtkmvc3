import unittest

import _importer
from gtkmvc.observer import observes
from gtkmvc.observable import Signal
from gtkmvc import Model, Observer


class MyOb (Observer):

    def __init__(self, m):
        Observer.__init__(self, m)
        self.notifications = []
        return

    @observes("p1")
    def assign_(self, model, name, old, new): 
        self.notifications.insert(0, (model, name, old, new))
        return

    @observes("p2")
    def before_(self, model, name, instance, mname, args, kwargs): return

    @observes("p3")
    def after_(self, model, name, instance, mname, res, args, kwargs): return

    @observes("p4")
    def signal_(self, model, name, arg): 
        self.notifications.insert(0, (model, name, arg))
        return

    
    # combination
    @observes("p1")
    @observes("p2", "p3", "p4")
    def assign_comb(self, model, name, old, new): 
        self.notifications.insert(0, (model, name, old, new))
        return

    # Assert warning "Ignoring notification no_matching: wrong number of
    # arguments"
    @observes("p1")
    def no_matching(self, model, name): return

    # Assert warning "Ignoring notification varargs: variable arguments
    # prevent type inference"
    @observes("p1")
    def varargs(self, model, *args): return
    pass # end of class

class MyMod (Model):
    p1 = 10
    p4 = Signal()
    __observables__ = ('p1','p4')   
    pass


class DeprecatedObservesTest (unittest.TestCase):
    
    def setUp(self):
        self.m = MyMod()
        self.o = MyOb(self.m)
        return
    
    def test_defined(self):
        for p, s in { 'p1' : set((self.o.assign_, self.o.assign_comb)), 
                      'p2' : set((self.o.before_, self.o.assign_comb)), 
                      'p3' : set((self.o.after_, self.o.assign_comb)),
                      'p4' : set((self.o.signal_, self.o.assign_comb)),
                      }.iteritems():
            os = self.o.get_observing_methods(p)
            self.assertEqual(os, s)
            pass
        return

    def test_types_match(self):
        right_types = { self.o.assign_: 'assign',
                        self.o.before_: 'before',
                        self.o.after_: 'after',
                        self.o.signal_: 'signal',
                        self.o.assign_comb: 'assign',
                        }
        for p in 'p1 p2 p3 p4'.split():
            for m in self.o.get_observing_methods(p):
                kw = self.o.get_observing_method_kwargs(p, m)
                self.assertTrue(right_types[m] in kw)
                self.assertTrue(kw[right_types[m]] is True)
                pass
            pass
        return

    def test_assign_p1(self):
        old = self.m.p1
        self.m.p1 += 1
        self.assertEqual(self.o.notifications[0], (self.m, 'p1', old, self.m.p1))
        return

    def test_assign_p4(self):
        old = self.m.p4
        self.m.p4 = Signal()
        self.assertEqual(self.o.notifications[0], (self.m, 'p4', old, self.m.p4))
        return

    def test_emit_p4(self):
        self.m.p4.emit("ciao")
        self.assertEqual(self.o.notifications[0], (self.m, 'p4', "ciao"))
        return

    def test_assign_emit_p4(self):
        old = self.m.p4
        self.m.p4 = Signal()
        self.assertEqual(self.o.notifications[0], (self.m, 'p4', old, self.m.p4))

        self.m.p4.emit("ciao")
        self.assertEqual(self.o.notifications[0], (self.m, 'p4', "ciao"))
        return
        

    pass # end of class



if __name__ == "__main__":
    unittest.main()
            
            
    
    
