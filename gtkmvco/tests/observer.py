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
    @gtkmvc.Observer.observe("signal", signal=True)
    def notify_signal(self, model, name, info):
        self.signal = info.arg

    @gtkmvc.Observer.observe("value", assign=True)
    def notify_value(self, model, name, info):
        self.value = info.old, info.new

    @gtkmvc.Observer.observe("before", before=True)
    def notify_before(self, model, name, info):
        self.before = info.method_name, info.args

    @gtkmvc.Observer.observe("after", after=True)
    def notify_after(self, model, name, info):
        self.after = info.method_name, info.args

class WithNameModule(gtkmvc.Observer):
    @gtkmvc.Observer.observe("signal", signal=True, old_style_call=True)
    @gtkmvc.Observer.observe("iduna", signal=True, old_style_call=True)
    def a(self, model, prop_name, arg):
        if prop_name == "signal":
            self.signal = arg

    @gtkmvc.Observer.observe("value", assign=True)
    @gtkmvc.Observer.observe("before", assign=True)
    def b(self, model, prop_name, info):
        if prop_name == "value":
            self.value = info.old, info.new

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def c(self, model, prop_name, info):
        if prop_name == "before":
            self.before = info.method_name, info.args

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def d(self, model, prop_name, info):
        if prop_name == "after":
            self.after = info.method_name, info.args

class WithName(gtkmvc.Observer):
    @gtkmvc.Observer.observe("signal", signal=True)
    @gtkmvc.Observer.observe("iduna", signal=True)
    def a(self, model, prop_name, info):
        if prop_name == "signal":
            self.signal = info.arg

    @gtkmvc.Observer.observe("value", assign=True)
    @gtkmvc.Observer.observe("before", assign=True)
    def b(self, model, prop_name, info):
        if prop_name == "value":
            self.value = info.old, info.new

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def c(self, model, prop_name, info):
        if prop_name == "before":
            self.before = info.method_name, info.args

    @gtkmvc.Observer.observe("before", before=True)
    @gtkmvc.Observer.observe("after", after=True)
    def d(self, model, prop_name, info):
        if prop_name == "after":
            self.after = info.method_name, info.args

class DynamicWithName(gtkmvc.Observer):
    def __init__(self, model):
        gtkmvc.Observer.__init__(self)

        # TODO only first name each works!
        for name in ("signal", "iduna"): 
            self.observe(self.a, name, signal=True)
            pass
        for name in ("value", "before"):
            self.observe(self.b, name, assign=True)
            pass
        for name in ("before", "after"):            
            self.observe(self.c, name, before=True)
            pass
        for name in ("before", "after"):            
            self.observe(self.d, name, after=True)
            pass

        self.observe_model(model)

    def a(self, model, prop_name, info):
        if prop_name == "signal":
            self.signal = info.arg

    def b(self, model, prop_name, info):
        if prop_name == "value":
            self.value = info.old, info.new

    def c(self, model, prop_name, info):
        if prop_name == "before":
            self.before = info.method_name, info.args

    def d(self, model, prop_name, info):
        if prop_name == "after":
            self.after = info.method_name, info.args

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

    def testWithName(self):
        self.notifications(WithName(self.m))

    def testDynamicWithName(self):
        self.notifications(DynamicWithName(self.m))

    def testWithNameModule(self):
        self.notifications(WithNameModule(self.m))

class Dynamic(gtkmvc.Observer):
    def a(self, model, prop_name, info):
        self.signal = info.arg

class DynamicTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.c = Dynamic()
        self.c.observe(self.c.a, "signal", signal=True)

    def testArgs(self):
        self.assertEqual(dict(signal=True),
            self.c.get_observing_method_kwargs(self.c.a))

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
