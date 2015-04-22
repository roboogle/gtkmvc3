"""
Like adapter1.py but inside controller.
"""
import unittest

from _importer import refresh_gui

import gtkmvc3
from gtkmvc3.adapters.basic import Adapter

class Model(gtkmvc3.Model):
    en1 = 10.0
    __observables__ = ["en1"]

class Controller(gtkmvc3.Controller):
    def on_button1_clicked(self, button):
        self.model.en1 += 1

    def handle(self, adapter, name, value):
        self.errors.append((adapter, name, value))
        adapter.update_widget()

    def register_adapters(self):
        a1 = Adapter(self.model, "en1",
                     prop_read=lambda v: v/2.0, prop_write=lambda v: v*2,
                     value_error=self.handle)
        a1.connect_widget(self.view["entry1"])
        self.adapt(a1)

        a2 = Adapter(self.model, "en1")
        a2.connect_widget(self.view["label1"],
            setter=lambda w,v: w.set_markup("<big><b>%.2f</b></big>" % v))
        self.adapt(a2)

        self.e = a1
        self.errors = []

class TwoForOne(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc3.View(builder="adapters.ui", top="window1")
        self.c = Controller(self.m, self.v)
        refresh_gui()

    def testArguments(self):
        self.assertEqual("5.0", self.v["entry1"].get_text())
        self.assertEqual("10.00", self.v["label1"].get_text())

        self.v["entry1"].set_text("1")
        self.assertEqual("2.00", self.v["label1"].get_text())

        self.v["button1"].clicked()
        self.assertEqual("1.5", self.v["entry1"].get_text())
        self.assertEqual("3.00", self.v["label1"].get_text())

        self.v["entry1"].set_text("?")
        self.assertEqual((self.c.e, "en1", "?"), self.c.errors[-1])
        self.assertEqual("1.5", self.v["entry1"].get_text())
        self.assertEqual("3.00", self.v["label1"].get_text())

if __name__ == "__main__":
    unittest.main()
