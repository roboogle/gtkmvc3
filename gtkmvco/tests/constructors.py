"""
This ensures that applications written for old versions of the framework
die on startup, before the errors get weird.
"""

import unittest

from _importer import refresh_gui

import gtkmvc

RUNTIME = (TypeError, NotImplementedError)

class Constructors(unittest.TestCase):
    def setUp(self):
        self.m = gtkmvc.Model()
        self.v = gtkmvc.View()
        self.c = gtkmvc.Controller(self.m, self.v)
        refresh_gui()

    def test1991(self):
        """
        def __init__(self, glade=None, top=None,
             parent=None, 
             builder=None):
        def __init__(self, model, view, spurious=False, auto_adapt=False):
        """
        self.assert_(self.c.model is self.m)
        self.assert_(self.c.view is self.v)

    def testSVN157(self):
        """
        def __init__(self, glade=None, top=None,
            builder=None,
            parent=None, 
            controller=None):
        def __init__(self, model, view=None, spurious=False,
            auto_adapt=False):
        """
        self.assertRaises(RUNTIME, lambda: gtkmvc.View(
            None, "window7", "adapter19.ui"))

    def test1990(self):
        """
        def __init__(self, glade=None, top=None, 
                     parent=None, 
                     controller=None):
        def __init__(self, model, view=None, spurious=False, auto_adapt=False):
        """
        self.assertRaises(NotImplementedError, lambda: gtkmvc.View(
            "adapters.glade", "window1", self.v, self.c))

        self.assertRaises(TypeError, lambda: gtkmvc.Controller(
            self.m))

    def test122(self):
        """
        def __init__(self, controller, glade_filename=None,
            glade_top_widget_name=None, parent_view=None, register=True):
        def __init__(self, model, spurious=False):
        """
        gtkmvc.require("1.2.0")

        self.assertRaises(NotImplementedError, lambda: gtkmvc.View(
            self.c))
        self.assertRaises(NotImplementedError, lambda: gtkmvc.View(
            self.c, "adapters.glade"))
        self.assertRaises(NotImplementedError, lambda: gtkmvc.View(
            self.c, "adapters.glade", "window1"))
        self.assertRaises(NotImplementedError, lambda: gtkmvc.View(
            self.c, "adapters.glade", "window1", self.v))
        self.assertRaises(TypeError, lambda: gtkmvc.View(
            self.c, "adapters.glade", "window1", self.v, False))

        self.assertRaises(TypeError, lambda: gtkmvc.Controller(
            self.m))
        self.assertRaises(NotImplementedError, lambda: gtkmvc.Controller(
            self.m, False))

if __name__ == "__main__":
    unittest.main()
