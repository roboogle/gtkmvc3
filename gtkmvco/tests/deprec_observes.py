import unittest

import _importer
from gtkmvc.observer import observes, Observer

class MyOb (Observer):

    @observes("p1")
    def assign_(self, model, name, old, new): return

    @observes("p2")
    def before_(self, model, name, instance, mname, args, kwargs): return

    @observes("p3")
    def after_(self, model, name, instance, mname, res, args, kwargs): return

    @observes("p4")
    def signal_(self, model, name, arg): return

    
    # combination
    @observes("p1")
    @observes("p2", "p3")
    def assign_comb(self, model, name, old, new): return

    # no matching
    @observes("p1")
    def no_matching(self, model, name): return

    @observes("p1")
    def varargs(self, model, *args): return
    pass # end of class

    
class DeprecatedObservesTest (unittest.TestCase):
    
    def setUp(self):
        self.o = MyOb()
        return
    
    def test_defined(self):
        for p, s in { 'p1' : set((self.o.assign_, self.o.assign_comb)), 
                      'p2' : set((self.o.before_, self.o.assign_comb)), 
                      'p3' : set((self.o.after_, self.o.assign_comb)),
                      'p4' : set((self.o.signal_,)),
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
                kw = self.o.get_observing_method_kwargs(m)
                self.assertTrue(right_types[m] in kw)
                self.assertTrue(kw[right_types[m]] is True)
                pass
            pass
        return
    pass # end of class



if __name__ == "__main__":
    unittest.main()
            
            
    
    
