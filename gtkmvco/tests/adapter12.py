import unittest

from gi.repository import Gtk

from _importer import refresh_gui

import gtkmvc3
# Importing this as default.__def_adapter or __def_adapter would get mangled
# with the name of the test class, because double underscores get replaced
# very early.
from gtkmvc3.adapters.default import __def_adapter as DEF

BAR = (Gtk.Toolbar, "style-changed", Gtk.Toolbar.get_style,
       Gtk.Toolbar.set_style, Gtk.ToolbarStyle, None)

class Model(gtkmvc3.Model):
    bar = Gtk.ToolbarStyle.TEXT
    __observables__ = ["bar"]


class Defaults(unittest.TestCase):
    def setUp(self):
        # Copy.
        self.backup = tuple(DEF)

        self.m = Model()
        self.v = gtkmvc3.View()
        self.v["bar"] = Gtk.Toolbar()
        # Relying on auto_adapt=False as the default.
        self.c = gtkmvc3.Controller(self.m, self.v)
        refresh_gui()

    def tearDown(self):
        # Replace in place.
        DEF[0:len(DEF)] = self.backup
        # TODO remove memoization from framework because the speed increase is
        # minimal and it likely messes up remove_adapter.
        gtkmvc3.adapters.default.__memoize__ = {}

    def adapterTest(self):
        """
        Not called by the unittest.main()
        """
        self.c.adapt()
        self.assertEqual(Gtk.ToolbarStyle.TEXT, self.v["bar"].get_style())
        self.v["bar"].set_style(Gtk.ToolbarStyle.ICONS)
        self.assertEqual(Gtk.ToolbarStyle.ICONS, self.m.bar)

    def testNegative(self):
        # Adapting toolbars doesn't make sense, so there shouldn't be a
        # default in the framework.
        self.assertRaises(TypeError, lambda: self.c.adapt())

    def testManual(self):
        DEF.append(BAR)
        self.adapterTest()

    def testCall(self):
        # TODO test insertion/overriding an existing default.
        gtkmvc3.adapters.default.add_adapter(*BAR)
        self.adapterTest()

    def testAPI(self):
        self.assertFalse(gtkmvc3.adapters.default.remove_adapter(Gtk.Toolbar))
        gtkmvc3.adapters.default.add_adapter(*BAR)
        self.assertTrue(gtkmvc3.adapters.default.remove_adapter(Gtk.Toolbar))
        self.assertRaises(TypeError, lambda: self.c.adapt())

if __name__ == "__main__":
    unittest.main()
