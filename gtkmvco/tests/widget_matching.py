import unittest

import gtk

import time
import gtk

# http://unpythonic.blogspot.com/2007/03/unit-testing-pygtk.html
def refresh_gui(delay=0):
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)
    time.sleep(delay)

import _importer

import gtkmvc

class Model(gtkmvc.Model):
    prop = None
    __observables__ = ("prop",)

class View(gtkmvc.View):
    def __contains__(self, key):
        """
        If __contains__ isn't implemented the `key in view` operator uses
        __iter__ which omits some types of widgets (that don't implement
        get_name). __getitem__ does not have that problem.
        """
        try:
            return bool(self[key])
        except KeyError:
            return False

class Foo(gtkmvc.Controller):
    def _find_widget_match(self, prop_name):
        """
        Don't try matching widgets because it doesn't work for some types.
        """

        self.called = True

        if prop_name not in self.view:
            raise ValueError
        return prop_name

class T(unittest.TestCase):
    def setUp(self):
        m = Model()
        self.v = View()
        self.v["wid"] = gtk.Entry()
        self.c = Foo(m, self.v)
        refresh_gui()

    def testContains(self):
        self.assertTrue("wid" in self.v)
        self.assertFalse("prop" in self.v)

    def testOverride(self):
        self.c.adapt()
        self.assertTrue(self.c.called)

    def testRaise(self):
        self.assertRaises(ValueError, lambda: self.c.adapt("prop"))

if __name__ == "__main__":
    unittest.main()
