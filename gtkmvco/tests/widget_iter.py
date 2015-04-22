"""
Tests using more than one concurrent iter on a view.
"""
import unittest

from _importer import refresh_gui

import gtkmvc3

class View(gtkmvc3.View):
    builder = "adapters.ui"
    top = "window6"

class Ctrl(gtkmvc3.Controller):

    def register_view(self, view):
        iter1 = iter(view)
        iter2 = iter(view)
        self.set1 = set()
        self.set2 = set()
        for item1 in iter1:
            item2 = iter2.next()
            self.set1.add(item1)
            self.set2.add(item2)

    def on_button7_clicked(self, button):
        pass

class TwoForOne(unittest.TestCase):
    def setUp(self):
        self.m = gtkmvc3.Model()
        self.v = View()
        self.c = Ctrl(self.m, self.v)

    def testIter(self):
        refresh_gui()
        self.assertEqual(self.c.set1, self.c.set2)

if __name__ == "__main__":
    unittest.main()
