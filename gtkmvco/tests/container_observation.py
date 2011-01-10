# This tests the observation of observables into lists and maps.
# This test should be converted to unittest

import _importer
from gtkmvc import Model, Observer, Observable


# ----------------------------------------------------------------------
# An ad-hoc class which has a chaging method 'change'
class MyObservable (Observable):
    def __init__(self, name):
        # name is used to distinguish instances in verbosity
        Observable.__init__(self)
        self.name = name
        return
    
    @Observable.observed
    def change(self):
        print "called change:", self.name
        return
    pass # end of class
# ----------------------------------------------------------------------

class MyModel (Model):

    # this model contains only dynamically declared observables in to
    # the list and the map.
  
    def __init__(self):
        Model.__init__(self)

        # self.list and self.map are not observable here, althought
        # that might be observable of course.
        
        self.list = [ MyObservable("ob.%02d" % i) for i in range(5) ]

        self.map = { 'k0' : MyObservable("k0"),
                     'k1' : [MyObservable("k1[0]"), MyObservable("k1[1]")],
                     }
        
        for i in range(len(self.list)):
            self.register_property("list[%d]" % i)
            pass

        # notice tha way keys are represented: map[k0], and not
        # map['k0']. This may change (TBD):        
        self.register_property("map[k0]")
        self.register_property("map[k1][0]") 
        self.register_property("map[k1][1]")
        return
    pass # end of class
# ----------------------------------------------------------------------


class MyObserver (Observer):

    # The observer exploits both dynamic and static declaration of
    # notification methods.
    
    def __init__(self, m):
        # notice that the observation of is delayed here, as in 1.99.1
        # dynamic observation work only before the model registration.
        Observer.__init__(self) 

        # dynamically observes list[0]
        self.observe(self.content_changed, "list[0]", before=True)

        # dynamically observes map[k0]
        self.observe(self.content_changed, "map[k0]", before=True)

        self.observe_model(m)
        return

    # statically observes list[1] and list[3]
    @Observer.observe("list[1]", after=True)
    @Observer.observe("list[3]", before=True)
    @Observer.observe("map[k1][0]", after=True)
    def content_changed(self, model, name, info):
        print "Observer:", model, name, info
        return

    pass # end of class
# ----------------------------------------------------------------------


if "__main__" == __name__:
    m = MyModel()
    o = MyObserver(m)

    # change the list's content
    for o in m.list: o.change()

    # change the map's content
    m.map['k0'].change()
    for i in range(2): m.map['k1'][i].change()
    pass

