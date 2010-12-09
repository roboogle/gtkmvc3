import unittest

import _importer
import gtkmvc

class Model(gtkmvc.Model):
    signal = gtkmvc.observable.Signal()
    iduna = gtkmvc.observable.Signal()
    value = 1
    before = None
    after = None
    __observables__ = "signal iduna value before after".split()

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.before = []
        self.after = []

class Implicit(gtkmvc.Observer):
    def property_signal_signal_emit(self, model, arg):
        self.signal = arg

    def property_value_value_change(self, model, old, new):
        self.value = old, new

    def property_before_before_change(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    def property_after_after_change(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class Explicit(gtkmvc.Observer):
    @gtkmvc.Observer.observes
    def signal(self, model, arg):
        self.signal = arg

    @gtkmvc.Observer.observes
    def value(self, model, old, new):
        self.value = old, new

    @gtkmvc.Observer.observes
    def before(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    @gtkmvc.Observer.observes
    def after(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class WithoutName(gtkmvc.Observer):
    @gtkmvc.Observer.observes("signal")
    def a(self, model, arg):
        self.signal = arg

    @gtkmvc.Observer.observes("value")
    def b(self, model, old, new):
        self.value = old, new

    @gtkmvc.Observer.observes("before")
    def c(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    @gtkmvc.Observer.observes("after")
    def d(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class WithoutNameModule(gtkmvc.Observer):
    @gtkmvc.observer.observes("signal")
    def a(self, model, arg):
        self.signal = arg

    @gtkmvc.observer.observes("value")
    def b(self, model, old, new):
        self.value = old, new

    @gtkmvc.observer.observes("before")
    def c(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    @gtkmvc.observer.observes("after")
    def d(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class WithNameModule(gtkmvc.Observer):
    @gtkmvc.observer.observes("signal", "iduna")
    def a(self, model, prop_name, arg):
        if prop_name == "signal":
            self.signal = arg

    @gtkmvc.observer.observes("value", "before")
    def b(self, model, prop_name, old, new):
        if prop_name == "value":
            self.value = old, new

    @gtkmvc.observer.observes("before", "after")
    def c(self, model, prop_name, instance, name,
        args, kwargs):
        if prop_name == "before":
            self.before = name, args

    @gtkmvc.observer.observes("after", "before")
    def d(self, model, prop_name, instance, name, res,
        args, kwargs):
        if prop_name == "after":
            self.after = name, args

class WithName(gtkmvc.Observer):
    @gtkmvc.Observer.observes("signal", "iduna")
    def a(self, model, prop_name, arg):
        if prop_name == "signal":
            self.signal = arg

    @gtkmvc.Observer.observes("value", "before")
    def b(self, model, prop_name, old, new):
        if prop_name == "value":
            self.value = old, new

    @gtkmvc.Observer.observes("before", "after")
    def c(self, model, prop_name, instance, name,
        args, kwargs):
        if prop_name == "before":
            self.before = name, args

    @gtkmvc.Observer.observes("after", "before")
    def d(self, model, prop_name, instance, name, res,
        args, kwargs):
        if prop_name == "after":
            self.after = name, args

class DynamicWithoutName(gtkmvc.Observer):
    def __init__(self, model):
        gtkmvc.Observer.__init__(self)

        self.add_observing_method(self.a, "signal")
        self.add_observing_method(self.b, "value")
        self.add_observing_method(self.c, "before")
        self.add_observing_method(self.d, "after")

        self.observe_model(model)

    def a(self, model, arg):
        self.signal = arg

    def b(self, model, old, new):
        self.value = old, new

    def c(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    def d(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class DynamicWithName(gtkmvc.Observer):
    def __init__(self, model):
        gtkmvc.Observer.__init__(self)

        self.add_observing_method(self.a, ["signal", "iduna"])
        self.add_observing_method(self.b, ["value", "before"])
        self.add_observing_method(self.c, ("before", "after"))
        self.add_observing_method(self.d, ("after", "before"))

        self.observe_model(model)

    def a(self, model, prop_name, arg):
        if prop_name == "signal":
            self.signal = arg

    def b(self, model, prop_name, old, new):
        if prop_name == "value":
            self.value = old, new

    def c(self, model, prop_name, instance, name,
        args, kwargs):
        if prop_name == "before":
            self.before = name, args

    def d(self, model, prop_name, instance, name, res,
        args, kwargs):
        if prop_name == "after":
            self.after = name, args

class Hack(gtkmvc.Observer):
    # This fails because the method without "custom" is called, which we
    # don't override.
    # Even then it fails because we don't also override methods like
    # does_observing_method_receive_prop_name.
    def get_custom_observing_methods(self, prop_name):
        if prop_name == "signal":
            return set([self.a])
        elif prop_name == "value":
            return set([self.b])
        elif prop_name == "before":
            return set([self.c])
        elif prop_name == "after":
            return set([self.d])
        else:
            return set

    def a(self, model, arg):
        self.signal = arg

    def b(self, model, old, new):
        self.value = old, new

    def c(self, model, instance, name,
        args, kwargs):
        self.before = name, args

    def d(self, model, instance, name, res,
        args, kwargs):
        self.after = name, args

class SingleTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()

    def notifications(self, c):
        # TODO use getattr with default value for FAIL instead of ERROR.
        self.m.signal.emit(4)
        self.assertEqual(4, c.signal)

        self.m.value = 2
        self.assertEqual((1, 2), c.value)

        self.m.before.append(5)
        self.assertEqual(("append", (5,)), c.before)

        self.m.after.append(5)
        self.assertEqual(("append", (5,)), c.after)

    def testImplicit(self):
        self.notifications(Implicit(self.m))

    def testExplicit(self):
        self.notifications(Explicit(self.m))

    def testWithoutName(self):
        self.notifications(WithoutName(self.m))

    def testWithName(self):
        self.notifications(WithName(self.m))

    def testDynamicWithoutName(self):
        self.notifications(DynamicWithoutName(self.m))

    def testDynamicWithName(self):
        self.notifications(DynamicWithName(self.m))

    # The following test backwards compatibility.

    def testWithoutNameModule(self):
        self.notifications(WithoutNameModule(self.m))

    def testWithNameModule(self):
        self.notifications(WithNameModule(self.m))

    def testHack(self):
        self.notifications(Hack(self.m))

class Dynamic(gtkmvc.Observer):
    def a(self, model, arg):
        self.signal = arg

class DynamicTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.c = Dynamic()
        self.c.add_observing_method(self.c.a, "signal")

    def testWithout(self):
        self.assertFalse(
            self.c.does_observing_method_receive_prop_name(self.c.a))

    def testGet(self):
        self.assertEqual(self.c.a,
            self.c.get_observing_methods("signal").pop())

    def testIs(self):
        self.assertTrue(self.c.is_observing_method(self.c.a))
        self.assertFalse(self.c.is_observing_method(self.c.observe_model))

    def testAdd(self):
        self.c.observe_model(self.m)
        self.m.signal.emit(4)
        self.assertEqual(4, self.c.signal)

    def testRemove(self):
        self.c.remove_observing_method(self.c.a, ["signal"])
        self.c.observe_model(self.m)
        self.m.signal.emit(4)
        self.assertFalse(hasattr(self.c, "signal"))

if __name__ == "__main__":
    unittest.main()
